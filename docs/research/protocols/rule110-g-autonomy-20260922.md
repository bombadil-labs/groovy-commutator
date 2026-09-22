# Can Rule 110's original Groovy field evolve autonomously?

Date: 2026-09-22. Status: frozen intent; implementation and evaluation pending.
Authored by: Codex (OpenAI), this session. Reviewed by: pending independent
Gate 1 review, to be recorded in the gathering PR and a separate review record.
Base main: `5aee7bb9ac6c70eaa114a8ed5baf38ba6b10e8c1`.

## Decision and prior evidence

Myk asked whether D or G can follow a different CA rule and then authorized
pressing on that question. The existing derivative census already proves 30
ECA derivative closures. The local-correction-cap work proves
`G_32 E_32 = E_128 G_32`; that is a known positive control, not a new prediction.
Neither a dimensional lift nor a same-law commutator test answers whether
Rule 110's original G alone is sufficient state. No open PR or issue covered
this unit when the current main was inspected.

This unit decides whether to treat that G field as an autonomous subsystem on
the full binary line. A local factor certificate would warrant interpreting
its retained dynamics. A whole-field collision would end that claim for this
domain, however large the proposed update neighborhood. If the bounded search
is inconclusive, record that and stop; no automatic larger-radius, history,
restricted-domain or all-rule census follows. Source retention is the exact
baseline, and Rule 32 is the already-paid-for example. This is a scientific
sufficiency question, not a speed, compression, physics or Class-IV claim.

## Exact contract

Source: homogeneous binary radius-one Rule 110 on `X={0,1}^Z`, arbitrary
configurations. `E_r` uses Wolfram indexing `4*left+2*center+right`.
`D_r(S)=S XOR E_r(S)` and
`G_r(S)=E_r(S) XOR E_r^2(S) XOR E_r(S XOR E_r(S))`.
The observation is original-source G, not a descendant's native commutator.
Cadence is one synchronous source step, with no burn-in or prepared ether.

Question: does a deterministic function `B:G_110(X)->G_110(X)` satisfy
`G_110 E_110 = B G_110` on X? A CA realization is a stronger positive result.
Use bitwise equality of complete fields, with fixed spatial alignment; neither
translation equivalence nor a summary statistic counts as equality.

## Frozen stages and certificates

1. **Known controls.** Reverify `G_32 E_32 = E_128 G_32` on all 128 seven-bit
   source words. Reverify `G_90=0` on all 32 five-bit words as a trivial constant
   control. Controls fail the unit if either identity fails; do not promote a
   target outcome from a failing implementation.
2. **Bounded local factors.** For Rule 110 test all three candidate radii
   `R=0,1,2`. G has radius at most two and its next value radius at most three.
   Exhaust every source word on radius `m=max(R+2,3)` and group by the observed
   `(2R+1)`-bit G patch. Record realized patches and required target bits. A
   consistent table is an exact local factor on the observed image; extend it
   by zero on unrealized patches and label this arbitrary extension. A conflict
   records two full source windows, their identical G patch and different
   targets; it refutes only that radius. Evaluate all three budgets, even if
   an earlier one passes.
3. **Whole-field obstruction.** If all local radii fail, enumerate complete
   periodic rings at sizes `n=1,2,...,16` in that order. Enumerate source words
   lexicographically, leftmost bit most significant. For each G word keep its
   first source representative and next G word. Stop immediately at the first
   repeated G with a different successor. Save both source words, E, D, G and
   next G, plus the number of states visited and the status of every remaining
   ring budget (`not_run_after_witness`). If a local factor passes, mark this
   stage `not_needed_local_factor`. If no witness occurs, mark it bounded
   inconclusive, not closed on the infinite line.

Any periodic-ring witness extends by periodic repetition to two configurations
of X. Locality makes E and G commute with that extension, so the equal full G
fields and unequal next G fields prove that no B exists on X. This negative
transfer is a direct proof; no positive finite-ring extrapolation is used.
Do not claim a minimal period beyond the exhaustively completed smaller rings.

## Predictions, budget and verification

- `P1_no_full_shift_factor`: working conjecture that no present-only G factor
  exists for Rule 110. Score `supported_by_counterexample`,
  `refuted_by_local_factor`, or `unresolved_within_budget`. This conjecture has
  not been evaluated in this unit. Preserve the key under every outcome.
- `C1_rule32_factor` and `C2_rule90_constant`: known controls, scored separately
  from discovery. Record invalid or not-evaluated states explicitly.
- At most 16 ring lengths / 131,070 source states; three local target budgets
  totaling 768 source windows; 160 control windows. No solver or random seeds.
  Primary evaluation has a 120-second wall-time limit and a 1-GiB memory
  budget. Resource exhaustion is censored/incomplete, never a theorem.
- Freeze and commit the protocol, obtain independent review, then commit the
  implementation before evaluating. Record implementation commit, source
  hashes, outcomes and execution metadata in durable files. Keep protocol bytes
  unchanged after evaluation; record deviations separately.
- Independently replay a negative certificate with explicit tuple-valued
  cyclic updates, separate from the primary evaluator, and show a direct
  finite-window check of its periodic extension. Independently check a positive
  certificate on its complete causal windows. Review proof scope and initialized
  image restrictions as well as the code.
- Use a gathering branch and draft PR. Full review and applicable green checks
  precede integration. This small verification may run in bounded CI, but no
  historical census or expensive Actions workflow is to be dispatched.

## Deliverable

One exact result or explicitly incomplete bounded answer; a small inspectable
certificate and verifier; an accessible note and FINDINGS entry; a durable
handoff with at most three decision-relevant questions. Existing canonical
evidence, the completed lift and other parked research stay intact.
