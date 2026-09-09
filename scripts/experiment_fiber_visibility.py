"""Research025: exact fiber residence / causal visibility census.

For Y_t=P(E^(q t)(S)), R_t counts unordered microstate pairs with identical
observed histories through time t. R_t-R_(t+1) is the exact number of pairs
whose first observed split occurs at t+1. On a finite state space the
partition stabilizes; R_infinity counts permanently observationally equivalent
pairs.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from experiment_history_lift_closure import FULL_CLASS, compress, state_map  # noqa:E402
from experiment_observer_search import NAMES, OBSERVERS, observation  # noqa:E402


def label_counts(labels: np.ndarray) -> np.ndarray:
    return np.bincount(labels.astype(np.int64))


def pair_count(labels: np.ndarray) -> int:
    counts = label_counts(labels)
    return int(np.sum((counts.astype(np.int64) * (counts.astype(np.int64) - 1)) // 2))


def partition_entropy(labels: np.ndarray) -> float:
    counts = label_counts(labels).astype(float)
    counts = counts[counts > 0]
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def eventual_synchronous_map(step: np.ndarray) -> tuple[np.ndarray, int]:
    """Map every state past the maximum transient depth.

    Once |E^(t+1)(X)| == |E^t(X)|, the image set is the cyclic core. Two
    initial states have coalesced synchronously iff their images at this T are
    equal.
    """
    s = np.arange(len(step), dtype=np.uint32)
    previous = len(s)
    for t in range(1, len(step) + 2):
        s = step[s]
        current = len(np.unique(s))
        if current == previous:
            return s, t
        previous = current
    raise RuntimeError("functional graph image did not stabilize")


def residence_spectrum(step: np.ndarray, obs: np.ndarray, obs_bits: int,
                       max_depth: int = 256, eventual_state: np.ndarray | None = None,
                       eventual_time: int | None = None) -> dict:
    states = np.arange(len(step), dtype=np.uint32)
    s = states.copy()
    labels = compress(obs[s])
    context_count = int(labels.max()) + 1
    initial_class_count = context_count
    initial_entropy = partition_entropy(labels)
    current_pairs = pair_count(labels)
    initial_pairs = current_pairs
    r_values = [current_pairs]
    first = {}

    for t in range(1, max_depth + 2):
        s = step[s]
        target = obs[s]
        pair_code = (labels.astype(np.uint64) << obs_bits) | target.astype(np.uint64)
        unique_pair, inverse = np.unique(pair_code, return_inverse=True)
        new_labels = inverse.astype(np.uint32)
        next_pairs = pair_count(new_labels)
        drop = current_pairs - next_pairs
        if drop:
            first[t] = int(drop)
        r_values.append(next_pairs)
        if len(unique_pair) == context_count:
            hstar = t - 1
            permanent = current_pairs
            break
        labels = new_labels
        context_count = int(labels.max()) + 1
        current_pairs = next_pairs
    else:
        raise RuntimeError(f"partition did not stabilize by depth {max_depth}")

    predictive_class_count = context_count
    predictive_entropy = partition_entropy(labels)
    visible = initial_pairs - permanent

    if eventual_state is None:
        eventual_state, eventual_time = eventual_synchronous_map(step)
    micro_bits = max(1, (len(step) - 1).bit_length())
    joint = (labels.astype(np.uint64) << micro_bits) | eventual_state.astype(np.uint64)
    coalescent_permanent = pair_count(compress(joint))
    persistent_permanent = permanent - coalescent_permanent

    if visible:
        mean_tau = sum(t*c for t,c in first.items()) / visible
        max_tau = max(first)
        cumulative = 0
        median_tau = None
        for t,c in sorted(first.items()):
            cumulative += c
            if cumulative * 2 >= visible:
                median_tau = t
                break
    else:
        mean_tau = math.nan
        median_tau = None
        max_tau = 0

    return {
        "initial_observation_classes": initial_class_count,
        "predictive_classes": predictive_class_count,
        "predictive_class_factor": predictive_class_count / initial_class_count,
        "initial_observation_entropy_bits": initial_entropy,
        "predictive_state_entropy_bits": predictive_entropy,
        "predictive_refinement_bits": predictive_entropy - initial_entropy,
        "initial_hidden_entropy_bits": math.log2(len(step)) - initial_entropy,
        "latent_future_relevant_bits": predictive_entropy - initial_entropy,
        "permanently_hidden_entropy_bits": math.log2(len(step)) - predictive_entropy,
        "latent_fraction_of_hidden_entropy": ((predictive_entropy - initial_entropy) / (math.log2(len(step)) - initial_entropy)) if (math.log2(len(step)) - initial_entropy) > 1e-12 else math.nan,
        "shielded_fraction_of_hidden_entropy": ((math.log2(len(step)) - predictive_entropy) / (math.log2(len(step)) - initial_entropy)) if (math.log2(len(step)) - initial_entropy) > 1e-12 else math.nan,
        "initial_hidden_pairs": initial_pairs,
        "permanent_hidden_pairs": permanent,
        "eventually_visible_pairs": visible,
        "eventually_visible_fraction": (visible / initial_pairs) if initial_pairs else math.nan,
        "permanent_hidden_fraction": (permanent / initial_pairs) if initial_pairs else math.nan,
        "coalescent_permanent_pairs": coalescent_permanent,
        "persistent_shielded_pairs": persistent_permanent,
        "persistent_fraction_of_permanent": (persistent_permanent / permanent) if permanent else math.nan,
        "eventual_core_time": eventual_time,
        "hstar": hstar,
        "max_finite_visibility_time": max_tau,
        "mean_first_visibility_time": mean_tau,
        "median_first_visibility_time": median_tau,
        "first_visibility_histogram": first,
        "residence_pairs_by_t": r_values,
    }


def block_rule(rule: int) -> list[dict]:
    n = 12
    e = state_map(rule, n)
    step = e[e]
    eventual_state, eventual_time = eventual_synchronous_map(step)
    rows = []
    for h in OBSERVERS:
        spec = residence_spectrum(step, observation(n, h), n//2, max_depth=4*n,
                                  eventual_state=eventual_state, eventual_time=eventual_time)
        rows.append({"rule": rule, "wclass": FULL_CLASS[rule], "observer": h,
                     "observer_name": NAMES[h], **spec})
    return rows


def derivative_rule(rule: int) -> dict:
    n = 12
    e = state_map(rule, n)
    states = np.arange(2**n, dtype=np.uint32)
    d = states ^ e
    eventual_state, eventual_time = eventual_synchronous_map(e)
    spec = residence_spectrum(e, d, n, max_depth=4*n,
                              eventual_state=eventual_state, eventual_time=eventual_time)
    return {"rule": rule, "wclass": FULL_CLASS[rule], **spec}


def compact_row(row: dict) -> dict:
    out = dict(row)
    out["first_visibility_histogram"] = json.dumps(out["first_visibility_histogram"], sort_keys=True)
    out["residence_pairs_by_t"] = json.dumps(out["residence_pairs_by_t"])
    return out


def aggregate_summary(block: pd.DataFrame, derivative: pd.DataFrame) -> dict:
    def desc(df: pd.DataFrame) -> dict:
        hidden = df.initial_hidden_pairs > 0
        return {
            "cases": int(len(df)),
            "cases_with_hidden_pairs": int(hidden.sum()),
            "cases_with_any_eventual_visibility": int((df.eventually_visible_pairs > 0).sum()),
            "cases_all_hidden_pairs_permanent": int(((df.initial_hidden_pairs > 0) & (df.eventually_visible_pairs == 0)).sum()),
            "cases_with_some_permanent_hidden_pairs": int((df.permanent_hidden_pairs > 0).sum()),
            "cases_all_hidden_pairs_eventually_visible": int(((df.initial_hidden_pairs > 0) & (df.permanent_hidden_pairs == 0)).sum()),
            "cases_with_persistent_shielded_pairs": int((df.persistent_shielded_pairs > 0).sum()),
            "cases_permanent_pairs_all_coalescent": int(((df.permanent_hidden_pairs > 0) & (df.persistent_shielded_pairs == 0)).sum()),
            "permanent_pair_total": int(df.permanent_hidden_pairs.sum()),
            "persistent_shielded_pair_total": int(df.persistent_shielded_pairs.sum()),
            "coalescent_permanent_pair_total": int(df.coalescent_permanent_pairs.sum()),
            "max_hstar": int(df.hstar.max()),
        }
    summary = {"block2_n12": desc(block), "derivative_n12": desc(derivative)}
    summary["block2_by_observer"] = {}
    for h,g in block.groupby("observer"):
        d=desc(g); d["name"] = NAMES[int(h)]
        summary["block2_by_observer"][str(int(h))]=d
    summary["block2_by_class"] = {}
    for cls,g in block.groupby("wclass"):
        summary["block2_by_class"][cls]=desc(g)
    summary["derivative_by_class"] = {}
    for cls,g in derivative.groupby("wclass"):
        summary["derivative_by_class"][cls]=desc(g)

    def entropy_desc(g: pd.DataFrame) -> dict:
        q=g[g.initial_hidden_entropy_bits > 1e-12]
        if len(q)==0:
            return {}
        return {
            "median_initial_hidden_bits": float(q.initial_hidden_entropy_bits.median()),
            "median_latent_future_relevant_bits": float(q.latent_future_relevant_bits.median()),
            "median_permanently_hidden_bits": float(q.permanently_hidden_entropy_bits.median()),
            "median_latent_fraction_of_hidden": float(q.latent_fraction_of_hidden_entropy.median()),
            "mean_latent_fraction_of_hidden": float(q.latent_fraction_of_hidden_entropy.mean()),
        }
    summary["entropy_decomposition_by_class"]={"block2":{},"derivative":{}}
    for cls,g in block.groupby("wclass"):
        summary["entropy_decomposition_by_class"]["block2"][cls]=entropy_desc(g)
    for cls,g in derivative.groupby("wclass"):
        summary["entropy_decomposition_by_class"]["derivative"][cls]=entropy_desc(g)

    safe_rows=[]
    for rule,g in block.groupby("rule"):
        x=g.sort_values(["predictive_state_entropy_bits","hstar"]).iloc[0]
        safe_rows.append(x)
    safe=pd.DataFrame(safe_rows)
    summary["best_block2_safe_forgetting_by_class"]={}
    for cls,g in safe.groupby("wclass"):
        summary["best_block2_safe_forgetting_by_class"][cls]={
            "median_permanently_hidden_bits":float(g.permanently_hidden_entropy_bits.median()),
            "mean_permanently_hidden_bits":float(g.permanently_hidden_entropy_bits.mean()),
            "median_predictive_state_entropy_bits":float(g.predictive_state_entropy_bits.median()),
        }
    summary["class_iv_best_block2_safe"]=[
        {"rule":int(x.rule),"observer":int(x.observer),"observer_name":x.observer_name,
         "hstar":int(x.hstar),"predictive_state_entropy_bits":float(x.predictive_state_entropy_bits),
         "permanently_hidden_entropy_bits":float(x.permanently_hidden_entropy_bits)}
        for x in safe[safe.wclass=="IV"].itertuples()
    ]
    return summary


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--workers",type=int,default=4); args=ap.parse_args()
    block_rows=[]; derivative_rows=[]
    with ProcessPoolExecutor(max_workers=max(1,args.workers)) as pool:
        bfs=[pool.submit(block_rule,r) for r in range(256)]
        dfs=[pool.submit(derivative_rule,r) for r in range(256)]
        for f in as_completed(bfs): block_rows.extend(f.result())
        for f in as_completed(dfs): derivative_rows.append(f.result())
    block=pd.DataFrame(block_rows).sort_values(["rule","observer"]).reset_index(drop=True)
    derivative=pd.DataFrame(derivative_rows).sort_values("rule").reset_index(drop=True)

    assert int((block.hstar == 0).groupby(block.rule).any().sum()) == 92
    parity=block[block.observer==6]
    assert int((parity.hstar==0).sum()) == 20
    assert int((derivative.hstar==0).sum()) == 30
    assert bool((block.loc[block.hstar==0,"eventually_visible_pairs"]==0).all())
    assert bool((derivative.loc[derivative.hstar==0,"eventually_visible_pairs"]==0).all())
    assert bool((block.max_finite_visibility_time == block.hstar).all())
    assert bool((derivative.max_finite_visibility_time == derivative.hstar).all())
    assert int(derivative.coalescent_permanent_pairs.sum()) == 0
    assert np.allclose(block.initial_observation_entropy_bits + block.latent_future_relevant_bits + block.permanently_hidden_entropy_bits, 12.0)
    assert np.allclose(derivative.initial_observation_entropy_bits + derivative.latent_future_relevant_bits + derivative.permanently_hidden_entropy_bits, 12.0)

    out=ROOT/"results"; out.mkdir(exist_ok=True)
    pd.DataFrame([compact_row(r) for r in block.to_dict(orient="records")]).to_csv(out/"fiber_visibility_block2_n12_20260908.csv",index=False)
    pd.DataFrame([compact_row(r) for r in derivative.to_dict(orient="records")]).to_csv(out/"fiber_visibility_derivative_n12_20260908.csv",index=False)
    summary=aggregate_summary(block,derivative)
    (out/"fiber_visibility_20260908_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    publication={k:summary[k] for k in (
        "block2_n12","derivative_n12","block2_by_class","derivative_by_class",
        "entropy_decomposition_by_class","best_block2_safe_forgetting_by_class",
        "class_iv_best_block2_safe",
    )}
    publication["publication_note"]="Compact exact summary; the full per-observer summary and raw atlases are regenerated by this script."
    (out/"fiber_visibility_20260908_publication.json").write_text(json.dumps(publication,indent=2)+"\n")
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
