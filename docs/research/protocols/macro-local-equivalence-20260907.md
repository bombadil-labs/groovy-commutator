# Local equivalence audit: frozen extension

The [first macro protocol](revisable-primitives-20260907.md) compares full
transformations on rings of width 6, 9, and 11. The first completed results
include programs shorter than the literal target, and a revised macro whose
word differs from the target's word. Finite rings can identify transformations
that differ on larger configurations. This extension asks which conclusions
survive that issue.

The [configuration](macro-local-equivalence-20260907.json) freezes the same
rule-pair panel, all words up to eight ticks, and a 17-cell causal window.
A radius-one CA word of length at most eight can affect a central cell only
through that window. Comparing every one of its 131,072 binary assignments
therefore checks equality of local maps, without a chosen periodic width.
Translation invariance extends equal central outputs to equal complete
transformations on every configuration, including every positive ring width.

The search for inexpensive programs remains bounded to eight physical ticks.
All prices, inherited and target words, and job counts stay exactly as in the
parent protocol. This removes finite-ring coincidences; it does not establish
unbounded optimal programs or a model of autonomous learning.

Audit every program in the parent's selected witnesses, preserving the first
counterexample window for any failure. Compare finite-ring and local target
equivalence classes and minimum execution costs. Re-run the same resource
comparisons with local equivalence. Independent shrinking-window evolution
checks the saved program comparisons.

This extension was chosen after seeing the parent's outcomes. Its protocol is
committed before the new enumeration, and it will be reported as a follow-up
rather than as independent confirmation of a preregistered hypothesis.
