"""Targeted independent cropped/full125bit verification of the new 3D census.
Reuses the independent solver, with a separately implemented directed Q encoder.
Checks every directed path, every new failure, and each successful geometry/mode.
"""
import json,sys,time
from pathlib import Path
import numpy as np
import verify_recursive_binary as v

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'runs/universal_3d'

def encode(a,b,rec,parent=False):
    sign=rec['recipe'][0]['shift'];p=rec['reference'].split(':');left,right=map(int,p[1:3])
    delta=v.combine(a,b)
    polar=v.combine(a,v.shifted(a,sign,1 if parent else 0))
    x=v.shifted(a,left,left*sign if parent else 0)
    y=v.shifted(a,right,right*sign if parent else 0)
    if p[0]=='directed':
        if p[3]=='left-and-not-right':y=v.negate(y)
        else:x=v.negate(x)
    q=v.combine(x,y,np.bitwise_and)
    return v.stack([polar,delta,v.mask(a,delta,rec['recipe'][0]['mask']),q],rec['order'])

def native_only(record):
    rec=record['first_floor'];width=record['source_width'];mid=record['source_origin_index']
    source=((np.arange(1<<width)[:,None]>>np.arange(width-1,-1,-1))&1).astype(np.uint8)
    src=[(0,source)]
    for _ in range(3):src.append(v.source_step(src[-1],rec['rule']))
    pa=[encode(src[t],src[t+1],rec) for t in range(3)]
    kids=[encode(pa[t],pa[t+1],rec,True) for t in range(2)]
    keys=v.ckeys(kids[0],mid);sort=np.argsort(keys);same=keys[sort][1:]==keys[sort][:-1]
    outputs={'native':v.value(v.combine(kids[0],kids[1]),mid).ravel(),'source':np.broadcast_to(source[:,mid,None,None],(len(source),4,4)).ravel(),'parent':np.broadcast_to(v.value(pa[0],mid)[:,None,:],(len(source),4,4)).ravel()}
    for name,bits in outputs.items():
        values=bits[sort];assert (not np.any(same&(values[1:]!=values[:-1])))==record['gates'][name]['passes'],(rec['rule'],name)
    return 3

def main():
    start=time.monotonic();rows=list(map(json.loads,(RUN/'candidates.jsonl').read_text().splitlines()))
    chosen={};patterns=set()
    for r in rows:
        rec=r['first_floor'];c=rec['recipe'][0]
        pattern=(rec['reference'],c['mask'],c['shift'],tuple(rec['order']),r['recursive_G'].get('mode'))
        constrains_parent=any(b['passes'] and b['rank'] for a in r['recursive_G_attempts'] for b in a['branches'])
        if constrains_parent or rec['reference'].startswith('directed') or (not r['recursive_G']['passes'] and r['G_eligible'] and not r['cache_sources']) or (r['recursive_G']['passes'] and not r['cache_sources'] and pattern not in patterns):chosen[r['rule']]=r
        patterns.add(pattern)
    # No-carrier rules need only recovery/native verification, not an invented G.
    nong=[r for r in rows if not r['G_eligible']]
    nativechecks=sum(native_only(r) for r in nong)
    eligible=[]
    for r in chosen.values():
        if not r['G_eligible']:continue
        for attempt in r['recursive_G_attempts']:
            eligible.append(dict(r,recursive_G=attempt))
    dest=RUN/'targeted_verification';dest.mkdir(exist_ok=False)
    (dest/'candidates.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in eligible))
    v.encode=encode;sys.argv=['verify_recursive_binary','--run',str(dest)];v.main()
    result=json.loads((dest/'verification.json').read_text())
    result.update({'independent_eligible_rules':len({r['rule'] for r in eligible}),'all_directed_selected_rules':sum(r['first_floor']['reference'].startswith('directed') for r in rows),'no_carrier_rules_checked':len(nong),'additional_native_recovery_decisions':nativechecks,'seconds_total':time.monotonic()-start,'scope':'Every directed path, all newly computed G failures, each new successful geometry/mode, all36no-carrier native/source/parent checks.53exact-cache paths retain earlier audits.'})
    (RUN/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':main()
