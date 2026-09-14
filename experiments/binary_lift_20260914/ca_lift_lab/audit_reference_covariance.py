"""Two-channel first-floor lift Z(S)=(L(S), broadcast Q(S)).
Native K has two output bits, no phase labels. Its physical derivative input
is delta Z=(L(S)^L(ES), Q(S)^Q(ES)), never (delta L,Q(S)).
Constrain both first-order outputs, and P/D rows of first-channel G_K.
Second-channel G_K and M-row G_K are not prescribed. Exact source words.
"""
import argparse,hashlib,json,time
from pathlib import Path
import numpy as np
from verify_polarization_proposal import d,encode
from audit_temporal_reach import patches,check

REFERENCES=['none','S','P','D','birth','death','stay_one','stay_zero','AL','AC','AR']
ROOT=Path(__file__).resolve().parent

def reference(s,rule,choice,name):
    ds=d(s,rule)
    if name.startswith('pair:'):
        left,right=map(int,name.split(':')[1:]); return np.roll(s,-left,axis=-1)&np.roll(s,-right,axis=-1)
    if name=='none':return np.zeros_like(s)
    if name=='S':return s
    if name=='P':return s^np.roll(s,-choice['shift'],axis=-1)
    if name=='D':return ds
    if name=='birth':return (1-s)&ds
    if name=='death':return s&ds
    if name=='stay_one':return s&(1-ds)
    if name=='stay_zero':return (1-s)&(1-ds)
    idx=4*np.roll(s,1,axis=-1)+2*s+np.roll(s,-1,axis=-1)
    toggle={'AL':4,'AC':2,'AR':1}[name]
    # Sensitivity of the integration rule E, matching the original catalog.
    return (((rule>>idx)^(rule>>(idx^toggle)))&1).astype(np.uint8)

def rowkeys(q,rx):
    mid=q.shape[-1]//2;key=np.zeros(len(q),dtype=np.uint64)
    for dx in range(-rx,rx+1):key=(key<<1)|q[:,mid+dx]
    return key

def augment(keys,q,rx):return (keys<<(2*rx+1))|rowkeys(q,rx)[:,None]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--references',nargs='+',default=REFERENCES);ap.add_argument('--q-radius',type=int,default=1);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    prior=[r for r in map(json.loads,(ROOT/'runs/probe_radius_2/candidates.jsonl').read_text().splitlines()) if r['horizontal_radius']==2]
    start=time.perf_counter();records=[]
    with (args.output/'candidates.jsonl').open('w') as log:
        for rx in (1,2):
            width=2*rx+2*args.q_radius+3;mid=width//2
            s=((np.arange(1<<width)[:,None]>>np.arange(width-1,-1,-1))&1).astype(np.uint8)
            for rec in prior:
                rule=rec['rule'];choice=rec['recipe'][0]
                ds=d(s,rule);es=s^ds;a=encode(s,rule,choice);b=encode(es,rule,choice);c=encode(es^d(es,rule),rule,choice)
                bk=patches(a,rx);pk=patches(a^b,rx)[:,:2];bv=(a^b)[...,mid]
                g=d(es,rule)^ds^d(ds,rule)
                cg=np.stack([g[:,mid]^g[:,mid+choice['shift']],g[:,mid]],axis=1)
                wanted=a[:,:2,mid]^c[:,:2,mid]^cg
                emptyk=np.zeros((0,),dtype=np.uint64);emptyv=np.zeros((0,),dtype=np.uint8)
                for name in args.references:
                    q=reference(s,rule,choice,name);qn=reference(es,rule,choice,name);dq=q^qn
                    kb=augment(bk,q,rx);kp=augment(pk,dq,rx)
                    qflip=np.repeat(dq[:,mid,None],3,axis=1)
                    qcheck=check(kb,qflip,emptyk,emptyv,None)
                    raw=check(kb,bv,kp,wanted,None)
                    corrected=wanted.copy();corrected[:,1]^=rule&1
                    center=[check(kb,bv,kp,corrected,z) for z in (0,1)]
                    out={'candidate':rec['candidate'],'rule':rule,'recipe':rec['recipe'],'radius':rx,'reference':name,'source_width':width,'reference_update':qcheck,'raw':raw,'centered_branches':center,'joint_raw':qcheck['passes'] and raw['passes'],'joint_centered':qcheck['passes'] and any(x['passes'] for x in center)}
                    records.append(out);log.write(json.dumps(out,separators=(',',':'))+'\n')
            log.flush()
            print(json.dumps({'radius':rx,'seconds':round(time.perf_counter()-start,3),'by_reference':{name:{mode:len({r['rule'] for r in records if r['radius']==rx and r['reference']==name and r['joint_'+mode]}) for mode in ('raw','centered')} for name in args.references}}),flush=True)
    summary={}
    for rx in (1,2):
        rows=[r for r in records if r['radius']==rx];summary[str(rx)]={}
        for name in args.references+['any_added','any_except_S']:
            chosen=[r for r in rows if r['reference']==name] if name in args.references else [r for r in rows if r['reference']!='none' and (name!='any_except_S' or r['reference']!='S')]
            summary[str(rx)][name]={mode:sorted({r['rule'] for r in chosen if r['joint_'+mode]}) for mode in ('raw','centered')}
            summary[str(rx)][name]['reference_update_rules']=sorted({r['rule'] for r in chosen if r['reference_update']['passes']})
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (args.output/'manifest.json').write_text(json.dumps({'seconds':time.perf_counter()-start,'variants':596,'admitted_codes':192,'references':args.references,'radii':[1,2],'source_width':'2*radius+2*q_radius+3','q_radius':args.q_radius,'state_alphabet_bits':2,'reference_broadcast_in_transverse_axis':True,'first_order_two_channel_native_dynamics':True,'physical_G_first_channel_P_D_rows_only':True,'M_row_and_second_channel_G_unconstrained':True,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
    (args.output/'source_audit.py').write_text(Path(__file__).read_text())

if __name__=='__main__':main()
