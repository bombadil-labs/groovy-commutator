# Protocol: typed difference geometry of the affine-oriented lift

**Status:** frozen before canonical implementation/evaluation on 2026-10-06.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-06. **Reviewed by:** none.

## Why this unit exists

OpenAI's 2026-10-06 math release suggested asking whether the dimensional lift can
be understood as an extension of dynamical systems and whether Groovy's `G`
is a cocycle or section/evolution obstruction. The current repository already
contains stronger relevant evidence than the initial handoff noticed:
`2026-09-17-affine-oriented-lift-theorem.md` proves the beam intertwining
identity and its verifier Section E records an affine-jet residual
`(0,0,K1,K2,0,0)`, with `K1 = G`, plus a horizon recurrence.

That existing evidence changes the first question. For the canonical marked-beam
section `L`, the theorem states

```
H_up(L(X)) = L(H(X)).
```

Therefore the naive section/evolution defect is exactly zero on the beam. This
unit will not relabel zero as `G`. It asks what nearby typed defect the old
residual actually measures.

## Pre-freeze exploratory orientation

Before freezing this protocol, the author:
- read the existing lift theorem, verifier and canonical result;
- algebraically noticed that the canonical section/evolution defect vanishes by
  the already-proved intertwining identity;
- ran a non-canonical scratch check on Rules 4 and 200 indicating that their
  centered horizon residual remains zero through horizons 1..7 on the 7-ring,
  and that one ad hoc dynamic third-cross-effect probe also vanishes.

Those scratch observations are post-hoc orientation, not canonical evidence and
will not be presented as pre-registered predictions.

## Definitions to test

Let `V` be a Boolean configuration space and `H: V -> V`.

Define the finite difference of `H` at basepoint `x` in displacement `u`:

```
partial_H(x,u) = H(x XOR u) XOR H(x).
```

Define the dynamical displacement

```
d_H(x) = x XOR H(x).
```

Define the centered point action

```
H0(u) = H(u) XOR H(0).
```

and polarization

```
B_H(x,u) = H(x XOR u) XOR H(x) XOR H(u) XOR H(0).
```

For the affine-oriented jet encoding `L1`, define its centered form

```
J_H(x) = L1_H(x) XOR L1_H(0).
```

All XORs are fibrewise Boolean addition on the declared finite domain.

## Gate A — kill or preserve the original cocycle hypothesis

Derive from the actual lift theorem whether

```
H_up(L1_H(x)) XOR L1_H(H(x))
```

is nonzero anywhere on the canonical marked beam.

**Prediction A1:** it is identically zero by intertwining.  
**Decision:** if A1 holds, `G` is not the canonical section/evolution defect;
do not pursue that identification further.

## Gate B — typed-difference identity

Derive, then verify independently, the identities

```
partial_H(x, d_H(x)) = d_H(H(x))
G_centered(x) = partial_H(x,d_H(x)) XOR partial_H(0,d_H(x))
              = B_H(x,d_H(x)).
```

**Prediction B1:** both are exact for every Boolean map, not ECA-specific.

Interpretation to test, not assume: centered `G` measures the error made by
identifying the tangent/difference action at basepoint `x` with the same
difference action at the origin. In this reading, the missing coordinate is
the basepoint.

## Gate C — cross-effect of the lift section

For the six fields

```
F0 = X XOR tau_+ X
F1 = 1 XOR X XOR tau_- X
F2 = X XOR H(X)
F3 = X XOR H^2(X)
F4 = 0
F5 = X,
```

derive the second cross-effect of the centered encoding `J_H`.

**Prediction C1:**

```
cr2(J_H)(X,Y)
 = (0, 0, B_H(X,Y), B_(H^2)(X,Y), 0, 0).
```

**Prediction C2:** along `Y = H(X)`, the temporal rows are the centered horizon
residuals

```
(B_H(X,HX), B_(H^2)(X,HX))
 = (K1 XOR H(0), K2 XOR H^2(0)).
```

where

```
Kt = d_H(H^t X) XOR H^t(d_H X).
```

Verification domain: all 256 ECAs, exhaustive states on at least rings 5, 6
and 7, with tiny rings handled separately if periodic aliasing changes local
dependencies. Prefer direct local truth-table equality where possible.

## Gate D — what kind of cocycle is the horizon recurrence?

Start from the existing exact recurrence rather than importing group-cohomology
notation:

```
K_(t+1)
 = G(H^t X) XOR partial_H(H^t(d_H X), K_t)
```

using the repository's finite-difference convention.

Derive it from pair/difference dynamics. Determine whether it is:
1. an ordinary additive cocycle under a fixed linear fibre action;
2. a cocycle only after enlarging the base to retain the transported point or
   displacement;
3. more naturally a skew-product / pair-groupoid transport law and should not
   be called a cocycle without qualification.

**Prediction D1:** nonlinear rules require basepoint-dependent fibre transport;
the affine case collapses to a fixed linear action.

No terminology will be promoted until a literature check.

## Gate E — third cross-effects are a falsification probe, not a promised layer

For ECA local rules, calculate ANF degree and exact second/third cross-effects.
Ask whether any structure missed by graph-restricted `B` (notably Rules 4 and
200) becomes visible under a principled third-order trajectory-derived probe.

Do not search arbitrary formulas. Freeze at most three probes derived from the
difference-bundle or jet identities before evaluation. A negative result ends
this gate.

## Evidence and stopping rules

- Exact algebra beats simulation.
- Finite sweeps are verification/counterexample search, not the proof premise.
- Save tiny counterexamples when a proposed identity fails.
- Preserve the distinction between the canonical beam section, an encoding
  cross-effect, and native descendant `G`.
- Do not infer orbit complexity, Wolfram class, resource advantage or lift
  optimality from any algebraic identity here.
- Stop the unit once Gates A-D are settled and Gate E is either one bounded
  result or a clean negative. Do not turn it into another all-rule metric hunt.

## Planned artifacts

- `scripts/experiment_typed_lift_defect.py`
- `results/typed_lift_defect_20261006.json`
- one research note giving derivations, exact checks, limits and terminology
- update to `FINDINGS.md` only if the unit changes the accessible synthesis

