"""Post-census front-lemma checks and scientific figure; not a fitted decoder."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from experiment_column_compatibility import step2

ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/interface_state_20260908'


def front_checks():
    # An outward new row only reads background or the existing extreme row.
    # All five-bit extreme rows and both ether phases, for both directions.
    patterns=((np.arange(32)[:,None]>>np.arange(5))&1).astype(np.uint8)
    xs=np.arange(-2,3);checked=0
    for phase in [0,1]:
        bg=(xs%2)^phase
        f=np.tile(bg,(32,5,1)).astype(np.uint8)
        f[:,2]^=patterns
        out=step2(f,shrink=True)^((xs[1:-1]%2)^(phase^1))
        # delta_new(top-1,x) = B_t(x) delta_old(top,x-1)
        top=bg[1:-1]*patterns[:,:-2]
        bottom=(1^bg[1:-1])*patterns[:,2:]
        assert np.array_equal(out[:,0],top)
        assert np.array_equal(out[:,2],bottom)
        checked+=32*2*3
    witness=json.loads(Path(str(STEM)+'_witness.json').read_text())
    for r in witness['records'][4:]:
        t=r['tick']
        assert r['top']==[[3-t,t]] and r['bottom']==[[t,3-t]]
        assert r['bounds'][:2]==[3-t,t]
    assert witness['records'][4]['top']==[[-1,4]]
    assert witness['records'][4]['bottom']==[[4,-1]]
    result=dict(front_row_patterns=32,phases=2,directions=2,local_cell_checks=checked,
                finite_witness_endpoint_checks=29,
                scope='Post-census lemma corroboration. The all-time result uses the local induction in Research019.',
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(str(STEM)+'_front_checks.json').write_text(json.dumps(result,indent=2)+'\n')


def figure(preview):
    data=json.loads(Path(str(STEM)+'_witness.json').read_text())
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,3,figsize=(11.5,5))
    fig.suptitle('A four-cell interaction escapes every fixed-height band',fontsize=16,y=.97)
    for ax,t in zip(axes,[4,12,32]):
        r=data['records'][t];ymin,ymax,xmin,xmax=r['bounds']
        delta=np.zeros((ymax-ymin+1,xmax-xmin+1),dtype=np.uint8)
        for y,x in r['changed']:delta[y-ymin,x-xmin]=1
        ax.imshow(delta,cmap=ListedColormap(['#ffffff','#176b86']),vmin=0,vmax=1,
                  interpolation='nearest',extent=[xmin-.5,xmax+.5,ymax+.5,ymin-.5],aspect='equal')
        for y in [-.5,3.5]:ax.axhline(y,color='#b65029',lw=1,ls='--')
        ax.scatter([t,3-t],[3-t,t],marker='s',s=28,facecolors='none',edgecolors='#b65029',linewidths=1)
        ax.set_title(f'Tick {t}: {r["mass"]} changed cells',fontsize=11,pad=10)
        ax.set_xlabel('Physical column x')
        ax.set_ylabel('Physical row y')
        ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.12,'Blue cells differ from the alternating background; dashed lines enclose the original four rows.',ha='center',fontsize=10)
    fig.text(.5,.07,'The two marked extreme cells lie at (y, x) = (3 − t, t) and (t, 3 − t) for every t ≥ 4.',ha='center',fontsize=10)
    fig.text(.5,.025,'Local induction proves continued escape. The growing wake is not an isolated traveling object.',ha='center',fontsize=9)
    fig.subplots_adjust(left=.06,right=.985,top=.84,bottom=.22,wspace=.35)
    fig.savefig(ROOT/'docs/research/assets/interface-state-20260908.svg',metadata={'Date':None})
    if preview:fig.savefig(preview,dpi=150)
    plt.close(fig)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preview',type=Path);args=parser.parse_args()
    front_checks();figure(args.preview)
