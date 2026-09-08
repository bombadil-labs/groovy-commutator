"""Post-census exact strip identity and finite matched-action checks."""
from pathlib import Path
import hashlib,itertools,json,sys
import numpy as np
from experiment_column_compatibility import step2
from audit_defect_fates import advance as bitstep,unpack
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from groovy.ca import apply_rule
STEM=ROOT/'results/defect_fates_20260908'


def strip(states,ys,xs):
    n=states.shape[-1]
    s=states[:,(xs//2)%n]
    out=np.broadcast_to((xs%2)[None,None,:],(len(states),len(ys),len(xs))).astype(np.uint8).copy()
    out[:,np.flatnonzero(ys==0)[:,None],np.flatnonzero(xs%2==1)] = 1^s[:,None,xs%2==1]
    out[:,np.flatnonzero(ys==1)[:,None],np.flatnonzero(xs%2==0)] = s[:,None,xs%2==0]
    return out


def pack_fields(a):
    # Independent evolution packs up to 64 trajectories into uint64 bits.
    assert len(a)<=64
    out=np.zeros(a.shape[1:],dtype=np.uint64)
    for i in range(len(a)):out|=a[i].astype(np.uint64)<<np.uint64(i)
    return out


def horizontal_period_step(a):
    # Exact horizontal ring, shrinking vertical interval (no vertical torus).
    return step2(np.pad(a,((0,0),(0,0),(1,1)),mode='wrap'),shrink=True)


def main():
    checks={'local_triples':0,'fine_fields':0,'coarse_states':0,'action_word_states':0}
    # states columns are indexed -1,0,+1 using a three-cell logical ring;
    # the physical interval provides the complete radius-two cone without wraps.
    triples=((np.arange(8)[:,None]>>np.arange(3))&1).astype(np.uint8)
    states=triples[:,[1,2,0]]
    ys=np.arange(-4,6);xs=np.arange(-2,4)
    f=strip(states,ys,xs);g=pack_fields(f)
    one=step2(f,shrink=True);g1=unpack(bitstep(g,'isolated'))[:8]
    assert np.array_equal(one,g1)
    for i,(l,c,r) in enumerate(triples):
        # First output has rows -3..4 and cols -1..2; inspect center block cols0/1.
        # Construct by absolute row to avoid phase/order assumptions.
        e=np.tile([1,0],(8,1))
        e[3]=[1^int(l)^int(c),0];e[4]=[1,int(c)^int(r)]
        assert np.array_equal(one[i,:,1:3],e)
    two=step2(one,shrink=True);g2=unpack(bitstep(bitstep(g,'isolated'),'isolated'))[:8]
    assert np.array_equal(two,g2)
    for i,(l,c,r) in enumerate(triples):
        q=int(l)^int(r);e=np.tile([0,1],(6,1));e[2]=[0,1^q];e[3]=[q,1]
        assert np.array_equal(two[i],e)
        checks['local_triples']+=1
    for n in [5,7]:
        allstates=((np.arange(1<<n)[:,None]>>np.arange(n))&1).astype(np.uint8)
        for start in range(0,len(allstates),64):
            s=allstates[start:start+64].copy();ys=np.arange(-8,10);xs=np.arange(2*n)
            f=strip(s,ys,xs);g=pack_fields(f)
            for fine in range(1,9):
                f=horizontal_period_step(f)
                g=bitstep(np.pad(g,((0,0),(1,1)),mode='wrap'),'isolated')
                assert np.array_equal(f,unpack(g)[:len(s)])
                checks['fine_fields']+=len(s)
                if fine%2==0:
                    s=np.array([apply_rule(row,90) for row in s])
                    assert np.array_equal(f,strip(s,ys[fine:-fine],xs))
                    checks['coarse_states']+=len(s)
        if n==5:
            for word in itertools.product([0,1],repeat=3):
                s=allstates.copy();ys=np.arange(-6,8);xs=np.arange(2*n);f=strip(s,ys,xs);g=pack_fields(f)
                for coarse,act in enumerate(word):
                    if act:
                        f[:,6-2*coarse,1]^=1;f[:,7-2*coarse,0]^=1
                        active=np.uint64((1<<len(s))-1);g[6-2*coarse,1]^=active;g[7-2*coarse,0]^=active
                        s[:,0]^=1
                    for _ in range(2):
                        f=horizontal_period_step(f);g=bitstep(np.pad(g,((0,0),(1,1)),mode='wrap'),'isolated')
                        assert np.array_equal(f,unpack(g)[:len(s)])
                    s=np.array([apply_rule(row,90) for row in s]);cut=2*(coarse+1)
                    assert np.array_equal(f,strip(s,ys[cut:-cut],xs))
                    checks['action_word_states']+=len(s)
    paths=['scripts/check_defect_strip.py','docs/research/protocols/defect-fates-strip-followup-20260908.md']
    result=dict(checks=checks,identity='F^2 U = U phi90',physical_flips_per_logical_flip=2,
                vertical_support_rows=2,chronology='Post-census conjecture and exact verification',
                sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
    Path(str(STEM)+'_strip.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
