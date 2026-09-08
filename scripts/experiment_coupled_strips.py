"""Exact composition residuals for two aligned strips under the fixed 2D law."""
from pathlib import Path
import hashlib,json,time
import numpy as np
from experiment_column_compatibility import step2
ROOT=Path(__file__).resolve().parents[1]
STEM=ROOT/'results/coupled_strips_20260908'
VARIABLES=['aL','aC','aR','bL','bC','bR']


def encode_pair(a,b,gap,ys,xs):
    n=a.shape[-1]
    out=np.broadcast_to((xs%2)[None,None,:],(len(a),len(ys),len(xs))).astype(np.uint8).copy()
    for states,start in [(a,0),(b,2+gap)]:
        for k,x in enumerate(xs):
            data=states[:,(x//2)%n]
            if x%2==1:
                out[:,np.flatnonzero(ys==start),k]=(1^data)[:,None]
            else:
                out[:,np.flatnonzero(ys==start+1),k]=data[:,None]
    return out


def algebra(truth):
    coefficients=truth.copy()
    for bit in range(6):
        for mask in range(64):
            if mask&(1<<bit):coefficients[mask]^=coefficients[mask^(1<<bit)]
    terms=[i for i in range(64) if coefficients[i]]
    essential=[j for j in range(6) if any(truth[q]!=truth[q^(1<<j)] for q in range(64))]
    return dict(terms=terms,essential=essential,degree=max((i.bit_count() for i in terms),default=0),
        mixed_terms=[i for i in terms if i&7 and i&56])


def cell_records(field,ys):
    return [dict(y=int(y),x=x,**algebra(field[:,j,x])) for j,y in enumerate(ys) for x in range(2)]


def main():
    start=time.time();inputs=((np.arange(64)[:,None]>>np.arange(6))&1).astype(np.uint8)
    a=inputs[:,[1,2,0]];b=inputs[:,[4,5,3]] # logical ring index0=center,1=right,2=left
    entries=[]
    for gap in range(5):
        ys=np.arange(-4,gap+8);xs=np.arange(-2,4)
        initial=encode_pair(a,b,gap,ys,xs)
        first=step2(initial,shrink=True)
        output=step2(first,shrink=True)
        rows=np.arange(-2,gap+6)
        qa=inputs[:,0]^inputs[:,2];qb=inputs[:,3]^inputs[:,5]
        independent=encode_pair(qa[:,None],qb[:,None],gap,rows,np.arange(2))
        decoded_a=output[:,3,0];decoded_b=output[:,gap+5,0]
        reconstructed=encode_pair(decoded_a[:,None],decoded_b[:,None],gap,rows,np.arange(2))
        valid=np.all(output==reconstructed,axis=(1,2))
        residual=output^independent
        differing=residual.any(axis=(1,2))
        poly=cell_records(output,rows);rpoly=cell_records(residual,rows)
        top_cross=[r for r in poly if r['y'] in [0,1] and any(j>=3 for j in r['essential'])]
        bottom_cross=[r for r in poly if r['y'] in [gap+2,gap+3] and any(j<3 for j in r['essential'])]
        failed=np.flatnonzero(~valid).tolist()
        witness=None
        if failed:
            q=failed[0]
            witness=dict(input_index=q,input_bits=inputs[q].tolist(),output=output[q].tolist(),
                decoded=[int(decoded_a[q]),int(decoded_b[q])],reconstructed=reconstructed[q].tolist(),
                invalid_cells=[dict(y=int(rows[y]),x=int(x)) for y,x in np.argwhere(output[q]!=reconstructed[q])])
        entry=dict(gap=gap,output_rows=rows.tolist(),valid_inputs=int(valid.sum()),
            independent_inputs=int((~differing).sum()),failed_inputs=failed,
            valid=valid.astype(int).tolist(),decoded_pairs=np.stack([decoded_a,decoded_b],axis=1).tolist(),
            first_tick_rows=ys[1:-1].tolist(),first_tick_center=first[:,:,1:3].tolist(),
            output=output.tolist(),independent=independent.tolist(),residual=residual.tolist(),
            output_polynomials=poly,residual_polynomials=rpoly,
            top_cross_cells=[dict(y=r['y'],x=r['x']) for r in top_cross],
            bottom_cross_cells=[dict(y=r['y'],x=r['x']) for r in bottom_cross],witness=witness)
        entries.append(entry)
        print(gap,'valid',int(valid.sum()),'independent',int((~differing).sum()),
              'maxdegree',max(r['degree'] for r in poly),'cross',len(top_cross),len(bottom_cross),flush=True)
    payload=dict(variables=VARIABLES,input_bit_order='variable index, little-endian',inputs=inputs.tolist(),gaps=entries)
    Path(str(STEM)+'_local.json').write_text(json.dumps(payload,indent=2)+'\n')
    sources=['scripts/experiment_coupled_strips.py','scripts/experiment_column_compatibility.py','docs/research/protocols/coupled-strips-20260908.md']
    Path(str(STEM)+'_metadata.json').write_text(json.dumps(dict(local_cases=320,seconds=round(time.time()-start,3),
        sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}),indent=2)+'\n')


if __name__=='__main__':main()
