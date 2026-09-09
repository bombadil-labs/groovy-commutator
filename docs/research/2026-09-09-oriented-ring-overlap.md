# Fixed rule rings do not tile; center-conditioned rule pairs do

The first preregistered dimensional-closure gate asked whether the existing eight-bit ECA rule ring can be realized consistently at every site of an extended 2D lattice, allowing only physical rotations/reflections of the square.

The answer is clean and negative for the strong Class-IV hope at this level:

- exact `3x3` periodic census: only Rules `0` and `255` admit a field;
- exact `4x4` periodic census: only Rules `0` and `255` admit a field.

So an architecture in which every site literally carries the same eight-bit rule table, even up to `D4` orientation, is too rigid. This is not a Class-IV discriminator; it collapses to the two constant rules in both frozen finite tests.

The result was produced by `scripts/experiment_oriented_ring_overlap.py` under the preregistered `protocols/oriented-ring-overlap-20260909.md`. Class labels were not used in the primary enumeration.

## Why the `3x3` failure is immediate

On a `3x3` torus, the Moore ring around any site consists of all eight other cells. Every allowed orientation of a fixed rule ring has the same Hamming weight. In any mixed configuration, a live center sees one fewer live ring cell than a dead center, so the local ring weights cannot all agree. Hence only the uniform zero and uniform one fields can satisfy the condition.

The `4x4` result is an exact enumeration rather than an all-size theorem.

## Exploratory relaxation after the primary result

After seeing that single-rule overlap was empty except for constants, we made one post-primary relaxation motivated by the earlier layered dimensional encoding:

> allow the local rule-ring orbit to depend on the center bit.

That is, every zero-centered site must see one fixed `D4` ring orbit `r0`, while every one-centered site must see another fixed orbit `r1`.

This is **exploratory**. It was defined after the primary outcome and is not evidence for the preregistered Class-IV hypothesis.

On the exact `4x4` census, 38 nonuniform fields satisfy this center-conditioned property, organized into only six ordered orbit pairs:

| center 0 ring | center 1 ring | fields |
| ---: | ---: | ---: |
| 14 | 31 | 8 |
| 39 | 54 | 8 |
| 54 | 39 | 8 |
| 85 | 170 | 2 |
| 91 | 41 | 8 |
| 187 | 17 | 4 |

The appearance of Rule `54` is notable because Rule 54 is one of the robust canonical Wolfram Class-IV elementary rules. It is paired here with Rule `39`, not isolated, and the observation was made only after defining the relaxed criterion from the failed primary test. It therefore motivates a fresh test but does not count as confirmation.

Published ECA class tables disagree on some boundary rules; Rule 41, which appears in another pair above, is one such classification-sensitive case. That makes a frozen-label sensitivity analysis especially important before interpreting the pair set dynamically.

## Selector persistence is mixed

As an additional exploratory diagnostic, the existing shared-state selector was applied to the 38 center-conditioned `4x4` fields with the default ring encoding.

Some center-conditioned fields immediately leave the family; others lie on short cycles while preserving the center-conditioned property. Examples include:

- `(14,31)`: some fields lie on a four-cycle under the horizontal selector;
- `(39,54)`: some fields lie on a four-cycle under the vertical selector;
- `(91,41)`: some fields lie on four-cycles under either axis;
- `(187,17)`: all four fields lie on a two-cycle under the horizontal selector.

The `(54,39)` orientation itself does not persist beyond the initial state under either default selector axis in this `4x4` census, while the reversed `(39,54)` pair has a persistent vertical subset.

These short-cycle results are descriptive only. The selector axis and default bit placement were inherited from the prior construction, not optimized for class separation.

## What this changes

The useful object may not be a single rule copied everywhere. The overlap constraints naturally suggest a **state-conditioned rule ecology**: the local center state and the surrounding rule geometry jointly determine which rule table is represented at that site.

That rhymes with the separate outer-totalistic dimensional lift, where the rule table is indexed by center value as well as neighbor count. It also gives a concrete next question that can be tested on a fresh size without retuning:

> Do the six center-conditioned rule-pair subshifts discovered at `4x4` survive on larger periodic lattices, and if so which of them remain invariant under the inherited selector dynamics?

A fresh-size protocol should be committed before testing that question. The Class-IV comparison should remain secondary until the larger-size structural table is frozen.
