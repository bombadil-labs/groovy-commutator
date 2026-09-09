"""Exact n=20 tail census for Rule106 under block-2 parity."""
from __future__ import annotations
import json,sys
from pathlib import Path
from collections import Counter
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'scripts'))
from experiment_history_lift_closure import compress,state_map  # noqa:E402
from experiment_observer_search import observation  # noqa:E402

RULE,N,OBS=106,20,6

def pair_count(labels:np.ndarray)->int:
    c=np.bincount(labels.astype(np.int64)).astype(np.int64)
    return int(np.sum(c*(c-1)//2))

def rotate(x:int,k:int)->int:
    mask=(1<<N)-1
    if k==0:return x
    return ((x<<k)|(x>>(N-k)))&mask

def canonical_rotation(x:int)->int:return min(rotate(x,k) for k in range(N))

def canonical_pair_rotation(a:int,b:int)->tuple[int,int]:
    vals=[]
    for k in range(N):
        x,y=rotate(a,k),rotate(b,k);vals.append((min(x,y),max(x,y)))
    return min(vals)

def main()->None:
    e=state_map(RULE,N);step=e[e];obs=observation(N,OBS);states=np.arange(2**N,dtype=np.uint32)
    s=states.copy();labels=compress(obs);current=pair_count(labels);initial=current;hist={};last_labels=None;last_target=None
    for t in range(1,80):
        s=step[s];target=obs[s]
        up,inv=np.unique((labels.astype(np.uint64)<<(N//2))|target.astype(np.uint64),return_inverse=True)
        new=inv.astype(np.uint32);nxt=pair_count(new);drop=current-nxt
        if drop:hist[t]=drop
        if t==51:
            last_labels=labels.copy();last_target=target.copy()
        if len(up)==int(labels.max())+1:
            hstar=t-1;permanent=current;break
        labels=new;current=nxt
    else:raise AssertionError('no stabilization')
    assert hstar==51 and hist[51]==60 and permanent==135001

    lab=last_labels;target=last_target;K=int(lab.max())+1
    mn=np.full(K,1<<(N//2),dtype=np.int32);mx=np.full(K,-1,dtype=np.int32)
    np.minimum.at(mn,lab,target.astype(np.int32));np.maximum.at(mx,lab,target.astype(np.int32))
    amb=np.flatnonzero(mn!=mx);idx=np.flatnonzero(np.isin(lab,amb));pairs=[]
    for q in amb:
        inds=idx[lab[idx]==q];vals=np.unique(target[inds]);assert len(vals)==2
        aa=inds[target[inds]==vals[0]];bb=inds[target[inds]==vals[1]]
        pairs.extend((int(a),int(b)) for a in aa for b in bb)
    assert len(pairs)==60
    masses=Counter((a^b).bit_count() for a,b in pairs)
    rot=Counter(canonical_rotation(a^b) for a,b in pairs)
    pair_orbits=Counter(canonical_pair_rotation(a,b) for a,b in pairs)
    assert masses=={2:60} and len(rot)==1 and next(iter(rot))==3
    assert len(pair_orbits)==6 and set(pair_orbits.values())=={10}

    result={
        'rule':RULE,'ring_width':N,'observer':'block2_XOR','hstar':hstar,
        'initial_hidden_pairs':initial,'permanent_hidden_pairs':permanent,
        'eventually_visible_pairs':initial-permanent,
        'mean_first_visibility_time':sum(t*c for t,c in hist.items())/(initial-permanent),
        'first_visibility_histogram':hist,
        'last_split_pairs':60,'last_split_time':51,
        'last_split_hamming_mass_counts':dict(masses),
        'last_split_difference_rotation_classes':len(rot),
        'last_split_joint_rotation_orbits':len(pair_orbits),
        'last_split_pairs_per_joint_rotation_orbit':10,
        'last_split_canonical_difference_sites':[0,1],
        'interpretation':'all 60 worst-case latent pairs carry the same adjacent two-bit defect up to cyclic translation; context distinguishes their six joint-rotation pair orbits',
    }
    (ROOT/'results'/'rule106_visibility_tail_n20_20260908.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
