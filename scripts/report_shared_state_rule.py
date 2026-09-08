"""Render the frozen shared-space enumeration; no additional simulation."""
from pathlib import Path
import csv,json
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'results/shared_state_rule_20260907'
rows=list(csv.DictReader(Path(str(P)+'.csv').open()))
groups=defaultdict(list)
for row in rows:groups[(row['model'],row['mode'],row['width'])].append(row)
lines=['| Model | Size | Longest cycle: default / range | Recurrent states: default / range |','| --- | --- | --- | --- |']
summary=[]
for (model,mode,width),rs in groups.items():
    fields={key:{'default':int(rs[0][key]),'min':min(int(r[key]) for r in rs),'max':max(int(r[key]) for r in rs)}
            for key in ['max_period','recurrent','fixed','image','max_transient','largest_basin','commutator_nonzero']}
    summary.append(dict(model=model,mode=mode,width=int(width),**fields))
    def cell(k):d=fields[k];return f"{d['default']} / {d['min']}–{d['max']}"
    lines.append(f'| {model}: {mode} | {width} | {cell("max_period")} | {cell("recurrent")} |')
Path(str(P)+'_table.md').write_text('\n'.join(lines)+'\n')
Path(str(P)+'_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
fig,axes=plt.subplots(1,2,figsize=(11,4.7),layout='constrained')
for mode,color,marker in [('frozen','#87909c','_'),('mutual','#146c94','o'),('derivative','#bc573c','s')]:
    rs=groups[('ring',mode,'8')]
    axes[0].scatter([int(r['encoding']) for r in rs],[int(r['max_period']) for r in rs],label=mode,color=color,marker=marker,s=32)
for mode,color,marker in [('horizontal','#146c94','o'),('vertical','#bc573c','s')]:
    rs=groups[('selector2d',mode,'4')]
    axes[1].scatter([int(r['encoding']) for r in rs],[int(r['max_period']) for r in rs],label=mode,color=color,marker=marker,s=32)
for ax,title in zip(axes,['Eight-cell coupled ring','Eight-neighbor selector on a 4×4 torus']):
    ax.set_title(title,pad=12);ax.set_xlabel('Encoding ID (0 = default)');ax.set_ylabel('Longest cycle, in steps')
    ax.set_xticks([0,7,8,15,16,23]);ax.set_ylim(bottom=0);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    ax.axvline(15.5,color='#aaaaaa',lw=1,ls=':');ax.legend(loc='upper left',frameon=False)
    ax.spines[['top','right']].set_visible(False)
axes[0].legend(loc='center right',frameon=False)
fig.suptitle('Mapping rule bits into space changes the dynamics',fontsize=15)
fig.supxlabel('All starting states enumerated. IDs 0–15: shifts/reflections; 16–23: seeded permutations.',fontsize=10)
fig.savefig(ROOT/'docs/research/assets/shared-state-rule-20260907.svg')
fig.savefig('/workspace/scratch/4e0fdfb9ecdc/shared-state-rule-preview.png',dpi=150)
