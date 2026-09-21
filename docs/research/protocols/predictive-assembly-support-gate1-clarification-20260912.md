# Gate-1 clarification: predictive assembly support — 2026-09-12

**Status:** binding protocol-only clarification before implementation.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Parent protocol:** `docs/research/protocols/predictive-assembly-support-20260912.md`.  
**Reviewed head:** `4acaef8b31c73f064e09b57a253bd4f4108c6bfc`.  
**Independent reviewer:** Claude Code / Fable 5.1, PR #172 Gate-1 review.  
**Gate decision:** approved on the reviewed head conditional only on the clarifications below being recorded before implementation; the reviewer explicitly said these do **not** require renewed Gate 1 because they do not change the predecessor domain, atom set, target, objective, or content of the remaining open predictions.

Nothing in this clarification authorizes evaluation. Implementation must still be pinned in a separate implementation-only/no-result stage before any PAS value is computed.

## 1. Name the combinatorial object accurately

`PAS_raw` is the minimum-cardinality **reduct / Minimum Test Collection** of the frozen finite decision table induced by the accepted #157 records. Equivalently, it is a minimum hitting set of the conflict-difference family: a support is prediction-sufficient iff it intersects every coordinate-difference set belonging to a pair of records with different targets.

This exact combinatorial identification is part of the interpretation. “Predictive assembly support” is the program-local name for the spacetime atomization and resource question; it is not claimed as a new general combinatorial primitive and is not Lee Cronin's molecular assembly index.

It is also **not** a measure of state complexity, information content, Shannon entropy, algorithmic/Kolmogorov complexity, thermodynamic cost, molecular assembly, or intrinsic dimension.

## 2. P2 lower bound is a predecessor deduction

For every one of the nine accepted global-pass cells, the same `D2` cell at `h=0` conflicts in #157. Therefore the next retained field is not constant over the declared record set, and

`PAS_raw > 0`

is **deduced**, not a fresh bet.

The genuinely open P2 content is only the strict upper bound

`PAS_raw < N_full`,

where

`N_full = 3 * n * (2 + popcount(mask))`.

The nine full atom counts are:

- ring 6, masks 11/13: `N_full=90`;
- ring 6, mask 15: `N_full=108`;
- ring 7, masks 3/5: `N_full=84`;
- ring 7, masks 7/11/13: `N_full=105`;
- ring 7, mask 15: `N_full=126`.

## 3. P3 is a deduced lag-2 consistency control

For all nine accepted global-pass cells, the same `D2` cell at `h=1` conflicts in #157. Any support containing no lag-2 atom is a subset of the complete one-lag history key, so the accepted h=1 conflict pair agrees on that support while requiring different targets.

Therefore **every** prediction-sufficient support, minimum or otherwise, must contain at least one lag-2 atom.

P3 is relabelled from a scientific bet to a **deduced consistency control** over all nine cells. A P3 failure is an implementation/provenance error, not a scientific outcome. Delete any interpretation that P3 is stronger than the predecessor result.

## 4. P5: lag-0 case deduced; lag-1/lag-2 cases remain open

A support restricted to the current-time (`lag 0`) translation orbits cannot be sufficient, because the accepted `D2,h=0` conflict already agrees on the complete current retained field and differs in target.

Thus the lag-0-only case of P5 is a predecessor deduction.

Whether a translation-orbit support using **only lag 1** or **only lag 2** can be sufficient is not decided by the accepted history ladder and remains the frozen open content of P5. These restricted cases should be solved directly as restricted exact orbit problems; do not infer them by enumerating every global minimum.

## 5. P1 predecessor replay does not compare nonexistent target hashes

The accepted #157 result stores source hashes and census/witness data, but no per-cell target-class hashes. P1 therefore means:

1. reproduce the accepted 192 global verdicts (nine pass, 183 conflict) from the imported machinery under the recorded predecessor source hashes;
2. reproduce the accepted canonical G7 witnesses required by the imported controls;
3. compute and record any target-class hashes used by this new verifier **fresh** as new implementation artifacts.

Do not claim equality to predecessor target-class hashes that do not exist.

## 6. Exact optimization and independent optimality certificates

The implementation is not restricted to hand-written branch-and-bound. It may use any exact method appropriate to the frozen minimum-hitting-set / minimum-test-collection instances, including exact ILP, SAT/MaxSAT with cardinality constraints, or another exact combinatorial solver.

Every reported `PAS_raw` optimum must have an **independent optimality certificate**. Acceptable forms include:

- two independent exact solvers using materially different formulations/methods that agree on the optimum; or
- one exact optimizer plus a machine-checked lower-bound certificate equal to the reported size (for example a verified disjoint-difference-set packing or another rigorous bound).

The reported support itself must always be checked directly against every inclusion-minimal conflict-difference set.

Exhaustive enumeration of all supports of size `PAS_raw-1` is required only where `C(N_full, PAS_raw-1)` is actually enumerable under the implementation budget; it is **not** a universal requirement.

For `PAS_orbit`, the frozen orbit count is at most `3*(2+m) <= 18`, so the independent verifier must exhaust the full `2^(3*(2+m))` orbit-subset space. This provides a complete exact cross-check for the symmetry-restricted quantity.

Counting all exact minimum raw supports remains optional only if tractable. Claims such as “every minimum support has property X” must instead be established by restricted exact solves/certificates unless exhaustive minimum enumeration is actually performed.

## 7. Strike the reuse-grammar diagnostic

The optional reuse-aware grammar / cyclic support-description diagnostic in the parent protocol is **not part of this unit**. It is struck before implementation.

Reasons recorded from Gate 1:

- a canonical cyclic representation/rotation was not sufficiently specified;
- a smallest-grammar problem would introduce another difficult optimization layer;
- minimizing over all canonical minimum-cardinality supports could require enumerating all minima;
- most importantly, it invites premature conflation with Assembly Theory before the simpler exact causal-support quantity is understood.

No reuse/assembly-index value may be reported from this unit. A reuse-aware constructive cost is a possible separately frozen future experiment after PAS is established.

## Difference-family implementation note

For computational efficiency without changing the mathematics, conflict-difference sets may be formed over distinct `(history key, target)` classes rather than every raw record pair, and supersets may be removed so only inclusion-minimal difference sets remain. The canonical underlying record/source ordering remains available for provenance and witness replay.

## Claim ceiling

All parent-protocol nonclaims remain binding. In particular, a finite PAS value is a minimum predictive coordinate support on the accepted finite record set. It is not an assembly index, a state-complexity measure, an intrinsic-dimensional invariant, a self-assembly or endogenous-control measure, or evidence for physics/metaphysics, consciousness, Class IV, universality, spacetime, or prime/`8n+1` claims.

Any later change to the predecessor domain, atom definition, target, optimization objective, P2 upper-bound content, P4, or the still-open lag-1/lag-2 content of P5 is material and requires renewed exact-head Gate 1.
