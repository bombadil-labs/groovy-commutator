#!/usr/bin/env python3
"""Display all frozen tasks; this plot performs no further selection."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'experiments/factor_balanced_interactions_20260915/confirmation-result.json').read_text())
pairs=sorted({tuple(t['rules']) for t in r['tasks']})
obs=[t['observation'] for t in r['summary']]
lookup={(tuple(t['rules']),t['observation']):min(t['models'][m]['mae']-t['models']['M2']['mae'] for m in ('M0','M1')) for t in r['tasks']}
x=np.array([[lookup[p,o] for o in obs] for p in pairs]);limit=max(abs(x.min()),abs(x.max()))
fig,ax=plt.subplots(figsize=(10,11),layout='constrained')
im=ax.imshow(x,cmap='RdBu',norm=TwoSlopeNorm(0,-limit,limit),aspect='auto')
ax.set_yticks(range(len(pairs)),[f'{a} / {b}' for a,b in pairs]);ax.set_xticks(range(9),['1','2','4','8','16','32','Basin','Cycle\nlength','Transient\ndepth'])
ax.set_xlabel('Future-state horizon (steps), then eventual graph observations')
ax.set_ylabel('Rule pair')
ax.set_title('Arithmetic interaction gains vary by rule pair and observation\nBlue: beats both baselines; red: loses to at least one',pad=14)
for i,pair in enumerate(pairs):
 for j,o in enumerate(obs):
  if lookup[pair,o]>1e-12:ax.text(j,i,'+',ha='center',va='center',fontsize=10,color='black')
fig.colorbar(im,ax=ax,label='Smaller of the two MAE reductions (positive = strict joint win)',shrink=.75)
for ext in ('svg','png'):fig.savefig(ROOT/f'results/factor_balanced_interactions_20260915.{ext}',dpi=150)
