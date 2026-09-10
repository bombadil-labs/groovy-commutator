# Finite program edits cannot switch a global rule everywhere in bounded time

A radius-R cellular automaton can move disagreement only distance Rt after t ticks. A fixed local decoder whose output anchors meet bounded target regions only finitely often therefore decodes only finitely many changed source cells from a finite physical edit at any common finite time.

Changing a globally applied ECA instruction has a period-three source witness with infinitely many changed next-output sites. Thus a fixed local interpreter cannot implement that global change through finitely many cell edits at a common finite cadence.

The [research note](../research/2026-09-09-program-edit-locality.md) states and proves the exact assumptions and gives a finite-world edit/latency bound. All 6,144 periodic witness cases and 2,048 local program-field cases pass the frozen audit.

This corrects the globally uniform reading of the previous finite-program-edit proposal. Local program-field edits, distributed global edits, and finite regions with propagation latency remain possible. The result does not prohibit mutable spatial programs, recursive typing, or universal computation.
