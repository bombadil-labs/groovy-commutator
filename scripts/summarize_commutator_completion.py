#!/usr/bin/env python3
"""Compact exact completion audit; no fitted scores or class labels."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/commutator_completion_20260915'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    primary = json.loads((UNIT / 'result.json').read_text())
    review = json.loads((ROOT / 'review/commutator_completion_independent.json').read_text())
    assert primary['completed_records'] == 1536 and primary['censored_records'] == 0
    assert review['all_checks_passed'] and review['reviewed_records'] == 1536
    assert review['reviewed_contracts'] == 2048
    assert review['primary_result_sha256'] == digest(UNIT / 'result.json')
    rows, groups = [], []
    for r in primary['records']:
        for contract, c in r['contracts'].items():
            rows.append({
                'id': r['id'], 'rule': r['rule'], 'width': r['width'], 'dimension': r['dimension'],
                'contract': contract,
                **{k: c[k] for k in ('cells', 'fixed_zero', 'fixed_one', 'free_cells', 'free_keys',
                   'fully_fixed_states', 'difference_in_family_states', 'fully_fixed_off_family_states',
                   'variables_shared_across_states', 'variable_state_uses_sum',
                   'mean_variable_occurrences', 'max_variable_occurrences',
                   'equal_G_pairs_from_shared_variable', 'opposite_G_pairs_from_shared_variable')},
            })
    for w in (7, 8):
        for d, contract in ((2, 'finite'), (2, 'full_input_d2'), (3, 'finite'), (4, 'finite')):
            rs = [r for r in rows if (r['width'], r['dimension'], r['contract']) == (w, d, contract)]
            totals = {k: sum(r[k] for r in rs) for k in ('cells', 'fixed_zero', 'fixed_one', 'free_cells', 'free_keys')}
            groups.append({'width': w, 'dimension': d, 'contract': contract,
                           'rules': len(rs), 'rules_with_ambiguity': sum(r['free_keys'] > 0 for r in rs),
                           'fully_determined_rules': [r['rule'] for r in rs if r['free_keys'] == 0],
                           'all_cells_ambiguous_rules': [r['rule'] for r in rs if r['free_cells'] == r['cells']],
                           **totals, 'free_fraction': totals['free_cells'] / totals['cells']})
    sources = set(primary['source_hashes']) | {
        'scripts/summarize_commutator_completion.py', 'scripts/package_commutator_completion.py',
        'review/commutator_completion_independent.py', 'review/commutator_completion_independent.json',
        'experiments/commutator_completion_20260915/freeze.json',
        'experiments/commutator_completion_20260915/raw-archive.json',
    }
    result = {
        'evidence': 'exact-within-declared-contracts',
        'source_hashes': {p: digest(ROOT / p) for p in sorted(sources)},
        'raw_input_hashes': primary['raw_input_hashes'],
        'raw_result_sha256': digest(UNIT / 'result.json'),
        'completed_records': 1536, 'source_rule_contracts': len(rows),
        'scalar_physical_checks': sum(r['scalar_physical_checks'] for r in primary['records']),
        'primary_seconds': primary['seconds'], 'primary_peak_rss_kib': primary['peak_rss_kib'],
        'independent_seconds': review['seconds'],
        'independent_waiting_seconds': review['waiting_for_primary_record_seconds'],
        'primary_arrays_bytes': primary['raw_arrays_bytes'],
        'groups': groups, 'records': rows,
        'finite_D2_free_cells_resolved_by_full_input': {
            str(w): sum(r.get('finite_free_cells_resolved_by_full_input', 0)
                        for r in primary['records'] if r['width'] == w) for w in (7, 8)
        },
        'identity': 'G_H(Y) = T(Y) XOR delta_H(D(Y)); one shared Boolean variable per distinct queried unforced physical key',
        'limits': [
            'D2 full-input membership is complete, but queried source states are the declared periodic rings.',
            'D3/D4 freedom is relative to each finite source-family table; larger input domains may add commitments.',
            'No pooling of widths; source-rule completions and distinct dimensions have separate variable spaces.',
            'Shared-variable equalities include periodic and translation-related repeats; no class specificity follows.',
            'No preferred completion, probability measure, classifier, recoding invariance or universal lift induction is supplied.',
        ],
    }
    target = ROOT / 'results/commutator_completion_20260915.json'
    target.write_text(json.dumps(result, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n')
    print(json.dumps({'groups': groups, 'seconds': primary['seconds'], 'bytes': target.stat().st_size}))


if __name__ == '__main__':
    main()
