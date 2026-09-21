# Next agent task: three executable representation case studies

**Ready to start:** tracked in [issue #280](https://github.com/bombadil-labs/groovy-commutator/issues/280). Read [START_HERE](START_HERE.md) and the
[boundaries guide](2026-09-21-research-boundaries.md), then only the sources
listed below. Deliver one compact scientific note and one fast verifier.
No new sweep, empirical predictor or general-purpose framework is needed.

## Purpose

Make the project's central distinction inspectable: a nonzero commutator,
failure of autonomous observation, and failure to transfer a certificate
between domains are different things. This is an exposition and certificate
extraction task. Do not claim the factor criterion or predictive equivalence
itself is new mathematics.

## Fixed cases

| Case | What to exhibit | Existing sources |
| --- | --- | --- |
| A: Rule 255, derivative observation | `D` is complementation, `G` is identically one, yet `D E = B D` with `B` constant zero. An explicit changed law repairs same-law disagreement without adding state. | [Erased distinctions](2026-09-08-dynamics-of-erased-distinctions.md), [shared closure account](2026-09-10-shared-closure-account.md), `scripts/verify_history_algebra.py`. |
| B: Rule 223, observation 22, ring 7 | Two actual ring states with equal present observed fields and different next observed fields. Verify the witness with the source CA. Explain why this rules out every deterministic present-only factor on that domain. | [Ring closure certificate](2026-09-11-ring-closure-certificate.md), `scripts/verify_ring_closure_certificate.py`, `results/ring_closure_certificate_20260911.json`. Rings 3–6 close; ring 7 does not. |
| C: Rule 58, observation 232 | The existing all-ring depth-at-most-one certificate and an eventually periodic pair witnessing failure at depth one on the full shift. Verify both tails, the finite bridge and the violating output; a cropped picture alone is insufficient. | [Depth-one certificate](2026-09-11-depth-one-certificate.md), [full-shift depth two](2026-09-11-full-shift-depth-two.md), `scripts/verify_depth_one_certificate.py`, `scripts/verify_full_shift_depth_two.py`, their canonical JSON results. The latter also excludes full-shift depth at most two; that stronger statement is optional here. |

In case C, depth refers to **forward observed-word refinement of initial
states**, not an online learner's suffix memory. Spell out the quantified
domain and time index before discussing “memory.”

## Deliverables and acceptance

1. `docs/research/representation-case-studies.md`: roughly 1,500–2,000 words,
   one common notation, three explicit contracts, certificate/witness links,
   and a short prior-art comparison. Explain what was already known and what
   this repository contributes. Cite the primary sources in the boundaries
   guide; do not label the examples novel without establishing that.
2. `scripts/verify_representation_case_studies.py`: deterministic, under one
   minute on an ordinary CPU, with a nonzero exit for a malformed witness.
   Reuse existing CA primitives and stored certificates; never invoke an
   entire historical census. Case B's 128 ring states are a sufficient bounded
   fallback if the stored file lacks explicit states. For C, use the existing
   graph-path certificate rather than extrapolating a finite ring sweep.
3. Register the note. If a new small certificate JSON is needed, preserve its
   source hashes and register it in the existing integrity checker. Update an
   existing knowledge entry only where the account changes; a new graph of
   near-duplicate entries is unnecessary.
4. End with one recommendation: either name a specific representation-cost
   comparison worth doing next, or say no new experiment is justified yet.
   A candidate comparison is the affine six-field lift against the period-three
   necklace under the same readout/intervention budget; do not execute it as
   part of this task.

Run the small verifier, `python scripts/check_result_integrity.py`,
`npm run test:research --prefix site`, and `npm run build --prefix site`.
Use a gathering PR with the normal review workflow. This is not a request
for a fresh scientific experiment; any changed scientific domain or new
empirical claim needs its own protocol boundary.

## Stop

Stop when the three cases can be checked and understood. If an existing
certificate cannot support its stated claim, document the exact gap, preserve
the evidence and correct the claim rather than launching a search to rescue
it. Do not expand to all rules, additional observations, greater depth,
classification metrics or solver recovery. Report an unresolved case explicitly;
it must not silently disappear from the deliverable.
