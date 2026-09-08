"""Independent encoder, truth-set evolution, and subset-parity polynomial audit."""
from pathlib import Path
import hashlib,json,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/coupled_strips_20260908'
FULL=np.uint64(2**64-1)


def bitstep(g):
    l,c,r=g[1:-1,:-2],g[1:-1,1:-1],g[1:-1,2:]
    zero=~(l|r);one=l^r;two=l&r
    up=(zero&g[:-2,:-2])|(one&g[:-2,1:-1])|(two&g[:-2,2:])
    down=(zero&g[2:,:-2])|(one&g[2:,1:-1])|(two&g[2:,2:])
    return ((~c)&up)|(c&down)


def unpack(g):
    raw=np.frombuffer(g.astype('<u8').tobytes(),dtype=np.uint8)
    return np.unpackbits(raw,bitorder='little').reshape(*g.shape,64).transpose(2,0,1)


def pack_fields(a):
    result=np.zeros(a.shape[1:],dtype=np.uint64)
    for i,row in enumerate(a):result|=row.astype(np.uint64)<<np.uint64(i)
    return result


def polynomial(truth):
    terms=[]
    for subset in range(64):
        value=0
        for q in range(64):
            if q&subset==q:value^=int(truth[q])
        if value:terms.append(subset)
    for q in range(64):assert int(truth[q])==sum((q&term)==term for term in terms)%2
    essential=[j for j in range(6) if any(truth[q]!=truth[q|(1<<j)] for q in range(64))]
    return dict(terms=terms,essential=essential,degree=max([0]+[s.bit_count() for s in terms]),
                mixed_terms=[s for s in terms if s&7 and s&56])


def main():
    start=time.time();data=json.loads(Path(str(STEM)+'_local.json').read_text());count=0
    variables=[np.uint64(sum(1<<q for q in range(64) if q&(1<<j))) for j in range(6)]
    for saved in data['gaps']:
        gap=saved['gap'];rows=list(range(-4,gap+8));cols=list(range(-2,4))
        g=np.array([[FULL if x%2 else 0 for x in cols] for y in rows],dtype=np.uint64)
        for j,y in enumerate(rows):
            for k,x in enumerate(cols):
                var=x//2+1
                if y==0 and x%2:g[j,k]=FULL^variables[var]
                if y==1 and x%2==0:g[j,k]=variables[var]
                if y==gap+2 and x%2:g[j,k]=FULL^variables[3+var]
                if y==gap+3 and x%2==0:g[j,k]=variables[3+var]
        one=unpack(bitstep(g));out=unpack(bitstep(bitstep(g)))
        assert np.array_equal(one[:,:,1:3],saved['first_tick_center'])
        assert np.array_equal(out,saved['output'])
        valid=[];pairs=[];reference=np.zeros_like(out)
        for q in range(64):
            aa=int(out[q,3,0]);bb=int(out[q,gap+5,0]);pairs.append([aa,bb])
            expected=np.tile([0,1],(gap+8,1))
            expected[2]=[0,1-aa];expected[3]=[aa,1]
            expected[gap+4]=[0,1-bb];expected[gap+5]=[bb,1]
            valid.append(int(np.array_equal(out[q],expected)))
            a=((q>>0)^(q>>2))&1;b=((q>>3)^(q>>5))&1
            reference[q]=np.tile([0,1],(gap+8,1))
            reference[q,2]=[0,1-a];reference[q,3]=[a,1]
            reference[q,gap+4]=[0,1-b];reference[q,gap+5]=[b,1]
        assert valid==saved['valid'] and pairs==saved['decoded_pairs']
        assert sum(valid)==saved['valid_inputs']
        assert [i for i,v in enumerate(valid) if not v]==saved['failed_inputs']
        assert np.array_equal(reference,saved['independent'])
        residual=out^reference;assert np.array_equal(residual,saved['residual'])
        assert int((~residual.any(axis=(1,2))).sum())==saved['independent_inputs']
        for name,field in [('output_polynomials',out),('residual_polynomials',residual)]:
            for record in saved[name]:
                actual=polynomial(field[:,record['y']+2,record['x']]);count+=1
                for key,value in actual.items():assert record[key]==value
        for name,ys,variables_range in [('top_cross_cells',[0,1],range(3,6)),('bottom_cross_cells',[gap+2,gap+3],range(3))]:
            expected=[]
            for y in ys:
                for x in range(2):
                    truth=out[:,y+2,x]
                    if any(any(truth[q]!=truth[q^(1<<j)] for q in range(64)) for j in variables_range):expected.append(dict(y=y,x=x))
            assert saved[name]==expected
    result=dict(local_cases=320,polynomials=count,all_fields_validity_and_influence_match=True,
        seconds=round(time.time()-start,3),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(str(STEM)+'_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
