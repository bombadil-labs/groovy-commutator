"""Fixed 4-row binary recipe to 3D; exact first-order gates and joint G extension.
Parent unknown flip outputs are solved as GF(2) variables, not zero-filled.
One deterministic previous successful recipe per source rule; no rescue search.
"""
import argparse,hashlib,json,time
from pathlib import Path
import numpy as np
from verify_polarization_proposal import d,encode
from audit_reference_covariance import reference
from audit_binary_reference import keys as parent_keys

ROOT=Path(__file__).resolve().parent

def selected():
    rows=[r for r in map(json.loads,(ROOT/'runs/binary_reference_4rows/candidates.jsonl').read_text().splitlines()) if r['ry']==2 and r['joint_centered'] or r['ry']==2 and r['joint_raw']]
    chosen=[]
    for rule in sorted({r['rule'] for r in rows}):
        rs=[r for r in rows if r['rule']==rule]
        chosen.append(min(rs,key=lambda r:(not r['joint_raw'],r['order']!=[0,1,2,3],r['reference']!='pair:-1:2',r['recipe'][0]['shift']!=1,r['candidate'],r['order'])))
    return chosen

def shift(x,dx,dy):return np.roll(x,(-dy,-dx),axis=(-2,-1))

def lift(a,b,rec):
    sign=rec['recipe'][0]['shift'];left,right=map(int,rec['reference'].split(':')[1:]);delta=a^b
    p=a^shift(a,sign,1);mname=rec['recipe'][0]['mask']
    if mname=='birth':m=(1-a)&delta
    elif mname=='death':m=a&delta
    elif mname=='stay_one':m=a&(1-delta)
    else:m=(1-a)&(1-delta)
    q=shift(a,left,left*sign)&shift(a,right,right*sign)
    return np.stack([p,delta,m,q],axis=1)[:,rec['order']]

def child_keys(grid,mid):
    # Radius2 sees all four positions on each period4 transverse axis;
    # omitted -2 repeats +2 exactly, so this canonical key has 80 bits.
    chunks=[]
    for z in (0,1,2,-1):
        for y in (0,1,2,-1):
            block=np.roll(grid,(-z,-y),axis=(1,2))[...,mid-2:mid+3]
            chunks.append(block)
    bits=np.concatenate(chunks,axis=-1)
    packed=np.packbits(bits,axis=-1,bitorder='big').reshape(-1,10)
    return np.ascontiguousarray(packed).view('V10').ravel()

def groups(keys,targets):
    unique,first,inverse=np.unique(keys,return_index=True,return_inverse=True)
    out={};values={}
    for name,t in targets.items():
        masks=np.zeros(len(unique),dtype=np.uint8);np.bitwise_or.at(masks,inverse,(1<<t.ravel()).astype(np.uint8));bad=np.flatnonzero(masks==3)
        values[name]=masks
        witness=None
        if len(bad):
            group=int(bad[0]);events=[int(np.flatnonzero((inverse==group)&(t.ravel()==bit))[0]) for bit in (0,1)]
            witness={'key_hex':bytes(unique[group]).hex(),'events':events,'outputs':[0,1]}
        out[name]={'passes':not len(bad),'conflicts':len(bad),'witness':witness}
    return unique,first,inverse,values,out

def pkeys(grid,mid):
    # Parent helper assumes centered horizontal source; roll chosen origin.
    return parent_keys(np.roll(grid,grid.shape[-1]//2-mid,axis=-1),2,2)

def build(rec):
    left,right=map(int,rec['reference'].split(':')[1:]);lo=min(-1,left);hi=max(1,right)
    origin=-(2*lo-3);width=2*(hi-lo)+7
    s=((np.arange(1<<width)[:,None]>>np.arange(width-1,-1,-1))&1).astype(np.uint8)
    rule=rec['rule'];states=[s]
    for _ in range(3):states.append(states[-1]^d(states[-1],rule))
    parents=[]
    for st in states:
        a=encode(st,rule,rec['recipe'][0]);q=reference(st,rule,rec['recipe'][0],rec['reference'])
        parents.append(np.concatenate([a,q[:,None,:]],axis=1)[:,rec['order']])
    kids=[lift(parents[t],parents[t+1],rec) for t in range(3)]
    return s,states,parents,kids,origin

def solve_g(rec,s,states,pa,kids,mid,beamkeys,beamunique,beamvalues,parent_zero_override=None):
    rule=rec['rule'];order=rec['order'];sign=rec['recipe'][0]['shift'];phases=[order.index(0),order.index(1)]
    mode='raw' if rec['joint_raw'] else 'centered'
    parent_zero=None if mode=='raw' else next(z for z,v in enumerate(rec['centered_branches']) if v['passes'])
    if parent_zero_override is not None:
        assert mode=='centered' and rec['centered_branches'][parent_zero_override]['passes']
        parent_zero=parent_zero_override
    a,b,c=pa[:3];dt=a^b
    ds=d(s,rule);g=d(states[1],rule)^ds^d(ds,rule)
    pg=np.stack([g[:,mid]^g[:,mid+sign],g[:,mid]],axis=1)
    bv=dt[...,mid];wanted=a[:,phases,mid]^c[:,phases,mid]^pg
    if mode=='centered':wanted[:,1]^=rule&1;wanted^=parent_zero
    pk=pkeys(dt,mid);bk=pkeys(a,mid)
    forced={} if parent_zero is None else {0:parent_zero}
    for ks,vs in [(bk,bv),(pk[:,phases],wanted)]:
        for key,value in zip(ks.ravel().tolist(),vs.ravel().tolist()):
            assert key not in forced or forced[key]==value
            forced[key]=value
    # Parent G expressions at i and i+sign need h_parent(delta a) there.
    shiftedpk=pkeys(dt,mid+sign)
    variable_keys=sorted(set(pk.ravel().tolist()+shiftedpk.ravel().tolist())-forced.keys())
    var_index={key:i+1 for i,key in enumerate(variable_keys)}
    def expressions(ks,const):
        result=[]
        for key,bit in zip(ks.ravel().tolist(),const.ravel().tolist()):
            if key in forced:result.append(int(bit)^forced[key])
            else:result.append((1<<var_index[key])|int(bit))
        return np.array(result,dtype=object).reshape(ks.shape)
    expr=expressions(pk,a[...,mid]^c[...,mid])
    exprshift=expressions(shiftedpk,a[...,mid+sign]^c[...,mid+sign])
    if mode=='centered':expr^=parent_zero;exprshift^=parent_zero
    # Shift across the newest old axis as well as horizontally.
    pexpr=expr^np.roll(exprshift,-1,axis=1)
    targets=np.stack([pexpr,expr],axis=1)
    targets ^= (kids[0][...,mid][:,phases,:]^kids[2][...,mid][:,phases,:]).astype(object)
    uk=child_keys(kids[0]^kids[1],mid).reshape(len(s),4,4)[:,phases].ravel()
    unique,first,inv=np.unique(uk,return_index=True,return_inverse=True)
    expressions_flat=targets.ravel();group_expr=expressions_flat[first]
    equations=[int(x) for x in (expressions_flat^group_expr[inv]) if x]
    # First-order forced child outputs at matching keys must agree.
    pos=np.searchsorted(beamunique,unique);hit=pos<len(beamunique);hit[hit]&=beamunique[pos[hit]]==unique[hit]
    constants=(beamvalues['native'][pos[hit]]==2).astype(np.uint8)
    cross=[int(x)^int(v) for x,v in zip(group_expr[hit],constants)]
    zero=np.zeros(1,dtype='V10')[0]
    child_zero_forced=None
    zero_index=np.searchsorted(beamunique,zero)
    if zero_index<len(beamunique) and beamunique[zero_index]==zero:child_zero_forced=int(beamvalues['native'][zero_index]==2)
    results=[]
    for childzero in ([None] if mode=='raw' else [0,1]):
        eqs=equations.copy();eqs.extend(x^(childzero or 0) for x in cross)
        if childzero is not None:
            if child_zero_forced is not None:eqs.append(childzero^child_zero_forced)
            zi=np.searchsorted(unique,zero)
            if zi<len(unique) and unique[zi]==zero:eqs.append(int(group_expr[zi]))
        basis={};conflict=False
        for equation in eqs:
            x=equation
            while x>1:
                pivot=x.bit_length()-1
                if pivot in basis:x^=basis[pivot]
                else:basis[pivot]=x;break
            if x==1:conflict=True;break
        solution={}
        if not conflict:
            assignment=0
            for pivot,row in sorted(basis.items()):
                if (row&assignment).bit_count()%2 ^ (row&1):assignment|=1<<pivot
            assert all(((eq&assignment).bit_count()%2)==(eq&1) for eq in eqs)
            solution={str(k):(assignment>>v)&1 for k,v in var_index.items()}
        results.append({'child_zero':childzero,'passes':not conflict,'equations':len(eqs),'rank':len(basis),'parent_free_assignment':solution if not conflict else None})
    return {'mode':mode,'parent_zero':parent_zero,'parent_forced_outputs':len(forced),'parent_probe_free_variables':len(variable_keys),'branches':results,'passes':any(r['passes'] for r in results)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter();picks=selected();rows=[]
    with (args.output/'candidates.jsonl').open('w') as log:
        for i,rec in enumerate(picks):
            s,states,pa,kids,mid=build(rec)
            bk=child_keys(kids[0],mid)
            targets={'native':(kids[0]^kids[1])[...,mid],'source':np.broadcast_to(s[:,mid,None,None],(len(s),4,4)),'parent':np.broadcast_to(pa[0][:,None,:,mid],(len(s),4,4))}
            unique,first,inv,values,gates=groups(bk,targets)
            good=all(v['passes'] for v in gates.values())
            out={'rule':rec['rule'],'first_floor':rec,'source_width':s.shape[-1],'source_origin_index':mid,'gates':gates,'first_order_pass':good}
            if good:out['recursive_G']=solve_g(rec,s,states,pa,kids,mid,bk,unique,values)
            else:out['recursive_G']={'passes':False,'not_tested_due_to_first_order_failure':True}
            rows.append(out);log.write(json.dumps(out,separators=(',',':'))+'\n');log.flush()
            if (i+1)%16==0 or rec['rule']==110:print(json.dumps({'completed':i+1,'last_rule':rec['rule'],'seconds':round(time.perf_counter()-start,2),'first_order':sum(r['first_order_pass'] for r in rows),'G':sum(r['recursive_G']['passes'] for r in rows),'last_gates':{k:v['passes'] for k,v in gates.items()},'last_G':out['recursive_G']['passes']}),flush=True)
    summary={'first_order_rules':[r['rule'] for r in rows if r['first_order_pass']],'recursive_G_rules':[r['rule'] for r in rows if r['recursive_G']['passes']],'raw_recursive_G_rules':[r['rule'] for r in rows if r['recursive_G'].get('mode')=='raw' and r['recursive_G']['passes']],'centered_recursive_G_rules':[r['rule'] for r in rows if r['recursive_G'].get('mode')=='centered' and r['recursive_G']['passes']]}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (args.output/'manifest.json').write_text(json.dumps({'seconds':time.perf_counter()-start,'selected_rules':len(picks),'native_radius':[2,2,2],'periods':[4,4],'native_binary':True,'first_floor_selection':'prefer raw, PDMQ, Q(-1,+2), positive horizontal P, then candidate/order','next_recipe':'repeat same mask/order/Q coefficients; spatial vector crosses newest old transverse axis +1','parent_completion':'solve free probe values jointly over GF2','source_width':13,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
    (args.output/'source_audit.py').write_text(Path(__file__).read_text())
    print(json.dumps({'seconds':time.perf_counter()-start,**{k:len(v) for k,v in summary.items()}}),flush=True)
if __name__=='__main__':main()
