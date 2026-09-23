#!/usr/bin/env python3
"""Independent full finite audit: library scalar CA, explicit future words,
set-partition grammar, direct grouping/action intersections. No search oracle.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import signal
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def encoders():
    partitions = [()]
    for x in range(8):
        updated = []
        for blocks in partitions:
            updated.append(blocks+((x,),))
            for i in range(len(blocks)):
                updated.append(blocks[:i]+(blocks[i]+(x,),)+blocks[i+1:])
        partitions = updated
    result = []
    for blocks in partitions:
        p = [None]*8
        for label, block in enumerate(blocks):
            for x in block:
                p[x] = label
        result.append(tuple(p))
    return sorted(result, key=lambda p: (len(set(p)), p))


def observe(p, s):
    bits = [(s >> i) & 1 for i in range(12)]
    return tuple(p[bits[i]+2*bits[i+1]+4*bits[i+2]] for i in range(0, 12, 3))


def common(sets):
    return set.intersection(*sets)


def verify(data):
    assert data['status'] == 'complete'
    for path, digest in data['source_hashes'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path
    spec = importlib.util.spec_from_file_location('scalar_ca', ROOT/'src/groovy/ca.py')
    ca = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ca)
    step = np.array([ca.apply_rule_int(s, 12, 54) for s in range(4096)])
    base = [0, 0, 1, 1]*3
    viable = {sum(base[(i-offset) % 12] << i for i in range(12)) for offset in range(12)}
    states = sorted(viable | {v ^ (1 << i) for v in viable for i in range(12)})
    assert sorted(viable) == data['viable_states']
    assert states == data['initial_states']
    assert len(viable) == 4 and len(states) == 52 and all(int(step[v]) in viable for v in viable)
    member = np.array([s in viable for s in range(4096)], dtype=np.uint8)
    current = np.arange(4096)
    columns = [member]
    counts = [len(np.unique(member))]
    for _ in range(64):
        current = step[current]
        columns.append(member[current])
        words = np.stack(columns, axis=1)
        _, first, labels = np.unique(words, axis=0, return_index=True, return_inverse=True)
        counts.append(len(first))
        if counts[-1] == counts[-2]:
            break
    else:
        raise AssertionError('explicit future words did not stabilize')
    assert counts == data['refinement_class_counts']
    assert np.array_equal(labels[step], labels[step[first[labels]]])
    wins = {}
    for s in states:
        wins[s] = set()
        for action in range(13):
            x = s if action == 0 else s ^ (1 << (action-1))
            for _ in range(4):
                x = int(step[x])
            if x in viable:
                wins[s].add(action)
        assert wins[s]
    assert [sum(1 << a for a in wins[s]) for s in states] == data['successful_action_masks']
    ps = encoders()
    assert len(ps) == len(set(ps)) == 4140
    assert [''.join(map(str, p)) for p in ps] == data['complete_table']['encoders']
    expected_flags = []
    groups_by_candidate = []
    for p in ps:
        groups = {}
        for s in states:
            groups.setdefault(observe(p, s), []).append(s)
        groups_by_candidate.append(groups)
        predicts = all(len({int(labels[s]) for s in group}) == 1 for group in groups.values())
        repairs = all(common([wins[s] for s in group]) for group in groups.values())
        expected_flags.append([predicts, repairs])
    assert expected_flags == data['complete_table']['flags_predict_repair']

    def witness(p, w, task):
        ss = w['states']
        assert len(ss) >= 2 and len(set(ss)) == len(ss) and set(ss) <= set(states)
        assert len({observe(p, s) for s in ss}) == 1
        if w['kind'] == 'predict':
            assert task in ('predict', 'joint') and len(ss) == 2
            times = np.flatnonzero(words[ss[0]] != words[ss[1]])
            assert len(times) and w['first_difference'] == int(times[0])
        else:
            assert task in ('repair', 'joint') and w['kind'] == 'repair'
            assert w['winning_masks'] == [sum(1 << a for a in wins[s]) for s in ss]
            assert not common([wins[s] for s in ss])
            assert all(common([wins[s] for s in ss if s != removed]) for removed in ss)

    def policy(p, record):
        groups = {}
        for s in states:
            groups.setdefault(observe(p, s), []).append(s)
        assert record is not None and record['state_count'] == len(states)
        assert len(record['entries']) == len(groups)
        seen, flips = set(), 0
        for row in record['entries']:
            key = tuple(row['observation'])
            assert key in groups and key not in seen
            seen.add(key)
            assert row['states'] == groups[key]
            options = common([wins[s] for s in groups[key]])
            assert row['action'] == min(options)
            flips += (row['action'] != 0)*len(groups[key])
        assert record['flips_on_uniform_domain'] == flips

    for task, result in data['searches'].items():
        accepted = [i for i, (p, r) in enumerate(expected_flags)
                    if (p if task == 'predict' else r if task == 'repair' else p and r)]
        minimum_k = len(set(ps[accepted[0]]))
        expected = {'sufficient_count': len(accepted), 'minimum_alphabet': minimum_k,
                    'all_minimum_indices': [i for i in accepted if len(set(ps[i])) == minimum_k]}
        assert expected == data['complete_table']['summary'][task]
        winner = result['winner']
        assert winner == accepted[0] and result['encoder'] == list(ps[winner])
        assert result['alphabet'] == minimum_k
        queried = result['queries']
        assert queried == [w['candidate'] for w in result['witnesses']]+[winner]
        assert len(set(queried)) == result['full_oracle_calls'] == len(queried)
        for w in result['witnesses']:
            witness(ps[w['candidate']], w, task)
        rejected = set()
        for candidate, wid in result['rejections']:
            assert 0 <= candidate < winner and 0 <= wid < len(result['witnesses'])
            assert candidate not in queried and candidate not in rejected
            rejected.add(candidate)
            witness(ps[candidate], result['witnesses'][wid], task)
        assert set(queried[:-1]) | rejected == set(range(winner))
        if expected_flags[winner][1]:
            policy(ps[winner], result['policy'])
        else:
            assert result['policy'] is None
    policy(tuple(range(8)), data['controls']['identity_policy'])
    fixed = [sum(a in wins[s] for s in states) for a in range(13)]
    assert data['controls']['fixed_action_success_counts'] == fixed
    assert data['controls']['best_fixed_success_count'] == max(fixed)
    assert data['controls']['noop_success_count'] == fixed[0]
    separation = next((i for i, (p, r) in enumerate(expected_flags) if p and not r), None)
    recorded = data['complete_table']['prediction_without_repair']
    assert (recorded is None) == (separation is None)
    if recorded is not None:
        assert recorded['index'] == separation and recorded['encoder'] == list(ps[separation])
        witness(ps[separation], recorded['witness'], 'repair')
    lossy = next((i for i, (_, r) in enumerate(expected_flags)
                  if r and len(groups_by_candidate[i]) < len(states)), None)
    record = data['complete_table']['lossy_repair']
    assert (record is None) == (lossy is None)
    if record is not None:
        assert record['index'] == lossy and record['fiber_count'] == len(groups_by_candidate[lossy])
    # Reconstruct the specified deterministic first-conflict/deletion sample.
    sizes = {}
    for i, (_, repairs) in enumerate(expected_flags):
        if repairs:
            continue
        group = next(list(g) for g in groups_by_candidate[i].values() if not common([wins[s] for s in g]))
        for s in list(group):
            rest = [x for x in group if x != s]
            if not common([wins[x] for x in rest]):
                group = rest
        size = str(len(group))
        sizes[size] = sizes.get(size, 0)+1
    assert sizes == data['complete_table']['first_failing_repair_fiber_minimal_sizes']
    summary = data['complete_table']['summary']
    predictions = {'P1': True, 'P2': separation is not None,
        'P3': summary['joint']['minimum_alphabet'] > summary['predict']['minimum_alphabet'],
        'P4': lossy is not None, 'P5': any(int(k) > 2 for k in sizes)}
    assert data['predictions'] == {k: 'supported' if v else 'failed' for k, v in predictions.items()}
    assert all(data['checks'].values())
    return {'ok': True, 'source_states_checked': 4096, 'initial_states_checked': 52,
            'candidate_rows_checked': 4140, 'guided_search_certificates_checked': 3,
            'predictions': data['predictions']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('result', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    def timeout(*_):
        raise TimeoutError('120-second independent verification wall cap')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(120)
    start = time.perf_counter()
    try:
        result = verify(json.loads(args.result.read_text()))
    except Exception as exc:
        result = {'ok': False, 'error_type': type(exc).__name__, 'message': str(exc)}
    finally:
        signal.alarm(0)
    result.update(elapsed_seconds=time.perf_counter()-start,
                  result_sha256=hashlib.sha256(args.result.read_bytes()).hexdigest())
    if args.output:
        with args.output.open('x') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
