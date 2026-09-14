"""Cheap preservation/accounting for the saved 6D pilot, never a CA replay."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = 'experiments/sequential_lift_6d_20260914/run'
RESULT = 'results/sequential_lift_6d_20260914.json'
SOURCES = {
    'script': 'scripts/sequential_lift_6d_pilot.py',
    'protocol': 'docs/research/protocols/sequential-lift-6d-pilot-20260914.md',
    'accounting': 'scripts/verify_sequential_lift_pilot.py',
    'raw_floors': RUN + '/floors.jsonl',
    'raw_summary': RUN + '/summary.json',
    'execution': RUN + '/execution.json',
}


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def derive():
    raw = json.loads((ROOT / SOURCES['raw_summary']).read_text())
    rows = [json.loads(line) for line in (ROOT / SOURCES['raw_floors']).read_text().splitlines()]
    assert raw['rules'] == [90, 54, 110, 157, 171, 233]
    assert raw['width'] == 7 and raw['max_dimension'] == 6
    assert raw['source_states_per_rule'] == 128
    assert len(rows) == raw['completed_floors']
    for path, recorded in raw['source_hashes'].items():
        assert path in (SOURCES['script'], SOURCES['protocol'])
        assert recorded == digest(path), path
    expected = {(rule, dimension) for rule in raw['rules'] for dimension in range(2, 7)}
    assert len({(r['rule'], r['dimension']) for r in rows}) == len(rows)
    assert {(r['rule'], r['dimension']) for r in rows} == expected
    for row in rows:
        assert row['status'] == 'passed'
        d, p = row['dimension'], 5 if row['rule'] in (171, 233) else 4
        assert row['transverse_period'] == p
        assert row['fields_per_source_site'] == p ** (d - 1)
        assert row['cells_per_configuration'] == 7 * p ** (d - 1)
        assert row['checked_native_cells'] == 128 * 7 * p ** (d - 1)
        assert row['full_neighborhood_bits'] == 5 ** d
        assert row['distinct_periodic_neighborhood_bits'] == 5 * p ** (d - 1)
        assert row['direct_patch_checks'] == 15
        for key in ('native', 'parent_recovery'):
            assert row[key]['passes'] and row[key]['conflicting_keys'] == 0 and row[key]['witness'] is None
        for key in ('native_replay', 'decoder_replay', 'composed_source_recovery', 'parent_rules_unchanged'):
            assert row[key] is True
    passed = [r['rule'] for r in rows if r['dimension'] == 6]
    assert passed == raw['passed_6d'] and not raw['failures'] and not raw['censored']
    timings = []
    for d in range(2, 7):
        for p in (4, 5):
            cases = [r for r in rows if r['dimension'] == d and r['transverse_period'] == p]
            timings.append({'from_dimension': d - 1, 'to_dimension': d, 'period': p,
                            'build_seconds_min': min(r['build_seconds'] for r in cases),
                            'build_seconds_max': max(r['build_seconds'] for r in cases)})
    return {'schema_version': 1, 'date': '2026-09-14',
            'scope': raw['scope'], 'baseline_commit': raw['baseline_commit'],
            'implementation_commit': raw['implementation_commit'],
            'source_paths': SOURCES, 'source_hashes': {key: digest(path) for key, path in SOURCES.items()},
            'summary': {'rules': raw['rules'], 'passed_through_6d': passed, 'completed_floors': len(rows),
                        'width': 7, 'states_per_rule': 128,
                        'native_constraint_cells': sum(r['checked_native_cells'] for r in rows),
                        'direct_patch_checks': sum(r['direct_patch_checks'] for r in rows),
                        'failures': [], 'censored': [], 'recursive_G': 'not tested',
                        'all_infinite_inputs': 'not tested', 'arbitrary_native_CA_generator': 'not established'},
            'measurements': {'wall_seconds': raw['wall_seconds'], 'peak_rss_bytes': raw['peak_rss_bytes'],
                             'build_times': timings},
            'completion_scope': 'New native tables synthesized on the finite width-seven family; archived full-shift/G constraints are not retained. Immutable zero completion at every level.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    rendered = json.dumps(derive(), indent=2) + '\n'
    path = ROOT / RESULT
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered)
    else:
        assert path.read_text() == rendered, 'Canonical account differs from preserved raw records'
        import check_result_integrity as integrity
        problems = integrity.check(RESULT)
        assert not problems, problems
    print(json.dumps({'accounting': 'passed', 'result': RESULT}))


if __name__ == '__main__':
    main()
