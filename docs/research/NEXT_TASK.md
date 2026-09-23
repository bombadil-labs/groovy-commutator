# Next agent: delayed Rule-54 repair fails under full-state control

Updated 2026-09-23. Authored by Codex (OpenAI). Reviewed by: none.
Inspected main `69c9121c627b15952d57b179a1bc6b0c95ccb29a`. Two
research units are currently **draft, not merged**: [PR #300](https://github.com/bombadil-labs/groovy-commutator/pull/300)
contains the frozen eight-state Rule-54 target preflight, while [PR #301](https://github.com/bombadil-labs/groovy-commutator/pull/301)
tests the one-flip, two-step delayed action contract on that exact target.
PR #301 is based on main but scientifically depends on #300; if Myk directs
integration, merge #300 first and reconcile this handoff without overwriting
the first unit's evidence. Its protocol commit is `58ae145`, implementation
commit `4d1f516`; the [note](2026-09-23-delayed-repair-feasibility.md),
canonical `results/delayed_repair_feasibility_20260923.json`, and separate
scalar verifier pin the completed finite result. All 96 injuries and 13
actions were checked, and the independent scalar implementation replayed
every outcome under the 30-second cap. No independent reviewer participated.

**Decision:** 36/96 sources return by step four without intervention; no
action at the two-step decision point rescues any of the other 60. The best
fixed policy and full-state policy also succeed on 36/96. Frozen P1 passed,
P2–P4 failed. Stop this exact observer/control contract. Do not rerun a
nearby delay, target or action simply to manufacture a positive result.

Myk explicitly directed reconciliation and merging of PRs #295–#299.
[START_HERE](START_HERE.md) is the scheduling authority;
[FINDINGS](FINDINGS.md) is the accessible running account;
the [integration record](2026-09-23-research-integration.md) pins original heads
and verification. On main, all five units are integrated; do not recreate them
or interpret their historical draft status as a current blocker.

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

1. **Integration:** if Myk directs it, reconcile and merge #300 before #301,
   retaining both frozen protocols and all failed predictions.
2. **Operational motivation:** identify a consumer or mechanism that needs
   repeated disturbance tolerance, an internal maintenance constraint, or
   another precisely specified task. Early return alone is not enough.
3. **Decision gate:** for any such new contract, compare passive dynamics,
   full-state action feasibility, and a fixed-action baseline before searching
   encoders; state in advance what negative result stops that line.

No next empirical unit is automatically queued by integration. Dimensional
applications, all-rule censuses, a fourth G generation, prime-distribution claims
and the archived hard recoder campaign remain outside the current task. The
earlier [research-drive synthesis](2026-09-22-research-drive-synthesis.md) remains
valid; integration is not a reversal of its stopping decisions.
