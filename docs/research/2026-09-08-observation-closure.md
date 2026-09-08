# Observation closure: the commutator is the same-rule slice

**Research checkpoint, 2026-09-08.** This follows the
[observation-closure protocol](protocols/observation-closure-20260908.md).
The motivating question is broader than differentiation: when a representation
throws information away, does the observed state still support autonomous
dynamics?

Let

\[
Y=P(S),\qquad Z=P(E^q(S)).
\]

The observation is **closed** when `Z` is a function of `Y`, equivalently when
some induced dynamics `B` exists with

\[
P E^q = B P.
\]

The original Groovy commutator tests the stricter special case `B=E`. This run
shows that distinction is substantive rather than terminological.

## A graded closure defect

On a finite exhaustive ensemble we measure

\[
\Delta_P = H(Z\mid Y).
\]

Because `Z` is deterministic given the microstate, this is the one-step
predictive relevance of distinctions among microstates that `P` identifies.
We also record

\[
L_P=H(S\mid Y)
\]

and `Delta_P/L_P` when defined, because a tiny defect is uninteresting when the
observation discarded almost nothing.

## Derivative observation: 30 closures, only 10 commutators vanish

For all 256 ECA rules we set

\[
P=D_A,\qquad D_A(S)=S\oplus E_A(S),\qquad q=1.
\]

Discovery exhausts the `n=12` ring; exact hits are rechecked at `n=16`. Every
ECA factor is also checked on every five-cell causal window, which proves the
radius-2 identity on arbitrary binary configurations.

The 30 exact derivative closures split into four groups:

| Type | Rules |
| --- | --- |
| Same rule `B=A` | 0, 4, 60, 90, 102, 150, 170, 200, 204, 240 |
| Bias flip `B=255-A` | 15, 51, 85, 105, 153, 165, 195, 255 |
| Variable commutator, derivative drains | 12, 68, 76, 205, 207, 221, 223, 236 |
| Variable commutator, nonconstant factor | 23, 77, 178, 232 |

All 30 survive `n=16`. All 310 ECA factor extensions listed by the census pass
the independent five-cell audit.

The bias-flip cases are the cleanest demonstration of the new abstraction.
Their old commutator is constant `G=1`, so the same-rule comparison disagrees
at every bit, yet the derivative is perfectly autonomous: it evolves under
`255-A`. A maximally nonzero same-rule commutator can therefore coexist with
zero closure defect.

The four nonconstant alternate-factor rules go further:

- Rules 23 and 178 close under Rule 250 or 254.
- Rules 77 and 232 close under Rule 128 or 160.

Those apparent factor ambiguities are only off-image ambiguities. The derivative
images of 23/178 forbid neighborhood `010`, exactly where Rules 250 and 254
differ. The images of 77/232 forbid `101`, exactly where Rules 128 and 160
differ. The induced law is unique on reachable observed states.

The loss normalization matters. At `n=12`, Rule 30 hides only about 0.031 bits
of the whole microstate and has about 0.030 bits of closure defect: its small
raw defect mostly says the derivative is nearly invertible. Rule 23 hides about
3.70 bits and has exactly zero defect, which is the stronger coarse-graining
phenomenon. Rule 110 hides about 2.47 bits and has about 2.47 bits of defect,
so nearly all hidden information is relevant to the next whole derivative
under this finite uniform ensemble.

## Block coarse-graining recovers scale-rhyme exactly

For a block observation `h:{0,1}^b->{0,1}` with matched stride `q=b`, one coarse
output after `b` microsteps depends on exactly three adjacent blocks. This lets
us test closure by exhausting a local window of `3b` fine cells, with no
periodic-ring assumption.

For `b=2`, all 14 nonconstant Boolean block maps and all 256 rules reproduce
**exactly the existing 404 scale-rhyme triples**, set for set. The 16
nontrivial same-rule fixed points are:

`60, 90, 102, 128, 136, 150, 153, 165, 170, 192, 195, 204, 238, 240, 252, 254`.

So the earlier scale-rhyme experiment was already an exact observation-closure
experiment; the new language tells us what the failures mean.

## Exploratory block-3 extension: fixed points depend on scale

After the block-2 control passed, we exhaustively scanned all 254 nonconstant
three-cell Boolean observations with `q=3`. This extension was selected after
the first pass; its numerical outcomes were not preregistered.

The exact local scan finds:

- 3,312 factor triples;
- 141 fine rules with at least one factor;
- only 14 distinct coarse ECA targets;
- 12 nontrivial same-rule fixed points:
  `15, 51, 85, 128, 136, 170, 192, 204, 238, 240, 252, 254`.

The fixed-point comparison is especially informative:

- at both block sizes: `128, 136, 170, 192, 204, 238, 240, 252, 254`;
- block-2 only: `60, 90, 102, 150, 153, 165, 195`;
- block-3 only: `15, 51, 85`.

Rule 90 is therefore not simply “scale invariant.” It is fixed under the
particular dyadic coarse-graining relation that the earlier work found, but not
under any binary block-3 observation in this search. Scale invariance belongs
to the tuple `(rule, observation, scale)`.

## Revised project-level interpretation

There are now three nested questions:

1. **Closure:** does any deterministic `B` exist on the observed image?
2. **Model-family closure:** can `B` be represented in a chosen family, such as
   an ECA rule?
3. **Self-similarity:** can `B` be the original rule itself?

The original Groovy commutator lives at level 3. Its failure field remains
interesting, but noncommutation no longer means the representation itself fails
to close.

When closure fails, the fibers of `P` become the natural defect object: two
microstates that look identical to the observer have different observed
futures. That unifies several existing repo threads. Scale-rhyme, derivative
commutators, history repairability, interface state, and defect fate can all be
read as questions about **where a representation stops being a sufficient state
description and what the discarded context does next**.

## Reproduce

```bash
python scripts/experiment_observation_closure.py
python scripts/audit_observation_closure.py
```

The experiment writes the derivative census and `n=16` verification, the exact
block-2/block-3 local factor atlas, and a compact JSON summary. The audit
independently rechecks every listed derivative factor on five-cell windows,
checks the special forbidden neighborhoods above, and confirms that the local
block-2 atlas exactly equals the pre-existing `results/scale_rhyme.csv` set.

The next strongest experiments are exact whole-history closure
`H(Y_{t+1}|Y_{t-h:t})`, spatial structure of nonclosure fibers, and composing
block-factor relations across scales rather than treating fixed points as a
single list.
