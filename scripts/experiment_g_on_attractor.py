"""G on the attractor: does the kinematic commutator EMERGE at the
attractor for rules that are nowhere near affine?

Scope: FINITE PERIODIC RINGS only (n = 8..20), exhaustive over all 2^n
states; nothing here is a full-line claim. Written 2026-07-21, ported to
main 2026-11-09; account in docs/research/2026-11-09-g-on-attractor.md.

Motivation: evaluate an observable where the dynamics settle instead of
over all states, applied to the affine implication
(docs/knowledge/affine-implication.md). Globally, G(S) is constant iff phi
is affine or one of the nonlinear rules {4, 200}
(docs/knowledge/affine-converse.md). The question: restrict S to phi's
EVENTUAL IMAGE (states on cycles of the ring map, iterated to exact
stabilisation, no round cap) and ask which other rules become G-constant
there. Note the k=0 rung of the commutator-jet recurrence
(docs/knowledge/commutator-jet.md), D(HX) = H(DX) xor G(X), is the
"difference lemma" below.

Triviality control, derived first, checked computationally below:

    Fixed-point lemma. If phi(S) = S then D(S) = 0, so
    G(S) = D(E(S)) xor E(D(S)) = 0 xor phi(0-vector) = all-zeros if
    lut[0] = 0, all-ones if lut[0] = 1. Hence ANY rule whose attractor is
    entirely fixed points has G trivially constant there, at a value set
    by bit 0 of the rule number alone.

So the honest survivors are rules with attractor cycles of period >= 2
that STILL pin G to a single value. phi restricted to its eventual image
is a permutation (the image is exactly the union of eventual cycles), so
per-state period = the containing cycle's length, computed by walking the
successor permutation.

Ring-size robustness: the whole computation is repeated at every n in
NS (8..14, odd sizes included -- result "memory variants" showed
bijectivity surprises sneak in at particular parities).

Two lemmas sharpen the empirics into structure (both verified below):

    Shift lemma (the two-point spectrum is forced, not achieved).
    G commutes with the ring shift sigma, and the
    attractor is closed under sigma (phi commutes with shift). So if G
    is constant = c on the attractor, c = G(sigma S) = sigma G(S) =
    sigma c: the constant is shift-invariant, and the only
    shift-invariant states are the two uniform ones. The observed
    "always all-zeros or all-ones, never mixed, at every n" is FORCED
    by equivariance -- kinematics, not a dynamical achievement.

    Covariance lemma (why the survivor set has the shape it has). G is
    reflection-covariant at the rule level -- G_{refl(phi)}(S) =
    reverse(G_phi(reverse(S))) for all 256 rules -- so the survivor set
    MUST be closed under left-right mirroring, and it is
    (13<->69, 79<->93, the rest self-mirrored). It is NOT
    conjugation-covariant: for psi = C phi C (bitwise complement
    conjugate),

        G_psi(S) = D_phi(E_phi(CS)) xor [E_phi(D_phi(CS) xor 1) xor 1]

    verified exactly for all 256 rules. Those two stray xor-1 terms are
    the whole asymmetry: D(S) = S xor phi(S) does not commute with
    complementation for a FIXED rule, so G's covariance picks up bias
    terms. Consequence, confirmed: rule 33 is a survivor while its
    conjugate 123 is not, despite IDENTICAL attractor geometry (image
    326, every state period 2, at n=12) -- 123 takes 130 distinct G
    values there. Same currency as the affine bias (docs/knowledge/commutator-complement-covariance.md): the zero vs.
    nonzero-constant dichotomy and the conjugation-symmetry breaking are
    both about where an xor-1 lands.

    Difference lemma. Along an attractor orbit S_t, write
    X_t = S_t xor S_{t+1}. Then G = c identically on the orbit iff
    X_{t+1} = phi(X_t) xor c for all t: constancy means the difference
    masks themselves evolve lawfully under phi (c = 0) or under
    complemented phi (c = ones). For period <= 2, X is constant and
    this collapses to the fixed-point/D^2 conditions. A period >= 3
    cycle with constant G would have to carry a genuinely nonconstant
    "shadow trajectory" of differences riding along it.

The period-2 wall: CONJECTURED, THEN FALSIFIED IN THIS SCRIPT. Keeping
the autopsy because the counterexample is the interesting part.

Conjecture was: outside the globally-constant rules (16 affine plus
{4, 200}), G-constancy tolerates attractor cycles of period <= 2 and
nothing longer. It held exhaustively at n = 8..14. (Affine rules were
always exempt: for affine phi the difference recursion below holds
identically, and rules 15, 60, 85, 102, 153, 170, 195, 240 do sail
through at max period n with constant G.)

It is FALSE. Rules 44 and 100 are non-affine, outside {4, 200},
G-constant (value all-zeros) on their whole attractor, and carry a
genuine period-3 cycle -- but only when 3 | n. The cycle is a rigidly
translating wave: 110110110110 -> 101101101101 -> 011011011011 ->
back, i.e. S_{t+1} = sigma(S_t), which only closes on the ring when
the spatial period divides n. That is why n = 8..14 missed it except
at 12, where the "survivors at every n" filter then discarded 44/100
for being fixed-point-only at the OTHER sizes. The wall was an
artifact of which ring sizes we probed.

The natural repair -- "constancy tolerates exactly the rigidly
translating orbits" -- is ALSO false, checked both directions at
n = 10 and 12: rules {13, 19, 23, 33, 55, 69, 77, 79, 93, 178, ...}
are constant with non-translating orbits, and ~60 rules per size have
all-translating attractors without constant G. Rigid translation is
neither necessary nor sufficient.

What survives is the difference lemma below, which is exact but is a
reformulation rather than a classification. Characterizing which
attractor orbits admit constant G is OPEN.

Output:
    results/g_on_attractor.parquet      -- one row per (n, rule), n in NS
    results/g_on_attractor_bign.parquet -- one row per (n, rule), big n
    site/src/data/g_on_attractor.json   -- headline numbers + survivors
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

NS = [8, 9, 10, 11, 12, 13, 14]


def rule_lut(rule_num: int) -> np.ndarray:
    return np.array([(rule_num >> i) & 1 for i in range(8)], dtype=np.uint8)


def apply_rule_batch(states: np.ndarray, lut: np.ndarray) -> np.ndarray:
    l = np.roll(states, 1, axis=1)
    r = np.roll(states, -1, axis=1)
    return lut[4 * l + 2 * states + r]


def g_batch(states: np.ndarray, lut: np.ndarray) -> np.ndarray:
    """G(S) = D(E(S)) xor E(D(S)) with D(S) = S xor phi(S), E = phi."""
    e = apply_rule_batch(states, lut)
    de = e ^ apply_rule_batch(e, lut)
    ed = apply_rule_batch(states ^ e, lut)
    return de ^ ed


def all_states(n: int) -> np.ndarray:
    ints = np.arange(2 ** n, dtype=np.uint32)
    return ((ints[:, None] >> np.arange(n, dtype=np.uint32)[None, :]) & 1).astype(np.uint8)


def state_keys(states: np.ndarray, n: int) -> np.ndarray:
    pow2 = (1 << np.arange(n, dtype=np.uint64))
    return (states.astype(np.uint64) * pow2[None, :]).sum(axis=1)


def is_affine(rule_num: int) -> bool:
    """f affine over GF(2) iff every second difference of the 8-entry LUT
    vanishes: f(x) ^ f(x^ei) ^ f(x^ej) ^ f(x^ei^ej) = 0 for basis pairs."""
    lut = rule_lut(rule_num).astype(int)
    basis = [4, 2, 1]
    for i in range(3):
        for j in range(i + 1, 3):
            for x in range(8):
                if lut[x] ^ lut[x ^ basis[i]] ^ lut[x ^ basis[j]] ^ lut[x ^ basis[i] ^ basis[j]]:
                    return False
    return True


def eventual_image_states(lut: np.ndarray, n: int, max_rounds: int = 1 << 14) -> np.ndarray:
    """(m, n) array of the states on eventual cycles of phi."""
    cur = all_states(n)
    size = cur.shape[0]
    for _ in range(max_rounds):
        cur = apply_rule_batch(cur, lut)
        keys = np.unique(state_keys(cur, n))
        cur = ((keys[:, None] >> np.arange(n, dtype=np.uint64)[None, :]) & 1).astype(np.uint8)
        if len(keys) == size:
            return cur
        size = len(keys)
    raise RuntimeError("eventual image did not stabilize")


def eventual_image_mask(lut: np.ndarray, n: int) -> np.ndarray:
    """Boolean mask over the 2^n integer-keyed states: on an eventual cycle."""
    att = eventual_image_states(lut, n)
    mask = np.zeros(2 ** n, dtype=bool)
    mask[state_keys(att, n)] = True
    return mask


def cycle_periods(att_keys: np.ndarray, succ_keys: np.ndarray) -> np.ndarray:
    """Per-state cycle length for the permutation att_keys -> succ_keys."""
    index = {int(k): i for i, k in enumerate(att_keys)}
    succ_idx = np.array([index[int(k)] for k in succ_keys], dtype=np.int64)
    periods = np.zeros(len(att_keys), dtype=np.int64)
    for start in range(len(att_keys)):
        if periods[start]:
            continue
        path = [start]
        cur = succ_idx[start]
        while cur != start:
            path.append(cur)
            cur = succ_idx[cur]
        for i in path:
            periods[i] = len(path)
    return periods


def run_one_n(n: int) -> list[dict]:
    states = all_states(n)
    ints = np.arange(2 ** n)
    rows = []
    for rule in range(256):
        lut = rule_lut(rule)
        g_keys = state_keys(g_batch(states, lut), n)
        g_global = len(np.unique(g_keys))

        mask = eventual_image_mask(lut, n)
        att_ints = ints[mask]
        att_states = states[mask]
        att_g = np.unique(g_keys[mask])
        g_att = len(att_g)

        succ = state_keys(apply_rule_batch(att_states, lut), n)
        periods = cycle_periods(att_ints.astype(np.uint64), succ)
        max_period = int(periods.max()) if len(periods) else 0
        frac_fixed = float((periods == 1).mean()) if len(periods) else 0.0

        ones_key = (1 << n) - 1
        if g_att == 1:
            v = int(att_g[0])
            const_kind = "zeros" if v == 0 else ("ones" if v == ones_key else "other")
        else:
            const_kind = ""

        # fixed-point lemma check: on every fixed point, G must equal
        # phi(0-vector) = all-zeros or all-ones by lut[0]
        fp_mask = mask.copy()
        fp_keys = g_keys[mask][periods == 1]
        expect = ones_key if lut[0] else 0
        lemma_ok = bool((fp_keys == expect).all()) if len(fp_keys) else True

        rows.append(dict(
            n=n, rule=rule, affine=is_affine(rule),
            image=int(mask.sum()), image_frac=float(mask.mean()),
            g_global=g_global, g_attractor=g_att,
            g_const_kind=const_kind,
            max_period=max_period, frac_fixed=round(frac_fixed, 4),
            fp_lemma_ok=lemma_ok,
        ))
    return rows


def run_bign(n: int, rules) -> list[dict]:
    """Vectorized big-n check: is G constant on the attractor, and does the
    attractor contain any state of period > 2 (A restricted to Fix(phi^2)
    complement)? No per-cycle decomposition -- period<=2 is a batch test."""
    rows = []
    for rule in rules:
        lut = rule_lut(rule)
        att = eventual_image_states(lut, n)
        g_keys = np.unique(state_keys(g_batch(att, lut), n))
        succ2 = apply_rule_batch(apply_rule_batch(att, lut), lut)
        per_le2 = (succ2 == att).all(axis=1)
        ones_key = (1 << n) - 1
        if len(g_keys) == 1:
            v = int(g_keys[0])
            kind = "zeros" if v == 0 else ("ones" if v == ones_key else "other")
        else:
            kind = ""
        rows.append(dict(
            n=n, rule=rule, affine=is_affine(rule),
            image=int(att.shape[0]),
            g_attractor=len(g_keys), g_const_kind=kind,
            n_period_gt2=int((~per_le2).sum()),
        ))
    return rows


def commensurability_scan(ns=range(6, 21)) -> dict:
    """The falsification of the period-2 wall, as a reproducible table:
    for each ring size, which non-affine rules (outside the globally
    constant {4, 200}) hold G constant while carrying an attractor cycle
    of period > 2, and what those periods are."""
    table = {}
    for n in ns:
        hits = []
        for rule in range(256):
            if is_affine(rule) or rule in (4, 200):
                continue
            lut = rule_lut(rule)
            att = eventual_image_states(lut, n)
            if len(np.unique(state_keys(g_batch(att, lut), n))) != 1:
                continue
            s2 = apply_rule_batch(apply_rule_batch(att, lut), lut)
            gt2 = ~(s2 == att).all(axis=1)
            if not gt2.any():
                continue
            s0 = att[gt2][0:1]
            s, p = s0.copy(), 0
            while True:
                s = apply_rule_batch(s, lut)
                p += 1
                if (s == s0).all():
                    break
            hits.append(dict(rule=rule, period=p))
        table[str(n)] = hits
    return table


def check_shift_lemma(n: int = 10) -> bool:
    """G is shift-equivariant for every rule, and a ring has exactly two
    shift-invariant states -- together these force any attractor-constant
    value to be all-zeros or all-ones."""
    states = all_states(n)
    for rule in range(256):
        lut = rule_lut(rule)
        if not (g_batch(np.roll(states, 1, axis=1), lut)
                == np.roll(g_batch(states, lut), 1, axis=1)).all():
            return False
    n_invariant = int(sum(1 for s in states if (np.roll(s, 1) == s).all()))
    return n_invariant == 2


def check_covariance_lemmas(n: int = 10) -> bool:
    """G is reflection-covariant at the rule level but only
    conjugation-covariant up to bias terms (see module docstring)."""
    states = all_states(n)

    def refl_rule(r: int) -> int:
        lut, out = rule_lut(r), 0
        for i in range(8):
            l, c, rr = (i >> 2) & 1, (i >> 1) & 1, i & 1
            out |= int(lut[(rr << 2) | (c << 1) | l]) << i
        return out

    def conj_rule(r: int) -> int:
        lut, out = rule_lut(r), 0
        for i in range(8):
            out |= (1 - int(lut[7 - i])) << i
        return out

    for r in range(256):
        lp = rule_lut(r)
        if not (g_batch(states[:, ::-1], lp)[:, ::-1]
                == g_batch(states, rule_lut(refl_rule(r)))).all():
            return False
        cs = states ^ 1
        d = lambda X: X ^ apply_rule_batch(X, lp)
        e = lambda X: apply_rule_batch(X, lp)
        if not (g_batch(states, rule_lut(conj_rule(r)))
                == d(e(cs)) ^ (e(d(cs) ^ 1) ^ 1)).all():
            return False
    return True


def check_difference_lemma(n: int = 12) -> bool:
    """G == c identically on an attractor orbit iff X_{t+1} = phi(X_t) xor c
    with X_t = S_t xor S_{t+1}. Verified as an identity: for EVERY attractor
    state of every rule, G(S) xor [phi(S) xor phi^2(S)] == phi(S xor phi(S)),
    i.e. X_1 = phi(X_0) xor G(S) pointwise -- so constancy of G is exactly
    lawfulness of the difference sequence."""
    states = all_states(n)
    for rule in range(256):
        lut = rule_lut(rule)
        mask = eventual_image_mask(lut, n)
        att = states[mask]
        s1 = apply_rule_batch(att, lut)
        s2 = apply_rule_batch(s1, lut)
        x0, x1 = att ^ s1, s1 ^ s2
        if not (x1 == (apply_rule_batch(x0, lut) ^ g_batch(att, lut))).all():
            return False
    return True


def main() -> None:
    rows = []
    for n in NS:
        print(f"n={n} ...", flush=True)
        rows.extend(run_one_n(n))
    df = pd.DataFrame(rows)

    assert df.fp_lemma_ok.all(), "fixed-point lemma violated somewhere"
    assert check_shift_lemma(), "shift lemma violated"
    assert check_covariance_lemmas(), "covariance lemmas violated"
    assert check_difference_lemma(), "difference lemma violated"
    print("shift + covariance + difference lemmas verified (all 256 rules)")

    # ---- big-n wall probe: 16 and 18 exhaustive, 20 for still-constant rules
    bign_rows = []
    for n in (16, 18):
        print(f"big n={n} ...", flush=True)
        bign_rows.extend(run_bign(n, range(256)))
    const_at_18 = sorted(r["rule"] for r in bign_rows
                         if r["n"] == 18 and not r["affine"] and r["g_attractor"] == 1)
    print(f"big n=20 (the {len(const_at_18)} rules still constant at 18) ...", flush=True)
    bign_rows.extend(run_bign(20, const_at_18))
    bdf = pd.DataFrame(bign_rows)
    bdf.to_parquet(ROOT / "results" / "g_on_attractor_bign.parquet", index=False)

    # the wall: any NON-affine constant rule (outside globally-constant
    # {4, 200}) with attractor period > 2, at any big n? Affine rules are
    # exempt by the difference lemma (linear D rides the recursion) and DO
    # show constant G over long cycles -- report them separately as the
    # exemption check.
    const_gt2 = bdf[(bdf.g_attractor == 1) & (bdf.n_period_gt2 > 0)]
    affine_riders = sorted(const_gt2[const_gt2.affine].rule.unique().tolist())
    wall_breakers = const_gt2[~const_gt2.affine & ~const_gt2.rule.isin([4, 200])]
    globals_gt2 = sorted(const_gt2[const_gt2.rule.isin([4, 200])].rule.unique().tolist())
    const_at_20 = sorted(bdf[(bdf.n == 20) & (bdf.g_attractor == 1)].rule.tolist())

    print("commensurability scan (n=6..20) ...", flush=True)
    comm = commensurability_scan()

    out_parquet = ROOT / "results" / "g_on_attractor.parquet"
    df.to_parquet(out_parquet, index=False)

    # ---- analysis over the reference size and across n ----
    ref = df[df.n == 12].set_index("rule")
    nonaff = ref[~ref.affine]
    const_ref = nonaff[nonaff.g_attractor == 1]

    # survivors of the triviality cut: constant G on an attractor that
    # contains genuine cycles (period >= 2)
    surv_ref = const_ref[const_ref.max_period >= 2]

    # robustness: constant at EVERY n in NS
    by_rule = df[~df.affine].groupby("rule")
    always_const = sorted(r for r, grp in by_rule if (grp.g_attractor == 1).all())
    always_surv = sorted(r for r in always_const
                         if (df[(df.rule == r)].max_period >= 2).all())
    kinds = {r: sorted(df[(df.rule == r) & (df.g_attractor == 1)].g_const_kind.unique())
             for r in always_const}
    kind_stable = {r: k for r, k in kinds.items() if len(k) == 1}

    med_ratio = float((df[~df.affine].g_attractor / df[~df.affine].g_global).median())

    summary = dict(
        ns=NS,
        ns_big=[16, 18, 20],
        n_ref=12,
        wall_breakers=sorted(wall_breakers.rule.unique().tolist()),
        commensurability_scan=comm,
        affine_riders_gt2=affine_riders,
        globally_const_gt2=globals_gt2,
        nonaffine_const_at_n18=const_at_18,
        nonaffine_const_at_n20=const_at_20,
        nonaffine_const_at_n12=sorted(const_ref.index.tolist()),
        survivors_at_n12=sorted(surv_ref.index.tolist()),
        const_at_every_n=always_const,
        survivors_at_every_n=always_surv,
        const_kind_by_rule={str(r): kinds[r] for r in always_const},
        median_att_over_global_ratio=round(med_ratio, 4),
        const_kinds_ever_seen=sorted(df[df.g_const_kind != ""].g_const_kind.unique().tolist()),
        survivor_details=[
            dict(rule=int(r),
                 image=int(ref.loc[r, "image"]),
                 g_global=int(ref.loc[r, "g_global"]),
                 max_period=int(ref.loc[r, "max_period"]),
                 frac_fixed=float(ref.loc[r, "frac_fixed"]),
                 kind=str(ref.loc[r, "g_const_kind"]))
            for r in always_surv
        ],
    )
    out_json = ROOT / "site" / "src" / "data" / "g_on_attractor.json"
    out_json.write_text(json.dumps(summary, indent=1))

    print(f"\nTHE WALL (non-affine, outside {{4,200}}, constant G with a "
          f"period>2 attractor state at n in (16,18,20)): "
          f"{sorted(wall_breakers.rule.unique().tolist()) or 'NONE -- wall holds'}")
    print(f"  affine rules riding past period 2 (exempt, expected): {affine_riders}")
    print("  commensurability: wall-breakers by ring size --")
    for k, v in comm.items():
        if v:
            print(f"    n={k}: {[(h['rule'], h['period']) for h in v]}")
    print(f"non-affine constant at n=18: {len(const_at_18)}; still at n=20: {len(const_at_20)}")
    print(f"\nnon-affine, G constant on attractor at n=12: {len(const_ref)}")
    print(f"  of those, attractor has cycles (period >= 2): {len(surv_ref)}")
    print(f"constant at EVERY n in {NS}: {len(always_const)}")
    print(f"  surviving the triviality cut at every n:     {len(always_surv)}")
    print(f"  -> {always_surv}")
    print(f"constant kinds ever seen: {summary['const_kinds_ever_seen']}")
    print(f"kind stable across n for {len(kind_stable)}/{len(always_const)} rules")
    print(f"median attractor/global G-diversity ratio (non-affine, all n): {med_ratio:.3f}")
    print("\nsurvivor details at n=12:")
    for d in summary["survivor_details"]:
        print(f"  rule {d['rule']:3d}: image {d['image']:4d}, G global {d['g_global']:4d}, "
              f"max period {d['max_period']}, frac fixed {d['frac_fixed']:.2f}, -> {d['kind']}")


if __name__ == "__main__":
    main()
