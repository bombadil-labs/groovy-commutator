#!/usr/bin/env python3
"""Summarize saved outputs and draw explanatory figures; no CA evaluation."""
from pathlib import Path
import json
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from rule_ring_selectors import atomic_json, sha256

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/rule_ring_structure_20260915'


def main():
    discovery = json.loads((UNIT/'discovery-result.json').read_text())
    confirmation = json.loads((UNIT/'confirmation-result.json').read_text())
    evidence = json.loads((UNIT/'confirmation-evidence.json').read_text())
    comparisons = confirmation['selected_confirmation']
    case_info = discovery['case_info'] + confirmation['case_info']
    compact = {}
    for row in evidence['rows']:
        for ring, relation in zip(row['rings'], row['relation_values']):
            key = (row['observation'], *row['rules'], ring)
            if key in compact:
                assert compact[key] == relation
            compact[key] = relation
    relations = [{'observation': obs, 'rules': [a,b], 'ring': ring, **value}
                 for (obs,a,b,ring),value in sorted(compact.items())]
    atomic_json(UNIT/'compact-relations.json', relations)

    # These two panels illustrate retained data after evaluation; they were not
    # additional scored selectors or a second classifier search.
    pairs = sorted({tuple(row['rules']) for row in evidence['rows']}, key=lambda p: tuple(map(int,p)))
    rings = list(range(4,17))
    fig, axes = plt.subplots(1,2,figsize=(12,10),sharey=True,layout='constrained')
    for ax, observation, title in zip(axes, ['future_32','basin'], ['Same state after 32 steps','Same eventual attractor basin']):
        matrix = np.array([[compact[observation,*pair,n]['vi_per_bit'] for n in rings] for pair in pairs])
        picture = ax.imshow(matrix, vmin=0,vmax=1,cmap='viridis',aspect='auto')
        ax.set_xticks(range(13),rings)
        ax.set_yticks(range(28),[f'{a} / {b}' for a,b in pairs],fontsize=8)
        ax.set_title(title,fontsize=12)
        ax.set_xlabel('Ring size')
        ax.axvline(8.5,color='white',linewidth=1.5,linestyle='--')
    axes[0].set_ylabel('Rule pair')
    fig.colorbar(picture,ax=axes,label='Partition distance / source bit (VI/n)',shrink=.65)
    fig.suptitle('Whole-state relations depend on the rule pair and the ring\nDashed line separates discovery from held-out ring sizes',fontsize=14)
    for extension in ('svg','png'):
        fig.savefig(ROOT/f'results/rule_ring_structure_20260915.{extension}',dpi=160)
    plt.close(fig)

    source_paths = [
        'scripts/rule_ring_structure.py', 'scripts/rule_ring_selectors.py',
        'scripts/summarize_rule_ring_structure.py', 'src/groovy/ca.py',
        'docs/research/protocols/rule-ring-structure-20260915.md',
    ]
    for name in ['implementation-freeze.json','confirmation-seal.json','discovery-selection.json',
                 'discovery-result.json','confirmation-result.json','discovery-execution.json',
                 'confirmation-execution.json','REPRODUCE.md','raw-manifest.json','raw-archive.json']:
        if (UNIT/name).exists():
            source_paths.append(str((UNIT/name).relative_to(ROOT)))
    for path in sorted((ROOT/'review/rule_ring_structure').glob('*')):
        if path.is_file() and path.suffix in ('.py','.md','.json'):
            source_paths.append(str(path.relative_to(ROOT)))
    output = {'status': 'complete', 'evidence': 'exploratory',
              'rules': discovery['rules'], 'widths': rings, 'observations': discovery['observations'],
              'source_state_cases': sum(r['states'] for r in case_info),
              'rule_ring_cases': len(case_info), 'partitions': len(case_info)*9,
              'unique_within_ring_rule_relations': len(relations),
              'cross_ring_comparisons': evidence['comparison_count'],
              'associations_per_stage': len(discovery['associations']),
              'selected_confirmation': comparisons,
              'sign_counts': {'same':sum(r['sign_agreement'] is True for r in comparisons),
                              'opposite':sum(r['sign_agreement'] is False for r in comparisons),
                              'undefined_or_zero':sum(r['sign_agreement'] is None for r in comparisons)},
              'case_info': case_info,
              'discovery_associations': discovery['associations'],
              'confirmation_associations': confirmation['associations'],
              'limits': ['Six dependent held-out ring pairs.', 'Overlapping selectors are not independent tests.',
                         'No adjustment eliminates ring-size confounding.', 'Two core rules do not form a class census.',
                         'VI is a scalar projection of retained partitions.', 'No lifted completion experiment was run.'],
              'source_hashes': {p:sha256(ROOT/p) for p in source_paths}}
    atomic_json(ROOT/'results/rule_ring_structure_20260915.json',output)
    print(json.dumps({k:output[k] for k in ['rule_ring_cases','partitions','unique_within_ring_rule_relations',
                                         'cross_ring_comparisons','sign_counts']}))


if __name__ == '__main__':
    if sys.argv[1:] == ['--refresh-hashes-only']:
        path = ROOT/'results/rule_ring_structure_20260915.json'
        value = json.loads(path.read_text())
        names = set(value['source_hashes']) | {
            'scripts/package_rule_ring_structure.py',
            'experiments/rule_ring_structure_20260915/raw-manifest.json',
            'experiments/rule_ring_structure_20260915/raw-archive.json',
        }
        value['source_hashes'] = {name:sha256(ROOT/name) for name in sorted(names)}
        atomic_json(path,value)
    else:
        main()
