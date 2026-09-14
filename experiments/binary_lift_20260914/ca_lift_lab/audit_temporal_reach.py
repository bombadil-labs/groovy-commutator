"""Exact temporal-G extension census at larger native horizontal radii.
Reuse certified positives and whole-sheet impossibility witnesses; enumerate
only unresolved candidate/branch cases. Sparse uint64 keys avoid dense tables.
"""
import argparse, hashlib, json, time
from pathlib import Path
import numpy as np
from verify_polarization_proposal import d, encode

ROOT = Path(__file__).resolve().parent

def patches(grid, radius):
    mid = grid.shape[-1]//2
    key = np.zeros(grid.shape[:2], dtype=np.uint64)
    for dy in (0,1,-1):
        for dx in range(-radius,radius+1):
            key = (key << 1) | grid[:,(np.arange(3)+dy)%3,mid+dx]
    return key

def check(bk, bv, pk, pv, zero):
    keys=np.concatenate([bk.ravel(),pk.ravel(),np.array([0],dtype=np.uint64) if zero is not None else np.array([],dtype=np.uint64)])
    bits=np.concatenate([bv.ravel(),(pv ^ (zero or 0)).ravel(),np.array([zero],dtype=np.uint8) if zero is not None else np.array([],dtype=np.uint8)])
    order=np.argsort(keys,kind='stable'); ks=keys[order]; vs=bits[order]
    bad=np.flatnonzero((ks[1:]==ks[:-1]) & (vs[1:]!=vs[:-1]))
    out={'passes':not len(bad),'forced_keys':int(1+np.count_nonzero(ks[1:]!=ks[:-1]))}
    if len(bad):
        j=int(bad[0]); out['conflict']={'key':int(ks[j]),'event_indices':[int(order[j]),int(order[j+1])],'bits':[int(vs[j]),int(vs[j+1])]}
    else:
        unique=np.r_[True,ks[1:]!=ks[:-1]]
        out['table_sha256']=hashlib.sha256(ks[unique].tobytes()+vs[unique].tobytes()).hexdigest()
    return out

def data(rule,choice,radius):
    width=2*radius+5
    s=((np.arange(1<<width)[:,None] >> np.arange(width-1,-1,-1)) & 1).astype(np.uint8)
    mid=width//2; ds=d(s,rule); es=s^ds
    a=encode(s,rule,choice); b=encode(es,rule,choice); c=encode(es^d(es,rule),rule,choice)
    g=d(es,rule)^ds^d(ds,rule)
    carrier=np.stack([g[:,mid]^g[:,mid+choice['shift']],g[:,mid]],axis=1)
    return patches(a,radius),(a^b)[...,mid],patches(a^b,radius)[:,:2],a[:,:2,mid]^c[:,:2,mid]^carrier

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--radii',type=int,nargs='+',default=[3,4]); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--resume',type=Path); args=ap.parse_args()
    assert max(args.radii)<=10
    args.output.mkdir(exist_ok=False,parents=True); start=time.perf_counter()
    prior=ROOT/'runs/probe_radius_2'
    records=[r for r in map(json.loads,(prior/'candidates.jsonl').read_text().splitlines()) if r['horizontal_radius']==2]
    glob={r['candidate']:r for r in map(json.loads,(prior/'global_obstructions.jsonl').read_text().splitlines())}
    states={}
    for rec in records:
        cid=rec['candidate']; p=rec['probes']['temporal']; g=glob[cid]['probes']['temporal']
        states[cid]={}
        for name,local,whole in [('raw',p['raw'],g['raw']),*[(str(z),p['centered_branches'][z],g['centered_branches'][z]) for z in (0,1)]]:
            states[cid][name]={'status':'exists' if local['passes'] else 'impossible' if whole['obstructed'] else 'unresolved','radius':2 if local['passes'] else None}
    summaries={}; tested=[]
    if args.resume:
        states={int(k):v for k,v in json.loads((args.resume/'candidate_status.json').read_text()).items()}
        summaries=json.loads((args.resume/'summary.json').read_text())
    with (args.output/'decisions.jsonl').open('w') as log:
        if args.resume: log.write((args.resume/'decisions.jsonl').read_text())
        for radius in args.radii:
            cases=0
            for rec in records:
                cid=rec['candidate']; names=[n for n,v in states[cid].items() if v['status']=='unresolved']
                if not names: continue
                bk,bv,pk,pv=data(rec['rule'],rec['recipe'][0],radius)
                result={'candidate':cid,'rule':rec['rule'],'recipe':rec['recipe'],'radius':radius,'source_width':2*radius+5,'branches':{}}
                for name in names:
                    wanted=pv.copy(); z=None if name=='raw' else int(name)
                    if z is not None: wanted[:,1]^=rec['rule']&1
                    v=check(bk,bv,pk,wanted,z); result['branches'][name]=v; cases+=1
                    if v['passes']: states[cid][name]={'status':'exists','radius':radius}
                tested.append(result); log.write(json.dumps(result)+'\n')
            log.flush(); stage={}
            for mode,names in [('raw',['raw']),('centered',['0','1'])]:
                groups={k:[] for k in ('exists','impossible','unresolved')}
                for rule in sorted({r['rule'] for r in records}):
                    vals=[states[r['candidate']][n]['status'] for r in records if r['rule']==rule for n in names]
                    status='exists' if 'exists' in vals else 'impossible' if all(v=='impossible' for v in vals) else 'unresolved'
                    groups[status].append(rule)
                stage[mode]=groups
            summaries[str(radius)]=stage
            print(json.dumps({'radius':radius,'new_branch_tests':cases,'seconds':round(time.perf_counter()-start,3),'counts':{m:{k:len(v) for k,v in s.items()} for m,s in stage.items()},'rule110':{m:next(k for k,v in s.items() if 110 in v) for m,s in stage.items()}}),flush=True)
    (args.output/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
    (args.output/'candidate_status.json').write_text(json.dumps(states,indent=2)+'\n')
    (args.output/'manifest.json').write_text(json.dumps({'elapsed_seconds':time.perf_counter()-start,'radii':args.radii,'admitted_rules':192,'admitted_variants':596,'source_words_exhaustive':True,'source_width':'2*radius+5','baseline':'probe_radius_2','resume':str(args.resume) if args.resume else None,'only_unresolved_branches_enumerated':True,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
    (args.output/'source_audit.py').write_text(Path(__file__).read_text())

if __name__=='__main__': main()
