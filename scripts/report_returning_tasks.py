#!/usr/bin/env python3
"""Summarize returning-task costs without treating shared cases as samples."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
PREFIX=ROOT/'results/returning_tasks_20260907'


def main():
    with PREFIX.with_suffix('.csv').open() as f:rows=list(csv.DictReader(f))
    summary={}
    for r in rows:
        key=tuple(int(r[k]) for k in ['dispatch','trace','K','cycles','useful_inheritance'])+(r['shift'],)
        if key not in summary:summary[key]=dict(zip(['dispatch','trace','K','cycles','useful_inheritance','shift'],key))
        out=summary[key]
        for k,value in r.items():
            if k in ['A','B','dispatch','trace','K','cycles','useful_inheritance','shift']:continue
            if k.endswith('_max'):out[k]=max(out.get(k,0),int(value))
            else:out[k]=out.get(k,0)+int(value)
    Path(str(PREFIX)+'_summary.json').write_text(json.dumps(list(summary.values()),indent=2)+'\n')
    table=['# Returning tasks at the primary prices','',
           'Dispatch=1, prepaid trace=4, four jobs per block, useful inherited compilation.',
           'Costs compare matched hindsight-oracle policies; regret compares reactive revision with its oracle.','',
           '| Return cycles | Task change | Cases | Revision cheaper than replacement | Mean saving | Reactive revision regret cases |',
           '| --- | --- | ---: | ---: | ---: | ---: |']
    for cycles in [1,2,4]:
        for shift in ['unchanged','one_edit','far']:
            r=summary[(1,4,4,cycles,1,shift)]
            gain=(r['sum_replacement_oracle']-r['sum_revision_oracle'])/r['cases']
            table.append(f"| {cycles} | {shift} | {r['cases']} | {r['revision_oracle_win_replacement']} | {gain:+.3f} | {r['revision_stay_regret_cases']} |")
    Path(str(PREFIX)+'_table.md').write_text('\n'.join(table)+'\n')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'returning-tasks-20260907'})
    fig,axes=plt.subplots(1,2,figsize=(11,4.3))
    for shift,label,color in [('one_edit','One-letter change','#36725a'),('far','Two or more letters','#396a92'),('unchanged','Unchanged word','#9a6743')]:
        selected=[summary[(1,4,4,c,1,shift)] for c in [1,2,4]]
        axes[0].plot([1,2,4],[(r['sum_replacement_oracle']-r['sum_revision_oracle'])/r['cases'] for r in selected],marker='o',label=label,color=color)
    axes[0].axhline(0,color='#555555',linewidth=.8)
    axes[0].set(title='Repeated changes can repay the trace',xlabel='Return cycles',ylabel='Mean saving over replacement',xticks=[1,2,4])
    axes[0].legend(frameon=False,fontsize=9)
    witness=next(w for w in json.loads(Path(str(PREFIX)+'_witnesses.json').read_text()) if w['category']=='reactive_revision_regret')
    for method,label,color in [('frozen','Keep inherited macro','#396a92'),('revision_reactive_stay','Cheapest current revision','#b26b2f')]:
        vals=[b['block_cost'] for b in witness['blocks'][method]]
        axes[1].plot([0,1,2],[0,vals[0],sum(vals)],marker='o',label=label,color=color)
    axes[1].set(title='A local saving can become a later cost',xlabel='Task block',ylabel='Cumulative cost after the shared prefix',xticks=[0,1,2],xticklabels=['Start','Changed\ntask','Old task\nreturns'])
    axes[1].legend(frameon=False,fontsize=9)
    for ax in axes:
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2)
    fig.subplots_adjust(left=.075,right=.98,top=.83,bottom=.24,wspace=.30)
    fig.text(.5,.04,'Left: primary prices, exact all-width programs. Right: the selected free-trace, one-job counterexample.',ha='center',fontsize=9)
    fig.savefig(ROOT/'docs/research/assets/returning-tasks-20260907.svg',metadata={'Date':None},facecolor='white')
    print(json.dumps({'summary_rows':len(summary),'primary_table_rows':9}))

if __name__=='__main__':main()
