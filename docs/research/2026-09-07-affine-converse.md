# A zero commutator does not imply a linear rule

## What changed

An earlier version of this project said that the commutator was constant
**if and only if** the evolution rule was affine. Affine evolution does imply
a constant commutator. The converse does not hold: Rules 4 and 200 are nonlinear,
yet both have an identically zero commutator.

This is a correction to the explanation, not a change to the CA engine.
The counterexamples were already visible in the older two-engine sweep;
the exhaustive check in the September research checkpoint made the
contradiction explicit.

## The statement that survives

Write evolution as E and its outgoing change mask as D(S)=S XOR E(S).
The commutator compares D(E(S)) with E(D(S)). If evolution has the affine
form

\[
E(S)=MS\oplus c,
\]

where M is linear over binary arithmetic and c is a fixed bias, then

\[
D(E(S))=MS\oplus M^2S\oplus Mc,
\]

while

\[
E(D(S))=MS\oplus M^2S\oplus Mc\oplus c.
\]

Their difference is therefore always c. Zero bias gives zero commutator;
a nonzero bias gives a fixed nonzero commutator. This implication does not
depend on working in one spatial dimension.

## The counterexamples

Rule 4 turns on only for the neighborhood 010. Its Boolean expression
is c(1+l)(1+r), with addition interpreted as XOR. Expanding it introduces
products of input bits, so it is nonlinear. Rule 200 has expression
lc + cr + lcr, also nonlinear. Nevertheless, both have G=0 for every
five-cell neighborhood, and therefore at every cell of every configuration.

The commutator of an elementary CA depends on five input cells. Enumerating
all 32 windows is consequently an exhaustive test of its local law; there
is no sampling or burn-in assumption here.

| Constant commutator | Elementary rules |
| --- | --- |
| Zero | 0, 4, 60, 90, 102, 150, 170, 200, 204, 240 |
| One | 15, 51, 85, 105, 153, 165, 195, 255 |

All other elementary rules have a commutator that varies across possible
configurations. A particular trajectory can still settle into a restricted
region where that field becomes constant.

## Why preserve this correction?

The commutator tests a specific compatibility: can the outgoing change mask
be evolved under the same rule as the state? Linearity guarantees a clean
answer, but it is not the only way to get one. Turning a sufficient condition
into a necessary one would obscure those other mechanisms.

The [history comparison](2026-09-07-history-repairability.md) makes a related
distinction: a useful observation is not automatically a complete
classification of the dynamics.

## Reproduce

Run `python scripts/verify_history_algebra.py` from the repository root.
The [script](../../scripts/verify_history_algebra.py) records the exhaustive
tables in [history_algebra_checks.json](../../results/history_algebra_checks.json).
The general affine implication is algebraic; the lists above are specific
to elementary cellular automata.
