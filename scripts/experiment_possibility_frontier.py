"""Research026: exact forgetting / future-possibility frontier census."""
from __future__ import annotations
import argparse, json, math, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import lru_cache
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"));sys.path.insert(0,str(ROOT/"scripts"))
from experiment_history_lift_closure import FULL_CLASS,state_map,compress  # noqa:E402
from experiment_fiber_visibility import residence_spectrum,eventual_synchronous_map,partition_entropy  # noqa:E402

N=12; STATES=np.arange(2**N,dtype=np.uint32); TOL=1e-10
SELECTED=[30,54,90,106,110,184]

@lru_cache(maxsize=None)
def observation(b:int,h:int)->np.ndarray:
    bits=((STATES[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8)
    blocks=bits.reshape(len(STATES),N//b,b)
    codes=(blocks*(1<<np.arange(b,dtype=np.uint8))).sum(2)
    lut=np.array([(h>>i)&1 for i in range(1<<b)],dtype=np.uint8)
    macro=lut[codes]
    return (macro.astype(np.uint64)*(1<<np.arange(N//b,dtype=np.uint64))).sum(1).astype(np.uint32)

def profile(step:np.ndarray,obs:np.ndarray,bits:int,eventual:tuple[np.ndarray,int])->dict:
    s=residence_spectrum(step,obs,bits,max_depth=128,eventual_state=eventual[0],eventual_time=eventual[1])
    return {
        "visible_bits":N-s["initial_hidden_entropy_bits"],
        "forgotten_bits":s["initial_hidden_entropy_bits"],
        "future_repertoire_bits":s["latent_future_relevant_bits"],
        "shielded_bits":s["permanently_hidden_entropy_bits"],
        "predictive_state_bits":s["predictive_state_entropy_bits"],
        "possibility_efficiency":s["latent_fraction_of_hidden_entropy"],
        "hstar":s["hstar"],
        "closed":abs(s["latent_future_relevant_bits"])<1e-12,
    }

def make(rule:int,kind:str,b:int,observer,canonical,p:dict)->dict:
    return {"rule":rule,"wclass":FULL_CLASS[rule],"kind":kind,"block_size":b,
            "observer":observer,"canonical_observer":canonical,**p}

def scan_rule(rule:int)->tuple[list[dict],dict]:
    e=state_map(rule,N); out=[]
    ev1=eventual_synchronous_map(e)
    out.append(make(rule,"identity",1,"identity","identity",profile(e,STATES,N,ev1)))
    out.append(make(rule,"constant",0,"constant","constant",profile(e,np.zeros_like(STATES),1,ev1)))
    step2=e[e];ev2=eventual_synchronous_map(step2)
    for h in range(1,8):
        p=profile(step2,observation(2,h),N//2,ev2)
        out.append(make(rule,"block2",2,h,h,p));out.append(make(rule,"block2",2,15-h,h,dict(p)))
    step3=e[e[e]];ev3=eventual_synchronous_map(step3)
    for h in range(1,128):
        p=profile(step3,observation(3,h),N//3,ev3)
        out.append(make(rule,"block3",3,h,h,p));out.append(make(rule,"block3",3,255-h,h,dict(p)))
    d=make(rule,"derivative",0,rule,rule,profile(e,STATES^e,N,ev1))
    return out,d

def canonical(df:pd.DataFrame)->pd.DataFrame:
    return df[(df.kind.isin(["identity","constant"]))|
              ((df.kind=="block2")&(df.observer.astype(str)==df.canonical_observer.astype(str)))|
              ((df.kind=="block3")&(df.observer.astype(str)==df.canonical_observer.astype(str)))].copy()

def oid(r)->str:
    return r.kind if r.kind in ("identity","constant") else f"{r.kind}:{int(r.observer)}"

def pareto(g:pd.DataFrame)->list[int]:
    a=g[["forgotten_bits","future_repertoire_bits"]].to_numpy(float);keep=[]
    for i,idx in enumerate(g.index):
        L,V=a[i]
        dom=(a[:,0]<=L+1e-12)&(a[:,1]>=V-1e-12)&((a[:,0]<L-1e-12)|(a[:,1]>V+1e-12))
        if not dom.any():keep.append(idx)
    return keep

def optimize(static:pd.DataFrame)->tuple[pd.DataFrame,pd.DataFrame]:
    sums=[];front=[]
    for rule,g in static.groupby("rule"):
        pos=g[g.future_repertoire_bits>TOL]
        if len(pos):
            L=float(pos.forgotten_bits.min());mn=pos[np.isclose(pos.forgotten_bits,L,atol=TOL)]
            V=float(g.future_repertoire_bits.max());mx=g[np.isclose(g.future_repertoire_bits,V,atol=TOL)]
            E=float(pos.possibility_efficiency.max());ef=pos[np.isclose(pos.possibility_efficiency,E,atol=TOL)]
        else:
            L=E=math.nan;V=0.;mn=ef=g.iloc[0:0];mx=g[np.isclose(g.future_repertoire_bits,0,atol=TOL)]
        fi=pareto(g);fg=g.loc[fi];mids=set(mn.apply(oid,axis=1));xids=set(mx.apply(oid,axis=1));eids=set(ef.apply(oid,axis=1))
        sums.append({"rule":rule,"wclass":FULL_CLASS[int(rule)],"has_closure_breaker":bool(len(pos)),
          "minimum_closure_breaking_forgetting_bits":L,"minimum_breaker_observers":";".join(sorted(mids)),
          "maximum_future_repertoire_bits":V,"minimum_forgetting_at_maximum_repertoire_bits":float(mx.forgotten_bits.min()) if len(mx) else math.nan,
          "maximum_repertoire_observers":";".join(sorted(xids)),"maximum_possibility_efficiency":E,
          "maximum_efficiency_observers":";".join(sorted(eids)),"minimum_maximum_optimizer_overlap":bool(mids&xids),
          "minimum_efficiency_optimizer_overlap":bool(mids&eids),"maximum_efficiency_optimizer_overlap":bool(xids&eids),
          "pareto_observer_count":len(fg),"pareto_point_count":len(fg[["forgotten_bits","future_repertoire_bits"]].round(10).drop_duplicates())})
        for _,r in fg.iterrows():front.append({"rule":rule,"wclass":r.wclass,"observer":oid(r),"kind":r.kind,
          "forgotten_bits":float(r.forgotten_bits),"future_repertoire_bits":float(r.future_repertoire_bits),
          "possibility_efficiency":None if pd.isna(r.possibility_efficiency) else float(r.possibility_efficiency)})
    return pd.DataFrame(sums),pd.DataFrame(front)

def class_summary(rs:pd.DataFrame)->dict:
    out={};q=rs[rs.has_closure_breaker]
    for c,g in q.groupby("wclass"):out[c]={
      "rules_with_breaker":len(g),"minimum_maximum_overlap_rules":int(g.minimum_maximum_optimizer_overlap.sum()),
      "minimum_maximum_overlap_fraction":float(g.minimum_maximum_optimizer_overlap.mean()),
      "median_minimum_breaking_forgetting_bits":float(g.minimum_closure_breaking_forgetting_bits.median()),
      "median_maximum_future_repertoire_bits":float(g.maximum_future_repertoire_bits.median()),
      "mean_maximum_future_repertoire_bits":float(g.maximum_future_repertoire_bits.mean()),
      "median_forgetting_at_maximum_repertoire_bits":float(g.minimum_forgetting_at_maximum_repertoire_bits.median()),
      "median_maximum_possibility_efficiency":float(g.maximum_possibility_efficiency.median()),
      "mean_maximum_possibility_efficiency":float(g.maximum_possibility_efficiency.mean()),
      "median_pareto_points":float(g.pareto_point_count.median())}
    return out

def loss_curves(static:pd.DataFrame)->tuple[dict,dict]:
    x=static.copy();x["loss"]=x.forgotten_bits.round(9)
    best=x.groupby(["rule","wclass","loss"]).future_repertoire_bits.max().reset_index();agg={}
    for c,g in best.groupby("wclass"):
        agg[c]={f"{L:.9f}":{"median":float(z.future_repertoire_bits.median()),"mean":float(z.future_repertoire_bits.mean())}
                for L,z in g.groupby("loss")}
    levels=sorted(L for L in best.loss.unique() if 1e-12<L<N-1e-12);kinds={}
    for rule,g in best.groupby("rule"):
        m={round(float(r.loss),9):float(r.future_repertoire_bits) for r in g.itertuples()};v=[m[round(float(L),9)] for L in levels]
        nd=all(b>=a-TOL for a,b in zip(v,v[1:]));st=all(b>a+TOL for a,b in zip(v,v[1:]))
        kinds[int(rule)]="strictly_increasing" if st else "nondecreasing" if nd else "nonmonotone"
    return agg,kinds

def obs_from_id(rule:int,identifier:str):
    e=state_map(rule,N)
    if identifier=="derivative":return e,STATES^e,N
    if identifier=="identity":return e,STATES,N
    if identifier=="constant":return e,np.zeros_like(STATES),1
    kind,h=identifier.split(":");h=int(h);b=2 if kind=="block2" else 3
    return (e[e] if b==2 else e[e[e]]),observation(b,h),N//b

def curve(rule:int,identifier:str,hstar:int)->list[float]:
    step,obs,bits=obs_from_id(rule,identifier);labels=compress(obs);h0=partition_entropy(labels);s=STATES.copy();out=[0.]
    for _ in range(hstar):
        s=step[s];target=obs[s];labels=compress((labels.astype(np.uint64)<<bits)|target.astype(np.uint64));out.append(partition_entropy(labels)-h0)
    return [float(x) for x in out]

def choose(g:pd.DataFrame,key:str):
    pos=g[g.future_repertoire_bits>TOL]
    if key=="minimum_breaker":
        if not len(pos):return None
        x=pos[np.isclose(pos.forgotten_bits,pos.forgotten_bits.min(),atol=TOL)].sort_values(["future_repertoire_bits","observer"],ascending=[False,True])
    elif key=="maximum_repertoire":
        x=g[np.isclose(g.future_repertoire_bits,g.future_repertoire_bits.max(),atol=TOL)].sort_values(["forgotten_bits","observer"])
    else:
        if not len(pos):return None
        x=pos[np.isclose(pos.possibility_efficiency,pos.possibility_efficiency.max(),atol=TOL)].sort_values(["forgotten_bits","observer"])
    return x.iloc[0]

def derivative_comparison(static:pd.DataFrame,d:pd.DataFrame)->dict:
    rows=[]
    for _,r in d.iterrows():
        g=static[static.rule==r.rule];dom=((g.forgotten_bits<=r.forgotten_bits+TOL)&(g.future_repertoire_bits>=r.future_repertoire_bits-TOL)&
          ((g.forgotten_bits<r.forgotten_bits-TOL)|(g.future_repertoire_bits>r.future_repertoire_bits+TOL))).any()
        rows.append({"wclass":r.wclass,"nondominated":not dom,"beats_eff":bool(np.isfinite(r.possibility_efficiency) and r.possibility_efficiency>g.possibility_efficiency.max()+TOL)})
    z=pd.DataFrame(rows);return {c:{"rules":len(g),"nondominated":int(g.nondominated.sum()),"beats_best_static_efficiency":int(g.beats_eff.sum())} for c,g in z.groupby("wclass")}

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument("--workers",type=int,default=4);args=ap.parse_args()
    sr=[];dr=[]
    with ProcessPoolExecutor(max_workers=max(1,args.workers)) as pool:
        fs=[pool.submit(scan_rule,r) for r in range(256)]
        for f in as_completed(fs):s,d=f.result();sr+=s;dr.append(d)
    full=pd.DataFrame(sr);der=pd.DataFrame(dr).sort_values("rule").reset_index(drop=True);st=canonical(full)
    assert st[st.kind=="block2"].groupby("rule").closed.any().sum()==92
    assert st[st.kind=="block3"].groupby("rule").closed.any().sum()==141
    assert st[st.kind=="block2"].closed.sum()==202 and st[st.kind=="block3"].closed.sum()==1656 and der.closed.sum()==30
    assert np.allclose(st.visible_bits+st.future_repertoire_bits+st.shielded_bits,N)
    rs,fr=optimize(st);agg,kinds=loss_curves(st);rs["interior_repertoire_curve"]=rs.rule.map(kinds)
    pos=rs[rs.has_closure_breaker];nonoverlap=len(pos)-int(pos.minimum_maximum_optimizer_overlap.sum())
    assert len(pos)==247 and nonoverlap==222 and pos[pos.wclass.isin(["III","IV"])].minimum_maximum_optimizer_overlap.sum()==0
    selected={}
    for rule in SELECTED:
        g=st[st.rule==rule];selected[str(rule)]={}
        for key in ("minimum_breaker","maximum_repertoire","maximum_efficiency"):
            r=choose(g,key);identifier=oid(r)
            selected[str(rule)][key]={"observer":identifier,"forgotten_bits":float(r.forgotten_bits),"future_repertoire_bits":float(r.future_repertoire_bits),
              "shielded_bits":float(r.shielded_bits),"possibility_efficiency":float(r.possibility_efficiency),"hstar":int(r.hstar),"V_t":curve(rule,identifier,int(r.hstar))}
        r=der[der.rule==rule].iloc[0];selected[str(rule)]["derivative"]={"observer":"derivative","forgotten_bits":float(r.forgotten_bits),
          "future_repertoire_bits":float(r.future_repertoire_bits),"shielded_bits":float(r.shielded_bits),
          "possibility_efficiency":None if pd.isna(r.possibility_efficiency) else float(r.possibility_efficiency),"hstar":int(r.hstar),"V_t":curve(rule,"derivative",int(r.hstar))}
    summary={"ring_width":N,"controls":{"block2_closed_fine_rules":92,"block2_canonical_factors":202,"block2_full_factors":404,
      "block3_closed_fine_rules":141,"block3_canonical_factors":1656,"block3_full_factors":3312,"derivative_closed_rules":30},
      "primary":{"rules_with_breaker":len(pos),"rules_without_breaker":9,"optimizer_overlap_rules":25,"optimizer_nonoverlap_rules":222,
      "optimizer_nonoverlap_fraction":222/247,"minimum_forgetting_distribution":{str(k):int(v) for k,v in pos.minimum_closure_breaking_forgetting_bits.value_counts().sort_index().items()},
      "maximum_repertoire_kind_counts":{"block3":int(pos.maximum_repertoire_observers.str.contains("block3").sum()),"block2":int(pos.maximum_repertoire_observers.str.contains("block2").sum())},
      "interior_curve_kind_counts":{k:int(v) for k,v in rs.interior_repertoire_curve.value_counts().items()},
      "pareto_point_count":{"minimum":int(rs.pareto_point_count.min()),"median":float(rs.pareto_point_count.median()),"maximum":int(rs.pareto_point_count.max())}},
      "by_wolfram_class":class_summary(rs),"best_repertoire_by_forgetting_level_and_class":agg,
      "derivative_vs_static":derivative_comparison(st,der),"selected_curves":selected}
    out=ROOT/"results";out.mkdir(exist_ok=True)
    full.to_csv(out/"possibility_frontier_static_n12_20260908.csv",index=False);der.to_csv(out/"possibility_frontier_derivative_n12_20260908.csv",index=False)
    rs.to_csv(out/"possibility_frontier_rule_summary_20260908.csv",index=False);fr.to_csv(out/"possibility_frontier_pareto_n12_20260908.csv",index=False)
    (out/"possibility_frontier_20260908_summary.json").write_text(json.dumps(summary,indent=2)+"\n");print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
