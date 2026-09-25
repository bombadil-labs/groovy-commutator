# Rule composition: order, phase and periodic points

**Status:** exact elementary argument for arbitrary maps; no new experiment or
claim of mathematical priority. Inspected main `95570ba142edebb7db466ceb88f6d600da8db868`.
The immediate question was whether composing two ECA rules in opposite orders
can create different recurrent organization. The answer depends on the
observable: their finite-ring recurrent **cycle structure is identical**, but
their states, transients and same-source trajectories need not agree.

## Three different operations

Write `A=E_a` and `B=E_b` for synchronous whole-configuration ECA maps.

1. **Sequential:** `F=B∘A`, `F'=A∘B`. Each is a 1D CA of radius at most two,
   generally no longer an ECA. An alternating schedule needs one clock bit to
   specify intermediate-step phase; `F` and `F'` are its two-step views.
2. **Output XOR:** `E_a(s) XOR E_b(s) = E_(a XOR b)(s)` is an ECA evaluated
   once on the *same* state, not sequential composition. In particular
   `D_r=E_(r XOR 204)`, so the existing `G_r` is exactly the existing
   `cross_commutator` of `E_r` and `E_(r XOR 204)`.
3. **Local selection:** a per-cell choice between `a` and `b` is a 4-input
   table with selector bit `x_i`, as `src/groovy/prehoc.py` already explains.
   Where that bit comes from, when it is available, and how it is stored and
   coordinated determine the actual system. It is neither `F` nor `F'`.

Prior work already studies ECA composition and composition-closed families:
Castillo-Ramirez and Magaña-Chavez, *A study on the composition of elementary
cellular automata* (2023; published 2025),
<https://arxiv.org/abs/2305.02947>. The code's `cross_commutator` and the five
empirical pair regimes in `NOTES.md` predate this note. No unrestricted
ordered-pair census is proposed here.

## Exact phase theorem

For **any** self-maps `A,B:X→X`, put `F=B∘A`, `F'=A∘B`. Then

```
A∘F = F'∘A;                 B∘F' = F∘B.
```

The first identity sends every periodic point of `F` to a periodic point of
`F'`. On periodic points it is one-to-one: if `A(x)=A(y)`, then
`F(x)=F(y)`; applying a common power of `F` that fixes both `x` and `y`
gives `x=y`. It is onto: if `(F')^k(y)=y`, take
`x=B((F')^(k-1)(y))`. Then `A(x)=y` and `F^k(x)=x`. Thus `A` is a
bijection between the periodic-point sets, conjugating their restricted
dynamics. It preserves **exact least periods** and therefore the number of
cycles of every length. No invertibility of either rule is assumed. The
statement holds even on an infinite configuration space *for periodic
points*, but it does not imply a topological conjugacy of the full systems.

On a finite ring of width `n`, let `P_k(F)` be the number of states fixed by
`F^k`. The theorem gives `P_k(F)=P_k(F')` for every `k≥1`, hence identical
finite-ring dynamical zeta functions
`ζ_F(z)=exp(Σ_(k≥1) P_k(F) z^k/k)`. This is a general cyclic-phase identity,
not evidence for a prime-specific mechanism. Cyclic rotations of any fixed
multi-rule schedule have the same periodic-point counts by applying the
two-factor statement to its first map and the composition of its other maps.

**Boundary example.** Rules 0 and 255 are constant maps. The two orders give
the constant-zero and constant-one maps respectively: distinct fixed *states*
and maximum same-state disagreement, but one fixed point each and no other
cycles. The conjugating map collapses the state space off its periodic part.
More elaborate rules can likewise have different transient and basin data,
different physical patterns, and different costs, even when cycle counts
match. The existing `divergence_trajectory` compares both orders starting
from the *same* input; the theorem pairs the recurrent states by a one-step
phase map instead. Neither statement invalidates the other.

## A three-rule permutation escapes that constraint

We [froze the rules, orders and widths](protocols/2026-09-25-three-rule-order.md)
in the repository at commit `736af639bbaad39ad3c30ef909f5d753976fbb9c`.
The published, independently verified runner follows at
`a53d95d504d09802227c7ef6e10f8d1f5222e7db`, before the saved result.
Every transition was computed both with the library's vectorized ECA step
and an independent scalar truth-table step; cycles were counted with two
independently organized algorithms. The result is [canonical JSON](../../results/three_rule_order_20260925.json)
(SHA-256 `9fd6af4bb8627c2777aa1602adf3711b6d40e41506da43165e94d0106c12dbbe`).

Each order lists its *first* rule first. Entries count cycles by **least**
stroboscopic period:

| Ring width | 30, 54, 110 | 30, 110, 54 | 54, 110, 30 |
| --- | --- | --- | --- |
| 4 | 5 of period 1; 1 of period 4 | 5 of period 1 | same as first order |
| 6 | 7 of period 1; 2 of period 9 | 1 of period 1; 1 of period 6 | same as first order |
| 8 | 5 of period 1; 3 of period 4 | 5 of period 1; 2 of period 4; 1 each of periods 8 and 16 | same as first order |

This is a **finite-ring counterexample** to extending cyclic phase
invariance to arbitrary three-rule permutations. It does not say any schedule
is more complex or useful; the rules and widths were selected in advance,
but there is no independently specified task or held-out ring. It also
does not imply analogous orbit counts on the infinite line.

The mechanism admits a concise identity. Let `A` be the first map, `B` and
`C` the other two; define their order defect
`K_(B,C)(u)=C(B(u)) XOR B(C(u))`. Then

```
(C∘B∘A)(s) XOR (B∘C∘A)(s) = K_(B,C)(A(s)).
```

Thus the schedules are **identical maps** exactly when `B` and `C` commute on
`A(X)`, their first rule's reachable image. They can fail to commute on
the full state space while their order is unobservable after `A` erases the
distinguishing states. Conversely source word `1` witnesses different
outputs for the frozen orders at widths 4, 6 and 8. The identity says when
the complete maps agree; differing maps may still have equal cycle counts.

This gives a representation question: *which distinctions in a first
rule's image allow subsequent rule order to remain observable?* It needs an
independently chosen source family or output task before searching for a
favorable prefix. A first rule costs an evaluation; it is not free
coarse-graining.

Every three-rule stroboscopic composition is also a single ordinary 1D
radius-at-most-three CA: its next bit reads at most seven source bits.
A fused lookup can store up to 128 output entries; the unfused schedule
stores three eight-entry ECA tables and performs three local updates.
These are different storage, access, computation and latency contracts, not
evidence that either presentation wins. The fused rule matches only the
three-step samples; exposing *intermediate* rows requires a phase counter
and the corresponding update choices. Any proposed benefit from the
three-rule sequence must compare against this exact fused baseline.

## Decision

Do not search for an advantage of `AB` over `BA` based solely on finite-ring
cycle counts or dynamical zeta: the result is fixed in advance by phase.
Same-source disagreement, transient basins, spatial pattern and task output
remain different observables; noncyclic three-rule permutations may also
change cycle structure. A next unit needs an independently specified task,
a phase-matched comparison, and a baseline that accounts for rule
evaluations, clock or controller state, local access and observations.
Local selection is already a separate four-input construction in this repo:
a same-time radius-one selector computed from the source collapses to an
ordinary ECA, whereas a stored-history or independently evolving selector
adds a real state coordinate. No local-selection outcome is established by
the present enumeration. The closed one-shot Rule-54 repair benchmark
supplies no new task. This note ends this bounded composition unit.
