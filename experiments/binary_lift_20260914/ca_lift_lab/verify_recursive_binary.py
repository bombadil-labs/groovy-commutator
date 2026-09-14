"""Independent interval-cropped construction and low-pivot GF2 verifier.
Uses full 125-bit physical child neighborhoods; primary uses 80-bit keys.
"""
import argparse,json,time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent

def align(fields):
    lo=max(f[0] for f in fields);hi=min(f[0]+f[1].shape[-1] for f in fields)
    return lo,[a[...,lo-start:hi-start] for start,a in fields]
def combine(f,g,op=np.bitwise_xor):
    lo,(a,b)=align([f,g]);return lo,op(a,b)
def shifted(f,dx,dy=0):return f[0]-dx,np.roll(f[1],-dy,axis=-2) if dy else f[1]
def negate(f):return f[0],1-f[1]
def stack(fields,order):
    lo,arrays=align(fields);return lo,np.stack([arrays[k] for k in order],axis=1)
def source_step(f,rule):
    start,a=f;idx=4*a[...,:-2]+2*a[...,1:-1]+a[...,2:];der=(((rule^204)>>idx)&1).astype(np.uint8)
    return start+1,a[...,1:-1]^der

def mask(a,delta,name):
    if name=='birth':return combine(negate(a),delta,np.bitwise_and)
    if name=='death':return combine(a,delta,np.bitwise_and)
    if name=='stay_one':return combine(a,negate(delta),np.bitwise_and)
    return combine(negate(a),negate(delta),np.bitwise_and)

def encode(a,b,rec,parent=False):
    sign=rec['recipe'][0]['shift'];left,right=map(int,rec['reference'].split(':')[1:])
    delta=combine(a,b)
    p=combine(a,shifted(a,sign,1 if parent else 0))
    q=combine(shifted(a,left,left*sign if parent else 0),shifted(a,right,right*sign if parent else 0),np.bitwise_and)
    return stack([p,delta,mask(a,delta,rec['recipe'][0]['mask']),q],rec['order'])

def value(f,i):return f[1][...,i-f[0]]
def pkeys(f,i):
    start,grid=f;mid=i-start;result=np.zeros(grid.shape[:2],dtype=np.uint32)
    for dy in [0,1,2,-1,-2]:
        for dx in [-2,-1,0,1,2]:result=2*result+np.roll(grid,-dy,axis=1)[...,mid+dx]
    return result

def ckeys(f,i):
    start,grid=f;mid=i-start;blocks=[]
    for dz in [-2,-1,0,1,2]:
        for dy in [-2,-1,0,1,2]:blocks.append(np.roll(grid,(-dz,-dy),axis=(1,2))[...,mid-2:mid+3])
    bits=np.concatenate(blocks,axis=-1);packed=np.packbits(bits,axis=-1,bitorder='big').reshape(-1,16)
    return np.ascontiguousarray(packed).view('V16').ravel()

def solve(equations):
    basis={}
    for row in equations:
        x=int(row)
        while x&~1:
            p=(x&~1)&-(x&~1)
            if p in basis:x^=basis[p]
            else:basis[p]=x;break
        if x==1:return False,len(basis)
    return True,len(basis)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);args=ap.parse_args();start=time.perf_counter()
    rows=list(map(json.loads,(args.run/'candidates.jsonl').read_text().splitlines()));checks=0;branchchecks=0;witnesses=[];direct=0
    for num,record in enumerate(rows):
        rec=record['first_floor'];rule=rec['rule'];width=record['source_width'];mid=record['source_origin_index'];order=rec['order'];phases=[order.index(0),order.index(1)];sign=rec['recipe'][0]['shift']
        source=((np.arange(1<<width)[:,None]>>np.arange(width-1,-1,-1))&1).astype(np.uint8)
        src=[(0,source)]
        for _ in range(4):src.append(source_step(src[-1],rule))
        parents=[encode(src[t],src[t+1],rec) for t in range(4)]
        kids=[encode(parents[t],parents[t+1],rec,True) for t in range(3)]
        delta=combine(kids[0],kids[1]);bk=ckeys(kids[0],mid);bv=value(delta,mid).ravel()
        sort=np.argsort(bk);same=bk[sort][1:]==bk[sort][:-1]
        outputs={'native':bv,'source':np.broadcast_to(source[:,mid,None,None],(len(source),4,4)).ravel(),'parent':np.broadcast_to(value(parents[0],mid)[:,None,:],(len(source),4,4)).ravel()}
        for name,vals in outputs.items():
            ordered=vals[sort];good=not np.any(same&(ordered[1:]!=ordered[:-1]));assert good==record['gates'][name]['passes'],(rule,name);checks+=1
        if not record['first_order_pass']:continue
        # Build independent first-floor forced outputs.
        pd=combine(parents[0],parents[1]);pk=pkeys(pd,mid);pbk=pkeys(parents[0],mid)
        # G_r from derivative-first cropped source calculus.
        ds=combine(src[0],src[1]);dnext=combine(src[1],src[2]);eds=source_step(ds,rule)
        gs=combine(dnext,eds)
        cg=np.stack([value(gs,mid)^value(gs,mid+sign),value(gs,mid)],axis=1)
        wanted=value(parents[0],mid)[:,phases]^value(parents[2],mid)[:,phases]^cg
        mode=record['recursive_G']['mode'];zparent=record['recursive_G']['parent_zero']
        if mode=='centered':wanted[:,1]^=rule&1;wanted^=zparent
        forced={} if zparent is None else {0:zparent}
        for keys,bits in [(pbk,value(pd,mid)),(pk[:,phases],wanted)]:
            for key,bit in zip(keys.ravel().tolist(),bits.ravel().tolist()):
                assert key not in forced or forced[key]==bit;forced[key]=bit
        pks=pkeys(pd,mid+sign);free=sorted(set(pk.ravel().tolist()+pks.ravel().tolist())-forced.keys());ids={k:i+1 for i,k in enumerate(free)}
        def expr(keys,constant):
            return np.array([int(c)^forced[k] if k in forced else (1<<ids[k])|int(c) for k,c in zip(keys.ravel().tolist(),constant.ravel().tolist())],dtype=object).reshape(keys.shape)
        ep=expr(pk,value(parents[0],mid)^value(parents[2],mid));eps=expr(pks,value(parents[0],mid+sign)^value(parents[2],mid+sign))
        if mode=='centered':ep^=zparent;eps^=zparent
        target=np.stack([ep^np.roll(eps,-1,axis=1),ep],axis=1)
        target^=(value(kids[0],mid)[:,phases,:]^value(kids[2],mid)[:,phases,:]).astype(object)
        uk=ckeys(delta,mid).reshape(len(source),4,4)[:,phases].ravel();target=target.ravel()
        base={bytes(k):int(v) for k,v in zip(bk,bv)}
        for branch in record['recursive_G']['branches']:
            zchild=branch['child_zero'];seen=base.copy();equations=[];conflict_witness=None
            events={} if rule!=110 else {bytes(k):{'kind':'beam','event':int(j),'expression':int(bv[j])}for j,k in enumerate(bk)}
            if zchild is not None:
                if bytes(16) in seen:equations.append(seen[bytes(16)]^zchild)
                else:seen[bytes(16)]=zchild
            for j,(key,e) in enumerate(zip(uk,target)):
                key=bytes(key);e=int(e)^(zchild or 0)
                if key in seen:
                    equation=seen[key]^e
                    if equation:equations.append(equation)
                    if rule==110 and equation==1 and conflict_witness is None:
                        conflict_witness={'rule':rule,'patch_hex_125_bits':key.hex(),'existing':events.get(key),'new':{'kind':'probe','event':j,'expression':e},'source_width':width,'origin_index':mid,'field_order':order,'source_event_decoding':'beam: divmod(event,16) gives word then new_phase*4+old_phase; probe: divmod(event,8) gives word then P/D index*4+old_phase','expression_encoding':'bit0=constant; bit i+1=parent free variable sorted by key','free_keys':free}
                else:
                    seen[key]=e
                    if rule==110:events[key]={'kind':'probe','event':j,'expression':e}
            good,rank=solve(equations);assert good==branch['passes'],(rule,zchild);branchchecks+=1
            if conflict_witness:witnesses.append(conflict_witness)
            if good:
                assignment=branch['parent_free_assignment'];assert set(map(int,assignment))==set(free)
                bits=sum(int(assignment[str(k)])<<ids[k] for k in free)
                assert all((int(eq)&bits).bit_count()%2==(int(eq)&1) for eq in equations)
                # Concrete child table from the satisfying parent assignment.
                concrete={k:(e&1)^((e&bits).bit_count()%2) for k,e in seen.items()}
                future=ckeys(kids[1],mid);flip=np.array([concrete[bytes(k)] for k in future],dtype=np.uint8).reshape(len(source),4,4)
                assert np.array_equal(flip,value(kids[1],mid)^value(kids[2],mid))
                hu=np.array([concrete[bytes(k)] for k in uk],dtype=np.uint8).reshape(len(source),2,4)
                actual=flip[:,phases,:]^value(delta,mid)[:,phases,:]^hu
                if zchild is not None:actual^=zchild
                carrier=np.stack([ep^np.roll(eps,-1,axis=1),ep],axis=1)
                expected=np.array([(int(e)&1)^((int(e)&bits).bit_count()%2) for e in carrier.ravel()],dtype=np.uint8).reshape(carrier.shape)
                assert np.array_equal(actual,expected);direct+=actual.size
        if (num+1)%16==0:print(json.dumps({'verified':num+1,'seconds':round(time.perf_counter()-start,2)}),flush=True)
    result={'status':'passed','rules':len(rows),'independent_first_order_gate_decisions':checks,'independent_GF2_branch_decisions':branchchecks,'direct_recursive_G_cells':direct,'seconds':time.perf_counter()-start}
    (args.run/'verification.json').write_text(json.dumps(result,indent=2)+'\n');(args.run/'rule110_witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
