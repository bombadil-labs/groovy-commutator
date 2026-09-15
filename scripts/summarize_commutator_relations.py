#!/usr/bin/env python3
"""Compact public record of the frozen, independently replayed relation audit."""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/commutator_relations_20260915'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    primary = json.loads((UNIT / 'result.json').read_text())
    replay = json.loads((ROOT / 'review/replay/result.json').read_text())
    compare = json.loads((ROOT / 'review/comparison.json').read_text())
    assert primary['completed_records'] == 78 and primary['completed_transfers'] == 52
    assert not primary['budget_expired'] and replay['complete'] and compare['agree']
    assert compare['primary_result_sha256'] == sha(UNIT / 'result.json')
    assert compare['replay_result_sha256'] == sha(ROOT / 'review/replay/result.json')
    assert compare['comparison_source_sha256'] == sha(ROOT / 'review/compare_relations.py')
    assert replay['source_sha256'] == sha(ROOT / 'review/replay_relations.py')
    groups = []
    for w, (d, contract) in itertools.product((7, 8), ((2, 'finite'), (2, 'full_input_d2'), (3, 'finite'), (4, 'finite'))):
        rs = [r for r in primary['census'] if (r['width'], r['dimension'], r['contract']) == (w, d, contract)]
        assert len(rs) == 256
        groups.append({'width': w, 'dimension': d, 'contract': contract,
                       'zero_relation_roots': [r['rule'] for r in rs if not r['rank']],
                       'roots_with_relations': sum(r['rank'] > 0 for r in rs),
                       'relation_rank_sum': sum(r['rank'] for r in rs)})
    panel = []
    for r in primary['records']:
        for contract, s in r['contracts'].items():
            l, f, b = s['longitudinal'], s['spatial'], s['child_sibling_blocks']
            panel.append([r['width'], r['rule'], r['dimension'], contract,
                          r['events_x0'], r['full_spatial_orbits'], l['rank'], f['rank'],
                          f['ambiguous_events'], f['variables'], f['equal_pairs'], f['opposite_pairs'],
                          b['all_free'], b['all_fixed'], b['mixed'], b['sibling_nonconstant_readout_no_go_conditions']])
    transfers = []
    for t in primary['transfers']:
        for contract, rr in t['contracts'].items():
            for r in rr:
                assert r['status'] != 'invalid_address_map'
                transfers.append([t['width'], t['rule'], t['parent_dimension'], contract,
                                  r['readout'], r['status'], r['eligible_pairs'], r['surviving_pairs'],
                                  r['fixed_agree'], r['fixed_reverse'], r['shared_nonempty_agree'],
                                  r['shared_nonempty_reverse'], r['lost_pairs']])
    assert len(panel) == 104 and len(transfers) == 546
    paths = set(primary['source_hashes']) | {
        'results/commutator_completion_20260915.json', 'scripts/summarize_commutator_relations.py',
        'scripts/package_commutator_relations.py', 'review/gate1-review.md',
        'review/replay_relations.py', 'review/replay_portable.py', 'review/compare_relations.py',
        'review/comparison.json', 'review/physical-replay-review.md',
        'experiments/commutator_relations_20260915/execution-freeze.json',
        'experiments/commutator_relations_20260915/raw-archive.json',
        'experiments/commutator_relations_20260915/REPRODUCE.md',
        'experiments/commutator_relations_20260915/publication-normalization.json'}
    for p, value in primary['source_hashes'].items():
        assert sha(ROOT / p) == value
    result = {
        'source_hashes': {p: sha(ROOT / p) for p in sorted(paths)},
        'input_hashes': primary['input_hashes'], 'raw_result_sha256': compare['primary_result_sha256'],
        'prior_summary_normalization': json.loads((UNIT / 'publication-normalization.json').read_text()),
        'independent_comparison': compare, 'groups': groups,
        'panel_columns': ['width', 'rule', 'dimension', 'contract', 'longitudinal_events', 'spatial_orbits',
                          'longitudinal_rank', 'spatial_rank', 'ambiguous_spatial_events', 'variables',
                          'equal_pairs', 'opposite_pairs', 'all_free_sibling_blocks', 'all_fixed_sibling_blocks',
                          'mixed_sibling_blocks', 'child_sibling_no_go_conditions'],
        'panel_rows': panel,
        'transfer_columns': ['width', 'rule', 'parent_dimension', 'parent_contract', 'readout', 'status',
                             'eligible_pairs', 'surviving_pairs', 'fixed_agree', 'fixed_reverse',
                             'shared_nonempty_agree', 'shared_nonempty_reverse', 'lost_pairs'],
        'transfer_rows': transfers,
        'address_maps_checked': 312,
        'all_address_maps_valid': all(all(m['respects_quotient'] and m['injective'] for m in t['maps']) for t in primary['transfers']),
        'primary_seconds': primary['seconds'], 'primary_peak_rss_kib': primary['peak_rss_kib'],
        'independent_seconds': replay['seconds'], 'independent_peak_rss_kib': replay['peak_rss_kib'],
        'limits': ['D3/D4 freedom is relative to each finite source-family table.',
                   'Each width is separate; equal physical keys share completion variables across widths.',
                   'Only seven prespecified same-address child readouts are evaluated.',
                   'No Class IV discriminator, recoding invariance, recurrence or universal lift theorem is established.',
                   'The all-free sibling Boolean obstruction applies only where its child-floor conditions hold.']}
    target = ROOT / 'results/commutator_relations_20260915.json'
    target.write_text(json.dumps(result, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n')
    print(json.dumps({'bytes': target.stat().st_size, 'contracts': len(panel), 'readout_rows': len(transfers), 'source_files': len(paths)}))


if __name__ == '__main__':
    main()
