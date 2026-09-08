"""Report the saved census and replay one physical process in three readouts."""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from experiment_block_compatibility import encode, step2, apply_rule

ROOT = Path(__file__).resolve().parents[1]
STEM = ROOT / 'results/block_compatibility_20260908'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', type=Path)
    args = parser.parse_args()
    records = list(csv.DictReader(Path(str(STEM) + '_successes.csv').open()))
    families = [
        ('Columns, stationary', lambda r: int(r['w']) == 1 and int(r['u']) == int(r['v']) == 0),
        ('Columns, fixed frames allowed', lambda r: int(r['w']) == 1),
        ('All rectangles, stationary', lambda r: int(r['u']) == int(r['v']) == 0),
        ('All rectangles, fixed frames allowed', lambda r: True),
    ]
    table = '| Encoding and observation | Distinct ECA targets |\n| --- | ---: |\n'
    for label, predicate in families:
        table += f'| {label} | {len({int(r["rule"]) for r in records if predicate(r)})} |\n'
    Path(str(STEM) + '_table.md').write_text(table)

    seed = np.zeros(41, dtype=np.uint8)
    seed[20] = 1
    fine = [encode(seed, 3, 2, 42, 11)]
    for _ in range(32):
        fine.append(step2(fine[-1]))
    panels = []
    checks = 0
    for rule, cadence, drift in [(60, 1, -1), (102, 1, 1), (90, 2, 0)]:
        expected = seed.copy()
        rows = []
        for tick in range(17):
            observed = np.roll(fine[cadence * tick], -drift * tick, axis=-1)
            decoded = observed[0, ::2]
            assert np.array_equal(observed, encode(decoded, 3, 2, 42, 11))
            assert np.array_equal(decoded, expected)
            rows.append(decoded.copy())
            expected = apply_rule(expected, rule)
            checks += 1
        panels.append(np.array(rows))

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(1, 3, figsize=(12, 5.0))
    fig.suptitle('One 2D process, three exact 1D readouts', fontsize=17, y=.96)
    titles = ['Rule 60: left XOR center', 'Rule 102: center XOR right', 'Rule 90: left XOR right']
    captions = ['Read every tick\nFrame moves left 1 physical cell',
                'Read every tick\nFrame moves right 1 physical cell',
                'Read every 2 ticks\nStationary frame']
    for ax, data, title, caption in zip(axes, panels, titles, captions):
        ax.imshow(data, cmap=ListedColormap(['#f0f4f7', '#176b86']),
                  interpolation='nearest', vmin=0, vmax=1, aspect='equal')
        ax.set_title(title, fontsize=11, pad=12)
        ax.set_xticks([4, 12, 20, 28, 36], ['−16', '−8', '0', '8', '16'])
        ax.set_yticks([0, 4, 8, 12, 16])
        ax.set_xlabel('Logical position (initial seed = 0)')
        ax.text(.5, -.55, caption, ha='center', transform=ax.transAxes, fontsize=9)
    axes[0].set_ylabel('Observed update number')
    fig.text(.5, .085, 'Identical initial encoding and physical trajectory in every panel. Only frame and sampling cadence change.',
             ha='center', fontsize=10)
    fig.text(.5, .035, '41 logical cells on a ring; one initial 1. Each logical bit occupies a 3-row × 2-column block in a 2D field.',
             ha='center', fontsize=9)
    fig.subplots_adjust(left=.06, right=.98, bottom=.25, top=.86, wspace=.22)
    fig.savefig(ROOT / 'docs/research/assets/block-compatibility-20260908.svg', metadata={'Date': None})
    if args.preview:
        fig.savefig(args.preview, dpi=150)
    plt.close(fig)
    Path(str(STEM) + '_replay.json').write_text(json.dumps({
        'checked_readouts': checks, 'logical_width': 41, 'fine_ticks': 32,
        'm': 3, 'w': 2, 'a': 42, 'b': 11,
        'readouts': [{'rule': r, 'k': k, 'u': u, 'v': 0} for r, k, u in [(60,1,-1),(102,1,1),(90,2,0)]],
        'scope': 'Illustrative replay after the census, with full block and independent ECA comparison at every plotted readout.'
    }, indent=2) + '\n')
    print(table)
    print(f'{checks} plotted readouts verified against the same physical trajectory.')


if __name__ == '__main__':
    main()
