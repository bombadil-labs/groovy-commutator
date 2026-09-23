# Research: start here

**Current direction, 2026-09-23.** This page is the scheduling authority for
research. Older notes and checkpoints preserve the evidence; their “next”
sections are historical proposals, not an instruction to resume them.

**Question:** which distinctions can a representation safely discard, which
must it retain, and what does changing representation buy us?

Our strongest work answers bounded versions of that question with exact
factors, counterexamples, graph certificates and explicit constructions.
“Class IV” remains a motivation, not a specification or success criterion.
The [limits and prior-art guide](2026-09-21-research-boundaries.md) explains
what the impossibility theorems constrain and where useful exact work remains.

## Active program: The Groovy Field

On 2026-09-22 Myk opened [The Groovy Field](2026-09-22-groovy-field-program.md)
as a new research program: can a rule's Groovy field run as a dynamical system
of its own, and what is it missing when it cannot? The first
[census](2026-09-22-groovy-field-census.md) applies an exact full-line method
to all 256 elementary rules, with explicit resource limits and evidence gaps. 140 Groovy fields close with one to four
steps of memory; every Groovy field is blind to the uniform D0 bit; and the
source gradient plus two steps of memory repairs all of them. Open questions
and their order are in the [checkpoint](checkpoints/groovy-field.md).

## Latest direct request: one-dimensional recursive G

Myk asks which autonomous 1D Groovy fields have an autonomous G field of
their own. The [present-only binary unit](2026-09-23-groovy-1d-second-generation.md)
is complete: of 36 first-stage laws, 33 have constant native G. Rules 2 and
16 have nonconstant inherited second-G laws under both specified derived
rules, while Rule 32 fails for both radius-one choices. Arbitrary descendant
starting rows give different answers; the note separates the domains.
Read the [handoff](checkpoints/groovy-1d-second-generation.md) before choosing
further work. Memory-bearing cases such as Rule 30 are outside this unit.
The spatial-geometry work in draft PR #295 remains separate; current work
is 1D recursion. Myk then requested [one further generation](2026-09-23-groovy-1d-third-generation.md).
Both 2/16 extend nontrivially with first-rule one-fill and second-rule zero-fill,
using a radius-four third update. Other tested choices fail or remain unresolved
beyond radius four. Read the [third-generation handoff](checkpoints/groovy-1d-third-generation.md).
This requested follow-up is complete; no fourth generation is queued.

## Preceding direct request: original-source G autonomy

After the research drive ended, Myk asked whether D or G could evolve under
its own law and authorized a bounded test of Rule 110. The
[completed unit](2026-09-22-rule110-g-autonomy.md) proves that Rule 110's G has
no deterministic present-only factor on the full binary line at cadence one:
periodic sources 001 and 011 have identical G fields and different next G
fields. A larger spatial neighborhood cannot fix this. The known Rule-32
G -> Rule128 identity remains an exact positive example.

This directly answers one sufficient-state question within Erased
Distinctions; it does not reopen dimensional applications or the scheduled
drive. See the [current handoff](checkpoints/g-autonomy.md) before choosing a
follow-up. No broader census, history search or restricted-domain experiment
is automatically queued.

## Portfolio after the completed unit

Read [What we have learned](FINDINGS.md) for the running plain-language
findings, and [the program survey](2026-09-22-program-survey.md) for the
recommended portfolio. The [research-drive synthesis](2026-09-22-research-drive-synthesis.md)
records the completed comparison, subsequent audits and current justified stop.
Keep one active design agenda under Erased Distinctions:
local sufficient state and the cost of representation. Representation Invariants
supplies shared methods; it is not a separate automatic census queue.

The [bounded Groovy readout comparison](2026-09-22-groovy-readout-cost.md)
is complete: a three-track cache matches the six-field lift's marked readout.
That caching benefit does not require the lift. Phase-free binary geometry is
a different interface, not a free property of named tracks. No broad benchmark
is justified by this candidate. A subsequent [consumer
audit](2026-09-22-phase-free-consumer-audit.md) found no current downstream
operation requiring the stricter interface: physical-window scripts study the
lift itself, and the public code has no lift caller. Leave the application
question dormant until a consumer supplies an exact operation and cost
contract. Do not replace the failed advantage proposal with a sequence of
friendlier targets.

The [recursive-G boundary audit](2026-09-22-recursive-g-boundary.md) also
resolves a stale naming conflict. Two-beam ancestral source-G transport is
proved through every finite depth; native descendant G remains generally
completion-dependent; one-beam typed compression is open but dormant. Do not
schedule “recursive G” without naming which of these objects is intended.

The only remaining experiment still marked planned was the 2026-09-10
representation-empowerment census. A prospective
[endpoint and cost audit](2026-09-22-representation-empowerment-disposition.md)
parks it unrun. Its primary stable-future outcome includes the post-action
observation, so identity attains the binary channel's one-bit ceiling for every
rule; a broad census would not test dynamical persistence. Any replacement
needs a delayed fixed target, common cadence, action-phase controls, a named
consumer and a cost baseline under a new protocol.

The CA/CRDT connection produced a completed fixed-interface retention result,
not a fifth program. The dimensional existence objective is complete. The
Class-IV, refinement, arithmetic and recoder extensions remain parked unless
they meet the reopening conditions in the survey.

## Completed bounded unit

The [three executable case studies](representation-case-studies.md) now let a
reader distinguish:

1. the proposed effective law being wrong;
2. the observation having no autonomous law on its declared domain;
3. a finite-ring claim failing to transfer to the infinite line.

Each has a fast verifier and explicit certificate. The separately frozen
[causal-retention audit](2026-09-21-causal-retention.md) adds a restricted
lower bound: Rule 110's Nakamura interface requires all twelve local states
when current/phase readout, radius one and atomic-update semantics are fixed.
It is compatible with established eight-state simulators that change protocol.

The [agent handoff](NEXT_TASK.md) records publication through PR #282 and
targeted verification. On main, this unit is integrated. No new
numerical campaign is queued. The readout design unit closed its candidate
comparison under a marked-track interface; the
closed direct-quotient question does not need more rings or source rules.

## What we have, and what is parked

| Thread | State and evidence | Condition for further work |
| --- | --- | --- |
| The Groovy Field | **Latest bounded unit complete.** [1D second-generation closure](2026-09-23-groovy-1d-second-generation.md): nonconstant inherited positives for 2/16 under specified laws; 32 fails for both radius-one choices; 33 pointwise cases collapse to constants. | Follow the [latest handoff](checkpoints/groovy-1d-second-generation.md). The [third generation](2026-09-23-groovy-1d-third-generation.md) extends both 2/16 on an explicit branch. Memory-bearing cases such as Rule 30 remain open; no fourth generation is queued. |
| Erased distinctions / representation invariants | **Bounded units complete.** Three executable representation cases, the restricted Rule-110 causal-retention lower bound, and the [original-source G autonomy boundary](2026-09-22-rule110-g-autonomy.md). The [depth-three onset result](2026-09-14-depth-three-onset.md) remains integrated. | Start from the completed unit (PR #282). Further depth or observation searches need a question whose answer changes a decision. |
| Dimensional lift | **Existence and finite recursion closed; application dormant** under the [affine-oriented theorem's contract](2026-09-17-affine-oriented-lift-theorem.md) and [consumer audit](2026-09-22-phase-free-consumer-audit.md). No current downstream caller, uniqueness, optimality or spontaneous organization theorem. | A concrete locality, readout or intervention advantage over ordinary history and the proof's period-three necklace construction, charging encoding and preprocessing costs fairly. |
| Class-IV discriminator | **Frozen finite benchmark**, with [partial original provenance](2026-09-17-selective-persistence-discriminator-record.md). Its two core positive families are 54 and 110. | An independently defined target and external validation domain; no further feature search on the same labels by default. |
| Refinement fibers / defects | **Paused.** Local mechanisms are useful in their stated height-two family. The [held-structures completion and correction](2026-09-21-held-structures-account.md) preserves the ninth unit and invalidates three mistimed predictor scores. | A standalone scientific payoff and a bounded protocol; a corrected run is required before reusing those three scores. There is no automatic tenth unit. |
| Source-recoder recovery (PR #231) | **Archived, incomplete:** 14/22 classified, eight unresolved; no certificate found in the frozen search. Data, code and resumable checkpoints are integrated. | A structural result or a credible method improvement with a small benchmark and hard budget. “More solver time” alone is insufficient. |
| Predictive assembly support (PR #172) | **Archived, unevaluated:** protocol and implementation preserved; no canonical PAS result. The last off-Actions attempt has an unrecovered outcome. | A concrete use for minimum-test-collection support beyond renaming feature selection, plus a bounded execution plan. |
| Ring arithmetic, weighted cohabitation, broader observation catalogs, older history/possibility proposals | **Parked.** Negative and partial results stay available. | A mechanism, comparison and stopping rule that justify reopening the line. |

Parking an incomplete computation does not turn it into a negative theorem.
Scheduling can stop while the mathematics remains open. The old protocol's
22/22 scientific completion condition does not obligate indefinite spending.

## Rules for choosing the next unit

Before a new experiment, answer these four questions in a short paragraph:

- What uncertainty matters to the project?
- What result would change the next action, including a negative result?
- What existing theorem, simpler method or baseline must this beat?
- What time/resource limit or result ends this line?

Declare the rule, state family, boundary, observation, cadence, horizon and
resource being measured. Keep an exact theorem, a finite computation, a
sampled observation and a conjecture distinct. A timeout, missing score or
lost artifact is never a scientific negative. Do not reuse observed outcomes
as fresh predictions. Integrity checks verify provenance, not the argument.

Historical research remains at the four Program pages and their checkpoints.
Read only the lineage needed for the chosen task. Do not append the whole
research history to agent instructions. Authorship, evaluation and review
chronology remain in the original records.

## Reset provenance

Myk authorized repository changes, consolidation, closure and merges on
2026-09-21 and explicitly suspended the Fable peer-review protocol **for this
reset**. This authorizes integration and correction, not a claim of independent
scientific review. The [integration record](2026-09-21-research-reset.md)
lists the four preserved PR heads, checks and limits. On 2026-09-22 Myk
retired the standing review gates; review is now requested case by case
(see `AGENTS.md`).

Myk subsequently authorized Codex to set up and continue this case-study and
causal-retention work **solo** on 2026-09-21. Its protocols and notes record
that additional exception. Self-verification does not constitute independent
review; the exception is scoped to this unit and its frozen locality follow-up.
