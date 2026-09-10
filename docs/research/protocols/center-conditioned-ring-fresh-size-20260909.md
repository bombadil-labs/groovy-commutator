# Protocol: fresh-size center-conditioned rule-ring confirmation

Date: 2026-09-09
Status: preregistered after the 4x4 exploratory discovery and before 5x5/6x6 evaluation

## Discovery being tested

The preregistered single-rule oriented-ring overlap census admitted only Rules 0 and 255 on 3x3 and 4x4 periodic fields.

After that result was known, an exploratory relaxation allowed the D4 orbit of the eight-bit rule ring to depend on the local center bit. On 4x4 this produced exactly 38 nonuniform fields in six ordered center-conditioned orbit pairs:

`(14,31), (39,54), (54,39), (85,170), (91,41), (187,17)`.

The appearance of Rule 54 is interesting because it is a robust canonical Class-IV ECA, but the discovery is post-hoc and is not confirmatory evidence.

## Frozen fresh-size test

Evaluate exactly the six ordered pairs above on periodic square lattices of sizes:

- `5x5`
- `6x6`

No additional pairs, arbitrary ring permutations, complement operations, or non-D4 orientations may be introduced in this note.

For pair `(r0,r1)`, a field is valid iff:

- every site with center bit 0 has an eight-neighbor Moore ring in the physical D4 orbit whose canonical representative is `r0`;
- every site with center bit 1 has a ring in the D4 orbit whose canonical representative is `r1`.

The center itself is not part of the stored ring.

## Exact solver

Use row transfer with periodic horizontal boundary conditions.

For width `n`, a local constraint is determined by three consecutive rows `(a,b,c)`. A transition `(a,b) -> (b,c)` is allowed iff every 3x3 neighborhood centered in row `b` satisfies the frozen center-conditioned ring constraint.

Periodic `n x n` fields are exact length-`n` row cycles with both vertical wrap constraints checked. Count every field in fixed row coordinates once; do not quotient translations/rotations in the primary counts.

Independently audit every returned witness by reconstructing all `n^2` local rings directly.

## Primary outputs

For each frozen pair and size record:

- exact number of valid periodic fields;
- one witness if nonempty;
- number of valid row-pair transitions;
- direct witness-audit pass/fail.

The primary fresh-size question is persistence of the spatial representation, not Wolfram class.

## Secondary inherited-dynamics diagnostic

If a pair has valid fresh-size fields, apply the existing shared-state selector with its inherited default encoding under both horizontal and vertical address axes.

For every valid field when enumeration remains tractable, record:

- whether one selector step remains in the same center-conditioned pair;
- whether it remains in *any* of the six frozen center-conditioned pairs;
- persistence depth until first exit, capped only if exact cycle detection is infeasible;
- exact cycle length when a closed cycle is detected.

If field counts become large, freeze a deterministic complete-state sampling rule before evaluating selector dynamics. Do not select witnesses for interesting behavior after looking at outcomes.

## Class-IV interpretation

The fresh-size test is not designed to prove the Class-IV conjecture. It asks whether the 4x4 center-conditioned rule ecology is a size artifact.

The Class-IV lead becomes more interesting if pair(s) containing Rule 54 survive at fresh sizes while many other discovered pairs disappear or fail dynamically. It becomes less interesting if all six survive similarly, if Rule-54 pairs disappear, or if persistence is controlled by an obvious periodic/symmetry mechanism unrelated to complexity.

No geometry may be retuned in this note to rescue Rule 54.
