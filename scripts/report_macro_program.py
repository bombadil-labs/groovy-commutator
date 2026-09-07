#!/usr/bin/env python3
"""Build readable summaries of finite and all-width macro cost experiments."""
import csv
import json
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

ROOT=Path(__file__).resolve().parents[1]
PREFIX=ROOT/'results/macro_program_20260907'


def main():
    summary={}
    for name in ['revisable_primitives','macro_local_equivalence']:
        with (ROOT/f'results/{name}_20260907.csv').open() as f:rows=list(csv.DictReader(f))
        for r in rows:
            domain=r.get('n','all-widths')
            key=(domain,)+tuple(int(r[k]) for k in ['dispatch','trace','K','useful_inheritance'])+(r['shift'],)
            if key not in summary:
                summary[key]=dict(zip(('domain','dispatch','trace','K','useful_inheritance','shift'),key))
            out=summary[key]
            for k in ['cases','same_task_map','sum_uncompiled','sum_frozen','sum_replace','sum_revisable',
                      'revision_win_replace','revision_tie_replace','revision_loss_replace']:
                out[k]=out.get(k,0)+int(r[k])
    records=list(summary.values())
    Path(str(PREFIX)+'_summary.json').write_text(json.dumps(records,indent=2)+'\n')
    table=['# Macro revision at the primary prices','',
           'Dispatch cost 1; prepaid trace reserve 4; four changed-task jobs after eight old-task jobs.',
           'Only inherited compilations that paid for themselves before the change are included here.',
           'Counts are configurations, not independent statistical replicates.','',
           '| Domain | Literal task change | Cases | Revision cheaper than replacement | Mean saving over replacement |',
           '| --- | --- | ---: | ---: | ---: |']
    primary=[]
    for domain in ['6','9','11','all-widths']:
        for shift in ['unchanged','one_edit','far']:
            r=summary[(domain,1,4,4,1,shift)];primary.append(r)
            saving=(r['sum_replace']-r['sum_revisable'])/r['cases']
            table.append(f"| {domain} | {shift} | {r['cases']:,} | {r['revision_win_replace']:,} | {saving:+.3f} |")
    Path(str(PREFIX)+'_table.md').write_text('\n'.join(table)+'\n')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'macro-program-20260907'})
    fig,axes=plt.subplots(1,4,figsize=(12,4.4),sharey=True)
    domains=['6','9','11','all-widths'];shifts=['unchanged','one_edit','far']
    for ax,domain in zip(axes,domains):
        data=np.zeros((3,4))
        for i,shift in enumerate(shifts):
            for j,trace in enumerate([0,2,4,8]):
                r=summary[(domain,1,trace,4,1,shift)]
                data[i,j]=(r['sum_replace']-r['sum_revisable'])/r['cases']
        im=ax.imshow(data,cmap='RdBu',norm=TwoSlopeNorm(vmin=-8,vcenter=0,vmax=5),aspect='auto')
        for (i,j),value in np.ndenumerate(data):
            ax.text(j,i,f'{value:+.1f}',ha='center',va='center',fontsize=10,color='white' if value<-5 or value>3.4 else '#202020')
        ax.set(xticks=range(4),xticklabels=[0,2,4,8],yticks=range(3),yticklabels=['Unchanged','One edit','Two+ edits'],xlabel='Prepaid trace reserve')
        ax.set_title('All widths' if domain=='all-widths' else f'{domain}-cell ring')
        ax.tick_params(length=0)
    fig.suptitle('When does retaining a construction record pay?',fontsize=15,y=.98)
    fig.text(.5,.875,'Mean cost saving over replacement · positive favors revision · dispatch cost 1, four new-task jobs',ha='center',fontsize=10)
    fig.subplots_adjust(left=.10,right=.95,top=.79,bottom=.30,wspace=.15)
    cax=fig.add_axes([.30,.12,.48,.035]);fig.colorbar(im,cax=cax,orientation='horizontal',label='Resource units saved per complete old/new task sequence')
    out=ROOT/'docs/research/assets/macro-costs-20260907.svg';fig.savefig(out,metadata={'Date':None},facecolor='white')
    plt.close(fig)
    with (ROOT/'results/macro_local_equivalence_20260907_finite_comparison.csv').open() as f:comparisons=list(csv.DictReader(f))
    fig,ax=plt.subplots(figsize=(10.5,4.3))
    pairs=[(0,51),(4,30),(30,110),(51,170),(54,110),(90,150),(110,184),(184,250)]
    for j,(n,color) in enumerate([(6,'#bb7236'),(9,'#447aa1'),(11,'#43785c')]):
        values=[]
        for a,b in pairs:
            r=next(r for r in comparisons if [int(r[k]) for k in ['n','A','B','dispatch']]==[n,a,b,1])
            values.append(100*int(r['finite_cost_lower'])/int(r['cost_entries']))
        ax.bar(np.arange(8)+(j-1)*.23,values,width=.23,label=f'{n} cells',color=color)
    ax.set(xticks=range(8),xticklabels=[f'{a}/{b}' for a,b in pairs],xlabel='Rule pair',ylabel='Library–target entries with lower cost (%)',ylim=(0,100))
    ax.set_title('Small rings can make a program look cheaper',fontsize=15,pad=18)
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    ax.legend(frameon=False,ncol=3)
    fig.subplots_adjust(left=.10,right=.98,bottom=.21,top=.82)
    fig.text(.5,.025,'Compared with exact local equivalence; 272 library–target entries per pair at dispatch cost 1.',ha='center',fontsize=9)
    fig.savefig(ROOT/'docs/research/assets/macro-finite-size-20260907.svg',metadata={'Date':None},facecolor='white')
    print(json.dumps({'summary_rows':len(records),'primary_rows':len(primary)}))

if __name__=='__main__':main()
