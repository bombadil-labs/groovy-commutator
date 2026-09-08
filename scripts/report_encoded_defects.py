"""Rebuild the defect comparison figure directly from audited response records."""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/encoded_defects_20260908'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',type=Path)
    args=parser.parse_args()
    data=json.loads(Path(str(STEM)+'_responses.json').read_text())
    rows={(r['mode'],r['mask'],r['fine_ticks']):r for r in data['records']}
    pairs={(r['mode'],r['a'],r['b'],r['fine_ticks']):r for r in data['pairs']}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    fig,(left,right)=plt.subplots(1,2,figsize=(11,5.3))
    fig.suptitle('A coordinated logical action behaves differently from its parts',fontsize=15,y=.97)
    colors=['#176b86','#b96934'];width=.34
    for i,(mode,label) in enumerate([('periodic','Repeated each vertical period'),('isolated','Confined to one block')]):
        values=[rows[mode,m,4]['distinct_responses'] for m in [1,32,33]]
        bars=left.bar(np.arange(3)+(i-.5)*width,values,width,color=colors[i],label=label)
        left.bar_label(bars,padding=3,fontsize=10)
        vals=[100*pairs[mode,0,5,t]['nonlinear_backgrounds']/512 for t in [2,4]]
        bars=right.bar(np.arange(2)+(i-.5)*width,vals,width,color=colors[i])
        right.bar_label(bars,labels=[f'{v:g}%' for v in vals],padding=3,fontsize=10)
    left.set_title('Response dependence on the background',fontsize=11,pad=13)
    left.set_xticks(range(3),['Top-left cell','Bottom-right cell','Both cells'])
    left.set_ylabel('Distinct response fields after 4 fine ticks')
    left.set_ylim(0,240);left.legend(fontsize=9,loc='upper center',bbox_to_anchor=(.5,-.15))
    right.set_title('Does the pair differ from XOR of its separate responses?',fontsize=11,pad=13)
    right.set_xticks(range(2),['2 fine ticks','4 fine ticks'])
    right.set_ylabel('Backgrounds with nonzero interaction (%)');right.set_ylim(0,118)
    for ax in [left,right]:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
    fig.text(.5,.055,'All 512 local backgrounds. The two cells are the variable positions of the six-cell Rule-90 code.',ha='center',fontsize=10)
    fig.text(.5,.015,'The repeated two-cell mask stays in the code; its individual parts and the isolated pair do not recover by tick 4.',ha='center',fontsize=9)
    fig.subplots_adjust(left=.075,right=.98,top=.81,bottom=.27,wspace=.30)
    fig.savefig(ROOT/'docs/research/assets/encoded-defects-20260908.svg',metadata={'Date':None})
    if args.preview:fig.savefig(args.preview,dpi=150)
    plt.close(fig)
    table='| Mode | Mask | Same | Valid changed | Outside | Distinct responses |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
    for mode in ['periodic','isolated']:
        for mask in [1,2,4,8,16,32,33]:
            r=rows[mode,mask,4]
            table+=f'| {mode} | {mask} | '+ ' | '.join(str(r[k]) for k in ['same','valid_changed','outside','distinct_responses'])+' |\n'
    Path(str(STEM)+'_table.md').write_text(table)
    print(table)


if __name__=='__main__':main()
