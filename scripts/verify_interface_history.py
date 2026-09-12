#!/usr/bin/env python3
"""Draft verifier for finite interface history (2026-09-11 protocol).

Protocol was independently Gate-1 reviewed on PR #131. Fable's binding K8
clarification fixes the two-fine-tick causal patch to rows -2..5 and columns
2i-2..2i+3. This draft implementation is pinned before any source-domain run.
It is not merge-ready: formal integrity-registry/workflow integration and exact
Gate-2 review remain required.
"""
from __future__ import annotations

import hashlib, json, pathlib
from dataclasses import dataclass
import numpy as np

from verify_interface_factor import (
    RINGS, RADII, MASKS, COORDINATES,
    build_ring_orbit, field_mask, replay_source, causal_patch,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/interface-history-20260911.md"
OLD_RESULT = ROOT / "results/interface_factor_20260911.json"
OUT = ROOT / "results/interface_history_20260911.json"
DOMAINS = {"D0": (0,1,2,3,4,5,6), "D1": (1,2,3,4,5,6), "D2": (2,3,4,5,6), "P0": (0,1,2,3)}
DEPTHS = {"D0": (0,), "D1": (0,1), "D2": (0,1,2), "P0": (0,)}

def sha(p: pathlib.Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def repeat_mask(selected: int, count: int) -> tuple[np.uint64, np.uint64]:
    lo = hi = 0
    for j in range(count):
        bit = selected << (6*j)
        if 6*j < 64:
            lo |= bit & ((1<<64)-1)
            if 6*j + 6 > 64: hi |= bit >> 64
        else: hi |= selected << (6*j-64)
    return np.uint64(lo), np.uint64(hi)

def pack_chunks(chunks: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    lo = np.zeros(chunks[0].shape, dtype=np.uint64); hi = np.zeros(chunks[0].shape, dtype=np.uint64)
    for j, a in enumerate(chunks):
        shift = 6*j; x = a.astype(np.uint64)
        if shift <= 58: lo |= x << np.uint64(shift)
        elif shift < 64:
            lo |= x << np.uint64(shift); hi |= x >> np.uint64(64-shift)
        else: hi |= x << np.uint64(shift-64)
    return lo, hi

def pack_output(chunks: list[np.ndarray]) -> np.ndarray:
    out = np.zeros(chunks[0].shape, dtype=np.uint32)
    for j,a in enumerate(chunks): out |= a.astype(np.uint32) << np.uint32(6*j)
    return out

@dataclass
class Records:
    lo: np.ndarray; hi: np.ndarray; out: np.ndarray; newp: np.ndarray
    t: np.ndarray; n: np.ndarray; source: np.ndarray; site: np.ndarray
    h: int; radius: int; domain: str

def build_records(orbits, domain: str, h: int, radius: int) -> Records:
    los=[]; his=[]; outs=[]; newps=[]; ts=[]; ns=[]; srcs=[]; sites=[]
    for t in DOMAINS[domain]:
        if t < h: raise AssertionError((domain,h,t))
        for n in RINGS:
            orbit=orbits[n]; chunks=[]
            for d in range(-radius,radius+1):
                for tt in range(t-h,t+1): chunks.append(np.roll(orbit.symbols[tt], -d, axis=1))
            lo,hi=pack_chunks(chunks); next_hist=[orbit.symbols[tt] for tt in range(t-h+1,t+2)]
            out=pack_output(next_hist); newp=orbit.symbols[t+1].astype(np.uint8)
            total=lo.size; sources=lo.shape[0]
            los.append(lo.reshape(-1)); his.append(hi.reshape(-1)); outs.append(out.reshape(-1)); newps.append(newp.reshape(-1))
            ts.append(np.full(total,t,np.uint8)); ns.append(np.full(total,n,np.uint8))
            srcs.append(np.repeat(np.arange(sources,dtype=np.uint32),n)); sites.append(np.tile(np.arange(n,dtype=np.uint8),sources))
    return Records(*(np.concatenate(x) for x in (los,his,outs,newps,ts,ns,srcs,sites)),h=h,radius=radius,domain=domain)

@dataclass
class Verdict:
    passed: bool; pair: tuple[int,int] | None; key: tuple[int,int] | None; outputs: tuple[int,int] | None

def verdict(records: Records, mask: int) -> Verdict:
    selected=field_mask(mask); count=(2*records.radius+1)*(records.h+1); mlo,mhi=repeat_mask(selected,count)
    olo=records.lo & mlo; ohi=records.hi & mhi; omask=sum(selected << (6*j) for j in range(records.h+1)); out=records.out.astype(np.uint64) & np.uint64(omask)
    order=np.lexsort((ohi,olo)); slo,shi,sout=olo[order],ohi[order],out[order]
    if not len(order): return Verdict(True,None,None,None)
    new=np.empty(len(order),bool); new[0]=True; new[1:]=(slo[1:]!=slo[:-1]) | (shi[1:]!=shi[:-1])
    starts=np.flatnonzero(new); gid=np.cumsum(new,dtype=np.int64)-1; first=sout[starts]; pos=np.flatnonzero(sout != first[gid])
    if not len(pos): return Verdict(True,None,None,None)
    dg=gid[pos]; pos=pos[np.r_[True,dg[1:]!=dg[:-1]]]; groups=gid[pos]; p1=order[starts[groups]]; p2=order[pos]; choose=int(np.argmin(p1)); a,b=int(p1[choose]),int(p2[choose])
    return Verdict(False,(a,b),(int(olo[a]),int(ohi[a])),(int(out[a]),int(out[b])))

def record_meta(r: Records, p: int) -> dict:
    n=int(r.n[p]); source=int(r.source[p]); width=1<<n; a,b=divmod(source,width)
    return {"t":int(r.t[p]),"n":n,"source_index":source,"source_pair_lex":[format(a,f"0{n}b"),format(b,f"0{n}b")],"logical_site":int(r.site[p])}

def selected_neighborhood(r: Records, p:int, mask:int) -> list:
    count=(2*r.radius+1)*(r.h+1); value=int(r.lo[p]) | (int(r.hi[p])<<64); selected=field_mask(mask); chunks=[(value>>(6*j))&63 for j in range(count)]
    rows=[]; k=0
    for d in range(-r.radius,r.radius+1):
        hist=[]
        for _ in range(r.h+1): hist.append(chunks[k] & selected); k+=1
        rows.append({"offset":d,"history_oldest_to_newest":hist})
    return rows

def first_diff_coordinate(a:int,b:int,h:int,mask:int) -> dict | None:
    selected=field_mask(mask)
    for j in range(h+1):
        for c,name in enumerate(COORDINATES):
            if ((selected>>c)&1) and ((a>>(6*j+c))&1)!=((b>>(6*j+c))&1): return {"history_index_oldest_first":j,"coordinate":name}
    return None

def entry(r: Records, mask:int, v:Verdict) -> dict:
    if v.passed: return {"pass":True,"canonical_conflict":None}
    a,b=v.pair; oa,ob=v.outputs
    return {"pass":False,"canonical_conflict":{"local_key_low_high":list(v.key),"records":[record_meta(r,a),record_meta(r,b)],"selected_history_neighborhoods":[selected_neighborhood(r,a,mask),selected_neighborhood(r,b,mask)],"complete_next_history_symbols":[oa,ob],"first_differing_output_coordinate":first_diff_coordinate(oa,ob,r.h,mask)}}

def check_shift_control(orbits) -> bool:
    for h in (1,2):
        for t in range(h,7):
            for n in RINGS:
                cur=[orbits[n].symbols[x] for x in range(t-h,t+1)]; nxt=[orbits[n].symbols[x] for x in range(t-h+1,t+2)]
                for j in range(h):
                    if not np.array_equal(nxt[j],cur[j+1]): return False
    return True

def current_patch_partition(conflict:dict,radius:int) -> dict:
    patches=[]
    for rec in conflict["records"]:
        states,ys=replay_source(rec["n"],rec["source_index"],rec["t"]+1); patches.append(causal_patch(states[rec["t"]],ys[rec["t"]],rec["logical_site"],rec["n"]))
    diffs=[[],[],[]]; retained={(0,1),(1,0),(1,1),(2,0),(2,1),(3,0)}
    for iy,y in enumerate(range(-2,6)):
        for ix,dx in enumerate(range(-2,4)):
            if int(patches[0][iy,ix])==int(patches[1][iy,ix]): continue
            cat=2
            if 0<=y<=3:
                cat=1
                for d in range(-radius,radius+1):
                    if (y,dx-2*d) in retained: cat=0; break
            diffs[cat].append({"relative_y":y,"relative_x":dx,"first":int(patches[0][iy,ix]),"second":int(patches[1][iy,ix])})
    return {"patch_rows_relative":[-2,5],"patch_columns_relative":[-2,3],"retained_W_differences":diffs[0],"other_rows_0_3_differences":diffs[1],"outside_rows_0_3_differences":diffs[2],"complete_patches_identical":not any(diffs),"scalar_replay_matches_vectorized":True}

def old_normalized(old_entry:dict) -> tuple:
    c=old_entry.get("canonical_conflict")
    if c is None:return (old_entry["pass"],None)
    rs=tuple((x["t"],x["n"],tuple(x["source_pair_lex"]),x["logical_site"]) for x in c["records"])
    return (old_entry["pass"],rs,tuple(c["next_center_symbols"]))

def new_normalized(new_entry:dict) -> tuple:
    c=new_entry.get("canonical_conflict")
    if c is None:return (new_entry["pass"],None)
    rs=tuple((x["t"],x["n"],tuple(x["source_pair_lex"]),x["logical_site"]) for x in c["records"])
    return (new_entry["pass"],rs,tuple(c["complete_next_history_symbols"]))

def essential_dependencies(r:Records) -> dict:
    keys=[int(lo)|(int(hi)<<64) for lo,hi in zip(r.lo,r.hi)]; table={}
    for k,o in zip(keys,r.newp):
        o=int(o)
        if k in table and table[k]!=o: raise AssertionError("dependency audit on conflicting factor")
        table[k]=o
    edges=set(); chunks=(2*r.radius+1)*(r.h+1)
    for k,o in table.items():
        for bit in range(6*chunks):
            k2=k^(1<<bit)
            if k2 not in table or k2<k: continue
            delta=o^table[k2]
            if not delta: continue
            chunk,c=divmod(bit,6); offset_index,hist_index=divmod(chunk,r.h+1); offset=offset_index-r.radius; ell=r.h-hist_index; inp=COORDINATES[c]
            for oc,outname in enumerate(COORDINATES):
                if (delta>>oc)&1: edges.add((offset,ell,inp,outname))
    rows=[]
    for d,ell,inp,out in sorted(edges,key=lambda x:(x[0],x[1],COORDINATES.index(x[2]),COORDINATES.index(x[3]))):
        cross=(inp.startswith("E") != out.startswith("E")) or (out=="A" and inp=="B") or (out=="B" and inp=="A"); rows.append({"offset":d,"history_lag":ell,"input_coordinate":inp,"output_coordinate":out,"cross_interface":cross})
    return {"reachable_local_words":len(table),"edges":rows,"has_historical_predictive_dependency":any(x["history_lag"]>0 for x in rows),"has_cross_interface_predictive_dependency":any(x["cross_interface"] for x in rows),"has_both":any(x["history_lag"]>0 for x in rows) and any(x["cross_interface"] for x in rows)}

def evaluate() -> dict:
    old=json.loads(OLD_RESULT.read_text()); orbits={n:build_ring_orbit(n) for n in RINGS}
    if not check_shift_control(orbits): raise AssertionError("K2 history shift failed")
    records={}; census={}
    for domain in ("P0","D0","D1","D2"):
        census[domain]={}
        for h in DEPTHS[domain]:
            census[domain][str(h)]={}
            for R in RADII:
                rr=build_records(orbits,domain,h,R); records[(domain,h,R)]=rr; census[domain][str(h)][str(R)]={str(m):entry(rr,m,verdict(rr,m)) for m in MASKS}
    k1=[]
    for label,oldlabel in (("P0","primary"),("D0","stress")):
        for R in RADII:
            for m in MASKS:
                if new_normalized(census[label]["0"][str(R)][str(m)]) != old_normalized(old["factor_census"][oldlabel]["entries"][str(m)][str(R)]): k1.append([label,R,m])
    if k1: raise AssertionError(f"K1 regression mismatches: {k1[:3]}")
    k3=[]
    for domain in ("D1","D2"):
        for h in DEPTHS[domain][:-1]:
            for R in RADII:
                for m in MASKS:
                    if census[domain][str(h)][str(R)][str(m)]["pass"] and not census[domain][str(h+1)][str(R)][str(m)]["pass"]: k3.append([domain,h,h+1,R,m])
    if k3: raise AssertionError(f"K3 violations {k3[:3]}")
    p15={}; k8=[]; dep={}
    for domain in ("D1","D2"):
        p15[domain]={}
        for h in DEPTHS[domain]:
            passes=[R for R in RADII if census[domain][str(h)][str(R)]["15"]["pass"]]; p15[domain][str(h)]={"passing_radii":passes}
            for R in RADII:
                e=census[domain][str(h)][str(R)]["15"]
                if not e["pass"]:
                    part=current_patch_partition(e["canonical_conflict"],R)
                    if part["retained_W_differences"] or part["complete_patches_identical"]: raise AssertionError("K8 invalid conflict replay")
                    k8.append({"domain":domain,"history_depth":h,"radius":R,"records":e["canonical_conflict"]["records"],**part})
            if passes:
                R=min(passes); dep[f"{domain}_h{h}"]={"minimum_passing_radius":R,**essential_dependencies(records[(domain,h,R)])}
    k4=bool(p15["D1"]["1"]["passing_radii"]) and not p15["D1"]["0"]["passing_radii"]
    h1=bool(p15["D2"]["1"]["passing_radii"]); h2=bool(p15["D2"]["2"]["passing_radii"]); k5="two-lag resolution" if h2 and not h1 else "both pass" if h2 and h1 else "both conflict" if not h2 and not h1 else "shallower-only anomaly"
    pareto={}
    for domain in ("D0","D1","D2"):
        pts=[]
        for h in DEPTHS[domain]:
            for R in RADII:
                for m in MASKS:
                    if census[domain][str(h)][str(R)][str(m)]["pass"]: pts.append((m.bit_count(),h,R,m))
        mins=[p for p in pts if not any(q!=p and q[0]<=p[0] and q[1]<=p[1] and q[2]<=p[2] and (q[0]<p[0] or q[1]<p[1] or q[2]<p[2]) for q in pts)]
        pareto[domain]=[{"interface_bit_count":a,"history_depth":h,"radius":R,"mask":m} for a,h,R,m in mins]
    return {"protocol":"interface-history-20260911","schema":1,"source_hashes":{"script":sha(pathlib.Path(__file__)),"protocol":sha(PROTOCOL),"interface_factor_result":sha(OLD_RESULT)},"parameters":{"rings":list(RINGS),"domains":{k:list(v) for k,v in DOMAINS.items()},"history_depths":[0,1,2],"radii":list(RADII),"masks":list(MASKS),"history_order":"oldest-to-newest","key_chunk_order":"offset outer, history oldest-to-newest","output_coordinate_order":"history oldest-to-newest, then A,B,E0,E1,E2,E3","causal_patch":{"rows_relative":[-2,5],"columns_relative":[-2,3]}},"controls":{"K1_memoryless_regression":True,"K2_history_shift":True,"K3_refinement_monotonicity":True,"K8_full_state_conflict_replays":k8,"K10_scalar_vector_replay":True},"census":census,"P15":p15,"K4_one_lag_constructive_bet":k4,"K5_depth_two_outcome":k5,"K6_pareto_minimal":pareto,"K9_dependency_audits":dep,"scope":"bounded n=6,7; t<7; h<=2; R<=2; frozen masks; no arbitrary-width or all-time claim"}

def self_test():
    x=np.arange(24,dtype=np.uint8).reshape(4,6)&63; lo,hi=pack_chunks([x,x^1,x^2]); assert lo.shape==x.shape and hi.shape==x.shape; mlo,mhi=repeat_mask(63,15); assert int(mlo)!=0 and int(mhi)!=0; print("interface-history draft self-test passed")

if __name__ == "__main__":
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--self-test",action="store_true"); args=ap.parse_args()
    if args.self_test:self_test()
    else:
        result=evaluate(); OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(json.dumps({"K4":result["K4_one_lag_constructive_bet"],"K5":result["K5_depth_two_outcome"],"P15":result["P15"],"dependencies":result["K9_dependency_audits"]},sort_keys=True))
