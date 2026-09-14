# Difficulty in one exact symbolic representation is not evidence of hard dynamics

Across the phase-splice / source-recoder frontier the same exact mathematical
question was posed twice in different encodings and behaved completely
differently.

Reduced ordered 8-valued MDDs carry the exact local dynamics of this frontier
cheaply — cheaply enough to clear the explicit sofic-graph wall, where raw
finite-horizon construction grew from 17 transitions at `h = 0` past the frozen
five-million-transition ceiling by `h = 3`. Yet phase-splice MDD evaluation
still censored all twelve Rule 122 / Rule 161 sentinel languages under its
frozen wall. Encoded directly as fine-ECA CNF, those *same* candidates were
tiny and completed exactly: `minisat22` recovered all twelve as negatives with
at most 1,314 variables and 9,943 clauses.

The moral the program adopted from this, and applied consistently afterwards:

> A censoring is a statement about the chosen proof representation and its
> resource envelope, unless an independent mathematical obstruction is
> supplied.

Compact exact local evolution does not imply a compact reachability proof, and
an expensive reachability proof does not imply intrinsically complex dynamics.
The two notions were separated rather than collapsed.

## Scope and limits

This is an exact observation on one frontier with a small number of encodings
(explicit sofic graphs, MDDs, fine-ECA CNF), not a theorem relating
representation classes in general, and not a claim that SAT, MDD, or sofic
difficulty measures the computational complexity of the underlying CA. It does
not say every wall dissolves under re-encoding; it says a wall alone is not
evidence.

What would change the account: a frontier question shown hard under a
representation-independent lower bound, which would convert one of these
censorings into a genuine mathematical obstruction.
