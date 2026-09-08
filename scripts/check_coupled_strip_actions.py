"""Finite paired-ring and matched-action corroboration after local identity checks."""
from pathlib import Path
import hashlib,itertools,json,sys,time
import numpy as np
from experiment_coupled_strips import encode_pair
from experiment_column_compatibility import step2
from audit_coupled_strips import bitstep,pack_fields,unpack
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from groovy.ca import apply_rule
STEM=ROOT/'results/coupled_strips_20260908'


def evolve(f,g):
    f=step2(np.pad(f,((0,0),(0,0),(1,1)),mode='wrap'),shrink=True)
    g=bitstep(np.pad(g,((0,0),(1,1)),mode='wrap'))
    assert np.array_equal(f,unpack(g)[:len(f)])
    return f,g


def main():
    start=time.time();local=json.loads(Path(str(STEM)+'_local.json').read_text())
    eligible=[r['gap'] for r in local['gaps'] if r['gap'] in [1,2] and r['independent_inputs']==64]
    counts=dict(fine_fields=0,coarse_states=0,action_word_states=0)
    for gap in eligible:
        d=gap+2
        for n in [5,7]:
            states=((np.arange(1<<n)[:,None]>>np.arange(n))&1).astype(np.uint8)
            # Cache package updates independently for every logical row, not flattened batches.
            lookup={tuple(s):apply_rule(s,90) for s in states}
            ys=np.arange(-8,d+10);xs=np.arange(2*n)
            for offset in range(0,1<<(2*n),64):
                q=np.arange(offset,min(offset+64,1<<(2*n)))
                a=states[q%(1<<n)].copy();b=states[q//(1<<n)].copy()
                f=encode_pair(a,b,gap,ys,xs);g=pack_fields(f)
                for fine in range(1,9):
                    f,g=evolve(f,g);counts['fine_fields']+=len(f)
                    if fine%2==0:
                        a=np.array([lookup[tuple(s)] for s in a]);b=np.array([lookup[tuple(s)] for s in b])
                        assert np.array_equal(f,encode_pair(a,b,gap,ys[fine:-fine],xs))
                        counts['coarse_states']+=len(f)
            print('gap',gap,'width',n,'all pairs passed',flush=True)
        if gap==1:
            n=5;states=((np.arange(32)[:,None]>>np.arange(5))&1).astype(np.uint8)
            lookup={tuple(s):apply_rule(s,90) for s in states};ys=np.arange(-6,d+8);xs=np.arange(10)
            for word in itertools.product(range(4),repeat=3):
                for offset in range(0,1024,64):
                    q=np.arange(offset,offset+64);a=states[q%32].copy();b=states[q//32].copy()
                    f=encode_pair(a,b,gap,ys,xs);g=pack_fields(f)
                    for coarse,act in enumerate(word):
                        for flag,startrow,logical in [(1,0,a),(2,d,b)]:
                            if act&flag:
                                row=startrow+6-2*coarse
                                f[:,row,1]^=1;f[:,row+1,0]^=1
                                g[row,1]^=np.uint64(2**64-1);g[row+1,0]^=np.uint64(2**64-1)
                                logical[:,0]^=1
                        for _ in range(2):f,g=evolve(f,g);counts['fine_fields']+=len(f)
                        a=np.array([lookup[tuple(s)] for s in a]);b=np.array([lookup[tuple(s)] for s in b])
                        cut=2*(coarse+1)
                        assert np.array_equal(f,encode_pair(a,b,gap,ys[cut:-cut],xs))
                        counts['action_word_states']+=len(f)
            print('all action words passed',flush=True)
    result=dict(eligible_gaps=eligible,checks=counts,seconds=round(time.time()-start,3),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(str(STEM)+'_actions.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
