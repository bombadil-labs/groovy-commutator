#!/usr/bin/env python3
"""Plot the saved off-image traces; no new experiment or fitted parameters."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

root = Path(__file__).resolve().parents[1]
result = json.loads((root/'results/extension_freedom_20260910.json').read_text())
fig, axes = plt.subplots(1, 2, figsize=(8, 3.3), sharey=True, constrained_layout=True)
for ax, record in zip(axes, result['defect_controls']):
    values = np.array([[int(x in row['top_zero_positions']) for x in range(-8, 9)]
                       for row in record['trace']])
    ax.imshow(values, cmap=ListedColormap(['#f3f5f7', '#315c92']), vmin=0, vmax=1,
              extent=(-8.5, 8.5, 8.5, -.5), interpolation='nearest', aspect='equal')
    ax.set_title(f"Top rule {record['top_word']}", fontsize=12)
    ax.set_xlabel('Horizontal position x', fontsize=10)
    ax.set_xticks([-8, -4, 0, 4, 8]); ax.set_yticks([0, 2, 4, 6, 8])
    ax.tick_params(labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#8a949f'); spine.set_linewidth(.6)
axes[0].set_ylabel('Time t', fontsize=10)
fig.suptitle('Same encoded evolution; different response to one top-row zero', fontsize=13)
fig.supxlabel('Colored cells: V = 0 against the undamaged V = 1 background', fontsize=10)
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['svg.hashsalt'] = 'extension-freedom-20260910'
fig.savefig(root/'results/extension_freedom_20260910.svg', metadata={'Date': None})
fig.savefig(root/'results/extension_freedom_20260910_preview.png', dpi=150)
