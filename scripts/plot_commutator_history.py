#!/usr/bin/env python3
"""Render saved commutator fields and frozen held-out prediction gains."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT/'experiments/commutator_history_20260915'


def main():
    result = json.loads((UNIT/'result.json').read_text())
    families = {f['id']: f for f in result['families']}
    plt.rcParams.update({'font.size': 10, 'svg.hashsalt': 'commutator-history-20260915'})
    fig = plt.figure(figsize=(12, 8.5), layout='constrained')
    grid = fig.add_gridspec(2, 3, height_ratios=(1, 1.25))
    with np.load(UNIT/'histories-and-counts.npz') as raw:
        for j, (key, title, seed, width) in enumerate([
            ('eca54', 'Rule 54', 6041512, 2039),
            ('eca110', 'Rule 110', 6041512, 2039),
            ('wide2_g1', 'Radius-two challenge (unclassified)', 6041542, 4121),
        ]):
            ax = fig.add_subplot(grid[0, j])
            g = np.unpackbits(raw[f'{key}_G_s{seed}'], axis=1)[:, :width]
            mid = width//2
            ax.imshow(g[:160, mid-96:mid+96], cmap='binary', interpolation='nearest',
                      aspect='auto', extent=(-96, 96, 160, 0), vmin=0, vmax=1)
            ax.set_title(title, fontsize=11)
            ax.set_xlabel('Original spatial coordinate (relative)')
            if j == 0:
                ax.set_ylabel('Time after retained start')
    ax = fig.add_subplot(grid[1, :])
    names = ['eca30', 'eca54', 'eca73', 'eca110', 'eca126', 'wide2_g1']
    labels = ['30', '54', '73', '110', '126', 'Radius 2\n(unclassified)']
    colors = ['#929aa2', '#287ca6', '#929aa2', '#287ca6', '#929aa2', '#b96739']
    x = np.arange(len(names))
    for i, name in enumerate(names):
        real = np.array([t['gain_bits'] for t in families[name]['tests']])
        null = np.array([t['gain_bits'] for t in families[name+'_shuffle']['tests']])
        ax.bar(i-.17, real.mean(), .32, color=colors[i], label='Ordered history' if i == 0 else None)
        ax.bar(i+.17, null.mean(), .32, color='#d8dce0', edgecolor='#666',
               label='Permuted time slices' if i == 0 else None)
        ax.scatter(np.full(len(real), i-.17), real, s=28, color='#172532', zorder=3)
        ax.text(i-.17, real.max()+.015, f'{real.mean():.3f}', ha='center', fontsize=10)
    ax.axhline(.01, color='#8d5b3a', linestyle='--', linewidth=1,
               label='Frozen memory threshold (0.01 bits)')
    ax.axhline(0, color='#888', linewidth=.7)
    ax.set_xticks(x, labels)
    ax.set_ylabel('Held-out log-loss reduction (bits per target)')
    ax.set_ylim(-.035, .61)
    ax.grid(axis='y', alpha=.2)
    ax.set_axisbelow(True)
    ax.legend(loc='upper left', frameon=False, fontsize=9)
    ax.set_title('Older G values help predict future G, but do not remove the radius-two challenge', pad=10)
    fig.suptitle('Following the commutator through its native trajectory', fontsize=16)
    fig.supxlabel('Top: actual G fields, fixed coordinates. Bottom: three held-out ECA seeds; one wider-radius seed.\n'
                  'Dots are observed runs. The shuffled control preserves spatial frames and may retain site heterogeneity.', fontsize=9)
    fig.savefig(ROOT/'results/commutator_history_20260915.svg', metadata={'Date': None})
    fig.savefig(ROOT.parent/'commutator-history-20260915.png', dpi=170)
    plt.close(fig)


if __name__ == '__main__':
    main()
