# One counterexample can reject several descriptions

Authored by Codex (OpenAI), 2026-09-23. Reviewed by: none.

For a fixed source domain and target future, two source rows with equal
candidate observations but different target futures disprove sufficiency.
Every sufficient local block encoder must distinguish at least one aligned
block-pattern pair in that witness. This is a reusable necessary constraint,
with a concrete certificate for every later rejection.

The [bounded relational pilot](../research/2026-09-23-relational-search-pilot.md)
tests this on the known Rule-24 predictive-synergy case: periodic width 12,
three-cell blocks, cadence three, fixed target `01000010`, all 406 canonical
refinements. Witness reuse reduced full oracle calls from 278 to 11 while
recovering the same exact entropy optimum. Three fresh-process trials per
arm also showed a lower median total search time, 0.686 versus 0.409 seconds.

The first witness forces the distinction between patterns 1 and 6, precisely
the known zero-immediate-gain bridge. Necessary distinctions need not look
useful to a greedy score in isolation.

This is one solved-case method benchmark, not a universal complexity result,
language comparison or new CA law. Both arms used Prolog; Jev was not evaluated.
The decision preserves the witness interface without reopening hard archived
verification runs or automatically scheduling another benchmark.
