"""The groovy commutator: D (differentiate), E (evolve), C (compare), and G
(the commutator), for a single rule -- plus the cross-rule generalization to
pairs of rules.

Single-rule construction (phi = an elementary CA rule):
    D(S) = S XOR phi(S)            differentiation
    E(S) = phi(S)                  evolution (I is trivial for elementary CA)
    G(S) = C(D(E(S)), E(D(S)))     the commutator

G(S) is literally the operator commutator [D, E] evaluated at the state S.
See NOTES.md for the derivation of the affine theorem (G(S) is constant
across all S iff phi is GF(2)-affine) and its correspondence to kinematic
vs. dynamical commutators in quantum mechanics.

Cross-rule construction (phi_a, phi_b = two different rules):
    cross_commutator(S) = C(phi_a(phi_b(S)), phi_b(phi_a(S)))
        -- does composition order matter, at this S?
    divergence_trajectory(S0, ...) -- two divergent unfoldings of the SAME
        initial state under the two different orderings, watched over time.
        This is the construction that produced the five empirical pair
        regimes documented in NOTES.md (commute / crystalline / noise /
        structured / drain).

Run calculus (orbit / run / identity):
    orbit(base, S0)[t]      = base^t(S0)        -- the ONLY place iteration lives
    run(gauge, base, S0)[t] = gauge(base^t(S0)) -- one gauge evaluation per row

Every spacetime picture is a run: the raw diagram is run(id, E) (the
identity gauge riding base E), the D-gallery is run(D(.,phi), E_phi), and
the "engine stance" -- a map fed its own output -- is the reflexive case
run(F, F), which equals orbit(F, S0) shifted one row. The laws, verified
in scripts/experiment_run_calculus.py:

    linearity     run(f XOR g, base) = run(f, base) XOR run(g, base)
                  (pointwise, exact, for ANY gauges f, g)
    re-anchoring  run(g o base, base)[t] = run(g, base)[t+1]
                  (a gauge-stance theorem; it has NO engine analog)
    breakage      engines are NOT linear: E XOR D = id identically, yet
                  run(E,E) XOR run(D,D) != run(id,id). The remainder-rule
                  question R(A,B) (NOTES.md) is exactly "when is the XOR
                  of two engine runs itself an engine run?"

Notation: in prose/math displays the identity map is written with the
blackboard one (U+1D7D9), NOT `I` -- `I` is integration (trivial for
elementary CA, a different reason to do nothing than identity's
by-definition triviality).
"""
from __future__ import annotations
from typing import Callable
import numpy as np
from .ca import apply_rule
from .metrics import absential_field

StateMap = Callable[[np.ndarray], np.ndarray]


def C(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Comparison operator. XOR over GF(2)."""
    return np.bitwise_xor(a, b)


def D(state: np.ndarray, rule_num: int) -> np.ndarray:
    """Differentiation: S XOR phi(S)."""
    return C(state, apply_rule(state, rule_num))


def E(state: np.ndarray, rule_num: int) -> np.ndarray:
    """Evolution: phi(S)."""
    return apply_rule(state, rule_num)


def G(state: np.ndarray, rule_num: int) -> np.ndarray:
    """Single-rule commutator: C(D(E(S)), E(D(S)))."""
    return C(D(E(state, rule_num), rule_num), E(D(state, rule_num), rule_num))


def cross_commutator(state: np.ndarray, rule_a: int, rule_b: int) -> np.ndarray:
    """C(phi_a(phi_b(S)), phi_b(phi_a(S))) -- does composition order matter
    between two DIFFERENT rules, at this S?"""
    ab = apply_rule(apply_rule(state, rule_b), rule_a)
    ba = apply_rule(apply_rule(state, rule_a), rule_b)
    return C(ab, ba)


def identity(state: np.ndarray) -> np.ndarray:
    """The do-nothing map (the blackboard-one of the run calculus).

    Named because it has the same State -> State type as every gauge, so
    it can fill the gauge slot: run(identity, E) IS the raw spacetime
    diagram. Distinct from integration I(a, b) = a XOR b, which is a real
    operation that merely happens to be trivial for elementary CA."""
    return state


def orbit(base: StateMap, state0: np.ndarray, steps: int) -> np.ndarray:
    """The trail one map leaves when fed its own output.

    orbit(base, S0)[t] = base^t(S0); rows 0..steps, shape (steps+1, n).
    This is the only primitive that iterates -- E, D, G and every gauge
    fire once per row. `base` is any State -> State callable, so orbits
    of composites (the engine stance: run(F, F) = orbit(F)[1:]) work the
    same as orbits of elementary rules. For a plain rule-phi orbit pass
    base=lambda s: apply_rule(s, phi)."""
    rows = np.zeros((steps + 1, len(state0)), dtype=np.uint8)
    rows[0] = state0
    for t in range(steps):
        rows[t + 1] = base(rows[t])
    return rows


def run(gauge: StateMap, base: StateMap, state0: np.ndarray, steps: int) -> np.ndarray:
    """A gauge evaluated along a base's orbit: run(gauge, base, S0)[t] =
    gauge(base^t(S0)), shape (steps+1, n).

    The two stances of the project are the two ways to fill the slots:
    gauge stance = run(F, E) (F measured along E's clockwork), engine
    stance = run(F, F) (F is its own base). Laws -- linearity in the
    gauge, the re-anchoring identity, and their failure under
    reflexivity -- are stated in the module docstring and verified in
    scripts/experiment_run_calculus.py."""
    return np.stack([gauge(row) for row in orbit(base, state0, steps)])


def absential_trajectory(state0: np.ndarray, rule_num: int, steps: int) -> np.ndarray:
    """Evolve state0 under a single rule for `steps`, recording the
    absential field (metrics.absential_field) at each step instead of the
    raw state. Feed the result to classify.compressibility for a cheap
    structure/noise diagnostic on the "off but adjacent to alive" view --
    candidate fast Class-IV detector: a still life's absential ring should
    be small and frozen, a Class III pattern's absential field should churn
    at high density with no structure, and a glider's absential field
    should trace a compressible, persistent moving shape."""
    n = len(state0)
    state = state0.copy()
    field = np.zeros((steps, n), dtype=np.uint8)
    for t in range(steps):
        field[t] = absential_field(state)
        state = apply_rule(state, rule_num)
    return field


def divergence_trajectory(state0: np.ndarray, rule_a: int, rule_b: int, steps: int) -> np.ndarray:
    """Two divergent unfoldings from one shared initial state:
    path1 repeats (apply A, then B); path2 repeats (apply B, then A).
    Returns the disagreement field over time, shape (steps, n)."""
    n = len(state0)
    path1, path2 = state0.copy(), state0.copy()
    field = np.zeros((steps, n), dtype=np.uint8)
    for t in range(steps):
        field[t] = C(path1, path2)
        path1 = apply_rule(apply_rule(path1, rule_a), rule_b)
        path2 = apply_rule(apply_rule(path2, rule_b), rule_a)
    return field
