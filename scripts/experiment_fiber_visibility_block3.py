"""Exploratory Research025 Class-IV search over all 3-cell Boolean observers.

Searches the 127 output-complement classes at n=12 and n=15, q=3. This is an
exploratory extension of the preregistered block-2 census, not an asymptotic
claim.
"""
from __future__ import annotations
import json,sys
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'scripts'))
from experiment_history_lift_closure import FULL_IV,compress,state_map  # noqa:E402


def observations3(n:int)->list[np.ndarray]:
    st=np.arange(2**n,dtype=np.uint32)
    a=(st[:,None]>>np.arange(0,n,3,dtype=np.uint32))&1
    b=(st[:,None]>>np.arange(1,n,3,dtype=np.uint32))&1
    c=(st[:,None]>>np.arange(2,n,3,dtype=np.uint32))&1
    code=a+2*b+4*c;weights=1<<np.arange(n//3,dtype=np.uint64)
    out=[]
    for h in range(1,128):
        lut=np.array([(h>>i)&1 for i in range(8)],dtype=np.uint8)
        macro=lut[code]
        out.append((macro.astype(np.uint64)*weights).sum(1).astype(np.uint32))
    return out


def entropy(labels:np.ndarray)->float:
    c=np.bincount(labels.astype(np.int64)).astype(float);c=c[c>0];p=c/c.sum()
    return float(-(p*np.log2(p)).sum())


def metrics(step:np.ndarray,obs:np.ndarray,bits:int,max_depth:int=128)->dict:
    s=np.arange(len(step),dtype=np.uint32);lab=compress(obs);cc=int(lab.max())+1;h0=entropy(lab)
    for t in range(1,max_depth+2):
        s=step[s];target=obs[s]
        up,inv=np.unique((lab.astype(np.uint64)<<bits)|target.astype(np.uint64),return_inverse=True)
        if len(up)==cc:
            hp=entropy(lab)
            return {'hstar':t-1,'H0':h0,'Hpredictive':hp,'safe_bits':np.log2(len(step))-hp,'latent_bits':hp-h0}
        lab=inv.astype(np.uint32);cc=int(lab.max())+1
    raise RuntimeError('no stabilization')


def one_hot(h:int)->bool:return h>0 and (h&(h-1))==0


def work(n:int,rule:int)->list[dict]:
    e=state_map(rule,n);step=e[e[e]];obs_all=observations3(n);rows=[]
    for h,obs in enumerate(obs_all,1):
        rows.append({'n':n,'rule':rule,'observer':h,**metrics(step,obs,n//3)})
    return rows


def main()->None:
    raw=[]
    with ProcessPoolExecutor(max_workers=7) as pool:
        fs=[pool.submit(work,n,r) for n in (12,15) for r in FULL_IV]
        for f in as_completed(fs):raw.extend(f.result())
    df=pd.DataFrame(raw).sort_values(['n','rule','observer']).reset_index(drop=True)
    summary=[]
    for (n,rule),g in df.groupby(['n','rule']):
        minH=g.Hpredictive.min();safe=g[np.isclose(g.Hpredictive,minH,atol=1e-12)]
        minh=int(g.hstar.min());fast=g[g.hstar==minh]
        winners=safe.observer.astype(int).tolist();assert all(one_hot(x) for x in winners)
        summary.append({'n':int(n),'rule':int(rule),'best_safe_predictive_entropy_bits':float(minH),
            'best_safe_bits':float(n-minH),'best_safe_observers':';'.join(map(str,winners)),
            'all_best_safe_are_single_motif_detectors':True,'best_safe_hstar_min':int(safe.hstar.min()),
            'minimum_hstar':minh,'minimum_hstar_observers':';'.join(map(str,fast.observer.astype(int).tolist())),
            'minimum_hstar_best_predictive_entropy_bits':float(fast.Hpredictive.min())})
    out=ROOT/'results';out.mkdir(exist_ok=True)
    df.to_csv(out/'fiber_visibility_block3_classiv_exploratory.csv',index=False)
    sdf=pd.DataFrame(summary);sdf.to_csv(out/'fiber_visibility_block3_classiv_exploratory_summary.csv',index=False)
    result={'status':'exploratory','sizes':[12,15],'rules':len(FULL_IV),'observer_classes':127,
        'all_best_safe_observers_single_motif_detectors':bool(sdf.all_best_safe_are_single_motif_detectors.all()),'rows':summary}
    (out/'fiber_visibility_block3_classiv_exploratory_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
