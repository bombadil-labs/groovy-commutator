"""History-repairable nonclosure across Wolfram ECA classes.

Measures how much macro prediction error induced by coarse-graining is repaired
when finite macro-history is restored. Writes:
  results/history_repairability_canonical88_parity.csv
  results/history_repairability_full256_majority.csv
  results/history_repairability_summary.json

Important: empirical sweeps use n=300/301, not power-of-two rings. Additive
rules such as Rule 90 can show special/nilpotent finite-ring behavior on
power-of-two tori.

Recovered from the conversation "Analysis of Collusion Wiki" on 2026-09-07.
The algorithm and seeds are preserved to reproduce its baseline CSVs. For a
matched-target, support-aware extension see experiment_history_validation.py.

The recovered 88-representative labels were attributed to Borriello & Walker (2017),
https://doi.org/10.1155/2017/1280351. The full-256 labels match the class sets
in Alfaro & Sanjuan (2024), Appendix A, https://arxiv.org/abs/2407.06175.
The recovered canonical table mislabels rule 41 as II; that paper calls it IV.
The legacy labels remain intact for reproducibility. Rule 106 is disputed:
the latter authors explicitly describe its periodic-ring behavior as Class III.
Symmetry-related rules are not independent replications of a class.

Unseen histories and tied vote counts predict 0 in this baseline. Targets
start later for deeper histories. Compression is one seed on a DIFFERENT
ring from prediction, with rowwise byte padding. These choices are recorded
for reproducibility, not endorsed as intrinsic measures of complexity.
"""
from __future__ import annotations
import json, zlib, sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule

CANONICAL = {'I': [0, 8, 32, 40, 128, 136, 160, 168], 'II': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 19, 23, 24, 25, 26, 27, 28, 29, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 46, 50, 51, 56, 57, 58, 62, 72, 73, 74, 76, 77, 78, 94, 104, 108, 130, 132, 134, 138, 140, 142, 152, 154, 156, 162, 164, 170, 172, 178, 184, 200, 204, 232], 'III': [18, 22, 30, 45, 60, 90, 105, 122, 126, 146, 150], 'IV': [54, 106, 110]}
FULL_I = [0, 8, 32, 40, 64, 96, 128, 136, 160, 168, 192, 224, 234, 235, 238, 239, 248, 249, 250, 251, 252, 253, 254, 255]
FULL_III = [18, 22, 30, 45, 60, 75, 86, 89, 90, 101, 102, 105, 122, 126, 129, 135, 146, 149, 150, 151, 153, 161, 165, 182, 183, 195]
FULL_IV = [41, 54, 97, 106, 107, 110, 120, 121, 124, 137, 147, 169, 193, 225]
FULL_II = sorted(set(range(256))-set(FULL_I)-set(FULL_III)-set(FULL_IV))
FULL_CLASS = {**{r:"I" for r in FULL_I}, **{r:"II" for r in FULL_II},
              **{r:"III" for r in FULL_III}, **{r:"IV" for r in FULL_IV}}

def project(s, block, kind):
    x=s.reshape(len(s)//block,block)
    if kind=="parity":
        return np.bitwise_xor.reduce(x,axis=1)
    if kind=="majority":
        return (x.sum(axis=1)>block//2).astype(np.uint8)
    raise ValueError(kind)

def trajectory(rule, block, projection, stride, n, micro_steps, burn, seed):
    rng=np.random.default_rng(seed)
    s=rng.integers(0,2,n,dtype=np.uint8)
    for _ in range(burn):
        s=apply_rule(s,rule)
    out=[project(s,block,projection)]
    for _ in range(micro_steps//stride):
        for __ in range(stride):
            s=apply_rule(s,rule)
        out.append(project(s,block,projection))
    return np.stack(out)

def neigh_codes(mt):
    return ((np.roll(mt,1,axis=1).astype(np.int64)<<2)
            |(mt.astype(np.int64)<<1)
            |np.roll(mt,-1,axis=1).astype(np.int64))

def examples(mt,h):
    ng=neigh_codes(mt); T,M=mt.shape
    key=np.zeros((T-1-h,M),dtype=np.int64); mult=1
    for j in range(h+1):
        key += ng[h-j:T-1-j]*mult
        mult *= 8
    return key.ravel(), mt[h+1:T].ravel()

def evaluate(rule,block,projection,stride,hmax,n,micro_steps,burn):
    train=[trajectory(rule,block,projection,stride,n,micro_steps,burn,s) for s in (1,2,3)]
    test=[trajectory(rule,block,projection,stride,n,micro_steps,burn,s) for s in (11,12)]
    errs=[]; covers=[]
    for h in range(hmax+1):
        k,y=zip(*(examples(mt,h) for mt in train))
        k=np.concatenate(k); y=np.concatenate(y); size=8**(h+1)
        c0=np.bincount(k[y==0],minlength=size); c1=np.bincount(k[y==1],minlength=size)
        pred=(c1>c0).astype(np.uint8); seen=(c0+c1)>0
        wrong=unseen=total=0
        for mt in test:
            kt,yt=examples(mt,h)
            wrong += np.count_nonzero(pred[kt]!=yt)
            unseen += np.count_nonzero(~seen[kt])
            total += len(yt)
        errs.append(wrong/total); covers.append(1-unseen/total)
    return errs,covers

def raw_compression(rule,n=301,steps=500,burn=150,seed=123):
    rng=np.random.default_rng(seed); s=rng.integers(0,2,n,dtype=np.uint8)
    for _ in range(burn): s=apply_rule(s,rule)
    tr=[]
    for _ in range(steps):
        tr.append(s.copy()); s=apply_rule(s,rule)
    raw=np.packbits(np.stack(tr),axis=1).tobytes()
    return len(zlib.compress(raw,9))/len(raw)

def main():
    out=ROOT/"results"; out.mkdir(exist_ok=True)
    rows=[]
    for cls,rules in CANONICAL.items():
        for r in rules:
            for b in (2,4):
                e,c=evaluate(r,b,"parity",b,3,300,700,150)
                rows.append(dict(rule=r,wclass=cls,projection="parity",block=b,stride=b,
                                 e0=e[0],e1=e[1],e2=e[2],e3=e[3],coverage_h3=c[3],
                                 repair_h3=np.nan if e[0]<1e-12 else (e[0]-e[3])/e[0]))
    pd.DataFrame(rows).to_csv(out/"history_repairability_canonical88_parity.csv",index=False)

    rows=[]
    for r in range(256):
        e,c=evaluate(r,3,"majority",1,4,300,550,150)
        rows.append(dict(rule=r,wclass=FULL_CLASS[r],projection="majority",block=3,stride=1,
                         e0=e[0],e1=e[1],e2=e[2],e3=e[3],e4=e[4],coverage_h4=c[4],
                         repair_h4=np.nan if e[0]<1e-12 else (e[0]-e[4])/e[0],
                         raw_compression=raw_compression(r)))
    df=pd.DataFrame(rows)
    df.to_csv(out/"history_repairability_full256_majority.csv",index=False)

    summary={}
    for cls in ("I","II","III","IV"):
        d=df[df.wclass==cls]
        summary[cls]=dict(n=int(len(d)),median_e0=float(d.e0.median()),
                          median_e4=float(d.e4.median()),
                          median_repair_h4=float(d.repair_h4.dropna().median()) if d.repair_h4.notna().any() else None,
                          median_raw_compression=float(d.raw_compression.median()))
    screen=(df.e0>0.15)&(df.e4<0.10)&(df.raw_compression>0.10)&(df.raw_compression<0.95)
    summary["negative_space_screen"]={}
    for cls in ("I","II","III","IV"):
        d=df[df.wclass==cls]; hits=int(screen[d.index].sum())
        summary["negative_space_screen"][cls]=dict(hits=hits,n=int(len(d)),fraction=hits/len(d))
    (out/"history_repairability_summary.json").write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
