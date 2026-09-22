# Next agent: one bounded representation-cost design

Updated 2026-09-22. PR #282 integrated the representation case studies and
causal-retention audit; #280 is closed. Do not recreate that work.

Read [START_HERE](START_HERE.md), [the accessible findings](FINDINGS.md), and
[the program survey](2026-09-22-program-survey.md). Historical next-unit
proposals do not override this handoff.

## Recommended deliverable

Write one short comparison contract and a go/no-go recommendation for reading
the **original Rule-110 Groovy field at one site**, comparing direct source
access, ordinary stored time slices, the period-three encoding and the affine
six-field lift. This is design work, not a frozen experiment or a finding of
advantage. Use arbitrary binary configurations on the integer line, a common
synchronous source cadence, and the same output semantics. Specify geometry
and local access before comparing costs.

Count storage, local reads, computation/table size, initialization and upkeep
of derived fields. Do not compare native descendant G with ancestral G or give
one representation free preprocessing. Start from the
[lift theorem and its simpler baseline](2026-09-17-affine-oriented-lift-theorem.md)
and the [locality obstruction](2026-09-21-causal-retention.md).

Budget: one short analysis pass, at most one agent session. Use existing
formulas and certificates. No new simulation, all-rule sweep, solver search,
or expensive replay. Conclude with a precise candidate tradeoff, a baseline
dominance argument, or a named unresolved assumption. Then stop. Failure to
find an advantage does not trigger another benchmark automatically.

A new empirical unit needs its own prospective protocol and applicable review
under AGENTS.md. This scheduling recommendation neither backdates review nor
extends the earlier unit-specific exception to new experiments.

## Maintaining the account

When a unit ends, update FINDINGS.md in plain language: curious about X, tried
Y, found Z, within domain W. Link its evidence and keep negatives, incomplete
computations and invalidated scores distinct. Do not re-run history merely to
write a summary. Preserve all canonical result bytes.

The other programs remain parked as described in START_HERE. There is no
parallel fifth CA/CRDT program and no automatic next numerical experiment.
