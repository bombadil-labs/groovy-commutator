"""One reflection-aligned, first-floor-only selection per ECA into 3D.
Generalizes the audited recursion's Q formula; reuses identical prior paths.
No recipe rescue or higher floor. All unknown parent outputs remain symbolic.
"""
import copy, hashlib, json, time
from pathlib import Path
import numpy as np
import audit_recursive_binary as core
from verify_polarization_proposal import d, encode

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/universal_3d'

def mirror(r):
    return sum(((r>>(((i&1)<<2)|(i&2)|((i>>2)&1)))&1)<<i for i in range(8))

def tag(r):
    c=r['recipe'][0]
    return (r['rule'],c['mask'],c['shift'],r['reference'],tuple(r['order']))

def reflected_tag(r):
    rule,mask,sign,ref,order=tag(r);p=ref.split(':');a,b=map(int,p[1:3])
    q=f'pair:{-b}:{-a}' if p[0]=='pair' else f"directed:{-b}:{-a}:"+('not-left-and-right' if p[3]=='left-and-not-right' else 'left-and-not-right')
    return (mirror(rule),mask,-sign,q,order)

def selected():
    rows=[]
    for name in ('binary_fresh_all256','directed_full256'):
        rows.extend(r for r in map(json.loads,(ROOT/f'runs/{name}/candidates.jsonl').read_text().splitlines()) if r['first_order_pass'])
    bytag={tag(r):r for r in rows};picks={}
    for rule in range(256):
        if rule in picks:continue
        rec=min((r for r in rows if r['rule']==rule),key=lambda r:(not r['joint_raw'],not r['joint_centered'],r['order']!=[0,1,2,3],r['reference'].startswith('directed'),r['reference'] not in ('pair:-1:2','directed:-1:2:not-left-and-right'),r['recipe'][0]['shift']!=1,('birth','death','stay_one','stay_zero').index(r['recipe'][0]['mask']),r['order']))
        picks[rule]=rec
        partner=mirror(rule)
        reflected=bytag[reflected_tag(rec)]
        assert all(rec[k]==reflected[k] for k in ('joint_raw','joint_centered','first_order_pass'))
        if partner!=rule:picks[partner]=reflected
    assert len(picks)==256
    assert sum(r['joint_raw'] for r in picks.values())==133
    assert sum(r['joint_raw'] or r['joint_centered'] for r in picks.values())==220
    return [picks[r] for r in range(256)]

def bounds(rec):return tuple(map(int,rec['reference'].split(':')[1:3]))

def product(x,y,rec):
    ref=rec['reference']
    if ref.startswith('pair:'):return x&y
    return (1-x)&y if ref.endswith(':not-left-and-right') else x&(1-y)

def lift(a,b,rec):
    sign=rec['recipe'][0]['shift'];left,right=bounds(rec);delta=a^b
    p=a^core.shift(a,sign,1);name=rec['recipe'][0]['mask']
    m=(1-a)&delta if name=='birth' else a&delta if name=='death' else a&(1-delta) if name=='stay_one' else (1-a)&(1-delta)
    q=product(core.shift(a,left,left*sign),core.shift(a,right,right*sign),rec)
    return np.stack([p,delta,m,q],axis=1)[:,rec['order']]

def build(rec):
    left,right=bounds(rec);lo=min(-1,left);hi=max(1,right)
    origin=-(2*lo-3);width=2*(hi-lo)+7
    s=((np.arange(1<<width)[:,None]>>np.arange(width-1,-1,-1))&1).astype(np.uint8)
    states=[s]
    for _ in range(3):states.append(states[-1]^d(states[-1],rec['rule']))
    parents=[]
    for st in states:
        q=product(np.roll(st,-left,axis=-1),np.roll(st,-right,axis=-1),rec)
        parents.append(np.concatenate([encode(st,rec['rule'],rec['recipe'][0]),q[:,None,:]],axis=1)[:,rec['order']])
    return s,states,parents,[lift(parents[t],parents[t+1],rec) for t in range(3)],origin

def cached():
    result={}
    for name in ('recursive_binary_3d_v2','recursive_binary_reflections','recursive_binary_centering_alternatives'):
        for row in map(json.loads,(ROOT/f'runs/{name}/candidates.jsonl').read_text().splitlines()):
            result.setdefault(tag(row['first_floor']),[]).append((name,row))
    return result

def main():
    start=time.monotonic();OUT.mkdir(exist_ok=False,parents=True)
    picks=selected();cache=cached();rows=[];reused=0;new=0
    (OUT/'selected.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in picks))
    with (OUT/'candidates.jsonl').open('w') as log:
        for rec in picks:
            prior=cache.get(tag(rec),[]);mode='raw' if rec['joint_raw'] else 'centered' if rec['joint_centered'] else None
            attempts=[copy.deepcopy(r['recursive_G']) for _,r in prior if r['first_order_pass'] and r['recursive_G'].get('mode')==mode]
            reuse=bool(prior) and (not prior[0][1]['first_order_pass'] or mode is None or any(g['passes'] for g in attempts) or (mode=='raw' and attempts) or (mode=='centered' and {g['parent_zero'] for g in attempts}=={z for z,v in enumerate(rec['centered_branches']) if v['passes']}))
            if reuse:
                out=copy.deepcopy(prior[0][1]);out['first_floor']=rec;out['cache_sources']=[n for n,_ in prior];reused+=1
            else:
                s,states,pa,kids,mid=build(rec);bk=core.child_keys(kids[0],mid)
                targets={'native':(kids[0]^kids[1])[...,mid],'source':np.broadcast_to(s[:,mid,None,None],(len(s),4,4)),'parent':np.broadcast_to(pa[0][:,None,:,mid],(len(s),4,4))}
                unique,_,_,values,gates=core.groups(bk,targets)
                out={'rule':rec['rule'],'first_floor':rec,'source_width':s.shape[-1],'source_origin_index':mid,'gates':gates,'first_order_pass':all(v['passes'] for v in gates.values()),'cache_sources':[]};new+=1
                if out['first_order_pass'] and mode is not None:
                    zeros=[None] if mode=='raw' else [z for z,v in enumerate(rec['centered_branches']) if v['passes']]
                    for z in zeros:
                        if any(g['parent_zero']==z for g in attempts):continue
                        attempts.append(core.solve_g(rec,s,states,pa,kids,mid,bk,unique,values,parent_zero_override=z))
                        if attempts[-1]['passes']:break
            out['G_eligible']=mode is not None
            out['recursive_G_attempts']=attempts
            if not out['first_order_pass']:out['recursive_G']={'passes':False,'status':'first_order_failure','mode':mode}
            elif mode is None:out['recursive_G']={'passes':False,'status':'missing_first_floor_carrier','mode':None}
            else:out['recursive_G']=next((g for g in attempts if g['passes']),attempts[0])
            out['reflection_orbit_representative']=min(rec['rule'],mirror(rec['rule']))
            out['self_reflection_orientation_convention']=rec['rule']==mirror(rec['rule'])
            rows.append(out);log.write(json.dumps(out,separators=(',',':'))+'\n');log.flush()
            if len(rows)%32==0:print(json.dumps({'completed':len(rows),'seconds':round(time.monotonic()-start,2),'reused':reused,'faithful':sum(r['first_order_pass'] for r in rows),'G':sum(r['recursive_G']['passes'] for r in rows)}),flush=True)
            if time.monotonic()-start>112:break
    summary={'status':'complete' if len(rows)==256 else 'checkpointed','rules':len(rows),'reused':reused,'new':new,'seconds':time.monotonic()-start}
    for name in ('native','source','parent'):summary[name+'_rules']=[r['rule'] for r in rows if r['gates'][name]['passes']]
    summary['faithful_rules']=[r['rule'] for r in rows if r['first_order_pass']]
    summary['G_eligible_rules']=[r['rule'] for r in rows if r['G_eligible']]
    for mode in ('raw','centered'):summary[mode+'_G_rules']=[r['rule'] for r in rows if r['recursive_G'].get('mode')==mode and r['recursive_G']['passes']]
    summary['recursive_G_rules']=sorted(summary['raw_G_rules']+summary['centered_G_rules'])
    summary['missing_first_floor_G']=[r['rule'] for r in rows if not r['G_eligible']]
    summary['eligible_first_order_failures']=[r['rule'] for r in rows if r['G_eligible'] and not r['first_order_pass']]
    summary['recursive_G_constraint_failures']=[r['rule'] for r in rows if r['G_eligible'] and r['first_order_pass'] and not r['recursive_G']['passes']]
    if len(rows)==256:
        for k in ('native_rules','source_rules','parent_rules','faithful_rules','recursive_G_rules'):assert {mirror(r) for r in summary[k]}==set(summary[k]),k
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    manifest={'selection':'First-floor only: original G, centered G, canonical order, symmetric Q, right Q placement, positive P, birth/death/stay-one/stay-zero, order; select min rule in each reflection orbit and reflect partner exactly. Self-mirror rules use an orientation convention; no invariant signed recipe is claimed.','diagnostic':'Original mode when first-floor raw passes, else centered. Exhaust every admissible parent zero before counting a centered failure.','native_radius':[2,2,2],'alphabet_bits':1,'periods':[4,4],'independent_information':'source line only','prepared_fields':16,'source_width':13,'native_neighborhood_bits':125,'distinct_prepared_neighborhood_bits':80,'G_scope':'nested P/D only','parent_outputs':'symbolic, unconstrained outside finite native/probe keys','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in summary.items()}),flush=True)

if __name__=='__main__':main()
