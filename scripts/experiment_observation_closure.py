"""Observation closure experiments for elementary cellular automata.

For Y=P(S), Z=P(E^q(S)), exact closure means Z is a function of Y:
P E^q = B P for some induced dynamics B. This separates closure from the
stricter same-rule Groovy condition P E^q = E P.

Runs:
1. Derivative observation D_A(S)=S XOR E_A(S), all 256 ECA rules.
2. Exact local block factors for every nonconstant Boolean block map at
   block sizes b=2 and b=3 with matched stride q=b.

See docs/research/protocols/observation-closure-20260908.md.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import rule_lut  # noqa: E402


def state_map(rule: int, n: int) -> np.ndarray:
    lut = rule_lut(rule)
    ints = np.arange(2**n, dtype=np.uint32)
    s = ((ints[:, None] >> np.arange(n, dtype=np.uint32)) & 1).astype(np.uint8)
    out = lut[4*np.roll(s, 1, 1) + 2*s + np.roll(s, -1, 1)]
    return (out.astype(np.uint64) * (1 << np.arange(n, dtype=np.uint64))).sum(1).astype(np.uint32)


def all_maps(n: int) -> np.ndarray:
    return np.stack([state_map(r, n) for r in range(256)])


def entropy(counts: np.ndarray) -> float:
    c = np.asarray(counts, dtype=float)
    c = c[c > 0]
    total = c.sum()
    return 0.0 if not len(c) else float(math.log2(total) - np.dot(c, np.log2(c))/total)


def closure_metrics(y: np.ndarray, z: np.ndarray) -> dict:
    """Exact H(Z|Y), Bayes whole-state error, and fiber ambiguity."""
    shift = max(1, max(int(y.max()), int(z.max())).bit_length())
    pairs = (y.astype(np.uint64) << shift) | z.astype(np.uint64)
    pair_vals, pair_counts = np.unique(pairs, return_counts=True)
    _, y_counts = np.unique(y, return_counts=True)
    pair_y = pair_vals >> shift
    starts = np.r_[0, np.flatnonzero(np.diff(pair_y)) + 1]
    successors = np.diff(np.r_[starts, len(pair_counts)])
    max_counts = np.maximum.reduceat(pair_counts, starts)
    hy = entropy(y_counts)
    hz_y = max(0.0, entropy(pair_counts) - hy)
    hidden = math.log2(len(y)) - hy
    ambiguous = int(np.count_nonzero(successors > 1))
    return {
        "observation_entropy_bits": hy,
        "hidden_information_bits": hidden,
        "closure_entropy_bits": hz_y,
        "hidden_relevance_fraction": hz_y/hidden if hidden > 1e-12 else np.nan,
        "closure_error": 1.0 - float(max_counts.sum())/len(y),
        "observed_state_count": int(len(y_counts)),
        "successor_state_count": int(len(np.unique(z))),
        "ambiguous_observation_count": ambiguous,
        "ambiguous_observation_fraction": ambiguous/len(y_counts),
        "exact_closure": ambiguous == 0,
    }


def exact_factors(y: np.ndarray, z: np.ndarray, maps: np.ndarray) -> list[int]:
    order = np.argsort(y, kind="stable")
    ys, zs = y[order], z[order]
    starts = np.r_[0, np.flatnonzero(np.diff(ys)) + 1]
    stops = np.r_[starts[1:], len(ys)]
    if any(np.any(zs[a:b] != zs[a]) for a, b in zip(starts, stops)):
        return []
    domain, image = ys[starts].astype(int), zs[starts]
    return np.flatnonzero(np.all(maps[:, domain] == image[None, :], axis=1)).astype(int).tolist()


def derivative_local_factor_ok(a: int, b: int, maps5: np.ndarray) -> bool:
    states = np.arange(32, dtype=np.uint32)
    d = states ^ maps5[a]
    return bool(np.array_equal(d[maps5[a]], maps5[b][d]))


def derivative_scan(n: int, maps: np.ndarray, maps5: np.ndarray) -> pd.DataFrame:
    states = np.arange(2**n, dtype=np.uint32)
    mask = np.uint32((1 << n) - 1)
    rows = []
    for a in range(256):
        d = states ^ maps[a]
        y, z = d, d[maps[a]]
        m = closure_metrics(y, z)
        same = maps[a][y]
        diff = z ^ same
        factors = exact_factors(y, z, maps) if m["exact_closure"] else []
        kind = "zero" if np.all(diff == 0) else "ones" if np.all(diff == mask) else "variable"
        is_same = a in factors
        is_flip = 255-a in factors
        if is_same:
            ctype = "same_rule"
        elif kind == "ones" and is_flip:
            ctype = "bias_flip"
        elif m["exact_closure"] and m["successor_state_count"] == 1:
            ctype = "drain"
        elif m["exact_closure"]:
            ctype = "alternate_rule"
        else:
            ctype = "nonclosed"
        rows.append({
            "fine_rule": a, **m,
            "image_fraction": m["observed_state_count"]/(2**n),
            "same_rule_state_error": float(np.mean(diff != 0)),
            "commutator_kind": kind,
            "closure_type": ctype,
            "factor_count": len(factors),
            "eca_factors": ";".join(map(str, factors)),
            "same_rule_factor": is_same,
            "complement_rule_factor": is_flip,
            "all_factors_five_cell_verified": all(derivative_local_factor_ok(a, b, maps5) for b in factors),
        })
    return pd.DataFrame(rows)


def verify_derivative(df: pd.DataFrame, n: int, maps: np.ndarray) -> pd.DataFrame:
    states = np.arange(2**n, dtype=np.uint32)
    rows = []
    for row in df[df.exact_closure].itertuples():
        a = int(row.fine_rule)
        d = states ^ maps[a]
        z = d[maps[a]]
        m = closure_metrics(d, z)
        factors = exact_factors(d, z, maps) if m["exact_closure"] else []
        expected = [int(x) for x in str(row.eca_factors).split(";") if x]
        rows.append({
            "fine_rule": a,
            "exact_closure_n16": bool(m["exact_closure"]),
            "hidden_information_bits_n16": m["hidden_information_bits"],
            "closure_entropy_bits_n16": m["closure_entropy_bits"],
            "n16_factors": ";".join(map(str, factors)),
            "all_n12_factors_survive": set(expected).issubset(factors),
        })
    return pd.DataFrame(rows)


def windows(width: int) -> np.ndarray:
    ints = np.arange(2**width, dtype=np.uint32)
    shifts = np.arange(width-1, -1, -1, dtype=np.uint32)
    return ((ints[:, None] >> shifts) & 1).astype(np.uint8)


def codes(block: np.ndarray) -> np.ndarray:
    b = block.shape[1]
    return (block.astype(np.uint64) * (1 << np.arange(b-1, -1, -1, dtype=np.uint64))).sum(1).astype(int)


def shrink_evolve(w: np.ndarray, rule: int, steps: int) -> np.ndarray:
    x, lut = w, rule_lut(rule)
    for _ in range(steps):
        x = lut[4*x[:, :-2] + 2*x[:, 1:-1] + x[:, 2:]]
    return x


def block_factor_scan(b: int) -> pd.DataFrame:
    """All-width local test: one macro output depends on exactly 3b fine cells."""
    w = windows(3*b)
    left, center, right = codes(w[:, :b]), codes(w[:, b:2*b]), codes(w[:, 2*b:])
    obs = []
    for h in range(1, 2**(2**b)-1):
        hb = np.array([(h >> i) & 1 for i in range(2**b)], dtype=np.uint8)
        macro = 4*hb[left] + 2*hb[center] + hb[right]
        obs.append((h, hb, [np.flatnonzero(macro == i) for i in range(8)]))
    rows = []
    for a in range(256):
        final = codes(shrink_evolve(w, a, b))
        for h, hb, groups in obs:
            z = hb[final]
            bits = []
            for g in groups:
                v = int(z[g[0]])
                if np.any(z[g] != v):
                    break
                bits.append(v)
            else:
                coarse = sum(v << i for i, v in enumerate(bits))
                rows.append({"block_size": b, "fine_rule": a, "block_map": h,
                             "coarse_rule": coarse, "same_rule": a == coarse,
                             "trivial_target": coarse in (0, 255)})
    return pd.DataFrame(rows)


def main() -> None:
    out = ROOT / "results"
    out.mkdir(exist_ok=True)

    maps5, maps12 = all_maps(5), all_maps(12)
    derivative = derivative_scan(12, maps12, maps5)
    derivative.to_csv(out / "observation_closure_derivative_20260908.csv", index=False)

    maps16 = all_maps(16)
    verify = verify_derivative(derivative, 16, maps16)
    verify.to_csv(out / "observation_closure_derivative_20260908_verify.csv", index=False)

    b2, b3 = block_factor_scan(2), block_factor_scan(3)
    atlas = pd.concat([b2, b3], ignore_index=True)
    atlas.to_csv(out / "observation_closure_block_local_20260908.csv", index=False)

    old = pd.read_csv(out / "scale_rhyme.csv")[["fine_rule", "block_map", "coarse_rule"]]
    new = b2[["fine_rule", "block_map", "coarse_rule"]]
    scale_match = set(map(tuple, old.to_numpy())) == set(map(tuple, new.to_numpy()))
    if not scale_match:
        raise AssertionError("local block-2 factor set disagrees with scale_rhyme.csv")

    exact = derivative[derivative.exact_closure]
    variable = exact[exact.commutator_kind == "variable"]
    f2 = set(b2.loc[b2.same_rule & ~b2.trivial_target, "fine_rule"].astype(int))
    f3 = set(b3.loc[b3.same_rule & ~b3.trivial_target, "fine_rule"].astype(int))
    summary = {
        "derivative": {
            "exact_closure_rules": int(len(exact)),
            "n16_survivors": int(verify.exact_closure_n16.sum()),
            "all_local_factor_checks_pass": bool(exact.all_factors_five_cell_verified.all()),
            "same_rule": exact[exact.closure_type == "same_rule"].fine_rule.astype(int).tolist(),
            "bias_flip": exact[exact.closure_type == "bias_flip"].fine_rule.astype(int).tolist(),
            "variable_commutator_drain": variable[variable.successor_state_count == 1].fine_rule.astype(int).tolist(),
            "variable_commutator_nonconstant_factor": variable[variable.successor_state_count > 1].fine_rule.astype(int).tolist(),
        },
        "block2": {"triples": int(len(b2)), "fine_rules": int(b2.fine_rule.nunique()),
                   "coarse_rules": int(b2.coarse_rule.nunique()), "matches_scale_rhyme": scale_match,
                   "fixed_points": sorted(f2)},
        "block3": {"triples": int(len(b3)), "fine_rules": int(b3.fine_rule.nunique()),
                   "coarse_rules": int(b3.coarse_rule.nunique()), "fixed_points": sorted(f3)},
        "fixed_point_intersection": sorted(f2 & f3),
        "block2_only_fixed_points": sorted(f2 - f3),
        "block3_only_fixed_points": sorted(f3 - f2),
    }
    (out / "observation_closure_20260908_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
