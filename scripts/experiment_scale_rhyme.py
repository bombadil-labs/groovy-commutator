"""Scale-rhyme: which rules coarse-grain onto which? (RG for ECA.)

A rule B is a COARSE IMAGE of rule A if there is a block map h taking
2 cells -> 1 cell such that observing A through h, at half resolution and
double time step, is exactly B:

    h ( A^2 (s) )  ==  B ( h(s) )        for every state s

(2 cells -> 1 and 2 steps -> 1 together preserve the light cone.) This is
the cellular-automata form of renormalization -- Israeli & Goldenfeld's
construction -- and the wet-math reading is literal: B is what A *rhymes
with across scale*. A rule with A -> A is its own coarse image: scale-
invariant, a fixed point of the renormalization step.

Method: exhaustive. All 256 rules x all 16 block maps h, condition checked
on every state at n=12 (blocked to n=6); every hit re-verified on every
state at n=16 (blocked to n=8) so ring-size accidents die. Constant block
maps (h == 0, h == 1) produce degenerate hits and are excluded; we also
flag hits whose coarse rule is 0 or 255 (everything looks conserved if
you project to nothing).

Output:
    results/scale_rhyme.csv  -- verified triples (A, h, B)
    printed: the coarse-graining graph's headline structure, the list of
    scale-invariant rules, and in/out degree leaders.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from groovy.ca import rule_lut  # noqa: E402


def rule_state_map(rn, n):
    lut = rule_lut(rn)
    ints = np.arange(2 ** n, dtype=np.uint32)
    S = ((ints[:, None] >> np.arange(n, dtype=np.uint32)[None, :]) & 1).astype(np.uint8)
    out = lut[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
    pow2 = (1 << np.arange(n, dtype=np.uint64))
    return (out.astype(np.uint64) * pow2[None, :]).sum(axis=1).astype(np.uint32)


def block_map_table(h_bits, n):
    """State-level map for blockwise h: n cells -> n/2 cells.
    h_bits: length-4 tuple, h[(b0<<1)|b1] for block (cell 2i, cell 2i+1)."""
    ints = np.arange(2 ** n, dtype=np.uint32)
    S = ((ints[:, None] >> np.arange(n, dtype=np.uint32)[None, :]) & 1).astype(np.uint8)
    blocks = (S[:, 0::2] << 1) | S[:, 1::2]
    hb = np.array(h_bits, dtype=np.uint8)
    coarse = hb[blocks]
    pow2 = (1 << np.arange(n // 2, dtype=np.uint64))
    return (coarse.astype(np.uint64) * pow2[None, :]).sum(axis=1).astype(np.uint32)


def find_hits(n):
    """All (A, h, B) with h(A^2(s)) == B(h(s)) for every s at ring size n."""
    n2 = n // 2
    maps_fine = {rn: rule_state_map(rn, n) for rn in range(256)}
    maps_coarse = {rn: rule_state_map(rn, n2) for rn in range(256)}
    hits = []
    for h_num in range(16):
        h_bits = tuple((h_num >> i) & 1 for i in range(4))
        if len(set(h_bits)) == 1:
            continue  # constant block maps: degenerate
        H = block_map_table(h_bits, n)
        for a in range(256):
            A2 = maps_fine[a][maps_fine[a]]
            lhs = H[A2]
            rhs_domain = H  # B must satisfy B[H[s]] == lhs[s]
            # build the partial constraint: for each coarse state u, required image
            req = {}
            ok = True
            for s in range(2 ** n):
                u = int(rhs_domain[s])
                v = int(lhs[s])
                if u in req:
                    if req[u] != v:
                        ok = False
                        break
                else:
                    req[u] = v
            if not ok:
                continue
            dom = np.fromiter(req.keys(), dtype=np.int64)
            img = np.fromiter(req.values(), dtype=np.int64)
            for b in range(256):
                if np.array_equal(maps_coarse[b][dom], img):
                    hits.append((a, h_num, b))
    return hits


def main() -> None:
    print("pass 1: exhaustive at n=12 ...")
    hits12 = find_hits(12)
    print(f"  candidate triples: {len(hits12)}")
    print("pass 2: re-verify every candidate at n=16 ...")
    verified = []
    maps_fine = {}
    maps_coarse = {}
    H_cache = {}
    for a, h_num, b in hits12:
        if a not in maps_fine:
            maps_fine[a] = rule_state_map(a, 16)
        if b not in maps_coarse:
            maps_coarse[b] = rule_state_map(b, 8)
        if h_num not in H_cache:
            h_bits = tuple((h_num >> i) & 1 for i in range(4))
            H_cache[h_num] = block_map_table(h_bits, 16)
        H = H_cache[h_num]
        A2 = maps_fine[a][maps_fine[a]]
        if np.array_equal(H[A2], maps_coarse[b][H]):
            verified.append((a, h_num, b))
    print(f"  verified at n=16: {len(verified)}")

    df = pd.DataFrame(verified, columns=["fine_rule", "block_map", "coarse_rule"])
    df["trivial_target"] = df.coarse_rule.isin([0, 255])
    df.to_csv(ROOT / "results" / "scale_rhyme.csv", index=False)

    nt = df[~df.trivial_target]
    self_similar = sorted(nt[nt.fine_rule == nt.coarse_rule].fine_rule.unique())
    print(f"\nnontrivial verified triples (coarse rule not 0/255): {len(nt)}")
    print(f"distinct fine rules with a nontrivial coarse image: {nt.fine_rule.nunique()}")
    print(f"SELF-SIMILAR rules (A coarse-grains onto itself): {self_similar}")
    print("\nmost 'renormalizable' fine rules (out-degree, nontrivial):")
    print(nt.groupby('fine_rule').coarse_rule.nunique().sort_values(ascending=False).head(12).to_dict())
    print("\nmost common coarse images (in-degree, nontrivial):")
    print(nt.groupby('coarse_rule').fine_rule.nunique().sort_values(ascending=False).head(12).to_dict())
    print("\nsample nontrivial pairs A -> B (block map shown as h(00)h(01)h(10)h(11)):")
    for r in nt[nt.fine_rule != nt.coarse_rule].head(20).itertuples():
        hb = ''.join(str((r.block_map >> i) & 1) for i in range(4))
        print(f"  {r.fine_rule:3d} --[{hb}]--> {r.coarse_rule}")


if __name__ == "__main__":
    main()
