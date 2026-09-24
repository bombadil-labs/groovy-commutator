# Next agent: require a concrete operation before another search

Updated 2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
Latest unit: the [observer-orbit hypotheses](2026-09-24-observer-orbit-program.md)
and [frozen Rule-30 preflight](protocols/observer-orbit-preflight-20260924.md)
were prepared against inspected main `37a3429e436060d6e6ee1662ca4b7d9d169c000d`.
Protocol commit `dd5abe650aeb2b11c5cc889dc510e2e94cf73a59` preceded
implementation commit `3a466968113fd342e5b45c032d682239b75d0aa1`;
evaluation followed the latter. [The bounded result](2026-09-24-observer-orbit-preflight.md)
on all 64 states of one six-cell Rule-30 ring found phantom G-graph closed
walks `9,15,27,39,39,69` for lengths 1..6. The primitive `G=9` self-loop
comes from `10 -> 27`, but the same run next reads `45`. The valid three-row
G history and source-identity controls have no phantom words through six.
The unchanged canonical JSON is `results/observer_orbit_preflight_20260924.json`
(SHA-256 `189a60e6c37e43b7bb12c6e7bdc242cf424ba28ab9d4a0ce4d43109593687d6a`);
the separate registered seal binds it to the protocol, runner and verifier.
An independent scalar implementation by the same author verifies truth
table, cycles, graph powers and witness; no independent peer reviewer.
The three-row control needs two updates and three G reads. No feedback,
Class-IV advantage or full-line recurrence claim follows.
The maintained [observation/law taxonomy](2026-09-24-observation-law-taxonomy.md)
defines the distinct same-rule, factor, recursive and controlled-switching
questions. It adds no empirical unit; require a specified operation and
matched control before searching rule schedules or recursive branches.
Latest completed unit: [observation discovery #303](https://github.com/bombadil-labs/groovy-commutator/pull/303).
Taxonomy-only update inspected main `7301e9dc1ac00549b72b97c46b7380c689ecb914`.
The earlier empirical unit inspected main `45c8698d2a2e3c0dfcd9bb01dee1556fde58ba15`; its protocol
`02948ab8ff523574a4ee11fdf0b379714ca87221` preceded implementation
`eced9cee90570db53a2280f6101abffe441ef7da` and evaluation. Myk authorized
this unit and merging completed work. Reviewed by: none.

We tested whether witnesses can select which raw, XOR or past observations
belong in a sufficient view. The Rule-90 calibration selected the known side
XOR. On Rule 30, all three search arms chose six current bits at -2..3; the
offered relations and history did not reduce feature count. Guided full
queries fell from 26,892 to 67, but raw-only search was fastest (0.0046 s
versus 0.4118 s guided total). P1/P3/P5 held; P2/P4 failed. Canonical result:
`results/observation_discovery_20260923.json`. Separate scalar audit checks all
1,024 calibration/test rows and 69 witnesses in under a second locally.

[The note](2026-09-23-observation-discovery.md) states the exact local full-line
one-step contract and post-evaluation algebraic cancellation. The interactive
site page `observation-discovery.html` displays saved failure pairs and costs.
The winner's six source bits already determine the mandatory G bit; a direct
six-bit lookup can omit G. This is grammar-bound observation selection, not
an autonomous reduced CA or a new biological object. Do not expand the grammar
or continue a census to force a relational advantage.

The five earlier gathering units #295–#299 and follow-ups
[target eligibility #300](https://github.com/bombadil-labs/groovy-commutator/pull/300),
[delayed action #301](https://github.com/bombadil-labs/groovy-commutator/pull/301),
and [masked-history sensing #302](https://github.com/bombadil-labs/groovy-commutator/pull/302)
are integrated on main at Myk's direction. Their original
protocol → implementation → evaluation chronology and canonical result bytes
are preserved. No independent reviewer participated in these three follow-ups;
scalar audits by the same author and CI checks are verification, not review.

The #300 exact finite target has both returning and nonreturning one-bit
injuries on a 12-cell Rule-54 ring. #301 shows that at the two-step decision
point, no addressed one-flip action rescues any of the 60 injuries that fail
the four-step target endpoint passively; 36/96 succeed by no action.
That negative result is limited to the fixed target, action budget, timing
and endpoint. P1 held and P2–P4 failed. See
[the note](2026-09-23-delayed-repair-feasibility.md) and
`results/delayed_repair_feasibility_20260923.json`.

The independent #302 known-erasure audit used 52 source states × 12 known
hidden-cell positions on the same 12-cell periodic Rule-54 ring. Ambiguous
observed fibers conflicting on the target task at times 0, 0–1 and 0–2:
**48, 24, 0**; exact-source reconstruction has the same counts.
P1–P3 held, P4 failed. A finite time-zero fiber deduction extends the
equality of task/source sufficiency to all later histories retaining the
initial observation in this domain. At sufficiency, 33 visible bits over
two updates replace a direct 12-bit initial read, if available; no efficiency
or biological claim. See [the note](2026-09-23-masked-history-sensing.md)
and `results/masked_history_sensing_20260923.json`.

[START_HERE](START_HERE.md) is the scheduling authority;
[FINDINGS](FINDINGS.md) is the accessible running account.
The [integration record](2026-09-23-research-integration.md) covers #295–#299.

## What the combined work says

1. **History geometry:** Rule 30's raw three-row encoding loses a temporal
   distinction; one constant fourth row repairs it. Both binary separator
   choices have exact uniform 13-by-4 laws. No speed or optimality claim.
2. **Recursive 1D G:** mirror Rules 2/16 have specified nonconstant second
   and third generations. Completion choices change third-level closure;
   one branch remains unresolved beyond radius four. After the first source
   step the dynamics translate rigidly. More depth alone has no established payoff.
3. **Reusable descriptions:** what an observation needs depends on the operation.
   Retaining erased state, widening access and choosing an off-image rule
   extension solve different problems. The arithmetic/CA interactive comparison
   is available at the site's reusable-descriptions route.
4. **Search method:** exact conflict witnesses reduced full queries from 278
   to 11 in the known Rule-24 test. Both arms used Prolog. No language-wide
   advantage, Jev result or universal-verifier breakthrough was established.
5. **Prediction and repair:** in the fixed Rule-54 task, minimum local alphabets
   are 2 for passive target prediction and 4 for repair. The repair view can
   forget global complement and is not a refinement of parity. However the
   target has no incoming passive paths, so delayed repair is static correction.

Read the linked unit notes in START_HERE for full contracts and evidence.
Original protocols, canonical bytes, failed predictions and unresolved outcomes
remain intact. Separate implementation checks and green CI are self-verification,
not an independent review. There is no standing cross-agent gate to reactivate.

## Next one to three decisions

1. **Sensing:** obtain a concrete corruption or observation operator and a
   task independently of the handpicked stripe family. Define the cost of
   observation, delay, computation and reconstruction before asking whether
   task identification can precede exact source recovery.
2. **Maintenance:** identify a concrete consumer of repeated disturbance
   tolerance or an internal constraint. Compare passive dynamics, full-state
   action feasibility and a fixed-action baseline before searching encoders.
3. **Scientific corrections:** correct a bounded claim if a witness or a
   reproducing check contradicts it; preserve original result bytes and
   failed predictions.

No empirical unit is queued. A next decision is whether a real controller
consumer supplies an independently specified organization target, causal
selector, horizon and priced fixed/clocked controls; otherwise keep H3
contingent. A second is whether a concrete scientific counterexample calls
for a bounded correction. Dimensional applications,
all-rule censuses, a fourth G generation, prime-distribution claims and the
archived hard recoder campaign remain outside the current task. The earlier
[research-drive synthesis](2026-09-22-research-drive-synthesis.md) remains
valid; integration does not reverse its stopping decisions.
