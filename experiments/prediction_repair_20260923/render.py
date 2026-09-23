#!/usr/bin/env python3
"""Render the preserved two-state obstruction; no new search or simulation."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('result', type=Path)
ap.add_argument('--svg', type=Path, required=True)
ap.add_argument('--preview', type=Path)
args = ap.parse_args()
data = json.loads(args.result.read_text())
witness = data['complete_table']['prediction_without_repair']['witness']
states = witness['states']
assert len(states) == 2
pred = data['searches']['predict']['encoder']
repair = data['searches']['repair']['encoder']
actions = [(mask & -mask).bit_length()-1 for mask in witness['winning_masks']]
assert all(mask.bit_count() == 1 for mask in witness['winning_masks'])
assert states[0] ^ (1 << (actions[0]-1)) == states[1] ^ (1 << (actions[1]-1))

plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none'})
fig, ax = plt.subplots(figsize=(12, 5.4))
fig.patch.set_facecolor('#f6f5f1')
ax.set(xlim=(0, 12), ylim=(0, 5.4))
ax.axis('off')
ink, muted, orange = '#18333d', '#51666b', '#cf5c26'
ax.text(.15, 5.0, 'The same forecast can require different repairs', fontsize=20, weight='bold', color=ink)
ax.text(.15, 4.59, 'Rule 54  /  12 cells  /  one unknown damaged bit  /  one repair flip', fontsize=11, color=muted)
ax.text(.72, 4.03, 'SOURCE CELLS', fontsize=10, weight='bold', color=muted)
ax.text(7.25, 4.03, 'PREDICTIVE VIEW', fontsize=10, weight='bold', color=muted)
ax.text(9.78, 4.03, 'REPAIR VIEW', fontsize=10, weight='bold', color=muted)
for i in range(12):
    ax.text(.72+.49*i+.205, 3.72, str(i), fontsize=9, ha='center', color=muted)

for row, (s, action) in enumerate(zip(states, actions)):
    y = 3.02-row*1.0
    ax.text(.18, y+.21, 'AB'[row], fontsize=16, weight='bold', color=ink, va='center')
    for i in range(12):
        bit = (s >> i) & 1
        x = .72+.49*i
        ax.add_patch(Rectangle((x,y),.41,.43, facecolor=ink if bit else '#ffffff',
                              edgecolor=orange if i == action-1 else '#bac7c7',
                              linewidth=3 if i == action-1 else 1))
        ax.text(x+.205,y+.215,str(bit),ha='center',va='center',fontsize=11,color='white' if bit else ink)
    for x0, encoder in ((7.25,pred),(9.78,repair)):
        values = [encoder[(s >> (3*j)) & 7] for j in range(4)]
        for j, label in enumerate(values):
            x = x0+.47*j
            ax.add_patch(Rectangle((x,y),.4,.43,facecolor='#dceae5',edgecolor='#a6bdb3'))
            ax.text(x+.2,y+.215,str(label),ha='center',va='center',fontsize=12,color=ink)
    ax.text(.72,y-.27,f'Only successful response: flip cell {action-1}',fontsize=11,color=orange,weight='bold')

ax.text(.72,1.15,'Both passive forecasts: remain outside the stripe family.',fontsize=12,color=ink)
ax.text(.72,.72,'Prediction needs 2 local labels. Reliable repair needs 4.',fontsize=12,color=ink,weight='bold')
ax.text(.72,.27,'Exact on the declared 52-state damage family. Repair is supplied by an external controller.',fontsize=10,color=muted)
fig.subplots_adjust(left=.02,right=.99,bottom=.02,top=.99)
with args.svg.open('x') as f:
    fig.savefig(f,format='svg',facecolor=fig.get_facecolor(),metadata={'Date':None})
if args.preview:
    with args.preview.open('xb') as f:
        fig.savefig(f,format='png',dpi=130,facecolor=fig.get_facecolor())
