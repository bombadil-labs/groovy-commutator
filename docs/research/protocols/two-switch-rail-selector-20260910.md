# Protocol: two-switch rail-selector source recoders — 2026-09-10

**Status:** frozen before evaluating any Research034 frontier seed language under this fresh selector family.  
**Branch:** `research/relational-source-recoder-20260909`.  
**Working identity:** `two-switch-rail-selector`; no public research-note number is assigned until publication.  
**Dependency:** the complete exact-negative phase-splice result and its SAT recovery, Note 037 / `symbolic-sofic-image`, Note 036 / `sofic-defect-orbit`, Research032, and Research034.

## Why this checkpoint exists

The one-defect orbit program has now ruled out two increasingly permissive exact closure mechanisms through macro-horizon 6:

1. same-provenance temporal recurrence `G^h = sigma^delta G^j` on all 170 Research034 frontier questions;
2. changed-provenance source recoding using the one-defect graph's single left/right phase cut (`LR` or `RL`) on all 22 frontier seed languages.

The second result is complete rather than representationally censored: ten Class-II seed languages were exact negatives under the primary MDD backend, and an independently encoded fine-ECA CNF/Minisat22 recovery resolved all twelve Rule-122/161 sentinels negatively under the same 1200-second per-seed wall.

So changed provenance is allowed, but one global binary phase cut is insufficient. The smallest fresh increase in selector expressivity is a finite island: two rail switches rather than one.

> **Can a later spread defect be re-presented by selecting one evolved source rail outside a finite interval and the other evolved rail inside it, then reinserting the original one-defect seed?**

This checkpoint does not enlarge the causal horizon or background window. It changes only the finite-state selector carried by the source recoder.

## Exact source language and dynamics

Let `G:A^Z -> A^Z`, `A={0,...,7}`, be the exact radius-one macro CA induced by three fine ECA ticks. Fix a hidden seed `s=(a,b)`, `a<b`. A genuine one-defect source consists of scalar rails `x^L,x^R` agreeing everywhere except at the origin, with `x^L_0=a`, `x^R_0=b`.

Choose `k>=1`, `j>=1`, `t=k+j`, and evolve both rails for `k` macrosteps:

`z^L = G^k(x^L)`, `z^R = G^k(x^R)`.

They agree outside `[-k,k]`.

As before choose a reinserted-seed displacement `delta in [-k,k]`.

## Fresh two-switch selector

Choose an integer interval `[u,v]` satisfying

- `-k < u <= v < k`;
- `[u,v]` contains at least one position other than `delta`.

The strict interior condition ensures both sides of the island occur inside the active defect cone. The non-seed condition prevents the entire island from being erased by seed reinsertion.

Two fresh orientations are allowed:

- `LRL`: use `z^L` for `q<u`, `z^R` for `u<=q<=v`, and `z^L` for `q>v`;
- `RLR`: exchange `L` and `R`.

At `q=delta`, ignore the selector and reinsert the original ordered seed `(a,b)`.

Thus the recoded paired row is diagonal everywhere except at exactly one copy of the original seed and therefore belongs to the same exact one-defect source shift `X_0(s)`.

The selector has exactly two dynamically active rail switches. Constant selectors and one-cut `LR/RL` selectors are already disclosed/closed families and are not counted as fresh evidence here.

## Exact certificate

A candidate `(k,j,delta,u,v,orientation)` passes when

`Ghat^(k+j)(x) = Ghat^j(P(x))`

for every genuine one-defect source row `x` with seed `s`, where `P` is the two-switch recoder above.

A pass proves

`X_(k+j)(s) subseteq X_j(s)`.

The all-diagonal topological-closure branch is handled exactly as in the phase-splice theorem by using `(G^k u,G^k u)` as the earlier all-diagonal source.

Since `j<k+j`, a pass closes the orbit union at time `t=k+j`. Research032 plus its independent h=6 recovery establishes target safety through `t<=6` for every incoming Research034 frontier question, so any fresh pass in the frozen range yields exact all-time permanence for every target attached to that seed language.

## Frozen primary domain

Use exactly the same 22 distinct `(rule,seed)` languages underlying the 170 Research034 survivor questions:

- 158 Class-II target questions;
- 12 Class-III target questions;
- frontier rules `{122,154,161,164,166,180,210,218}`;
- all Rule-122/161 sentinel languages retained.

Reconstruct this domain from the committed phase-splice primary audit whose SHA-256 is

`af00ce04f134bd98ecd2d2bd7a0bf2a00b2c2c5d9b7d34c2ebcd9cc22e329138`

and assert 22 seed languages / 170 target questions before interpretation.

No frontier seed may be added or removed after outcomes are inspected.

## Frozen candidate family

For every frontier seed language test exactly:

- `2 <= t=k+j <= 6`;
- `k>=1`, `j>=1`;
- `delta in [-k,k]`;
- `orientation in {LRL,RLR}`;
- every strictly interior interval `[u,v]` with `-k<u<=v<k` and not `u=v=delta`.

This contains exactly **2,788** fresh candidates per seed language through `t<=6`.

Candidate order is frozen as:

1. increasing `t`;
2. increasing `j`;
3. `delta` by `(abs(delta),delta)`;
4. increasing island width `v-u+1`;
5. increasing `u`, then `v`;
6. `LRL` before `RLR`.

Stop a seed-language search at the first passing candidate. A non-certified language must exhaust all 2,788 candidates unless censored.

## Exact SAT verification

Reuse the independently encoded fine-ECA CNF backend from the successful phase-splice SAT recovery, not the MDD implementation.

For each candidate and output position `p in [-t,t]`:

1. create one exact finite source cone of `2t+1 <= 13` macro symbols / `6t+3 <= 39` fine cells;
2. constrain the two source rails to share every background fine bit and to carry `a` versus `b` at the latent origin;
3. evolve both rails under the original ECA for `3k` fine ticks;
4. build the recoded source by selecting evolved-rail bits according to the frozen `LRL/RLR` island and reinserting `(a,b)` at `delta`;
5. evolve the actual and recoded rails for the remaining `3j` fine ticks;
6. ask Minisat22 for any disagreement among the six final fine output bits.

SAT is an explicit counterexample and must be independently scalar-replayed before a candidate is recorded as failed. UNSAT proves exact equality for that output position.

A candidate passes only if every required output position is UNSAT.

Checking `p in [-t,t]` is complete by finite propagation, exactly as in the parent phase-splice protocol.

### Frozen output-position order

Retain the already-frozen phase-splice operational order for comparability:

1. positions outside the reinserted seed's `j`-step future cone `[delta-j,delta+j]`, ascending;
2. then positions inside that cone, ascending;
3. stop at the first SAT counterexample.

This affects resource behavior only, never exact pass/fail semantics.

## Frozen resource envelope

Keep the same scientific wall as the phase-splice primary/recovery:

- maximum wall time per frontier seed language: **1200 seconds**;
- `t<=6`, hence at most 39 source fine bits in one causal cone.

The selector adds only wire choice, not new dynamical state or a larger cone. Therefore assert that no query exceeds the phase-splice SAT structural maxima:

- **1,314 CNF variables**;
- **9,943 CNF clauses**.

Crossing a structural assertion is an implementation failure. Reaching the 1200-second seed wall is censoring only; do not raise it after outcomes are known.

Seed-language status:

- `two-switch-certified`: first exact fresh candidate passes;
- `no-two-switch-through-6`: all 2,788 candidates fail exactly;
- `censored`: no pass is found and the fixed seed wall prevents completion.

## Frozen controls

Controls are semantic implementation checks, not fresh frontier evidence.

### Rule 204 positive end-to-end selector control

Rule 204 is the identity ECA. Require the exact candidate

- rule `204`;
- seed `(0,1)`;
- `t=3`, `k=2`, `j=1`, `delta=0`;
- orientation `LRL`;
- island `[-1,1]`

to pass at every output position. This exercises the two-switch selector and successful-certificate path end to end. Because identity evolution leaves the two rails equal away from the latent seed, the selector cannot alter the common background.

### Rule 35 negative/witness control

For Rule 35 / seed `(2,6)` the first exact target witness is at macro-horizon 3. Therefore every fresh two-switch candidate with `t<=3` must fail. There are **62** such candidates under the frozen family. Every accepted SAT failure must scalar-replay.

Any control failure blocks frontier evaluation.

## Frozen primary hypothesis

Before evaluating any frontier two-switch outcome:

> **At least one of the 22 Research034 frontier seed languages admits an exact two-switch rail-selector certificate with `k+j<=6`.**

A complete zero is scientifically useful. It would show that changed provenance plus a three-phase finite selector (`LRL/RLR`) is still insufficient and would justify moving to a switch-count hierarchy / arbitrary finite selector mask or a synthesized local repair transducer.

No prediction is frozen for the number of certificates or for the Rule-122/161 families.

## Measurements and durable outputs

For every seed language record:

- rule/class/seed and attached target IDs;
- candidates tested;
- first exact certificate if any;
- first scalar-replayed counterexample for each failed candidate in the full audit;
- maximum CNF variables/clauses;
- SAT solver time and wall time;
- censoring point if any.

Persist three layers in the same publication commit:

1. full machine-audit JSON;
2. compact canonical JSON summary;
3. concise Markdown report carrying the full-result SHA-256.

Do not leave the only copy of a full result in ephemeral Actions storage.

## Independent audit of a fresh success

If any frontier candidate passes, freeze the earliest canonical success before interpretation and re-encode that candidate independently in Z3 without importing the Minisat/CNF implementation. Prove the negation UNSAT at every required position and scalar-replay any SAT model.

A disagreement invalidates the certificate and blocks publication.

If the fresh family is a complete exact negative, no additional positive-outcome audit is required beyond the frozen controls and scalar replay of SAT failures.

## Interpretation boundaries

- A pass is an exact source-language inclusion certificate, not a heuristic.
- A failed candidate refutes only that particular two-switch selector.
- Exhausting this family does not refute selectors with three or more switches, arbitrary local rail masks, nondeterministic source transducers, or general orbit inclusion.
- The selector state is latent proof state, not a new physical degree of freedom in the CA.
- Runtime differences between MDD and SAT backends are representational, not intrinsic dynamical complexity.
- No Class-IV or dimensional-lift claim is tested here.

## Decision rule

- If fresh certificates appear, characterize the minimal island geometry and independently Z3-audit the first canonical success before publication.
- If all 22 seed languages are exact negatives, proceed to a finite switch-count hierarchy / arbitrary rail-selector masks before introducing unrestricted local repair synthesis.
- If only some seeds censor under the fixed wall, keep the family fixed and optimize/recover the SAT enumeration without changing the scientific envelope.
- Do not return to projected sofic graphs or enlarge the causal horizon in response to a negative result.
