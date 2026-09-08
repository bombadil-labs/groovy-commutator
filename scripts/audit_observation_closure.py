"""Independent checks for scripts/experiment_observation_closure.py."""
from __future__ import annotations
import json, sys
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
    return (out.astype(np.uint64)*(1 << np.arange(n, dtype=np.uint64))).sum(1).astype(np.uint32)


def factor_ok(a: int, b: int) -> bool:
    states = np.arange(32, dtype=np.uint32)
    am, bm = state_map(a, 5), state_map(b, 5)
    d = states ^ am
    return bool(np.array_equal(d[am], bm[d]))


def derivative_triples(a: int) -> list[int]:
    ints = np.arange(32, dtype=np.uint32)
    w = ((ints[:, None] >> np.arange(4, -1, -1, dtype=np.uint32)) & 1).astype(np.uint8)
    lut = rule_lut(a)
    e = lut[4*w[:, :-2] + 2*w[:, 1:-1] + w[:, 2:]]
    d = w[:, 1:4] ^ e
    return sorted(set(map(int, 4*d[:, 0] + 2*d[:, 1] + d[:, 2])))


def main() -> None:
    d = pd.read_csv(ROOT / "results" / "observation_closure_derivative_20260908.csv", dtype={"eca_factors": str})
    atlas = pd.read_csv(ROOT / "results" / "observation_closure_block_local_20260908.csv")
    old = pd.read_csv(ROOT / "results" / "scale_rhyme.csv")
    exact = d[d.exact_closure]
    checks = []
    for r in exact.itertuples():
        for b in [int(x) for x in str(r.eca_factors).split(";") if x]:
            ok = factor_ok(int(r.fine_rule), b)
            checks.append(ok)
            if not ok:
                raise AssertionError(f"five-cell factor failure {r.fine_rule}->{b}")
    b2 = atlas[atlas.block_size == 2][["fine_rule", "block_map", "coarse_rule"]]
    scale_match = set(map(tuple, b2.to_numpy())) == set(map(tuple, old[["fine_rule", "block_map", "coarse_rule"]].to_numpy()))
    if not scale_match:
        raise AssertionError("block-2 local atlas differs from scale_rhyme.csv")
    special = {str(a): [i for i in range(8) if i not in derivative_triples(a)] for a in [23, 178, 77, 232]}
    assert special == {"23": [2], "178": [2], "77": [5], "232": [5]}
    audit = {"exact_derivative_rules": int(len(exact)), "local_factor_checks": len(checks),
             "all_local_factor_checks_pass": bool(all(checks)), "block2_matches_scale_rhyme": scale_match,
             "forbidden_derivative_neighborhoods": special}
    (ROOT / "results" / "observation_closure_20260908_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
