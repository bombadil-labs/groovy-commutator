"""Research028: exact block-3 constructive representation design.

Evaluates all canonical binary targets on the 8-pattern local partition lattice.
Shardable by ECA rule interval for CI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from experiment_history_lift_closure import FULL_CLASS, state_map, compress  # noqa:E402

TOL = 1e-10
PROTOCOL = "docs/research/protocols/block3-representation-design-20260908.md"
SENTINELS = [30,54,90,106,110,184]


def canonicalize(labels: tuple[int, ...]) -> tuple[int, ...]:
    remap: dict[int,int] = {}
    out=[]
    for x in labels:
        if x not in remap: remap[x]=len(remap)
        out.append(remap[x])
    return tuple(out)


def pkey(p: tuple[int, ...]) -> str:
    return "".join(str(x) for x in p)


def blocks_of(p: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    d: dict[int,list[int]] = {}
    for i,x in enumerate(p): d.setdefault(x,[]).append(i)
    return tuple(tuple(d[k]) for k in sorted(d))


@lru_cache(maxsize=None)
def partitions_of(elements: tuple[int, ...]) -> tuple[tuple[tuple[int, ...], ...], ...]:
    elements=tuple(sorted(elements))
    m=len(elements)
    if m==0: return ((),)
    strings=[]
    def rec(prefix:list[int], maxlab:int)->None:
        if len(prefix)==m:
            strings.append(tuple(prefix)); return
        for lab in range(maxlab+2):
            rec(prefix+[lab], max(maxlab,lab))
    rec([0],0)
    out=[]
    for s in strings:
        d: dict[int,list[int]]={}
        for e,l in zip(elements,s): d.setdefault(l,[]).append(e)
        out.append(tuple(tuple(d[k]) for k in sorted(d)))
    return tuple(out)


def labels_from_blocks(blocks: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    labels=[-1]*8
    for lab,block in enumerate(sorted(blocks,key=lambda b:min(b))):
        for e in block: labels[e]=lab
    return canonicalize(tuple(labels))


def target_from_mask(mask:int)->tuple[int,...]:
    return canonicalize(tuple(0 if ((mask>>i)&1) else 1 for i in range(8)))


TARGETS=tuple(target_from_mask(mask) for mask in range(1,256) if (mask&1) and mask!=255)
assert len(TARGETS)==127 and len(set(TARGETS))==127


@lru_cache(maxsize=None)
def interval(target: tuple[int,...])->tuple[tuple[int,...],...]:
    a,b=blocks_of(target)
    out=set()
    for pa in partitions_of(a):
        for pb in partitions_of(b):
            out.add(labels_from_blocks(pa+pb))
    return tuple(sorted(out,key=lambda p:(len(set(p)),p)))


def refines(fine:tuple[int,...], coarse:tuple[int,...])->bool:
    return all(fine[i]!=fine[j] or coarse[i]==coarse[j] for i in range(8) for j in range(8))


def split_class_partitions(p:tuple[int,...])->list[tuple[tuple[int,...],tuple]]:
    blocks=blocks_of(p)
    out=[]
    for ci,C in enumerate(blocks):
        if len(C)<2: continue
        first=C[0]
        rest=C[1:]
        for mask in range(1<<(len(rest))):
            left=(first,)+tuple(rest[j] for j in range(len(rest)) if (mask>>j)&1)
            if len(left)==len(C): continue
            left_set=set(left)
            right=tuple(x for x in C if x not in left_set)
            new_blocks=list(blocks)
            new_blocks.pop(ci)
            new_blocks.extend([tuple(sorted(left)),tuple(sorted(right))])
            fine=labels_from_blocks(tuple(new_blocks))
            sig=(tuple(C),tuple(sorted(left)),tuple(sorted(right)))
            out.append((fine,sig))
    ded={p:s for p,s in out}
    return sorted([(q,ded[q]) for q in ded],key=lambda x:pkey(x[0]))


@lru_cache(maxsize=None)
def covers(p:tuple[int,...])->tuple[tuple[tuple[int,...],tuple],...]:
    return tuple(split_class_partitions(p))


def local_entropy(p:tuple[int,...])->float:
    cnt=np.bincount(np.asarray(p,dtype=np.int16))
    cnt=cnt[cnt>0].astype(float)
    prob=cnt/8.0
    return float(-(prob*np.log2(prob)).sum())


def entropy_counts(counts:np.ndarray)->float:
    c=counts[counts>0].astype(float)
    prob=c/c.sum()
    return float(-(prob*np.log2(prob)).sum())


def block_codes(n:int)->np.ndarray:
    states=np.arange(2**n,dtype=np.uint32)
    bits=((states[:,None]>>np.arange(n,dtype=np.uint32))&1).astype(np.uint8)
    blocks=bits.reshape(len(states),n//3,3)
    return (blocks*(1<<np.arange(3,dtype=np.uint8))).sum(2).astype(np.uint8)


class ObservationCache:
    def __init__(self,codes:np.ndarray):
        self.codes=codes
        self.blocks=codes.shape[1]
        self.cache:dict[tuple[int,...],np.ndarray]={}
    def get(self,p:tuple[int,...])->np.ndarray:
        if p in self.cache: return self.cache[p]
        k=len(set(p))
        lut=np.asarray(p,dtype=np.uint8)
        macro=lut[self.codes]
        weights=np.asarray([k**i for i in range(self.blocks)],dtype=np.uint32)
        arr=(macro.astype(np.uint32)*weights).sum(1).astype(np.uint16)
        self.cache[p]=arr
        return arr


def target_future(step:np.ndarray,target_obs:np.ndarray,max_steps:int)->dict:
    y0=compress(target_obs)
    k=int(y0.max())+1
    labels=y0.copy(); count=k
    s=np.arange(len(step),dtype=np.uint32)
    for t in range(1,max_steps+1):
        s=step[s]
        y=y0[s]
        new=compress(labels.astype(np.uint64)*np.uint64(k)+y.astype(np.uint64))
        nc=int(new.max())+1
        if nc==count:
            return {"labels":labels,"hstar":t-1,"classes":count}
        labels=new;count=nc
    raise RuntimeError(f"target future partition did not stabilize by {max_steps}")


def node_metrics(p:tuple[int,...],obs:np.ndarray,cinf:np.ndarray,cinf_classes:int,blocks:int)->dict:
    k=len(set(p))
    z_classes=k**blocks
    hz=blocks*local_entropy(p)
    joint=obs.astype(np.uint64)*np.uint64(cinf_classes)+cinf.astype(np.uint64)
    _,counts=np.unique(joint,return_counts=True)
    joint_classes=len(counts)
    hj=entropy_counts(counts)
    w=max(0.0,hj-hz)
    return {"H":hz,"W":w,"closed":joint_classes==z_classes,"classes":z_classes,"joint_classes":joint_classes}


def greedy_path(target:tuple[int,...],nodes:dict[tuple[int,...],dict])->list[tuple[int,...]]:
    path=[target]; cur=target
    while not nodes[cur]["closed"]:
        choices=[]
        for child,_sig in covers(cur):
            if child not in nodes: continue
            dh=nodes[child]["H"]-nodes[cur]["H"]
            if dh<=TOL: continue
            g=(nodes[cur]["W"]-nodes[child]["W"])/dh
            choices.append((-g,pkey(child),child))
        if not choices: raise AssertionError((target,cur,"no refinement cover"))
        cur=min(choices)[2];path.append(cur)
    return path


def deterministic_path(target:tuple[int,...],goal:tuple[int,...])->list[tuple[int,...]]:
    path=[target];cur=target
    while cur!=goal:
        candidates=[c for c,_ in covers(cur) if refines(goal,c)]
        if not candidates: raise AssertionError((target,goal,cur,"no path"))
        cur=sorted(candidates,key=pkey)[0];path.append(cur)
    return path


def path_detail(path:list[tuple[int,...]],nodes:dict[tuple[int,...],dict])->list[dict]:
    out=[]
    for i,p in enumerate(path):
        row={"partition":pkey(p),"H":nodes[p]["H"],"W":nodes[p]["W"],"closed":nodes[p]["closed"]}
        if i:
            prev=path[i-1];dh=nodes[p]["H"]-nodes[prev]["H"]
            row["gain"]=(nodes[prev]["W"]-nodes[p]["W"])/dh if dh>TOL else None
        out.append(row)
    return out


def beam_result(target:tuple[int,...],nodes:dict[tuple[int,...],dict],width:int)->dict:
    ht=nodes[target]["H"]
    beam=[target]
    seen={target}
    for depth in range(8):
        closed=[p for p in beam if nodes[p]["closed"]]
        if closed:
            best=min(closed,key=lambda p:(nodes[p]["H"]-ht,pkey(p)))
            return {"found":True,"partition":pkey(best),"added_bits":nodes[best]["H"]-ht,"depth":depth}
        nxt=[]
        for p in beam:
            for c,_ in covers(p):
                if c in nodes and c not in seen:
                    seen.add(c);nxt.append(c)
        if not nxt: break
        beam=sorted(nxt,key=lambda p:(nodes[p]["H"]-ht,nodes[p]["W"],pkey(p)))[:width]
    closed=[p for p in beam if nodes[p]["closed"]]
    if closed:
        best=min(closed,key=lambda p:(nodes[p]["H"]-ht,pkey(p)))
        return {"found":True,"partition":pkey(best),"added_bits":nodes[best]["H"]-ht,"depth":len(blocks_of(best))-2}
    return {"found":False}


def diminishing_audit(nodes:dict[tuple[int,...],dict])->dict:
    groups:dict[tuple,list[tuple[tuple[int,...],tuple[int,...],float,float]]]=defaultdict(list)
    for coarse in nodes:
        for fine,sig in covers(coarse):
            if fine not in nodes: continue
            raw=nodes[coarse]["W"]-nodes[fine]["W"]
            cost=nodes[fine]["H"]-nodes[coarse]["H"]
            groups[sig].append((coarse,fine,raw,raw/cost if cost>TOL else math.nan))
    tested=viol=norm_viol=0
    worst=None
    for sig,edges in groups.items():
        for i in range(len(edges)):
            for j in range(i+1,len(edges)):
                e1,e2=edges[i],edges[j]
                if refines(e2[0],e1[0]):
                    ec,ef=e1,e2
                elif refines(e1[0],e2[0]):
                    ec,ef=e2,e1
                else:
                    continue
                tested+=1
                gap=ef[2]-ec[2]
                ngap=ef[3]-ec[3]
                if gap>TOL:
                    viol+=1
                    if worst is None or gap>worst["gap"]:
                        worst={"signature":str(sig),"coarse":pkey(ec[0]),"finer":pkey(ef[0]),"coarse_gain":ec[2],"finer_gain":ef[2],"gap":gap}
                if ngap>TOL: norm_viol+=1
    return {"tested":tested,"violations":viol,"normalized_violations":norm_viol,"worst":worst}


def target_record(rule:int,target:tuple[int,...],step:np.ndarray,oc:ObservationCache,max_steps:int,n:int)->dict:
    tobs=oc.get(target)
    fut=target_future(step,tobs,max_steps)
    cinf=fut["labels"]
    cinf_classes=fut["classes"]
    ints=interval(target)
    nodes={p:node_metrics(p,oc.get(p),cinf,cinf_classes,n//3) for p in ints}
    for p in ints:
        for c,_ in covers(p):
            if c in nodes and nodes[c]["W"]>nodes[p]["W"]+1e-9:
                raise AssertionError((rule,pkey(target),pkey(p),pkey(c),"W monotonicity"))
    base=nodes[target]
    identity=tuple(range(8))
    assert nodes[identity]["closed"] and nodes[identity]["W"]<=TOL
    balance=min(len(b) for b in blocks_of(target))
    expected={1:877,2:406,3:260,4:225}[balance]
    assert len(ints)==expected
    rec={"rule":rule,"wclass":FULL_CLASS[rule],"target":pkey(target),"balance":balance,"interval_nodes":len(ints),
         "target_hstar":fut["hstar"],"target_W":base["W"],"closed":base["closed"]}
    if base["closed"]:
        rec.update({"greedy_optimal":True,"greedy_added_bits":0.0,"global_min_added_bits":0.0,"regret":0.0,
                    "relative_regret":0.0,"greedy_path":[pkey(target)],"global_optima":[pkey(target)],
                    "diminishing":diminishing_audit(nodes)})
        return rec
    path=greedy_path(target,nodes)
    ht=nodes[target]["H"]
    gend=path[-1]
    gcost=nodes[gend]["H"]-ht
    closed_nodes=[p for p in ints if nodes[p]["closed"]]
    mincost=min(nodes[p]["H"]-ht for p in closed_nodes)
    opts=sorted([p for p in closed_nodes if abs((nodes[p]["H"]-ht)-mincost)<1e-9],key=pkey)
    regret=gcost-mincost
    optimal=regret<=1e-9
    rec.update({"greedy_optimal":optimal,"greedy_added_bits":gcost,"global_min_added_bits":mincost,"regret":regret,
                "relative_regret":regret/mincost if mincost>TOL else 0.0,"greedy_path":[pkey(p) for p in path],
                "global_optima":[pkey(p) for p in opts],"diminishing":diminishing_audit(nodes)})
    if not optimal:
        opt=opts[0]
        opath=deterministic_path(target,opt)
        rec["counterexample"]={"greedy_path_detail":path_detail(path,nodes),"optimal_path_detail":path_detail(opath,nodes),
                               "beam":{"2":beam_result(target,nodes,2),"4":beam_result(target,nodes,4),"8":beam_result(target,nodes,8)}}
    return rec


def scan_rule(rule:int,n:int,max_steps:int)->dict:
    codes=block_codes(n);oc=ObservationCache(codes)
    e=state_map(rule,n);step=e[e[e]]
    rows=[target_record(rule,target,step,oc,max_steps,n) for target in TARGETS]
    return {"rule":rule,"wclass":FULL_CLASS[rule],"targets":rows,"cached_observers":len(oc.cache)}


def hashes()->dict:
    paths=[Path(__file__),ROOT/PROTOCOL]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--rule-start",type=int,default=0);ap.add_argument("--rule-end",type=int,default=256)
    ap.add_argument("--rules",type=str,default="",help="comma-separated explicit rules; overrides range")
    ap.add_argument("--n",type=int,default=12);ap.add_argument("--max-steps",type=int,default=128)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    if args.n%3: raise SystemExit("n must be divisible by 3")
    if args.rules:
        rules=[int(x) for x in args.rules.split(",") if x.strip()]
    else:
        if not (0<=args.rule_start<args.rule_end<=256): raise SystemExit("bad rule range")
        rules=list(range(args.rule_start,args.rule_end))
    rows=[scan_rule(r,args.n,args.max_steps) for r in rules]
    result={"experiment":"block3-representation-design","schema":1,"ring_width":args.n,"cadence":3,"rules":rules,"rule_count":len(rules),
            "target_count":len(TARGETS),"source_hashes":hashes(),"rows":rows}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    failures=sum(not t["greedy_optimal"] for r in rows for t in r["targets"] if not t["closed"])
    nonclosed=sum(not t["closed"] for r in rows for t in r["targets"])
    print(json.dumps({"rules":rules,"nonclosed":nonclosed,"greedy_failures":failures,"output":str(args.output)},indent=2))

if __name__=="__main__": main()
