"""Research024: exhaustive static two-cell observer search for elementary CA.

For Y_t = P(E^(2t)(S)), h* is the least history depth such that Y_(t+1) is
an exact deterministic function of Y_t,...,Y_(t-h*) over every microstate of
the finite periodic ring. h*=0 is ordinary factor closure.

The 14 nonconstant Boolean maps on a two-cell block form seven output-
complement pairs. Output complementation is an invertible relabeling, so one
representative per pair is sufficient.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from experiment_history_lift_closure import (  # noqa: E402
    FULL_CLASS, FULL_IV, minimum_memory_depth, state_map,
)

SIZES = [8, 10, 12, 14, 16]
OBSERVERS = range(1, 8)
NAMES = {
    1:"NOR", 2:"x_and_not_y", 3:"not_y", 4:"not_x_and_y",
    5:"not_x", 6:"XOR", 7:"NAND", 8:"AND", 9:"XNOR", 10:"x",
    11:"y_implies_x", 12:"y", 13:"x_implies_y", 14:"OR",
}
FAMILY = {1:"and_or",2:"directional",3:"projection",4:"directional",
          5:"projection",6:"parity",7:"and_or"}


@lru_cache(maxsize=None)
def observation(n: int, h: int) -> np.ndarray:
    states = np.arange(2**n, dtype=np.uint32)
    x = (states[:, None] >> np.arange(0, n, 2, dtype=np.uint32)) & 1
    y = (states[:, None] >> np.arange(1, n, 2, dtype=np.uint32)) & 1
    code = x + 2*y
    lut = np.array([(h >> i) & 1 for i in range(4)], dtype=np.uint8)
    macro = lut[code]
    weights = 1 << np.arange(n//2, dtype=np.uint64)
    return (macro.astype(np.uint64)*weights).sum(1).astype(np.uint32)


def scaling(values: list[int | None]) -> str:
    if any(v is None for v in values):
        return "unresolved"
    if len(set(values[-3:])) == 1:
        return "stabilized_last3"
    if all(b >= a for a, b in zip(values, values[1:])):
        return "monotone_growing"
    return "nonmonotone"


def scan_rule(rule: int) -> list[dict]:
    rows = []
    for n in SIZES:
        e = state_map(rule, n)
        step = e[e]
        for h in OBSERVERS:
            hs = minimum_memory_depth(step, observation(n, h), n//2, 4*n)
            rows.append({"rule":rule, "wclass":FULL_CLASS[rule],
                         "observer":h, "n":n, "hstar":hs})
    return rows


def build_atlas(raw: pd.DataFrame) -> pd.DataFrame:
    out = []
    for (rule, h), g in raw.groupby(["rule", "observer"]):
        by = {int(x.n): x.hstar for x in g.itertuples()}
        vals = [None if pd.isna(by[n]) else int(by[n]) for n in SIZES]
        base = {"rule":int(rule), "wclass":FULL_CLASS[int(rule)],
                "observer":int(h), "observer_name":NAMES[int(h)],
                "family":FAMILY[int(h)],
                **{f"hstar_n{n}":vals[i] for i,n in enumerate(SIZES)},
                "scaling_kind":scaling(vals)}
        out.append(base)
        # Q=1-P is exactly the same observed process up to bit relabeling.
        cp = base.copy(); cp["observer"] = 15-int(h); cp["observer_name"] = NAMES[15-int(h)]
        out.append(cp)
    return pd.DataFrame(out).sort_values(["rule","observer"]).reset_index(drop=True)


def summarize(atlas: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    canon = atlas[atlas.observer <= 7]
    rows = []
    for rule, g in canon.groupby("rule"):
        best = g.hstar_n16.astype(float).fillna(np.inf).min()
        winners = g[g.hstar_n16.astype(float).fillna(np.inf) == best]
        exact = g[g.hstar_n12 == 0]
        stable = g[g.scaling_kind == "stabilized_last3"]
        rows.append({"rule":int(rule), "wclass":FULL_CLASS[int(rule)],
                     "min_hstar_n16":None if math.isinf(best) else int(best),
                     "memory_winner_pairs":";".join(map(str,winners.observer.astype(int))),
                     "exact_memoryless_pair_count_n12":int(len(exact)),
                     "exact_memoryless_pairs_n12":";".join(map(str,exact.observer.astype(int))),
                     "stabilized_pair_count":int(len(stable)),
                     "stabilized_pairs":";".join(map(str,stable.observer.astype(int)))})
    per_rule = pd.DataFrame(rows)

    summary = {
        "observer_truth_tables": {str(h):{"name":NAMES[h],"complement":15-h,"family":FAMILY[h]} for h in OBSERVERS},
        "sizes":SIZES,
        "rules_with_any_memoryless_block2_observer_n12":int((per_rule.exact_memoryless_pair_count_n12>0).sum()),
        "rules_with_any_stabilized_observer":int((per_rule.stabilized_pair_count>0).sum()),
        "min_hstar_n16_distribution":{str(k):int(v) for k,v in per_rule.min_hstar_n16.value_counts().sort_index().items()},
        "memoryless_n12_by_observer_and_class":{},
        "scaling_by_observer_pair":{},
        "best_memory_scaling_by_class":{},
    }
    for h,g in canon.groupby("observer"):
        exact = g[g.hstar_n12 == 0]
        summary["memoryless_n12_by_observer_and_class"][str(int(h))] = {k:int(v) for k,v in exact.wclass.value_counts().sort_index().items()}
        summary["scaling_by_observer_pair"][str(int(h))] = {k:int(v) for k,v in g.scaling_kind.value_counts().items()}

    kinds=[]
    for rule,g in canon.groupby("rule"):
        best=g.hstar_n16.astype(float).fillna(np.inf).min(); w=g[g.hstar_n16.astype(float).fillna(np.inf)==best]
        kind = "winner_has_stabilized" if (w.scaling_kind=="stabilized_last3").any() else ("winner_growing" if (w.scaling_kind=="monotone_growing").any() else "winner_nonmonotone_or_unresolved")
        kinds.append((FULL_CLASS[int(rule)],kind))
    kd=pd.DataFrame(kinds,columns=["wclass","kind"])
    for cls,g in kd.groupby("wclass"):
        summary["best_memory_scaling_by_class"][cls]={k:int(v) for k,v in g.kind.value_counts().items()}
    return per_rule, summary


def class_iv_n18() -> pd.DataFrame:
    n=18; rows=[]
    for rule in FULL_IV:
        e=state_map(rule,n); step=e[e]
        vals=[minimum_memory_depth(step,observation(n,h),n//2,4*n) for h in OBSERVERS]
        best=min(v for v in vals if v is not None)
        winners=[h for h,v in zip(OBSERVERS,vals) if v==best]
        rows.append({"rule":rule,"min_h18":best,"winner_pairs_n18":";".join(map(str,winners)),**{f"h{h}":vals[h-1] for h in OBSERVERS}})
    return pd.DataFrame(rows)


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--workers",type=int,default=4); ap.add_argument("--class-iv-n18",action="store_true"); args=ap.parse_args()
    raw=[]
    with ProcessPoolExecutor(max_workers=max(1,args.workers)) as pool:
        fs=[pool.submit(scan_rule,r) for r in range(256)]
        for f in as_completed(fs): raw.extend(f.result())
    atlas=build_atlas(pd.DataFrame(raw)); per_rule,summary=summarize(atlas)
    out=ROOT/"results"; out.mkdir(exist_ok=True)
    atlas.to_csv(out/"observer_search_block2_20260908.csv",index=False)
    per_rule.to_csv(out/"observer_search_rule_summary_20260908.csv",index=False)

    exact_rules=set(per_rule.loc[per_rule.exact_memoryless_pair_count_n12>0,"rule"].astype(int)); assert len(exact_rules)==92
    scale=out/"scale_rhyme.csv"
    if scale.exists(): assert exact_rules==set(pd.read_csv(scale).fine_rule.astype(int))
    parity=atlas[atlas.observer==6]; assert int((parity.hstar_n12==0).sum())==20; assert int((parity.scaling_kind=="stabilized_last3").sum())==100; assert int((parity.scaling_kind=="monotone_growing").sum())==148

    if args.class_iv_n18:
        ext=class_iv_n18(); ext.to_csv(out/"observer_search_classiv_n18_20260908.csv",index=False); summary["class_iv_n18"]=ext.to_dict(orient="records")
    (out/"observer_search_block2_20260908_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))


if __name__ == "__main__": main()
