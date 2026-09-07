# History-repairable nonclosure

## Result

A simple pilot suggested:

> Class IV = coarse nonclosure whose missing context is repaired by finite history.

The broad sweep **falsifies that simple statement**. Periodic Class-II rules are
often highly history-repairable too. The stronger surviving pattern is a
negative-space combination: substantial present-state nonclosure, strong repair
by path/history, and trajectory structure that is neither crystalline nor
effectively random.

Using a full-256 published Wolfram-class assignment, 3-cell majority
coarse-graining, four macro-history steps, and non-power-of-two lattices:

| class | median e0 | median e4 | median repair | median raw compression |
|---|---:|---:|---:|---:|
| I | 0.000 | 0.000 | n/a | 0.003 |
| II | 0.104 | 0.000 | 0.891 | 0.063 |
| III | 0.416 | 0.097 | 0.767 | 1.001 |
| IV | 0.268 | 0.039 | 0.861 | 0.458 |

`e0` is held-out next-macrocell error from the current radius-1 macro
neighborhood. `e4` adds four previous radius-1 macro neighborhoods.

Interpretation:

- **I:** exact/trivial closure.
- **II:** history often repairs apparent nonclosure by locating a low-dimensional
  periodic phase; raw spacetime is highly compressible.
- **III:** strong nonclosure with a materially larger residual after history;
  raw spacetime is typically near-incompressible.
- **IV:** substantial initial nonclosure, low historical residual, intermediate
  structure.

A deliberately crude exclusion screen (`e0 > .15`, `e4 < .10`,
`.10 < compression < .95`) selects:

- I: 0 / 24
- II: 10 / 192
- III: 6 / 26
- IV: 9 / 14

These thresholds are **not a proposed classifier**; they only show that the
joint residual condition is far more Class-IV-enriched than repairability
alone.

## Observer dependence

On the 88 canonical inequivalent representatives, parity coarse-graining
separates the three Class-IV exemplars:

- Rule 110: strongly repairable at blocks 2 and 4.
- Rule 54: strongly repairable at block 2, weaker at block 4.
- Rule 106: poorly repairable under parity, even though it is Class IV.

With 3-cell majority projection, however, all three become strongly repairable
(approximately 93%, 73%, 93% repair respectively in the corrected sweep).

Therefore:

> **History repairability is a property of dynamics × projection, not of a rule alone.**

That is a first-class result, not nuisance variance.

## Methodological correction

Early pilots used a 256-cell ring. This was caught and corrected: additive
rules such as Rule 90 can have special/nilpotent behavior on power-of-two
tori. The broad empirical sweeps use `n=300` for block experiments and
`n=301` for raw compression. Exact algebraic Rule-90 identities are unaffected.

## Current hypothesis

> **Class-IV-like dynamics are enriched for nontrivial nonclosure whose missing
> context remains encoded in history, while avoiding both low-dimensional
> periodic closure and effectively noisy residual uncertainty.**

Informally:

> **The present is insufficient, but the path is not lost.**

## Next

- Fit explicit memory kernels / Mori-Zwanzig-style reduced dynamics.
- Measure minimum sufficient history `H*_L(epsilon)` versus coarse scale.
- Sweep projection families and identify observer-robust invariants.
- Study entire repair curves rather than one history depth.
- Repeat on systems with a tunable genuine critical point.
