"""Rebuild the composition figure and verify compact first-tick formulas."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,BoundaryNorm
ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/coupled_strips_20260908'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',type=Path);args=parser.parse_args()
    data=json.loads(Path(str(STEM)+'_local.json').read_text())
    x=np.array(data['inputs'],dtype=np.uint8);aL,a,aR,bL,b,bR=x.T
    ha=aL^a;ga=a^aR;hb=bL^b;gb=b^bR
    for r in data['gaps']:
        rows=r['first_tick_rows'];g=r['gap']
        expected=np.tile(np.array([1,0],dtype=np.uint8),(64,len(rows),1))
        expected[:,rows.index(0)]=np.stack([1^ha,0*a],axis=1)
        expected[:,rows.index(1)]=np.stack([1+0*a,ga],axis=1)
        expected[:,rows.index(g+2)]=np.stack([1^hb,0*b],axis=1)
        expected[:,rows.index(g+3)]=np.stack([1+0*b,gb],axis=1)
        if g==0:
            expected[:,rows.index(1)]=np.stack([1^(a*b),(1^b)*ga],axis=1)
            expected[:,rows.index(2)]=np.stack([1^((1^a)*hb),a*b],axis=1)
        assert np.array_equal(expected,r['first_tick_center'])
    interaction=np.stack([np.stack([a*b,b*ga],axis=1),np.stack([a*hb,a*b],axis=1)],axis=1)
    summary=dict(first_tick_formula_cases=320,adjacent_first_tick_interaction_inputs=int(interaction.any(axis=(1,2)).sum()),
                 all_ones_first_tick_interaction=interaction[63].tolist(),
                 all_ones_second_tick_residual=data['gaps'][0]['residual'][63],
                 scope='Compact formulas derived from and checked against the completed local census.')
    Path(str(STEM)+'_formula_checks.json').write_text(json.dumps(summary,indent=2)+'\n')
    table='| Background rows between strips | Valid local inputs | Independent Rule-90 inputs | Maximum output degree |\n| ---: | ---: | ---: | ---: |\n'
    for r in data['gaps']:
        table+=f'| {r["gap"]} | {r["valid_inputs"]}/64 | {r["independent_inputs"]}/64 | {max(p["degree"] for p in r["output_polynomials"])} |\n'
    Path(str(STEM)+'_table.md').write_text(table)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    fig,(left,right)=plt.subplots(1,2,figsize=(11,5.5),gridspec_kw={'width_ratios':[1.15,1]})
    fig.suptitle('One background row separates exact logical dynamics',fontsize=16,y=.96)
    residual=np.array(data['gaps'][0]['residual']).sum(axis=(1,2)).reshape(8,8)
    colors=['#e1eee9','#f6dfba','#e9b978','#d78b49','#ab512f']
    im=left.imshow(residual,cmap=ListedColormap(colors),norm=BoundaryNorm(np.arange(-.5,5.5),5),origin='lower',interpolation='nearest')
    for bi in range(8):
        for ai in range(8):left.text(ai,bi,str(residual[bi,ai]),ha='center',va='center',fontsize=9,color='white' if residual[bi,ai]>=3 else '#243643')
    labels=[''.join(str((q>>j)&1) for j in range(3)) for q in range(8)]
    left.set_xticks(range(8),labels,fontsize=8);left.set_yticks(range(8),labels,fontsize=8)
    left.set_xlabel('Upper input (left, center, right)');left.set_ylabel('Lower input (left, center, right)')
    left.set_title('Adjacent strips: mismatched physical cells at tick 2',fontsize=10,pad=12)
    valid=[r['valid_inputs'] for r in data['gaps']]
    bars=right.bar(range(5),valid,color=['#ab512f']+['#176b86']*4,width=.65)
    right.bar_label(bars,labels=[f'{n}/64' for n in valid],padding=4,fontsize=10)
    right.set_xticks(range(5));right.set_ylim(0,74);right.set_xlabel('Background rows between strips')
    right.set_ylabel('Local inputs preserving the whole code')
    right.set_title('All valid outputs equal independent Rule 90',fontsize=10,pad=12)
    right.spines[['top','right']].set_visible(False);right.grid(axis='y',alpha=.15);right.set_axisbelow(True)
    fig.text(.5,.065,'Adjacency creates nonlinear cross-influence in the two touching rows; 47 of 64 local inputs leave the declared code.',ha='center',fontsize=10)
    fig.text(.5,.025,'These are exhaustive local truth tables, not probabilities of whole trajectories. The 2D update law is unchanged.',ha='center',fontsize=9)
    fig.subplots_adjust(left=.08,right=.98,top=.82,bottom=.22,wspace=.35)
    fig.savefig(ROOT/'docs/research/assets/coupled-strips-20260908.svg',metadata={'Date':None})
    if args.preview:fig.savefig(args.preview,dpi=150)
    plt.close(fig);print(table)


if __name__=='__main__':main()
