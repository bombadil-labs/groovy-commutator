"""Exact prepared-family lift census with replaceable lift definitions.

Each lift consumes one horizontal halo cell per side. Thus dimension d uses
all source words of width 2d+1 to cover its radius-one observations and target.
No source state or phase is an input to the native lookup. Tagged lookups are
recorded only as diagnostic controls. Local failure is not global noninjectivity.
"""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, itertools, json, platform
import sqlite3, sys, time, traceback, zlib
from pathlib import Path
import numpy as np

TARGETS = ('derivative', 'source', 'parent', 'parent_derivative')
OFFSETS = (0, 1, -1)

def raw(value): return json.dumps(value, sort_keys=True, separators=(',', ':'))
def sha(value): return hashlib.sha256(value).hexdigest()
def words(n): return ((np.arange(1 << n, dtype=np.uint64)[:, None] >> np.arange(n-1, -1, -1, dtype=np.uint64)) & 1).astype(np.uint8)
def derive(source, rule):
    index = 4*source[..., :-2] + 2*source[..., 1:-1] + source[..., 2:]
    return (((rule ^ 204) >> index) & 1).astype(np.uint8)
def load_operator(path):
    spec = importlib.util.spec_from_file_location('candidate_lift', path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

class Compiler:
    def __init__(self, rule, depth, operator, source=None):
        self.rule, self.operator = rule, operator
        self.source = words(2*depth+3) if source is None else source
        self.jets = [self.source]; self.source_masks = []
        for _ in range(depth+1):
            mask = derive(self.jets[-1], rule)
            self.source_masks.append(mask)
            self.jets.append(self.jets[-1][..., 1:-1] ^ mask)
        self.cache = {}

    def encode(self, path, t=0):
        if not path: return self.jets[t]
        key = (raw(path), t)
        if key not in self.cache:
            parent = self.encode(path[:-1], t)
            # Induced Boolean variation under the primitive source mask.
            # On a certified parent this equals its native flip predicate.
            mask = self.mask(path[:-1], t)
            result = self.operator.lift(parent, mask, path[-1])
            expected_tail = (*parent.shape[1:-1], parent.shape[-1]-2)
            if result.shape[0] != parent.shape[0] or result.shape[2:] != expected_tail:
                raise ValueError(f'Lift shape contract failed: {result.shape}, parent {parent.shape}')
            if result.dtype != np.uint8 or not np.all((result == 0) | (result == 1)):
                raise ValueError('The lift must return binary uint8 cells')
            self.cache[key] = result
        return self.cache[key]

    def mask(self, path, t=0):
        if not path: return self.source_masks[t]
        return self.encode(path, t)[..., 1:-1] ^ self.encode(path, t+1)

def physical_observations(grid):
    periods = grid.shape[1:-1]
    if grid.shape[-1] != 3: raise ValueError('Causal window did not leave three x cells')
    patches = []
    for offsets in itertools.product(OFFSETS, repeat=len(periods)):
        shifted = grid
        for axis, offset in enumerate(offsets, 1):
            if offset: shifted = np.roll(shifted, -offset, axis=axis)
        patches.append(shifted.reshape(grid.shape[0], -1, 3))
    return np.concatenate(patches, axis=-1)

def make_targets(compiler, path):
    grid = compiler.encode(path)
    count, phases = grid.shape[0], int(np.prod(grid.shape[1:-1]))
    source = np.repeat(compiler.source[:, compiler.source.shape[1]//2, None], phases, axis=1)
    parent = compiler.encode(path[:-1]); parent_center = parent[..., parent.shape[-1]//2]
    parent_mask = compiler.mask(path[:-1]); mask_center = parent_mask[..., parent_mask.shape[-1]//2]
    new_period = grid.shape[1]
    return {'derivative': compiler.mask(path)[..., 0].reshape(count, phases),
            'source': source,
            'parent': np.repeat(parent_center[:, None, ...], new_period, axis=1).reshape(count, phases),
            'parent_derivative': np.repeat(mask_center[:, None, ...], new_period, axis=1).reshape(count, phases)}

def group_constraints(observations, targets, periods, source_width, tagged):
    word_count, phases, nbits = observations.shape
    flat = observations.reshape(-1, nbits)
    packed = np.packbits(flat, axis=1, bitorder='big')
    if tagged:
        labels = np.tile(np.arange(phases, dtype='>u4'), word_count).view(np.uint8).reshape(-1, 4)
        packed = np.concatenate((labels, packed), axis=1)
    packed = np.ascontiguousarray(packed)
    key_bytes = packed.shape[1]
    opaque = packed.view(np.dtype((np.void, key_bytes))).ravel()
    unique, first, inverse, frequency = np.unique(opaque, return_index=True, return_inverse=True, return_counts=True)
    inverse = inverse.ravel()
    values = np.stack([targets[name].reshape(-1) for name in TARGETS], axis=1)
    output_masks = np.zeros((len(unique), len(TARGETS)), dtype=np.uint8)
    np.bitwise_or.at(output_masks, inverse, (1 << values).astype(np.uint8))
    keys = unique.view(np.uint8).reshape(-1, key_bytes)
    tasks = {}
    for col, name in enumerate(TARGETS):
        bad = np.flatnonzero(output_masks[:, col] == 3)
        witness = None
        if len(bad):
            group = int(bad[0]); events = []
            for desired in (0, 1):
                event = int(np.flatnonzero((inverse == group) & (values[:, col] == desired))[0])
                word, phase = divmod(event, phases)
                events.append({'word': word, 'source_word': format(word, f'0{source_width}b'),
                               'phase': phase, 'phase_coordinates': list(map(int, np.unravel_index(phase, periods))),
                               'required': desired, 'all_targets': {n: int(values[event, j]) for j, n in enumerate(TARGETS)}})
            patch = flat[int(first[group])].reshape((3,)*len(periods)+(3,)).tolist()
            witness = {'key_hex': keys[group].tobytes().hex(), 'patch': patch, 'events': events}
        tasks[name] = {'conflicts': int(len(bad)), 'witness': witness}
    payload = keys.tobytes() + output_masks.tobytes() + frequency.astype('<u4').tobytes()
    record = {'observed': len(unique), 'events': int(word_count*phases), 'tasks': tasks,
              'table_sha256': sha(payload), 'key_bytes': key_bytes}
    return record, zlib.compress(payload, 3)

def passed(record, names=('derivative', 'source', 'parent')):
    return all(record['tasks'][name]['conflicts'] == 0 for name in names)

def evaluate(compiler, path):
    start = time.perf_counter()
    grid = compiler.encode(path); periods = grid.shape[1:-1]
    observations = physical_observations(grid)
    targets = make_targets(compiler, path)
    constraints = {}; payloads = {}
    for mode, tagged in (('unmarked', False), ('tagged', True)):
        constraints[mode], payloads[mode] = group_constraints(observations, targets, periods, compiler.source.shape[1], tagged)
    flat_fields = grid.reshape(grid.shape[0], -1, grid.shape[-1])
    constants = [i for i in range(flat_fields.shape[1]) if np.all(flat_fields[:, i] == flat_fields[0, i, 0])]
    constant_values = {str(i): int(flat_fields[0, i, 0]) for i in constants}
    dimension = len(path)+1; nbits = 3**dimension
    record = {'dimension': dimension, 'recipe': path, 'periods': list(periods),
              'source_width': int(compiler.source.shape[1]), 'source_words': int(grid.shape[0]),
              'events': int(grid.shape[0]*np.prod(periods)), 'physical_neighborhood_bits': nbits,
              'distinct_neighborhood_cells': int(3*np.prod([min(3, p) for p in periods])),
              'projection_layers': int(np.prod(periods)), 'constant_layers': constant_values,
              'unseen_native_neighborhoods': str((1 << nbits)-constraints['unmarked']['observed']),
              **constraints,
              'source_and_update_pass': passed(constraints['unmarked'], ('derivative', 'source')),
              'strict_pass': passed(constraints['unmarked']),
              'all_four_pass': passed(constraints['unmarked'], TARGETS),
              'tagged_strict_pass': passed(constraints['tagged']),
              'elapsed_seconds': time.perf_counter()-start}
    return record, payloads

def create_database(path):
    db = sqlite3.connect(path)
    db.executescript('''
      CREATE TABLE candidates(id INTEGER PRIMARY KEY,rule INTEGER,dimension INTEGER,parent_id INTEGER,
                              strict_pass INTEGER,source_and_update_pass INTEGER,tagged_strict_pass INTEGER,record_json TEXT);
      CREATE TABLE local_tables(candidate_id INTEGER,mode TEXT,nkeys INTEGER,key_bytes INTEGER,
                                targets_json TEXT,payload_zlib BLOB,PRIMARY KEY(candidate_id,mode));
      CREATE INDEX by_rule_dimension ON candidates(rule,dimension);
      CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT);
    ''')
    return db

def run(args):
    destination = Path(args.output).resolve()
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f'Refusing to overwrite an existing run: {destination}')
    destination.mkdir(parents=True, exist_ok=True)
    operator_path = Path(args.lift).resolve(); operator = load_operator(operator_path)
    (destination/'source_harness.py').write_bytes(Path(__file__).read_bytes())
    (destination/'source_lift.py').write_bytes(operator_path.read_bytes())
    rules = list(range(256)) if args.rules == 'all' else [int(r) for r in args.rules.split(',')]
    manifest = {'status': 'running', 'operator': getattr(operator, 'NAME', operator_path.stem),
                'lift_path': str(operator_path), 'lift_sha256': sha(operator_path.read_bytes()),
                'harness_sha256': sha(Path(__file__).read_bytes()), 'python': platform.python_version(),
                'numpy': np.__version__, 'rules': rules, 'max_dimension': args.max_dimension,
                'source_derivative': 'rule XOR 204; integration is source XOR derivative',
                'gate': ['derivative', 'source', 'parent'], 'diagnostic': ['parent_derivative', 'tagged'],
                'off_image_completion': None, 'argv': sys.argv[1:]}
    (destination/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    db = create_database(destination/'constraints.sqlite3')
    db.execute('INSERT INTO metadata VALUES(?,?)', ('manifest', raw(manifest)))
    start = time.perf_counter(); last_progress = start
    summaries = []; next_id = 1
    try:
        for rule in rules:
            parents = [(None, [])]; stages = []
            for dimension in range(2, args.max_dimension+1):
                stage = {'dimension': dimension, 'status': 'tested' if parents else 'blocked',
                         'parents': len(parents), 'candidates': 0, 'strict_passes': 0,
                         'source_update_passes': 0, 'tagged_strict_passes': 0, 'all_four_passes': 0,
                         'without_constant_layers': 0, 'best_candidate_id': None, 'best_recipe': None,
                         'by_geometry': {}, 'by_mask': {}}
                survivors = []
                for parent_id, path in parents:
                    # Release candidate arrays after each parent; retain shared prefixes within it.
                    compiler = Compiler(rule, dimension-1, operator)
                    for choice in operator.choices(dimension, path):
                        recipe = path+[choice]
                        record, payloads = evaluate(compiler, recipe)
                        candidate_id = next_id; next_id += 1
                        db.execute('INSERT INTO candidates VALUES(?,?,?,?,?,?,?,?)',
                                   (candidate_id, rule, dimension, parent_id, int(record['strict_pass']),
                                    int(record['source_and_update_pass']), int(record['tagged_strict_pass']), raw(record)))
                        for mode, payload in payloads.items():
                            db.execute('INSERT INTO local_tables VALUES(?,?,?,?,?,?)',
                                       (candidate_id, mode, record[mode]['observed'], record[mode]['key_bytes'], raw(TARGETS), payload))
                        stage['candidates'] += 1
                        stage['strict_passes'] += int(record['strict_pass'])
                        stage['source_update_passes'] += int(record['source_and_update_pass'])
                        stage['tagged_strict_passes'] += int(record['tagged_strict_pass'])
                        stage['all_four_passes'] += int(record['all_four_pass'])
                        stage['without_constant_layers'] += int(record['strict_pass'] and not record['constant_layers'])
                        for field, key in (('by_geometry', choice.get('geometry', 'unspecified')), ('by_mask', choice.get('mask', 'unspecified'))):
                            category = stage[field].setdefault(key, {'candidates': 0, 'strict_passes': 0, 'source_update_passes': 0})
                            category['candidates'] += 1; category['strict_passes'] += int(record['strict_pass'])
                            category['source_update_passes'] += int(record['source_and_update_pass'])
                        if record['strict_pass']:
                            survivors.append((candidate_id, recipe))
                            if stage['best_candidate_id'] is None:
                                stage['best_candidate_id'] = candidate_id; stage['best_recipe'] = recipe
                stage['rule_pass'] = bool(survivors)
                stages.append(stage); parents = survivors
            summary = {'rule': rule, 'derivative_rule': rule ^ 204, 'stages': stages}
            summaries.append(summary)
            db.commit()
            with (destination/'rules.jsonl').open('a') as stream: stream.write(raw(summary)+'\n')
            now = time.perf_counter()
            if now-last_progress >= args.progress_seconds or rule == rules[-1]:
                counts = {str(d): sum(row['stages'][d-2]['rule_pass'] for row in summaries) for d in range(2, args.max_dimension+1)}
                print(raw({'rules_done': len(summaries), 'rules_total': len(rules), 'candidates': next_id-1,
                           'passing_rules_by_dimension': counts, 'elapsed_seconds': round(now-start, 3)}), flush=True)
                last_progress = now
        aggregate = {}
        for d in range(2, args.max_dimension+1):
            stages = [(row['rule'], row['stages'][d-2]) for row in summaries]
            aggregate[str(d)] = {'passing_rules': [r for r, s in stages if s['rule_pass']],
                                  'source_update_rules': [r for r, s in stages if s['source_update_passes']],
                                  'tagged_rules': [r for r, s in stages if s['tagged_strict_passes']],
                                  'blocked_rules': [r for r, s in stages if s['status']=='blocked'],
                                  'failed_tested_rules': [r for r, s in stages if s['status']=='tested' and not s['rule_pass']],
                                  'candidates': sum(s['candidates'] for _, s in stages),
                                  'passing_candidates': sum(s['strict_passes'] for _, s in stages),
                                  'all_four_candidates': sum(s['all_four_passes'] for _, s in stages),
                                  'without_constant_layers': [r for r, s in stages if s['without_constant_layers']],
                                  'by_geometry': {g: [r for r, s in stages if s['by_geometry'].get(g, {}).get('strict_passes', 0)]
                                                  for g in sorted({g for _, s in stages for g in s['by_geometry']})},
                                  'by_mask': {m: [r for r, s in stages if s['by_mask'].get(m, {}).get('strict_passes', 0)]
                                              for m in sorted({m for _, s in stages for m in s['by_mask']})}}
        (destination/'summary.json').write_text(json.dumps(aggregate, indent=2)+'\n')
        with (destination/'rules.csv').open('w') as stream:
            fields = ['rule', 'derivative_rule'] + [f'd{d}_{name}' for d in range(2,args.max_dimension+1) for name in ('status','candidates','strict_passes','source_update_passes','tagged_strict_passes','best_candidate_id')]
            writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader()
            for row in summaries:
                flat = {k:row[k] for k in ('rule','derivative_rule')}
                for stage in row['stages']:
                    for name in ('status','candidates','strict_passes','source_update_passes','tagged_strict_passes','best_candidate_id'):
                        flat[f'd{stage["dimension"]}_{name}'] = stage[name]
                writer.writerow(flat)
        manifest.update(status='complete', elapsed_seconds=time.perf_counter()-start, candidates=next_id-1)
    except BaseException:
        manifest.update(status='interrupted_or_failed', elapsed_seconds=time.perf_counter()-start,
                        rules_completed=len(summaries), error=traceback.format_exc())
        raise
    finally:
        db.execute('INSERT OR REPLACE INTO metadata VALUES(?,?)', ('final_manifest', raw(manifest)))
        db.commit(); db.close()
        (destination/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return destination

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lift', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--max-dimension', type=int, default=3)
    ap.add_argument('--rules', default='all')
    ap.add_argument('--progress-seconds', type=float, default=5)
    args = ap.parse_args()
    if not 2 <= args.max_dimension <= 6: ap.error('Supported dimensions: 2 through 6; branching costs grow quickly')
    run(args)

if __name__ == '__main__': main()
