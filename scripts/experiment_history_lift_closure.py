"""Exact finite-memory closure under lossy observations of elementary CA.

For Y_t = P(E^{q t}(S)), define the minimum history depth h* as the least h
for which a deterministic map F exists with

    Y_{t+1} = F(Y_t, Y_{t-1}, ..., Y_{t-h})

for every microstate S and therefore (by time homogeneity) every t.  h*=0 is
ordinary observation closure.  This experiment uses exact exhaustive finite-ring
state spaces, not learned predictors.

Experiments:
1. Derivative observation D_A(S)=S XOR E_A(S), q=1, n=8,10,12,14,16.
2. Block-2 parity coarse graining, q=2, same ring sizes.
3. For derivative at n=12, exact local spatiotemporal rules with radius 1..4
   and history <=6.
4. Matched-target control at n=12, T=6: hold Y_7 fixed as target while adding
   Y_5,Y_4,... behind Y_6, so improvement cannot be attributed to predicting
   a later time.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import rule_lut  # noqa: E402

SIZES = [8, 10, 12, 14, 16]
FULL_I = [0,8,32,40,64,96,128,136,160,168,192,224,234,235,238,239,248,249,250,251,252,253,254,255]
FULL_III = [18,22,30,45,60,75,86,89,90,101,102,105,122,126,129,135,146,149,150,151,153,161,165,182,183,195]
FULL_IV = [41,54,97,106,107,110,120,121,124,137,147,169,193,225]
FULL_II = sorted(set(range(256)) - set(FULL_I) - set(FULL_III) - set(FULL_IV))
FULL_CLASS = {**{r:"I" for r in FULL_I}, **{r:"II" for r in FULL_II},
              **{r:"III" for r in FULL_III}, **{r:"IV" for r in FULL_IV}}


@lru_cache(maxsize=None)
def state_map(rule: int, n: int) -> np.ndarray:
    lut = rule_lut(rule)
    ints = np.arange(2**n, dtype=np.uint32)
    s = ((ints[:, None] >> np.arange(n, dtype=np.uint32)) & 1).astype(np.uint8)
    out = lut[4*np.roll(s, 1, 1) + 2*s + np.roll(s, -1, 1)]
    weights = 1 << np.arange(n, dtype=np.uint64)
    return (out.astype(np.uint64) * weights).sum(1).astype(np.uint32)


def compress(values: np.ndarray) -> np.ndarray:
    _, inv = np.unique(values, return_inverse=True)
    return inv.astype(np.uint32)


def minimum_memory_depth(step: np.ndarray, observation: np.ndarray,
                         observation_bits: int, hmax: int) -> int | None:
    """Exact deterministic history closure by partition refinement.

    Each context partition is refined by the next observed whole state. If the
    next observation is constant inside every context fiber, history closes.
    Enumerating all microstates at t=0 makes the resulting F time homogeneous.
    """
    states = np.arange(len(step), dtype=np.uint32)
    s = states
    labels = compress(observation[s])
    context_count = int(labels.max()) + 1
    for h in range(hmax + 1):
        s = step[s]
        target = observation[s]
        pair = (labels.astype(np.uint64) << observation_bits) | target.astype(np.uint64)
        unique_pair, inverse = np.unique(pair, return_inverse=True)
        if len(unique_pair) == context_count:
            return h
        labels = inverse.astype(np.uint32)
        context_count = int(labels.max()) + 1
    return None


@lru_cache(maxsize=None)
def block2_parity_map(n: int) -> np.ndarray:
    if n % 2:
        raise ValueError("block-2 parity needs even n")
    states = np.arange(2**n, dtype=np.uint32)
    bits = ((states[:, None] >> np.arange(n, dtype=np.uint32)) & 1).astype(np.uint8)
    macro = np.bitwise_xor.reduce(bits.reshape(len(states), n//2, 2), axis=2)
    weights = 1 << np.arange(n//2, dtype=np.uint64)
    return (macro.astype(np.uint64) * weights).sum(1).astype(np.uint32)


def scaling_scan(kind: str) -> pd.DataFrame:
    rows = []
    for rule in range(256):
        row = {"rule": rule, "wclass": FULL_CLASS[rule], "observer": kind}
        for n in SIZES:
            e = state_map(rule, n)
            states = np.arange(2**n, dtype=np.uint32)
            if kind == "derivative":
                step = e
                observation = states ^ e
                bits = n
            elif kind == "block2_parity":
                step = e[e]
                observation = block2_parity_map(n)
                bits = n // 2
            else:
                raise ValueError(kind)
            row[f"hstar_n{n}"] = minimum_memory_depth(step, observation, bits, n + 4)
        vals = [row[f"hstar_n{n}"] for n in SIZES]
        if None not in vals and len(set(vals[-3:])) == 1:
            row["scaling_kind"] = "stabilized_last3"
        elif None not in vals and all(vals[i+1] >= vals[i] for i in range(len(vals)-1)):
            row["scaling_kind"] = "monotone_growing"
        else:
            row["scaling_kind"] = "nonmonotone"
        rows.append(row)
    return pd.DataFrame(rows)


def bitrows(values: np.ndarray, n: int) -> np.ndarray:
    return ((values[:, None] >> np.arange(n, dtype=np.uint32)) & 1).astype(np.uint8)


def local_exact(key: np.ndarray, target: np.ndarray) -> bool:
    pair = (key.astype(np.uint64) << 1) | target.astype(np.uint64)
    vals = np.unique(pair)
    contexts = vals >> 1
    return len(vals) == len(np.unique(contexts))


def derivative_local_hstar(rule: int, n: int, radius: int, hmax: int) -> int | None:
    states = np.arange(2**n, dtype=np.uint32)
    e = state_map(rule, n)
    d = states ^ e
    micro = [states]
    for _ in range(hmax + 1):
        micro.append(e[micro[-1]])
    obs = [bitrows(d[s], n) for s in micro]
    width = 2*radius + 1
    neigh = []
    for y in obs:
        code = np.zeros_like(y, dtype=np.uint64)
        for offset in range(-radius, radius + 1):
            code = (code << 1) | np.roll(y, -offset, axis=1)
        neigh.append(code)
    key = np.zeros_like(neigh[0], dtype=np.uint64)
    for h in range(hmax + 1):
        key = (key << width) | neigh[h]
        if local_exact(key.ravel(), obs[h+1].ravel()):
            return h
    return None


def locality_scan(n: int = 12, hmax: int = 6) -> pd.DataFrame:
    rows = []
    states = np.arange(2**n, dtype=np.uint32)
    for rule in range(256):
        e = state_map(rule, n)
        d = states ^ e
        micro = [states]
        for _ in range(hmax + 1):
            micro.append(e[micro[-1]])
        obs = [bitrows(d[x], n) for x in micro]
        row = {"rule": rule, "wclass": FULL_CLASS[rule], "n": n, "hmax": hmax}
        for radius in range(1, 5):
            width = 2*radius + 1
            neigh = []
            for y in obs:
                code = np.zeros_like(y, dtype=np.uint64)
                for offset in range(-radius, radius + 1):
                    code = (code << 1) | np.roll(y, -offset, axis=1)
                neigh.append(code)
            key = np.zeros_like(neigh[0], dtype=np.uint64)
            found = None
            for h in range(hmax + 1):
                key = (key << width) | neigh[h]
                if local_exact(key.ravel(), obs[h+1].ravel()):
                    found = h
                    break
            row[f"hstar_r{radius}"] = found
        rows.append(row)
    return pd.DataFrame(rows)


def matched_target_hstar(rule: int, n: int = 12, target_time: int = 6,
                          hmax: int = 6) -> int | None:
    """Past-history repair while holding target Y_{T+1} fixed."""
    states = np.arange(2**n, dtype=np.uint32)
    e = state_map(rule, n)
    d = states ^ e
    micro = [states]
    for _ in range(target_time + 1):
        micro.append(e[micro[-1]])
    y = [d[s] for s in micro]
    target = y[target_time + 1]
    labels = compress(y[target_time])
    context_count = int(labels.max()) + 1
    for h in range(hmax + 1):
        pair_target = (labels.astype(np.uint64) << n) | target.astype(np.uint64)
        if len(np.unique(pair_target)) == context_count:
            return h
        if h == hmax:
            break
        older = y[target_time - h - 1]
        refine = (labels.astype(np.uint64) << n) | older.astype(np.uint64)
        labels = compress(refine)
        context_count = int(labels.max()) + 1
    return None


def summary_for_scaling(df: pd.DataFrame) -> dict:
    result = {
        "scaling_kind_counts": {k: int(v) for k, v in df.scaling_kind.value_counts().items()},
        "by_wolfram_class": {},
        "hstar_distributions": {},
    }
    for cls in ("I", "II", "III", "IV"):
        counts = df[df.wclass == cls].scaling_kind.value_counts()
        result["by_wolfram_class"][cls] = {k: int(v) for k, v in counts.items()}
    for n in SIZES:
        counts = Counter(int(x) for x in df[f"hstar_n{n}"].dropna())
        result["hstar_distributions"][str(n)] = {str(k): int(v) for k, v in sorted(counts.items())}
    return result


def main() -> None:
    out = ROOT / "results"
    out.mkdir(exist_ok=True)

    derivative = scaling_scan("derivative")
    parity = scaling_scan("block2_parity")
    locality = locality_scan()
    derivative.to_csv(out / "history_lift_derivative_scaling_20260908.csv", index=False)
    parity.to_csv(out / "history_lift_block2_parity_scaling_20260908.csv", index=False)
    for column in [f"hstar_r{r}" for r in range(1, 5)]:
        locality[column] = locality[column].astype("Int64")
    locality.to_csv(out / "history_lift_derivative_locality_20260908.csv", index=False)

    mt = {rule: matched_target_hstar(rule) for rule in range(256)}
    matched = pd.DataFrame({
        "rule": range(256),
        "wclass": [FULL_CLASS[r] for r in range(256)],
        "n": 12, "target_time": 6, "hmax": 6,
        "matched_target_hstar": [mt[r] for r in range(256)],
    })
    matched["matched_target_hstar"] = matched["matched_target_hstar"].astype("Int64")
    matched.to_csv(out / "history_lift_derivative_matched_target_20260908.csv", index=False)
    mt_current_closed = sum(h == 0 for h in mt.values())
    mt_history_repaired = sum(h not in (None, 0) for h in mt.values())
    mt_unresolved = sum(h is None for h in mt.values())

    global_le6 = int(sum((derivative.hstar_n12.notna()) & (derivative.hstar_n12 <= 6)))
    local_counts = {f"radius_{r}": int(locality[f"hstar_r{r}"].notna().sum()) for r in range(1, 5)}
    key_rules = [28, 30, 41, 54, 78, 90, 106, 110, 136, 184]
    examples = {}
    for rule in key_rules:
        examples[str(rule)] = {
            "derivative": [int(derivative.loc[derivative.rule == rule, f"hstar_n{n}"].iloc[0]) for n in SIZES],
            "block2_parity": [int(parity.loc[parity.rule == rule, f"hstar_n{n}"].iloc[0]) for n in SIZES],
        }

    assert int((derivative.hstar_n12 == 0).sum()) == 30
    assert int((parity.hstar_n12 == 0).sum()) == 20
    assert local_counts["radius_4"] == global_le6
    assert mt_current_closed + mt_history_repaired + mt_unresolved == 256
    assert examples["90"]["derivative"] == [0, 0, 0, 0, 0]
    assert examples["90"]["block2_parity"] == [0, 0, 0, 0, 0]

    summary = {
        "definition": "h* is the least past-history depth making the next observed whole state deterministic for every microstate",
        "sizes": SIZES,
        "derivative": summary_for_scaling(derivative),
        "block2_parity": summary_for_scaling(parity),
        "derivative_locality_n12_hmax6": {
            "global_hstar_le6": global_le6,
            **local_counts,
        },
        "matched_target_derivative_n12_T6_hmax6": {
            "current_closed": mt_current_closed,
            "history_repaired": mt_history_repaired,
            "unresolved": mt_unresolved,
        },
        "examples": examples,
    }
    (out / "history_lift_closure_20260908_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
