#!/usr/bin/env python3
"""Render the saved discovery and validation results; never simulate or rescore."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'experiments/class4_independent_20260915/figures'
OUT.mkdir(parents=True, exist_ok=True)
a = json.loads((ROOT/'results/class4_independent_20260915.json').read_text())
b = json.loads((ROOT/'results/class4_composite_20260915.json').read_text())
configs = [('primary',a), ('replication',a), ('validation_384',b), ('validation_768',b)]
labels = ['Discovery\nN=256, burn=256', 'Discovery\nN=512, burn=512',
          'Fresh validation\nN=384, burn=1536', 'Fresh validation\nN=768, burn=3072']
series = {}
for rule in [54,110,9,73]:
    series[rule] = [next(r for r in data['per_rule'] if r['rule']==rule)['configurations'][name]
                    for name,data in configs]
plt.rcParams.update({'font.size':11, 'svg.hashsalt':'class4-independent-20260915',
                     'axes.spines.top':False, 'axes.spines.right':False})
fig, (ax, bx) = plt.subplots(1,2,figsize=(13.6,5.2), gridspec_kw={'width_ratios':[1.22,1]})
x=np.arange(4)
colors={54:'#245b91',110:'#008574',9:'#ba6333',73:'#96549c'}
for rule, records in series.items():
    values=[v['retention']['7']['score']*v['prediction']['8']['score'] for v in records]
    ax.plot(x,values,marker='o',lw=2.2,color=colors[rule],label=f'Rule {rule}')
ax.axvspan(1.5,3.5,color='#e9eef2',alpha=.75,zorder=-1)
ax.set(xlim=(-.15,3.15),ylim=(0,.108),xticks=x,xticklabels=labels,ylabel='Composite score C = A × B',
       title='Clean separation failed fresh validation')
ax.legend(ncol=2,frameon=False,loc='upper right')
ax.grid(axis='y',alpha=.18)
for field,label,color in [('predictive_gain','History predictive gain M','#008574'),
                         ('innovation','Remaining local uncertainty U','#ba6333')]:
    values=[sum(d[field] for d in v['prediction']['8']['directions'])/2 for v in series[110]]
    bx.plot(x,values,marker='o',lw=2.2,color=color,label=label)
bx.axvspan(1.5,3.5,color='#e9eef2',alpha=.75,zorder=-1)
bx.set(xlim=(-.15,3.15),ylim=(0,1),xticks=x,xticklabels=labels,ylabel='Bits per observed next cell',
       title='110 gained predictability as its score fell')
bx.legend(frameon=False,loc='center left')
bx.grid(axis='y',alpha=.18)
fig.suptitle('Independent ECA discriminator attempt: preserve the failure',fontsize=16,y=.99)
fig.text(.5,.017,'All 88 symmetry families evaluated; left panel highlights the two primary positives and both fresh false positives.\n'
         'Connecting lines compare configurations. Ring size, burn-in, seeds and sampling length changed together.',
         ha='center',fontsize=9.5,color='#48505a')
fig.tight_layout(rect=(0,.095,1,.94))
for ext in ['svg','png']:
    fig.savefig(OUT/f'class4-independent-validation.{ext}',dpi=165,metadata={'Date':None} if ext=='svg' else None)
plt.close(fig)
print(OUT/'class4-independent-validation.svg')
