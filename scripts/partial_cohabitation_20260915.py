#!/usr/bin/env python3
"""Compare partial constraints with four chosen completions; reuse saved D2 grids."""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
from pathlib import Path
import platform
import resource
import signal
import tarfile
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = 'docs/research/protocols/partial-cohabitation-20260915.md'
LABELS = 'experiments/on_beam_256_4d_20260914/labels.json'
SCRIPT = 'scripts/partial_cohabitation_20260915.py'
ARCHIVE_SHA = '766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1'
POLICIES = ('no_flip', 'flip', 'output_zero', 'output_one')
ANCHORS = (0, 1, 18, 30, 41, 54, 90, 106, 110, 122, 126, 204)
PAIR_COLUMNS = ('a', 'b', 'shared_zero', 'shared_one', 'conflicts', *POLICIES)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''): h.update(block)
    return h.hexdigest()


def write_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n')
    temp.replace(path)


def unpack(value, shape):
    raw = base64.b64decode(value, validate=True); n = int(np.prod(shape))
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder='big')
    assert len(raw) == (n + 7) // 8 and not bits[n:].any()
    return bits[:n].reshape(shape)


def physical_keys(grid):
    line = np.zeros(grid.shape, dtype=np.uint64)
    for dx in range(-2, 3): line = (line << 1) | np.roll(grid, -dx, axis=-1)
    out = np.zeros(grid.shape, dtype=np.uint64)
    for dy in range(-3, 4): out = (out << 5) | np.roll(line, -dy, axis=-2)
    return out


def scalar_key(grid, row, col):
    value = 0
    for dy in range(-3, 4):
        for dx in range(-2, 3):
            value = (value << 1) | int(grid[(row + dy) % 6, (col + dx) % grid.shape[1]])
    return value


def read_record(raw):
    d = json.loads(raw); w = d['width']; r = d['rule']; n = 1 << w
    assert d['format'] == 'grid-referenced-physical-partial-rule-v1'
    assert d['dimension'] == 2 and d['mode'] == 'jet6' and d['radii_array_order'] == [3, 2]
    assert d['grid_shape'] == [n, 6, w]
    assert d['unforced_derivative'] == 0
    g = unpack(d['grid_bits_big'], (n, 6, w)); q = physical_keys(g)
    representatives = np.frombuffer(base64.b64decode(d['representative_flat_indices_u32le'], validate=True), dtype='<u4')
    ks = q.ravel()[representatives]
    vs = unpack(d['forced_derivative_bits_big'], (len(ks),))
    order = np.argsort(ks); ks, vs = ks[order], vs[order]
    assert len(ks) == d['forced_root_count'] and np.array_equal(np.unique(q), ks)
    # Reuse stored grid and its source-indexed successor; no new lifts are made.
    x = ((np.arange(n)[:, None] >> np.arange(w-1, -1, -1)) & 1).astype(np.uint8)
    assert np.array_equal(g[:, 4] ^ g[:, 5], x)
    p = 4*np.roll(x, 1, axis=-1) + 2*x + np.roll(x, -1, axis=-1)
    y = ((r >> p.astype(np.uint16)) & 1).astype(np.uint8)
    successor = (y.astype(np.uint64) * (1 << np.arange(w-1, -1, -1))).sum(axis=-1).astype(int)
    assert np.array_equal(g ^ vs[np.searchsorted(ks, q)], g[successor])
    for source in (0, n//3, n-1):
        for row in range(6):
            for col in (0, w-1): assert scalar_key(g[source], row, col) == int(q[source, row, col])
    return (w, r), (ks, vs)


def as_bits(indices):
    value = 0
    for i in indices: value |= 1 << int(i)
    return value


def conflict(p, q):
    return (p[0] & q[1]) | (p[1] & q[0])


def deviations(p, center_one, universe):
    z, o = p; center_zero = universe ^ center_one
    return o, z, (o & center_zero) | (z & center_one), (z & center_zero) | (o & center_one)


def witness(bits, p, q, global_keys):
    if not bits: return None
    at = (bits & -bits).bit_length() - 1; b = 1 << at; key = int(global_keys[at])
    def value(pair): return 0 if pair[0] & b else 1 if pair[1] & b else None
    return {'key': key, 'bits_35': format(key, '035b'), 'a_forced': value(p), 'b_forced': value(q)}


def conjugate(r):
    return sum((1 ^ ((r >> (7-i)) & 1)) << i for i in range(8))


def census(name, tables, global_keys, center_one, label_data, run):
    total = len(global_keys); universe = (1 << total)-1
    supports = [z | o for z, o in tables]
    ds = [deviations(p, center_one, universe) for p in tables]
    rows = []; degrees = [0]*256; occupied = [0]*256; shared_sum = [0]*256
    conflict_sum = [0]*256; costs = [0]*256; shared_compatible = [0]*256
    adjacency = np.eye(256, dtype=bool); eq_counts = [0]*4
    first_false = [None]*4; first_conflict = None; vacuous = 0
    for a in range(256):
        for b in range(a+1, 256):
            p, q = tables[a], tables[b]; bad = conflict(p, q)
            z = (p[0] & q[0]).bit_count(); o = (p[1] & q[1]).bit_count()
            c = bad.bit_count(); s = z+o+c
            eq = [int(ds[a][i] == ds[b][i]) for i in range(4)]
            assert not c or not any(eq)
            rows.append((a, b, z, o, c, *eq))
            for i in range(4): eq_counts[i] += eq[i]
            for r in (a, b): shared_sum[r] += s; conflict_sum[r] += c
            if c:
                if first_conflict is None: first_conflict = {'a':a, 'b':b, **witness(bad,p,q,global_keys)}
                continue
            adjacency[a,b] = adjacency[b,a] = True
            vacuous += int(s == 0)
            for r, other in ((a,b),(b,a)):
                degrees[r] += 1; occupied[r] += int(s > 0); shared_compatible[r] += s
                costs[r] += supports[other].bit_count()-s
            for i in range(4):
                if not eq[i] and first_false[i] is None:
                    first_false[i] = {'a':a, 'b':b, **witness(ds[a][i] ^ ds[b][i],p,q,global_keys)}
    matrix = np.array(rows, dtype=np.uint32); pair_path = run / f'pairs_{name}.npz'
    np.savez_compressed(pair_path, rows=matrix)
    edges = int(np.count_nonzero(adjacency)-256)//2
    assert sum(degrees) == 2*edges and edges == int(np.count_nonzero(matrix[:,4] == 0))
    per_rule = []
    for r, (z,o) in enumerate(tables):
        per_rule.append({'rule':r,'forced':(z|o).bit_count(),'forced_zero':z.bit_count(),
                         'forced_one':o.bit_count(),'compatible_partners':degrees[r],
                         'occupied_partners':occupied[r],'shared_keys_sum_all_partners':shared_sum[r],
                         'conflicting_keys_sum_all_partners':conflict_sum[r],
                         'shared_keys_sum_compatible_partners':shared_compatible[r],
                         'additional_pins_sum_compatible_partners':costs[r]})
    classes = {}
    for cl, reps in label_data['representatives'].items():
        selected = [r for r in reps if r not in (41,106)]
        vals = [degrees[r] for r in selected]
        classes[cl] = {'representatives':selected,'n':len(vals),'mean_degree':float(np.mean(vals)),
                       'median_degree':float(np.median(vals)),'min_degree':min(vals),'max_degree':max(vals)}
    transforms = {}
    for tag, f in (('output_complement',lambda r:255-r),('boolean_conjugacy',conjugate)):
        pairs = [(r,f(r)) for r in range(256) if r < f(r)]
        transforms[tag] = {'distinct_pairs':len(pairs),'compatible_pairs':sum(int(adjacency[a,b]) for a,b in pairs),
                           'incompatible_pairs':[[a,b] for a,b in pairs if not adjacency[a,b]]}
    return {'pairs':len(rows),'compatible_pairs':edges,'compatible_fraction':edges/len(rows),
            'vacuous_compatible_pairs':vacuous,'occupied_compatible_pairs':edges-vacuous,
            'completed_equal_pairs':dict(zip(POLICIES,eq_counts)),
            'false_conflicts':{p:edges-eq_counts[i] for i,p in enumerate(POLICIES)},
            'first_false_conflicts':dict(zip(POLICIES,first_false)), 'first_conflict':first_conflict,
            'per_rule':per_rule, 'anchors':{str(r):per_rule[r] for r in ANCHORS},
            'classes_core_convention':classes,'transforms':transforms,
            'pair_file':pair_path.name,'pair_file_sha256':sha(pair_path)}, adjacency


def self_test():
    # A forced one versus an unspecified entry is compatible but no-flip fills disagree.
    a, b = (0,1), (2,0); u = 3; center = 2
    assert conflict(a,b) == 0 and deviations(a,center,u)[0] != deviations(b,center,u)[0]
    assert conflict(a,(1,0)) == 1
    assert conflict((3,0),(2,4)) == 0
    # Exhaustive ternary two-key tables: independent truth-table interpretation.
    import itertools
    for pa in itertools.product((-1,0,1),repeat=2):
        p = tuple(sum(1<<i for i,x in enumerate(pa) if x==v) for v in (0,1))
        for qa in itertools.product((-1,0,1),repeat=2):
            q = tuple(sum(1<<i for i,x in enumerate(qa) if x==v) for v in (0,1))
            compatible = all(x<0 or y<0 or x==y for x,y in zip(pa,qa))
            assert (conflict(p,q)==0) == compatible
            for i, default in enumerate(((0,0),(1,1),(0,1),(1,0))):
                pp = tuple(d if x<0 else x for d,x in zip(default,pa))
                qq = tuple(d if x<0 else x for d,x in zip(default,qa))
                assert (deviations(p,2,3)[i]==deviations(q,2,3)[i]) == (pp==qq)
    return {'ternary_pair_controls':81,'completion_equality_controls':324}


def run(archive, output, run_dir):
    start=time.perf_counter(); signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('300 second budget'))); signal.alarm(300)
    archive=Path(archive); run_dir=Path(run_dir); run_dir.mkdir(parents=True,exist_ok=True)
    assert not (run_dir/'freeze.json').exists(), 'Use a fresh run directory'
    source_hashes={path:sha(ROOT/path) for path in (SCRIPT,PROTOCOL,LABELS)}
    assert sha(archive)==ARCHIVE_SHA
    write_json(run_dir/'freeze.json',{'source_hashes':source_hashes,'archive_sha256':ARCHIVE_SHA,
                                    'base_commit':'0d941dd50258e36fc240d468f83006d68a5fdb7e'})
    controls=self_test(); records={}; members={}
    with tarfile.open(archive,'r|gz') as tf:
        for member in tf:
            if member.name.split('/')[0] not in ('w7','w8') or not member.name.endswith('/d2.json'): continue
            raw=tf.extractfile(member).read(); key, table=read_record(raw)
            assert key not in records; records[key]=table
            members[member.name]=hashlib.sha256(raw).hexdigest()
    assert set(records)=={(w,r) for w in (7,8) for r in range(256)}
    keys=np.unique(np.concatenate([v[0] for v in records.values()]))
    compressed={}
    for (w,r),(ks,vs) in records.items():
        compressed[f'w{w}_r{r:03d}_keys']=ks; compressed[f'w{w}_r{r:03d}_values']=vs
    np.savez_compressed(run_dir/'physical_tables.npz',**compressed)
    center=as_bits(np.flatnonzero((keys>>17)&1)); tables={w:[] for w in (7,8)}
    for w in (7,8):
        for r in range(256):
            ks,vs=records[(w,r)]; ids=np.searchsorted(keys,ks)
            tables[w].append((as_bits(ids[vs==0]),as_bits(ids[vs==1])))
    label_data=json.loads((ROOT/LABELS).read_text()); domains={}; adjacency={}
    for w in (7,8):
        domains[f'w{w}'],adjacency[w]=census(f'w{w}',tables[w],keys,center,label_data,run_dir)
        print(f'width {w}: {domains[f"w{w}"]["compatible_pairs"]} compatible pairs; no-flip equal {domains[f"w{w}"]["completed_equal_pairs"]["no_flip"]}',flush=True)
    cross=[]; pool=[]
    for r in range(256):
        p,q=tables[7][r],tables[8][r]; bad=conflict(p,q)
        cross.append({'rule':r,'conflicts':bad.bit_count(),'witness':witness(bad,p,q,keys)})
        pool.append((p[0]|q[0],p[1]|q[1]))
    if not any(x['conflicts'] for x in cross):
        domains['pooled'],adjacency['pooled']=census('pooled',pool,keys,center,label_data,run_dir)
        assert not np.any(adjacency['pooled'] & ~(adjacency[7]&adjacency[8]))
    upper=np.triu(np.ones((256,256),dtype=bool),k=1)
    width_change={'w7_only':int(np.count_nonzero(upper & adjacency[7] & ~adjacency[8])),
                  'w8_only':int(np.count_nonzero(upper & adjacency[8] & ~adjacency[7])),
                  'both':int(np.count_nonzero(upper & adjacency[7] & adjacency[8]))}
    if 'pooled' in adjacency: width_change['both_but_not_pooled']=int(np.count_nonzero(upper & adjacency[7] & adjacency[8] & ~adjacency['pooled']))
    elapsed=time.perf_counter()-start; signal.alarm(0)
    raw_files={p.name:sha(p) for p in run_dir.iterdir() if p.is_file()}
    result={'schema_version':1,'experiment':'partial-cohabitation-20260915','source_hashes':source_hashes,
            'archive_sha256':ARCHIVE_SHA,'member_sha256':members,'global_physical_keys':len(keys),
            'local_neighborhood_bits':35,'ambient_table_entries':1<<35,'pair_columns':PAIR_COLUMNS,
            'domains':domains,'cross_width':cross,'width_change':width_change,'controls':controls,
            'predictions':{'P1_archive_validation':True,'P2_completed_equal_subset':True,
                           'P3_no_flip_false_conflicts':all(x['false_conflicts']['no_flip']>0 for x in domains.values()),
                           'P4_cross_width_consistent':not any(x['conflicts'] for x in cross)},
            'execution':{'seconds':elapsed,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                         'python':platform.python_version(),'numpy':np.__version__,'scientific_replays':0},
            'raw_files':raw_files}
    write_json(output,result)
    print(json.dumps({'seconds':elapsed,'predictions':result['predictions'],'width_change':width_change,'result':str(output)}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--archive',type=Path);parser.add_argument('--output',type=Path)
    parser.add_argument('--run-dir',type=Path);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    if args.self_test: print(json.dumps(self_test()))
    else:
        assert args.archive and args.output and args.run_dir
        run(args.archive,args.output,args.run_dir)
