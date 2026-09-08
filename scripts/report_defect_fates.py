"""Rebuild long-run summaries and the exceptional strip illustration."""
from pathlib import Path
import argparse,base64,json,zlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from check_defect_strip import strip
from experiment_column_compatibility import step2
ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/defect_fates_20260908'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',type=Path)
    args=parser.parse_args()
    p=json.loads(Path(str(STEM)+'_metrics.json').read_text())
    m=np.frombuffer(zlib.decompress(base64.b64decode(p['data'])),dtype='<i4').reshape(p['shape'])
    bgs=json.loads(Path(str(STEM)+'_backgrounds.json').read_text())
    cases=json.loads(Path(str(STEM)+'_cases.json').read_text())
    summary=[]
    for mi,mode in enumerate(p['modes']):
        for cohort in ['periodic','random-a','random-b']:
            rows=[r for r in cases if r['mode']==mode and r['cohort']==cohort and r['mask'] not in ([0,33] if mode=='periodic' else [0])]
            bi=[i for i,b in enumerate(bgs) if b['cohort']==cohort]
            masks=[i for i in range(1,64) if mode!='periodic' or i!=33]
            a=m[mi][bi][:,masks]
            summary.append(dict(mode=mode,cohort=cohort,initially_invalid=len(rows),
                returns=sum(r['first_return'] is not None for r in rows),
                screens=sum(r['screen'] is not None for r in rows),
                certificates=sum(r['certificate'] is not None for r in rows),
                median_mass_32=float(np.median(a[:,:,-1,0])),
                final_mass_below_prior_peak=int((a[:,:,-1,0]<a[:,:,:,0].max(axis=2)).sum())))
    Path(str(STEM)+'_summary.json').write_text(json.dumps(dict(groups=summary,
        initially_invalid=sum(r['initially_invalid'] for r in summary),
        certified_structure_followup={'eligible':0,'performed':0},
        strip_followup='Separate post-census algebraic hypothesis, verified in _strip.json'),indent=2)+'\n')
    table='| Mode | Background cohort | Initially invalid cases | Returns | Shape screens | Median changed cells at tick 32 |\n| --- | --- | ---: | ---: | ---: | ---: |\n'
    for r in summary:table+=f'| {r["mode"]} | {r["cohort"]} | {r["initially_invalid"]} | {r["returns"]} | {r["screens"]} | {r["median_mass_32"]:g} |\n'
    Path(str(STEM)+'_table.md').write_text(table)
    # Reproduce the complete exceptional response, then extract the strip bit.
    seed=np.zeros((1,65),dtype=np.uint8);seed[0,0]=1
    ys=np.arange(-65,68);xs=np.arange(-64,66)
    field=strip(seed,ys,xs);natural=strip(np.zeros_like(seed),ys,xs)
    rows=[]
    for t in range(33):
        if t%2==0:
            margin=32-t;d=(field^natural)[0,margin:margin+69,margin:margin+66]
            assert int(d.sum())==m[1,0,6,t//2,0]
            assert int(d.sum())==2*(1 << (t//2).bit_count())
            assert m[1,0,6,t//2,4]-m[1,0,6,t//2,3]+1==2*t+2
            rows.append(d[34,::2]) # absolute row1, even columns.
        if t<32:field=step2(field,shrink=True);natural=step2(natural,shrink=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    fig,(left,right)=plt.subplots(1,2,figsize=(11.5,5.2),gridspec_kw={'width_ratios':[1.15,1]})
    fig.suptitle('A sparse return is not a spatial reunion',fontsize=16,y=.96)
    left.imshow(np.array(rows),cmap=ListedColormap(['#edf2f5','#176b86']),vmin=0,vmax=1,interpolation='nearest',aspect='equal')
    left.set_title('Rule 90 in a finite two-row strip',fontsize=11,pad=12)
    left.set_xticks([0,8,16,24,32],['−16','−8','0','8','16']);left.set_xlabel('Logical position')
    left.set_yticks([0,4,8,12,16],['0','8','16','24','32']);left.set_ylabel('Fine ticks (two per logical update)')
    ticks=np.array(p['times']);r=m[1,0,6]
    right.plot(ticks,r[:,0],'-o',color='#176b86',markersize=4,label='Changed physical cells')
    right.plot(ticks,r[:,4]-r[:,3]+1,'-',color='#b96934',label='Horizontal span in physical cells')
    right.set_title('Mask 6 on the zero logical background',fontsize=11,pad=12)
    right.set_xlabel('Fine ticks');right.set_ylabel('Cell count or span');right.set_xticks([0,8,16,24,32])
    right.grid(alpha=.15);right.legend(fontsize=9,loc='upper left')
    fig.text(.5,.085,'At tick 30: 32 changed cells across 62 columns. At tick 32: 4 changed cells across 66 columns.',ha='center',fontsize=10)
    fig.text(.5,.035,'This trajectory stays outside the original repeated code, but belongs to a different exact Rule-90 encoding from the start.',ha='center',fontsize=9)
    fig.subplots_adjust(left=.07,right=.98,top=.81,bottom=.25,wspace=.30)
    fig.savefig(ROOT/'docs/research/assets/defect-fates-20260908.svg',metadata={'Date':None})
    if args.preview:fig.savefig(args.preview,dpi=150)
    plt.close(fig)
    print(table)


if __name__=='__main__':main()
