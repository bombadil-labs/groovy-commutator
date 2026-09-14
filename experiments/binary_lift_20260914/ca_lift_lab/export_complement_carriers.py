"""Export and directly verify the shared complemented-T2 recipe for all eight.

Uses the independent cropped-source implementation and keeps unknown table
outputs explicitly unspecified. This is a post-census concrete construction.
"""
import gzip,hashlib,json,time
from pathlib import Path
import numpy as np
from verify_dt2_holdouts import arrays,keys,table,lookup,S
ROOT=Path(__file__).resolve().parent;RUN=ROOT/'runs/row_complements_8'
def main():
    start=time.monotonic();rr=[json.loads(s)for s in(RUN/'common_recipe.jsonl').read_text().splitlines()]
    counts={'rules':[],'direct_G_cells':0,'native_next_cells':0,'decoder_cells':0,'table_sizes':{}}
    for r in rr:
        d=arrays(r['rule'],r['mask'],r['shift'],r['reference']);order=r['order']
        flip=np.array([0,0,31,0,0],dtype=np.uint32)
        bk=keys(d['ac']^flip,order);kb=keys(d['bc']^flip,order);pk=keys(d['uc'],order)[:,:2]
        native=d['flip'][:,order];wanted=d['want'].copy();wanted[:,1]^=r['rule']&1
        ok,decoder=table(bk,np.broadcast_to(S[:,5,None],bk.shape));assert ok
        assert np.array_equal(lookup(decoder,bk),np.broadcast_to(S[:,5,None],bk.shape));counts['decoder_cells']+=bk.size
        assert not np.intersect1d(bk,pk).size
        for zero in(0,1):
            ok,h=table(np.concatenate([bk.ravel(),pk.ravel(),[0]]).astype(np.uint32),np.concatenate([native.ravel(),(wanted^zero).ravel(),[zero]]).astype(np.uint8));assert ok
            assert np.array_equal(lookup(h,bk),native)
            next_flip=lookup(h,kb);assert np.array_equal(next_flip,(d['b'][...,2]^d['c'])[:,order])
            actual=next_flip[:,:2]^native[:,:2]^lookup(h,pk)^zero
            expected=d['carrier'].copy();expected[:,1]^=r['rule']&1
            assert np.array_equal(actual,expected)
            counts['direct_G_cells']+=actual.size;counts['native_next_cells']+=2*bk.size
            if zero==0:
                encoded={'rule':r['rule'],'recipe':{k:r[k]for k in('mask','shift','reference','order','polarity')},'h_zero':0,'key_order':'dy=-2..2 then dx=-2..2, first bit most significant','derivative_table':np.stack(h,axis=1).tolist(),'source_decoder':np.stack(decoder,axis=1).tolist(),'unspecified_outputs':'free outside listed keys; no zero completion implied','carrier':'centered G on P/D only'}
                payload=json.dumps(encoded,separators=(',',':')).encode();name=f'carrier-rule-{r["rule"]}.json.gz'
                (RUN/name).write_bytes(gzip.compress(payload,mtime=0))
                counts['table_sizes'][str(r['rule'])]={'derivative_keys':len(h[0]),'decoder_keys':len(decoder[0]),'native_probe_overlap':0,'file':name,'sha256':hashlib.sha256((RUN/name).read_bytes()).hexdigest()}
        counts['rules'].append(r['rule'])
    counts.update(status='passed',seconds=time.monotonic()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (RUN/'common_recipe_verification.json').write_text(json.dumps(counts,indent=2)+'\n');print(json.dumps(counts))
if __name__=='__main__':main()
