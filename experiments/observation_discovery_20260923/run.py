#!/usr/bin/env python3
"""Frozen bounded observation selection; target evaluations only in main()."""
import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import platform
import signal
import subprocess
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = '02948ab8ff523574a4ee11fdf0b379714ca87221'
SOURCES = ['experiments/observation_discovery_20260923/run.py',
           'experiments/observation_discovery_20260923/verify.py',
           'docs/research/protocols/observation-discovery-20260923.md']
RAW_IDS = tuple(range(7)) + (14, 15, 16)


def grammar():
    features = []
    def add(name, ops):
        features.append({'id': len(features), 'name': name, 'operands': ops})
    for x in range(-3, 4): add(f'now[{x}]', [[0, x]])
    for x in range(-3, 3): add(f'now[{x}] XOR now[{x+1}]', [[0, x], [0, x+1]])
    add('now[-1] XOR now[1]', [[0, -1], [0, 1]])
    for x in range(-1, 2): add(f'past[{x}]', [[-1, x]])
    for x in range(-1, 2): add(f'past[{x}] XOR now[{x}]', [[-1, x], [0, x]])
    return features


def evolve(a, rule):
    idx = 4*a[:, :-2] + 2*a[:, 1:-1] + a[:, 2:]
    return ((rule >> idx.astype(np.int64)) & 1).astype(np.uint8)


def groovy(a, rule):
    b = evolve(a, rule)
    c = evolve(b, rule)
    return b[:, 1:-1] ^ c ^ evolve(a[:, 1:-1] ^ b, rule)


def make_rows(rule):
    seeds = ((np.arange(512)[:, None] >> np.arange(9)) & 1).astype(np.uint8)
    now = evolve(seeds, rule)
    nxt = evolve(now, rule)
    base = now[:, 3] if rule == 90 else groovy(now, rule)[:, 1]
    target = nxt[:, 2] if rule == 90 else groovy(nxt, rule)[:, 0]
    words = np.zeros(512, dtype=np.int64)
    for f in grammar():
        col = np.zeros(512, dtype=np.uint8)
        for t, x in f['operands']:
            col ^= seeds[:, x+4] if t == -1 else now[:, x+3]
        words |= col.astype(np.int64) << f['id']
    return [{'seed': s, 'base': int(base[s]), 'target': int(target[s]),
             'features': int(words[s]), 'now': now[s].tolist()} for s in range(512)]


def candidates(ids):
    fs = grammar()
    encoded = []
    for f in fs:
        raw = sum(1 << (x+3 if t == 0 else x+8) for t, x in f['operands'])
        encoded.append(raw)
    out = []
    for k in range(8):
        for combo in itertools.combinations(ids, k):
            raw = 0
            for i in combo: raw |= encoded[i]
            cost = (k, raw.bit_count(), (raw >> 7).bit_count(),
                    sum(len(fs[i]['operands']) == 2 for i in combo), combo)
            out.append((cost, sum(1 << i for i in combo)))
    out.sort()
    return out


def oracle(rows, mask):
    seen = {}
    for row in rows:
        key = (row['base'], row['features'] & mask)
        if key in seen:
            before = seen[key]
            if rows[before]['target'] != row['target']:
                return [before, row['seed']]
        else: seen[key] = row['seed']
    return None


def lookup(rows, mask):
    ids = [i for i in range(20) if mask >> i & 1]
    table = {}
    for row in rows:
        address = row['base'] | sum(((row['features'] >> i) & 1) << (j+1)
                                   for j, i in enumerate(ids))
        value = row['target']
        assert str(address) not in table or table[str(address)] == value
        table[str(address)] = value
    return dict(sorted(table.items(), key=lambda kv: int(kv[0])))


def costs(mask, rule, rows):
    fs = grammar()
    ids = [i for i in range(20) if mask >> i & 1]
    ops = {tuple(op) for i in ids for op in fs[i]['operands']}
    base_ops = {(0, x) for x in range(-2, 3)} if rule == 30 else {(0, 0)}
    union = ops | base_ops
    return {'selected_bits': len(ids), 'retained_bits_including_base': 1+len(ids),
            'feature_operands': [list(x) for x in sorted(ops)],
            'all_raw_operands': [list(x) for x in sorted(union)],
            'raw_read_count_including_base': len(union),
            'past_buffer_cells': sum(t == -1 for t, x in union),
            'feature_xors': sum(len(fs[i]['operands']) == 2 for i in ids),
            'base_rule_evaluations': 5 if rule == 30 else 0,
            'base_xors': 5 if rule == 30 else 0,
            'reachable_lut_entries': len(lookup(rows, mask)),
            'dense_lut_address_capacity': 1 << (1+len(ids))}


def search(rows, rule, arm):
    start = time.perf_counter()
    cands = candidates(RAW_IDS if arm == 'raw' else range(20))
    prep = time.perf_counter() - start
    t = time.perf_counter()
    witnesses, calls, pruned, comparisons, winner = [], 0, 0, 0, None
    visited = 0
    for rank, (cost, mask) in enumerate(cands):
        visited += 1
        reject = False
        if arm == 'guided':
            for witness in witnesses:
                comparisons += 1
                if not mask & witness['distinguish_mask']:
                    pruned += 1
                    reject = True
                    break
        if reject: continue
        calls += 1
        pair = oracle(rows, mask)
        if pair is None:
            winner = {'mask': mask, 'features': list(cost[-1]), 'rank': rank,
                      'cost_order': list(cost[:4]), 'lookup': lookup(rows, mask),
                      'costs': costs(mask, rule, rows)}
            break
        if arm == 'guided':
            a, b = pair
            assert rows[a]['base'] == rows[b]['base']
            diff = rows[a]['features'] ^ rows[b]['features']
            assert not diff & mask and rows[a]['target'] != rows[b]['target']
            witnesses.append({'pair': pair, 'candidate_mask': mask,
                              'candidate_rank': rank, 'distinguish_mask': diff})
    elapsed = time.perf_counter() - t
    return {'arm': arm, 'candidate_count': len(cands), 'visited': visited,
            'full_oracle_calls': calls, 'pruned': pruned,
            'witness_comparisons': comparisons, 'witnesses': witnesses,
            'winner': winner, 'status': 'success' if winner else 'bounded_exhaustion',
            'preparation_seconds': prep, 'search_seconds': elapsed,
            'total_seconds': prep+elapsed}


def evaluate(rule):
    rows = make_rows(rule)
    arms = {a: search(rows, rule, a) for a in ('scan', 'guided', 'raw')}
    assert arms['scan']['winner'] == arms['guided']['winner']
    windows = []
    for radius in range(4):
        mask = sum(1 << (x+3) for x in range(-radius, radius+1))
        pair = oracle(rows, mask)
        windows.append({'radius': radius, 'mask': mask, 'witness': pair,
                        'sufficient': pair is None,
                        'costs': costs(mask, rule, rows) if pair is None else None})
    return {'rule': rule, 'rows': rows, 'arms': arms, 'raw_windows': windows}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--implementation-commit', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('120-second cap')))
    signal.alarm(120)
    start = time.perf_counter()
    # Pin exactly the implementation sources without requiring the whole tree clean.
    for name in SOURCES:
        committed = subprocess.check_output(['git', 'show', f'{a.implementation_commit}:{name}'], cwd=ROOT)
        assert committed == (ROOT/name).read_bytes(), f'unpinned source: {name}'
    cases = [evaluate(90), evaluate(30)]
    cal, test = [c['arms'] for c in cases]
    cw, cr = cal['guided']['winner'], cal['raw']['winner']
    tw, tr = test['guided']['winner'], test['raw']['winner']
    def outcome(x): return 'supported' if x else 'failed'
    predictions = {
        'P1': outcome(cw is not None and cr is not None and cw['features'] == [13] and len(cr['features']) >= 2),
        'P2': outcome(len(tw['features']) < len(tr['features'])) if tw and tr else 'not_evaluated',
        'P3': outcome(test['guided']['full_oracle_calls'] < test['scan']['full_oracle_calls']),
        'P4': outcome(any(i >= 14 for i in tw['features'])) if tw else 'not_evaluated',
        'P5': outcome(test['guided']['total_seconds'] < test['scan']['total_seconds'])}
    result = {'protocol_commit': PROTOCOL, 'implementation_commit': a.implementation_commit,
              'created_at': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(),
              'numpy': np.__version__, 'source_hashes': {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in SOURCES},
              'grammar': grammar(), 'cases': cases, 'predictions': predictions,
              'elapsed_seconds': time.perf_counter()-start}
    with Path(a.output).open('x') as f: json.dump(result, f, indent=2); f.write('\n')
    signal.alarm(0)
    print(json.dumps({'predictions': predictions, 'elapsed_seconds': result['elapsed_seconds'],
                      'winners': {str(c['rule']): {n: v['winner'] for n, v in c['arms'].items() if n != 'scan'} for c in cases}}, indent=2))

if __name__ == '__main__': main()
