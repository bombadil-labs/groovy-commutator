#!/usr/bin/env python3
"""Build the canonical, source-pinned summary of both frozen experiments."""
import json
from pathlib import Path
from commutator_history import ROOT, UNIT, digest, save


def main():
    history = json.loads((UNIT/'result.json').read_text())
    response = json.loads((UNIT/'response-result.json').read_text())
    audit_history = json.loads((ROOT/'review/commutator_history_independent.json').read_text())
    audit_response = json.loads((ROOT/'review/commutator_response_independent.json').read_text())
    assert audit_history['all_families_replayed'] and audit_response['all_cases_replayed']
    paths = set(history['source_hashes']) | set(response['source_hashes'])
    paths.update('scripts/'+p+'.py' for p in ['summarize_commutator_history',
                 'plot_commutator_history', 'package_commutator_history'])
    paths.update('review/'+p+s for p in ['commutator_history_independent', 'commutator_response_independent']
                 for s in ['.py', '.json'])
    paths.update('experiments/commutator_history_20260915/'+name for name in [
        'freeze.json', 'response-freeze.json', 'response-result.json', 'raw-archive.json'])
    for source, recorded in history['source_hashes'].items():
        assert digest(ROOT/source) == recorded
    for source, recorded in response['source_hashes'].items():
        assert digest(ROOT/source) == recorded
    normal = [f for f in history['families'] if not f['shuffled']]
    reps = [f for f in normal if f['kind'] == 'eca' and f['rule'] == f['representative']]
    tests = [t for f in reps for t in f['tests']]
    core = [t for f in reps if f['rule'] in (54, 110) for t in f['tests']]
    negative = [t for f in reps if f['rule'] not in (41, 54, 106, 110) for t in f['tests']]
    delayed = {}
    for case in response['cases']:
        label = ('eca'+str(case['rule'])) if case['kind'] == 'eca' else f"wide{case['radius']}_g{int(case['correction'])}"
        row = case['outcomes'][-1]
        out = delayed.setdefault(label, {'local_trials': 0, 'changed': 0, 'remote_trials': 0, 'remote_changed': 0})
        out['local_trials'] += row['local_trials']
        out['changed'] += row['changed_local_responses']
        out['remote_trials'] += row['remote_trials']
        out['remote_changed'] += row['remote_changed']
    result = {
        'evidence': 'exploratory',
        'source_hashes': {p: digest(ROOT/p) for p in sorted(paths)},
        'raw_input_hashes': history['raw_input_hashes'],
        'raw_output_hashes': {'histories-and-counts.npz': history['raw_output_sha256'],
                              'response-arrays.npz': response['raw_sha256']},
        'summary': {
            'history_representatives': len(reps), 'history_heldout_representative_tests': len(tests),
            'baseline_selected': sum(t['baseline_selected'] for t in tests),
            'augmented_selected': sum(t['augmented_selected'] for t in tests),
            'changed_decisions': sum(t['baseline_selected'] != t['augmented_selected'] for t in tests),
            'core_selected': sum(t['augmented_selected'] for t in core), 'core_tests': len(core),
            'undisputed_negative_selected': sum(t['augmented_selected'] for t in negative),
            'undisputed_negative_tests': len(negative),
            'eca_rules_admitting_short_interaction': sum(c['interacting_contexts'] > 0 for c in response['short_census']),
            'short_zero_family': 'f(l,c,r)=a*c XOR g(l,r), with constant a; exactly 32 tables',
            'radius_two_short_interacting_contexts': response['wider_short_census']['interacting_contexts'],
            'radius_two_short_contexts': response['wider_short_census']['contexts'],
            'rule4_G_zero_interacting_contexts': response['short_census'][4]['interacting_contexts'],
        },
        'history_family_summaries': [
            {'id': f['id'], 'velocity': f['chosen_velocity'],
             'test_seeds': [t['seed'] for t in f['tests']],
             'gain_bits': [t['gain_bits'] for t in f['tests']],
             'augmented_selected': [t['augmented_selected'] for t in f['tests']]}
            for f in history['families']],
        'delayed_response_horizon32': delayed,
        'timings_seconds': {'history': history['seconds'], 'response': response['seconds'],
                            'independent_history': audit_history['seconds'],
                            'independent_response': audit_response['seconds']},
        'limits': [
            'Finite model-relative predictive gain; no irreducible temporal-memory or causal G-feedback proof.',
            'No held-out baseline decision changes; the radius-two rule is unclassified and remains selected.',
            'R6 baseline-positive rule 106 seed trains this test and is not a held-out removal test.',
            'All ECA families were inspected previously; held-out units are initial conditions.',
            'Generic response modulation does not establish adaptation, response quality or Class IV specificity.',
            'Raw G-history gains change under complement conjugation; no beam invariance is established.'
        ]
    }
    save(ROOT/'results/commutator_history_20260915.json', result)
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
