"""Cropped-source verification of new positives; scalar failure witnesses."""
import argparse,json,time
from pathlib import Path
import numpy as np
from harness import Compiler,derive,load_operator
from verify_probe_radius import consistent,reconstruct

def read(grid,rx):
    width=2*rx+1; start=(grid.shape[-1]-width)//2
    b=grid[...,start:start+width]
    b=np.concatenate([b,np.roll(b,-1,axis=1),np.roll(b,1,axis=1)],axis=-1)
    return b @ (np.uint64(1)<<np.arange(3*width-1,-1,-1,dtype=np.uint64))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);args=ap.parse_args();start=time.perf_counter()
    root=Path(__file__).resolve().parent;op=load_operator(root/'lifts/fixed_transverse.py')
    rows=list(map(json.loads,(args.run/'decisions.jsonl').read_text().splitlines()))
    positives=0; failures=0; whole=[]
    for rec in rows:
        rx=rec['radius'];rule=rec['rule'];path=rec['recipe'];width=2*rx+5;n=1<<width;mid=width//2
        good=[(name,v) for name,v in rec['branches'].items() if v['passes']]
        if good:
            compiler=Compiler(rule,rx+1,op)
            a=compiler.encode(path); c=compiler.encode(path,2); delta=compiler.mask(path)
            bk=read(a,rx);bv=delta[...,rx];ds=compiler.source_masks[0]
            gt=compiler.source_masks[1]^(ds[...,1:-1]^derive(ds,rule))
            carrier=np.stack([gt[:,rx]^gt[:,rx+path[0]['shift']],gt[:,rx]],axis=1)
            keys=read(delta,rx)[:,:2];bits=a[:,:2,rx+1]^c[:,:2,rx-1]^carrier
            for name,v in good:
                z=None if name=='raw' else int(name);wanted=bits.copy()
                if z is not None:wanted[:,1]^=rule&1
                assert consistent(bk,bv,keys,wanted,z),(rule,rx,name)
                positives+=1
        for name,v in rec['branches'].items():
            if v['passes']:continue
            z=None if name=='raw' else int(name);events=[];sheets=[]
            for event_index,bit in zip(v['conflict']['event_indices'],v['conflict']['bits']):
                if event_index==5*n:
                    event={'kind':'chosen_zero_bit','required':bit}
                else:
                    kind='beam' if event_index<3*n else 'temporal'
                    index=event_index if kind=='beam' else event_index-3*n
                    word,phase=divmod(index,3 if kind=='beam' else 2)
                    source=f'{word:0{width}b}';source=source[mid:]+source[:mid]
                    event={'kind':kind,'source':source,'phase':phase,'required':bit}
                grid,wanted=reconstruct(event,rule,path[0],z)
                key=0
                for row in grid:
                    for dx in range(-rx,rx+1):key=(key<<1)|row[dx%len(row)]
                assert key==v['conflict']['key'] and wanted==bit,(rule,rx,name,event)
                events.append(event);sheets.append(grid)
            failures+=1
            equal=all(sheets[0][j][i%len(sheets[0][j])]==sheets[1][j][i%len(sheets[1][j])] for j in range(3) for i in range(width))
            if equal:whole.append({'candidate':rec['candidate'],'rule':rule,'recipe':path,'branch':name,'events':events,'from_radius':rx})
    (args.run/'new_global_witnesses.json').write_text(json.dumps(whole,indent=2)+'\n')
    result={'passed':True,'independent_exhaustive_positive_branches':positives,'scalar_local_conflicts_verified':failures,'whole_periodic_conflicts_found':len(whole),'seconds':time.perf_counter()-start}
    (args.run/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
