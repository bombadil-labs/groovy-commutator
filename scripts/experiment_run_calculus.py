"""The run calculus: verify the laws that make `base` an honest parameter.

Two primitives (src/groovy/operators.py):

    orbit(base, S0)[t]      = base^t(S0)         the only iteration anywhere
    run(gauge, base, S0)[t] = gauge(base^t(S0))  one gauge evaluation per row

with engine(F) := run(F, F) as the reflexive case. Claims verified here,
each a hard assert (all exact except the two measured disagreements):

1. The raw spacetime diagram is run(identity, E) -- even the plainest
   picture has a base; it was just set to invisible values.
2. run(D(.,psi), E_phi) with psi != phi (the Explorer's decoupled D card)
   is a genuinely different field from the matched psi == phi gauge.
3. Re-anchoring: run(g o base, base)[t] == run(g, base)[t+1], exact --
   and its engine analog is FALSE (the identity is a theorem of the gauge
   stance, not of the maps).
4. Linearity: run(f XOR g, base) == run(f, base) XOR run(g, base) for any
   gauges (so the G-gallery IS the (D o E)-gallery XOR the (E o D)-gallery
   row for row). Engines break it, with our own operators as the minimal
   counterexample: E XOR D == identity as maps, yet
   engine(E) XOR engine(D) != engine(identity) (~0.48 mean disagreement).
5. engine(F) == orbit(F) shifted one row (a source card is already an
   engine; an engine is a source card whose rule is a composite), and
   U[0] == G(S0) -- the two stances agree for exactly one step, then
   diverge (~0.48 by row 5).

These laws are the backbone of the Concepts page's #run section; the
gauge/engine formalization writeup is in NOTES.md.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from groovy import apply_rule, identity, orbit, run  # noqa: E402

PHI = 110
N, T = 64, 64
SEED = 7


def main() -> None:
    rng = np.random.default_rng(SEED)
    s0 = rng.integers(0, 2, N).astype(np.uint8)

    def E(s):
        return apply_rule(s, PHI)

    def Dmap(s, psi=PHI):
        return s ^ apply_rule(s, psi)

    def compose(f, g):
        return lambda s: f(g(s))

    def engine(f):
        return run(f, f, s0, T)

    ED = compose(E, Dmap)          # E o D
    DE = compose(Dmap, E)          # D o E

    # 1. raw diagram = run(identity, E)
    assert np.array_equal(run(identity, E, s0, T), orbit(E, s0, T))
    print("1. run(identity, E) == orbit(E): the raw diagram is a run")

    # 2. decoupled ingredient slot: D(.,30) on E_110's orbit is a new object
    matched = run(Dmap, E, s0, T)
    crossed = run(lambda s: Dmap(s, 30), E, s0, T)
    assert not np.array_equal(matched, crossed)
    print("2. run(D(.,30), E_110) != run(D(.,110), E_110): psi is a real slot")

    # 3. re-anchoring holds for gauges, has no engine analog
    assert np.array_equal(run(DE, E, s0, T), run(Dmap, E, s0, T + 1)[1:])
    assert not np.array_equal(engine(ED), run(Dmap, Dmap, s0, T + 1)[1:])
    print("3. run(D∘E, E)[t] == run(D, E)[t+1] exact; engine analog false")

    # 4. linearity in the gauge; engines shred it via E XOR D == identity
    f_xor_g = lambda s: DE(s) ^ ED(s)  # noqa: E731 -- this IS the map G
    assert np.array_equal(run(f_xor_g, E, s0, T), run(DE, E, s0, T) ^ run(ED, E, s0, T))
    assert np.array_equal(run(lambda s: E(s) ^ Dmap(s), E, s0, T), run(identity, E, s0, T))
    eng_xor = engine(E) ^ engine(Dmap)
    frozen = engine(identity)
    assert not np.array_equal(eng_xor, frozen)
    dis = float((eng_xor ^ frozen).mean())
    assert dis > 0.3, dis
    print(f"4. run linear in gauge; engines break it (mean disagreement {dis:.3f})")

    # 5. engine(F) == orbit(F) shifted; U[0] == G(S0); stances then diverge
    assert np.array_equal(engine(ED), orbit(ED, s0, T + 1)[1:])
    U = engine(DE) ^ engine(ED)
    Ggal = run(f_xor_g, E, s0, T)
    assert np.array_equal(U[0], f_xor_g(s0))
    assert not np.array_equal(U, Ggal)
    row5 = float((U[5] ^ Ggal[5]).mean())
    assert row5 > 0.3, row5
    print(f"5. engine == shifted orbit; U[0] == G(S0); row-5 divergence {row5:.3f}")

    print("all run-calculus laws verified")


if __name__ == "__main__":
    main()
