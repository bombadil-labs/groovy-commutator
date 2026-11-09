# Frozen Gate-E probes: dynamic third cross-effects

**Status:** frozen 2026-10-06 before the canonical Gate-E evaluation.  
**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

This supplement instantiates the "at most three" trajectory-derived probes allowed
by the parent protocol. The earlier scratch probe of `cr3(H)(X,HX,H^2X)` on
Rules 4 and 200 was already observed before the parent protocol freeze, so its
4/200 outcome is explicitly post-hoc. It is retained here only so the bounded
comparison has three geometrically related coordinates and its provenance is
clear.

Let `U = d_H(X) = X XOR H(X)` and let

```
T_X(U) = partial_H(X,U) = H(X XOR U) XOR H(X)
```

be typed finite-difference transport. The three frozen probes are:

1. **Orbit triad**
   `C3_orbit(X) = cr3(H)(X, H(X), H^2(X))`.
   For Rules 4/200 this probe's zero outcome on the 7-ring was already seen in
   scratch work; all-rule counts and other domains remain unevaluated.

2. **Raw-displacement triad**
   `C3_raw(X) = cr3(H)(X, U, H(U))`.
   This follows the same mistaken point-action route whose second-order defect
   is centered G.

3. **Typed-displacement triad**
   `C3_typed(X) = cr3(H)(X, U, T_X(U))`.
   By the Gate-B identity, the third argument equals `d_H(HX)`; this follows
   the correctly typed transported displacement.

No threshold or ranking is permitted. For each probe record only whether it is
identically zero on the exhaustive finite domain and whether it distinguishes
the known nonlinear self-flat Rules 4/200 from affine rules. If none does,
Gate E ends as a negative result. We do not invent a fourth probe in this unit.

Separately, calculate the unrestricted local `cr3` and ANF degree for every ECA
truth table. This is an algebraic control: it determines whether a zero dynamic
probe means "no cubic term" or merely "the selected trajectory directions do
not encounter it."
