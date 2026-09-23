# Finding which observations belong together

2026-09-23. Authored by Codex (OpenAI). Reviewed by: none.
Exact exhaustive local certificate, with separately written same-author scalar
verification. One timing trial; no independent scientific review.

[Open the visual witness viewer](../../site/observation-discovery.html).
The published viewer is also available at `observation-discovery.html` beside
the site's main index.

## What we asked

Could failed predictions guide selection of the observations themselves? Our
previous relational pilot chose a partition of already supplied blocks. Here
the search chooses source bits, XOR relations or past observations from a
fixed grammar. We fixed the task first: predict one next central output.
This makes a proposed observation boundary answerable to a specific operation.
It does not identify an autonomous subsystem or discover arbitrary objects.

The calibration predicts Rule 90's next central source bit from its current
central bit plus selected features. The prospective case predicts Rule 30's
next central **source G** bit from its current central G bit plus features.
This source rule is familiar; the feature-selection answer was not used to
tune the protocol. It is not external validation on an unknown natural system.

## Result and decision

The calibration recovers the known side XOR: one added binary feature in
place of two separate side bits. Both choices read the same source cells.
That is a retained-label saving with computation, not a raw-access saving.

For Rule 30, both full-grammar methods and raw-only search choose the same
six current bits: **sites -2, -1, 0, 1, 2, 3**. No subset of at most five
features from the declared 20-feature grammar suffices, even when the current
central G bit is also provided. History and the offered XOR relations save
nothing. The first sufficient symmetric raw window has radius three (seven
raw cells), while the winning input support is asymmetric (six cells).

| Rule-30 search | Full oracle calls | Total seconds including candidate preparation |
| --- | ---: | ---: |
| Full grammar, ordinary scan | 26,892 | 0.4606 |
| Full grammar, retained witnesses | 67 | 0.4118 |
| Raw-only scan | 645 | 0.0046 |

The witness arm rejects 26,825 candidates through already proved necessary
distinctions. Its certificate records 66 failed-query witnesses; the
calibration records three more. This reduces expensive checks but only
slightly reduces total time here; generating and ordering 137,980 possible
feature subsets dominates. Raw-only has 968 candidates and is much faster.
These are single local measurements; they do not establish a general speedup.
The producing run took 1.840 seconds; scalar verification took 0.765 seconds
in the initial audit, separately charged. Installation time was not measured.

**Keep the witness interface and visualization. Stop expanding this grammar
for Rule 30.** This test supports exact selection of useful input support,
but provides no benefit for its proposed relational/history enrichment.
Do not add another feature family merely to force the prediction to succeed.

## A transparent boundary: six bits, with G redundant

The winning input carries the six raw bits plus the mandatory current G bit:
seven interface bits, six distinct current source reads, no past buffer and
no added feature XORs. The frozen generic base-G acquisition recipe costs
five rule-table evaluations and five XOR operations. Refreshing needs those
raw source readings again; no compressed-state maintenance rule was found.
The source itself still advances at one rule evaluation per source cell per
step. The reachable lookup table has 64 entries; the seven-bit address format
has 128 possible addresses, half unreachable.

A **post-evaluation deduction** makes the simpler baseline explicit: current
G is already determined by the winning raw bits, so the base bit is redundant.
All 64 six-bit patterns occur in the audited rows. Dropping G leaves an exact
64-entry source-to-next-G lookup using six current reads and six address bits,
with no separate G acquisition. The grammar deliberately did not offer the
arbitrary target-valued Boolean function as a one-bit feature; allowing that
would move prediction into the encoder. Thus “six features” is a grammar-bound
minimum, never an information-theoretic lower bound on all encoders.

There is also a direct algebraic explanation for the asymmetric support.
For Rule 30, write `f(l,c,r) = l XOR (c OR r)`, and set
`a = f(x[-1],x[0],x[1])`, `b = f(x[0],x[1],x[2])`. Expanding the definition
of G cancels the leftmost evolved term and gives

```
G(x)[0] = a XOR x[-1] XOR (a OR b)
          XOR ((x[0] XOR a) OR (x[1] XOR b)).
```

So current G depends only on `x[-1..2]`; applying this readout after one
source update needs `x[-2..3]`. The six-cell support is therefore consistent
with a simple cancellation in Rule 30's existing formula. This is a
post-evaluation explanatory derivation, not a claim of a novel theorem or
an emergent organism. The frozen generic G acquisition costs are conservative;
the displayed algebra admits a cheaper specialized implementation as well.

## What makes the certificate exact

The domain contains every nine-bit predecessor word on sites -4 through 4.
We evolve shrinking valid cones without wrapping. All features and the target
lie inside this cone; every word extends to a full-line configuration. The
512-word computation therefore certifies a one-step local readout on every
legal predecessor/current trajectory, independent of exterior bits. It does
not certify a closed evolution law for the selected observations or unlimited
future prediction from one stored measurement.

The feature menu consists of seven current bits, six adjacent current XORs,
one side-to-side XOR, three past bits and three temporal XORs. Up to seven
features are selected. Ranking first minimizes feature count, then distinct
feature operands, past operands, XOR operations, and the index tuple. It is
not optimization of total runtime or acquisition cost.

A witness consists of two concrete predecessor words with equal mandatory
base and candidate feature values but unequal target bits. Any sufficient
candidate must include at least one offered feature that differs on this
pair. The scalar audit rebuilds all 1,024 calibration/test rows, verifies the
69 witnesses, replays the pruning chronology and coverage of all earlier
candidates, checks the successful lookup tables, and independently checks
raw-only and contiguous-window baselines. A hash check alone does none of this.

The viewer displays those preserved pairs, including the past and current
rows, the failed observation and the winning observation. Its values come
directly from the canonical result; it is an explanation, not another trial.

## Frozen predictions

| Prediction | Outcome |
| --- | --- |
| P1: known Rule-90 side XOR beats separate raw features | Supported, calibration only |
| P2: Rule-30 relational features beat raw-only in selected bits | **Failed: both require six** |
| P3: witnesses reduce Rule-30 full oracle calls | Supported: 26,892 to 67 |
| P4: Rule-30 winner uses history | **Failed: all six bits are current** |
| P5: guided total is lower in this one Rule-30 run | Supported: 0.4118 versus 0.4606 seconds; raw-only is much faster |

## Provenance and reproduction

- Inspected main: `45c8698d2a2e3c0dfcd9bb01dee1556fde58ba15`.
- [Frozen protocol](protocols/observation-discovery-20260923.md), commit
  [02948ab](https://github.com/bombadil-labs/groovy-commutator/commit/02948ab8ff523574a4ee11fdf0b379714ca87221).
- Implementation pinned before evaluation:
  [eced9ce](https://github.com/bombadil-labs/groovy-commutator/commit/eced9cee90570db53a2280f6101abffe441ef7da).
- Canonical SHA256: `c21a9a2a36f37cdef5b2a968c8bf7c0065e933d8b7d567b77f9f3f63581f151a`.
- [Canonical evidence](../../results/observation_discovery_20260923.json) and
  [runner/scalar verifier](../../experiments/observation_discovery_20260923/).
- Gathering [PR #303](https://github.com/bombadil-labs/groovy-commutator/pull/303)
  carries protocol, implementation, failed predictions, viewer and integration.
- Run `python experiments/observation_discovery_20260923/verify.py results/observation_discovery_20260923.json`
  for semantic checking. The runner requires `--implementation-commit` and
  an exclusive new `--output` path. Both have a 120-second cap.
