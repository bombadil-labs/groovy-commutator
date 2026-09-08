"""Summaries and figure from the exact provenance enumeration."""
from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'results/spacetime_provenance_20260908'
rows=list(csv.DictReader(Path(str(P)+'.csv').open()))
lookup={(int(r['width']),int(r['observed_steps']),int(r['future_steps']),r['mode']):r for r in rows}
summary=[];lines=['| Width | Observed steps | Distinct panels | Rule ambiguous | Multiple autonomous futures | Multiple flipped futures |','| --- | --- | --- | --- | --- | --- |']
for t in [2,6]:
 for n in [6,8,10]:
  a=lookup[n,t,4,'autonomous'];b=lookup[n,t,4,'flip_cell_0'];count=int(a['panels'])
  d=dict(width=n,observed_steps=t,future_steps=4,panels=count,
         rule_ambiguous=count-int(a['unique_rule_panels']),
         autonomous_ambiguous=int(a['multiple_future_panels']),flip_ambiguous=int(b['multiple_future_panels']),
         rule_bits=float(a['mean_rule_bits']),autonomous_bits=float(a['mean_future_bits']),flip_bits=float(b['mean_future_bits']))
  summary.append(d)
  def item(key):return f"{d[key]:,} ({100*d[key]/count:.2f}%)"
  lines.append(f'| {n} | {t} | {count:,} | {item("rule_ambiguous")} | {item("autonomous_ambiguous")} | {item("flip_ambiguous")} |')
Path(str(P)+'_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
Path(str(P)+'_table.md').write_text('\n'.join(lines)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
fig,axes=plt.subplots(1,3,figsize=(12,4.8),sharey=True,layout='constrained')
for ax,n in zip(axes,[6,8,10]):
 ts=list(range(7));rule=[];auto=[];flip=[]
 for t in ts:
  a=lookup[n,t,4,'autonomous'];b=lookup[n,t,4,'flip_cell_0'];den=int(a['panels'])
  rule.append(100*(den-int(a['unique_rule_panels']))/den)
  auto.append(100*int(a['multiple_future_panels'])/den)
  flip.append(100*int(b['multiple_future_panels'])/den)
 ax.plot(ts,rule,'--',color='#6b7280',label='More than one rule',marker='.')
 ax.plot(ts,auto,color='#146c94',label='More than one autonomous future',marker='o',ms=4)
 ax.plot(ts,flip,color='#b85b3f',label='More than one future after a flip',marker='s',ms=4)
 ax.set_title(f'{n}-cell periodic ring');ax.set_xlabel('Observed evolution steps');ax.set_xticks(ts)
 ax.set_ylim(-2,102);ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Percent of distinct observed panels')
fig.suptitle('Agreement along a path can conceal different responses\nFour-step continuations under a fixed unknown rule',fontsize=14)
handles,labels=axes[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='outside lower center',ncol=1,frameon=False)
fig.savefig(ROOT/'docs/research/assets/spacetime-provenance-20260908.svg')
fig.savefig('/workspace/scratch/4e0fdfb9ecdc/provenance-preview.png',dpi=150)
print('\n'.join(lines))
