#!/usr/bin/env python3
"""Render the independently audited Rule232 full-field ambiguity witness."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/'results/transverse_witness_extension_20260910.json').read_text())
case = next(c for c in data['certificates'] if c['rule'] == 232)
fig, axes = plt.subplots(2, 3, figsize=(9, 6.1))
fig.patch.set_facecolor('#f8f6ef')
cmap = ListedColormap(['#ffffff', '#244b63'])
for row in range(2):
    words = [case['source_words'][row], case['observed_periodic_word'], case['next_transverse_words'][row]]
    labels = [('Source A', 'Source B: first column flipped')[row],
              ('Current differences T(A)', 'Current differences T(B)')[row],
              ('Next differences T(G(A))', 'Next differences T(G(B))')[row]]
    for col, (word, label) in enumerate(zip(words, labels)):
        ax = axes[row, col]
        bits = [[(word >> (x+3*y)) & 1 for x in range(3)] for y in range(4)]
        ax.imshow(bits, cmap=cmap, vmin=0, vmax=1, origin='lower', interpolation='none')
        ax.set_title(label, fontsize=10, pad=9, color='#193c50')
        ax.set_xticks(range(3), labels=range(3), fontsize=8)
        ax.set_yticks(range(4), labels=range(4), fontsize=8)
        ax.set_xticks([x-.5 for x in range(4)], minor=True)
        ax.set_yticks([y-.5 for y in range(5)], minor=True)
        ax.grid(which='minor', color='#b9c4c9', linewidth=.7)
        ax.tick_params(which='both', length=0)
        for spine in ax.spines.values():
            spine.set_color('#b9c4c9')
        for y in range(4):
            for x in range(3):
                ax.text(x, y, str(bits[y][x]), ha='center', va='center', fontsize=11,
                        color='white' if bits[y][x] else '#647782')
        if col == 2:
            ax.add_patch(Rectangle((.5, .5), 1, 1, fill=False, linewidth=2.8, edgecolor='#da7b35'))
fig.suptitle('Same observed state, different observed future', x=.5, y=.98, fontsize=16, color='#193c50')
fig.text(.5, .92, 'Rule 232 along x, then y. Each 3 × 4 tile repeats in both directions.',
         ha='center', fontsize=10, color='#48616f')
fig.text(.5, .035, 'The column flip is invisible to T. The orange cells disagree after one macro update.',
         ha='center', fontsize=10, color='#48616f')
fig.subplots_adjust(top=.83, bottom=.10, hspace=.35, wspace=.38)
fig.savefig(ROOT/'results/transverse_difference_witness_20260910.svg', facecolor=fig.get_facecolor())
fig.savefig(ROOT/'results/transverse_difference_witness_20260910_preview.png', dpi=140, facecolor=fig.get_facecolor())
