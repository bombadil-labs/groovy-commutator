"""Run independent saved-data reconstruction after the relevant stage is authorized."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np
import oracle

ROOT = Path(__file__).resolve().parents[2]
UNIT = ROOT / 'experiments/rule_ring_structure_20260915'
RULES = [0, 18, 30, 54, 90, 110, 126, 204]
OBS = [f'future_{n}' for n in oracle.HORIZONS] + ['basin', 'cycle_length', 'transient_depth']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(stage):
    start = time.monotonic()
    widths = range(4, 13) if stage == 'discovery' else range(13, 17)
    if stage == 'confirmation':
        seal = json.loads((UNIT / 'confirmation-seal.json').read_text())
        assert seal['selection_sha256'] == sha(UNIT / 'discovery-selection.json')
        assert seal['discovery_result_sha256'] == sha(UNIT / 'discovery-result.json')
    info = json.loads((UNIT / f'{stage}-result.json').read_text())
    infos = {(r['ring'], r['rule']): r for r in info['case_info']}
    rows = json.loads((UNIT / f'{stage}-evidence.json').read_text())['rows']
    recorded_relations = {}
    for row in rows:
        for ring, rel in zip(row['rings'], row['relation_values']):
            key = (row['observation'], ring, *map(int, row['rules']))
            if key in recorded_relations:
                assert recorded_relations[key] == rel
            recorded_relations[key] = rel
    checked, labels_checked, relations_checked, max_entropy_error = 0, 0, 0, 0.
    predicted = {}
    for n in widths:
        all_labels = {}
        for rule in RULES:
            nxt, labels = oracle.partitions(rule, n)
            labels['transient_depth'] = labels.pop('transient_distance')
            meta = infos[n, rule]
            path = ROOT / meta['path']
            assert sha(path) == meta['sha256']
            with np.load(path, allow_pickle=False) as data:
                assert np.array_equal(data['successor'], nxt), (n, rule, 'successor')
                for name in OBS:
                    expected = labels[name]
                    if name == 'basin':
                        assert oracle.canonical_partition(data[name]) == oracle.canonical_partition(expected), (n, rule, name)
                    else:
                        assert np.array_equal(data[name], expected), (n, rule, name)
                    actual_entropy = oracle.entropy_counts(Counter(expected).values())
                    delta = abs(actual_entropy - meta['entropies'][name])
                    assert delta < 1e-11, (n, rule, name, delta)
                    max_entropy_error = max(delta, max_entropy_error)
                    assert meta['blocks'][name] == len(set(expected))
                    labels_checked += len(expected)
            assert meta['max_transient'] == max(labels['transient_depth'])
            assert meta['max_cycle_length'] == max(labels['cycle_length'])
            if rule == 90:
                for horizon in oracle.HORIZONS:
                    rank = oracle.rule90_rank(n, horizon)
                    actual_entropy = oracle.entropy_counts(Counter(labels[f'future_{horizon}']).values())
                    assert abs(actual_entropy - rank) < 1e-11, (n, horizon, actual_entropy, rank)
                assert (len(set(labels['future_16'])) == 1) == (n in (4, 8, 16))
            checked += 1
            all_labels[rule] = labels
        for name in OBS:
            for a, b in itertools.combinations(RULES, 2):
                ha, hb, joint, vi = oracle.relation(all_labels[a][name], all_labels[b][name])
                expected = dict(h_a=ha, h_b=hb, h_joint=joint, vi=max(0., min(float(n), vi)), vi_per_bit=max(0., min(float(n), vi))/n)
                key = (name, n, a, b)
                recorded = recorded_relations[key]
                for field, value in expected.items():
                    err = abs(recorded[field] - value)
                    assert err < 1e-11, (key, field, value, recorded[field])
                    max_entropy_error = max(max_entropy_error, err)
                predicted[repr(key)] = expected
                relations_checked += 1
        print(f'{stage} width {n}: complete', flush=True)
    result = {'status': 'verified', 'stage': stage, 'cases': checked,
              'partition_label_entries': labels_checked, 'relations': relations_checked,
              'maximum_entropy_relation_error': max_entropy_error,
              'wall_seconds': time.monotonic() - start, 'oracle_sha256': sha(Path(oracle.__file__)),
              'verifier_sha256': sha(Path(__file__)), 'input_result_sha256': sha(UNIT / f'{stage}-result.json')}
    target = Path(__file__).parent
    (target / f'{stage}-verification.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    (target / f'{stage}-independent-relations.json').write_text(json.dumps(predicted, sort_keys=True) + '\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['discovery', 'confirmation'])
    verify(parser.parse_args().stage)
