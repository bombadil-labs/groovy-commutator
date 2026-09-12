# Protocol: dimensional history scaling under a codimension-one shadow — 2026-09-12

**Status:** frozen before implementation/evaluation. Nothing in this protocol has been run.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** pending independent Gate 1 on the exact integrated gathering head. No implementation or evaluation is authorized before Gate 1.

## 1. Question

The accepted touching-strip result found one finite 2D representation in which zero and one retained lags do not determine the next complete retained field, while two retained lags do for a small set of masks. That is **not** evidence that spatial dimension `d` generally requires history depth `h=d`.

This unit asks a deliberately cleaner cross-dimensional control:

> For one dimension-uniform linear CA family, when a `d`-dimensional state is observed only through one codimension-one slice, what is the minimum retained history depth required for the complete observed slice to determine its next slice?

The user's conjecture is frozen as a falsifiable bet:

`h_min(d) = d` for `d = 1,2,3`,

where `h` is the number of retained previous observations in addition to the current one. Thus `h=2` means the three-time stack `(Y_t,Y_{t-1},Y_{t-2})`.

A failure is a result, not a reason to alter the observation or choose another rule after inspection.

## 2. Why a separate matched control is needed

The existing interface-history result is physically 2D but does not provide matched 1D and 3D instances of the same observation/interpreter recipe. It therefore supplies motivation only.

This protocol uses a family where exact full-state evolution and exact observability can be decided by finite GF(2) linear algebra without sampling or fitting. That makes it a discriminating control for the proposed dimension/history law, not a claim that the chosen linear family is the Turtle Beam itself.

## 3. Frozen dynamics

Use the accepted guard-free ordered-axis constructor with ECA Rule 90 as the source rule.

For dimension `d`, one macro-step `F_d` applies Rule 90 once along each axis in the fixed accepted axis order. Because Rule 90 is linear over GF(2), `F_d` is a linear map.

Evaluate periodic boxes

`X_{d,n} = GF(2)^((Z/nZ)^d)`

for

- dimensions `d in {1,2,3}`;
- odd side lengths `n in {5,7}`.

Odd sizes avoid the most immediate power-of-two parity degeneracies while keeping the exact matrices small (`7^3 = 343` state bits). The two sizes are separate exact controls; do not pool them into one fitted law.

## 4. Frozen observation

For each `(d,n)`, observe the complete codimension-one slice at newest-axis coordinate zero:

`O_d(X) = X[..., x_d = 0]`.

For `d=1`, this is one distinguished site. For `d=2`, it is one complete line. For `d=3`, it is one complete plane.

The observation is fixed before evaluation and is not widened after a failure. It is intentionally lossy for `d>=1`.

## 5. Exact history-closure criterion

For a history depth `h >= 0`, define the stacked observation operator

`H_h = [O_d ; O_d F_d ; ... ; O_d F_d^h]`.

The next observed slice is uniquely determined by the retained history for **all full states** iff

`ker(H_h) subseteq ker(O_d F_d^(h+1))`.

Equivalently over GF(2),

`rowspan(O_d F_d^(h+1)) subseteq rowspan(H_h)`.

This is an exact full-state criterion, not a finite-state sample.

Define

`h_min(d,n) = min { h : the criterion holds }`

if it holds for some `h <= H_max`, with frozen cap

`H_max = 8`.

If no depth through 8 closes, report `>8`; do not extend the cap in this unit.

## 6. Frozen predictions

### P1 — implementation controls

Independent bit-matrix and basis-vector implementations of `F_d`, `O_d`, matrix powers, ranks and kernel-inclusion verdicts agree for every `(d,n,h)`.

Rule-90 local evolution must match the accepted CA implementation on exhaustive basis states and a deterministic set of composite states. Any mismatch blocks interpretation.

### P2 — primary dimension/history bet

For both `n=5` and `n=7`:

- `h_min(1,n) = 1`;
- `h_min(2,n) = 2`;
- `h_min(3,n) = 3`.

This is intentionally strong. If ring size rather than dimension controls the minimum, or if no simple monotone law appears, the conjecture fails.

### P3 — monotonic dimension bet

Independently of P2's exact values, freeze the weaker prediction

`h_min(1,n) <= h_min(2,n) <= h_min(3,n)`

for each tested `n`, treating `>8` as larger than any finite scored depth.

Report P2 and P3 separately; P3 surviving does not rescue a failed P2.

### P4 — rank-increment diagnostic

For every cell, report the rank sequence

`rank(H_0), rank(H_1), ..., rank(H_8)`

and the first depth at which the next-slice rows enter the accumulated row span. These are exact descriptive diagnostics, not new post-hoc predictions.

## 7. Interpretation

Allowed interpretations are narrow:

- P2 pass: this one codimension-one observation of this linear dimension-uniform family has the proposed `1,2,3` history law on both declared tori.
- P2 fail: the current empirical `h=2` touching-strip result does not generalize even to this clean control in the proposed way.
- P3 pass with P2 fail: history requirement may grow with dimension here without equalling dimension.
- size dependence: periodic geometry is materially involved and no dimension-only scaling law is supported.

No outcome establishes an intrinsic dimension, a general space/time equivalence, or that a spatial dimension literally *is* a memory step.

## 8. Relation to the Turtle Beam

The motivating idea is that information simultaneous in a higher-dimensional state may appear as temporal hidden state under a lower-dimensional shadow. A possible beam would then spatialize information that a shadow must carry as history.

This protocol tests only the first clean scaling question. It does not test endogenous resonance, self-recognition, self-assembly, or semantic program inheritance.

## 9. Nulls and non-claims

Mandatory boundaries:

- linear Rule 90 is a control family, not a selected universal model;
- codimension-one slice observation is one representation choice;
- finite odd tori `n=5,7` are not the infinite lattice;
- `H_max=8` is a declared censoring bound;
- a history-closure result is information sufficiency, not locality of the induced factor;
- no `8n+1`, prime, Class-IV, intrinsic-dimension, spacetime-emergence, metaphysical, consciousness or Buddhist-doctrinal claim;
- the accepted 2D touching-strip result remains separate evidence and is not retrofitted as the `d=2` datum of this matched experiment.

## 10. Required implementation after Gate 1

Pin, before evaluation:

1. a GF(2) packed-bit matrix constructor for `F_d` and `O_d`;
2. an independent basis-action constructor for the same operators;
3. exact Gaussian-elimination rank and row-span inclusion without floating point;
4. deterministic hashes of every operator and rank table;
5. a verifier emitting one canonical result JSON;
6. permanent two-tier integrity/replay CI with a green no-result implementation stage.

Implementation-only/no-result must merge green before the first scored matrix census.

## 11. Gate-1 questions

The independent reviewer should attack especially:

1. Is codimension-one slice observation a scientifically useful matched shadow, or is it too arbitrary to test the user's scaling conjecture?
2. Is Rule 90 a fair dimension-uniform linear control, or would its algebra decide the answer so strongly that the experiment becomes tautological?
3. Are odd `n=5,7` sufficient controls against small-ring aliasing for this exact finite test?
4. Is `h_min` defined by kernel inclusion the correct all-state notion of observed-history sufficiency?
5. Is `H_max=8` defensible and honestly censored?
6. Is the exact P2 `1,2,3` bet genuinely open before evaluation?
7. Does `d=1` as a one-site observation make the cross-dimensional comparison malformed?
8. Are the P2/P3 interpretations and non-claims strong enough?

Binding changes to dynamics, dimensions, side lengths, observation, history cap, scoring or predictions require renewed exact-head Gate 1 before evaluation.