"""Rebuild the compatibility table and scientific figure from saved data."""
from pathlib import Path
import csv
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/column_compatibility_20260908'


def main():
    summary=json.loads(Path(str(STEM)+'_summary.json').read_text())
    damage=list(csv.DictReader(Path(str(STEM)+'_damage.csv').open()))
    aggregate=[]
    for k in [1,2,3]:
        rows=[v for v in summary['census'] if v['k']==k]
        aggregate.append([k,sum(v['candidates'] for v in rows),
                          sum(v['accepted']+v['outer_context'] for v in rows),
                          sum(v['accepted'] for v in rows)])
    table='| Fine ticks per logical update | Codes tested | Code family preserved | Elementary update |\n| --- | ---: | ---: | ---: |\n'
    for row in aggregate:table+='| '+' | '.join(map(str,row))+' |\n'
    Path(str(STEM)+'_table.md').write_text(table)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    fig,(left,right)=plt.subplots(1,2,figsize=(12,4.9),gridspec_kw={'width_ratios':[1.15,1]})
    fig.suptitle('An encoding can survive while its effective neighborhood grows',fontsize=16,y=.97)
    left.axis('off')
    left.set_title('Exact census: every ordered column pair, heights 1–6',fontsize=11,pad=15)
    cells=[[str(k),f'{valid:,}',f'{eca:,}'] for k,total,valid,eca in aggregate]
    artist=left.table(cellText=cells,colLabels=['Fine ticks','Code survives','Elementary rule'],
                      bbox=[0,.40,1,.47],cellLoc='center')
    artist.auto_set_font_size(False);artist.set_fontsize(11)
    for (r,c),cell in artist.get_celld().items():
        cell.set_edgecolor('#d0d8df')
        cell.set_facecolor('#eaf1f7' if r==0 else '#ffffff')
    left.text(0,.25,'5,334 candidate codes per cadence; symmetry copies included.',fontsize=9)
    left.text(0,.13,'All-height graph: only 23 and 232 at one tick;\nno elementary target at two or three ticks.',fontsize=10)
    for n,style in [(5,'--'),(7,'-')]:
        rows=[v for v in damage if int(v['m'])==2 and int(v['a'])==1 and int(v['b'])==2
              and int(v['n'])==n and int(v['damaged_row'])==0]
        rows.sort(key=lambda v:int(v['h']))
        for field,color,label in [('valid','#176b86','Valid encoding'),('same_natural','#ac6234','Undamaged trajectory')]:
            right.plot([int(v['h']) for v in rows],[100*int(v[field])/int(v['states']) for v in rows],
                       style,color=color,marker='o',label=f'{label}, width {n}')
    right.set_title('Rule 23 encoding after one physical cell flip',fontsize=11,pad=15)
    right.set_xlabel('Coarse ticks after damage');right.set_ylabel('Initial states (%)')
    right.set_xticks(range(5));right.set_ylim(-2,35);right.grid(alpha=.2)
    right.legend(fontsize=8,loc='upper left')
    fig.text(.05,.03,'Damage: complete 2×5 and 2×7 tori, fixed row-0/column-0 flip. Matched logical flips change both code cells.',fontsize=9)
    fig.subplots_adjust(left=.05,right=.98,bottom=.19,top=.82,wspace=.35)
    target=ROOT/'docs/research/assets/column-compatibility-20260908.svg'
    fig.savefig(target)
    fig.savefig('/workspace/scratch/4e0fdfb9ecdc/compatibility-preview.png',dpi=150)
    plt.close(fig)
    print(table)


if __name__=='__main__':main()
