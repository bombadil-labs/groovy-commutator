# Protocol: oriented Moore-ring overlap census

Date: 2026-09-09
Status: preregistered before enumeration

## Question

Given the existing encoding of an elementary CA's eight rule-output bits on the eight cells surrounding the center of a 3x3 Moore neighborhood, can copies of that rule geometry coexist on an extended 2D lattice when overlapping neighborhoods must agree?

The earlier dimensional-lift note proves that if every site must see the *same fixed orientation* of the same eight-bit ring, only the all-zero and all-one tables survive. Here we relax only physical orientation: each site may see any rotation or reflection of one fixed square-ring pattern.

This is an overlap-consistency test, not yet an evolution or recursive-closure test.

## Frozen geometry

Number ring positions clockwise beginning at north:

`N, NE, E, SE, S, SW, W, NW`.

For ECA rule number `r`, use its standard eight output bits in address order `0..7`, least-significant output bit first. The default ring pattern puts bit `k` at ring position `k`. This is the same underlying eight-bit storage convention as the shared-state-rule work before arbitrary permutation search.

The allowed local orientation group is the physical dihedral symmetry group of the square, `D4` (four rotations and four reflections). No arbitrary `8!` permutation is allowed in the primary test.

For a periodic `n x n` binary field `X`, let `ring_X(x)` be the ordered eight-neighbor pattern around site `x` in the frozen compass order. `X` is an oriented rule field for `r` iff for every site `x`, `ring_X(x)` belongs to the `D4` orbit of the rule ring for `r`.

The center bit is unconstrained by this definition.

## Primary finite census

Enumerate all binary periodic fields exactly for `n=3` and `n=4`.

For every ECA `r=0..255`, record:

- whether an oriented rule field exists at each size;
- the exact number of satisfying fields;
- the rule's `D4` ring-orbit size;
- one canonical witness when nonempty.

Do not attach Wolfram class labels until the complete rule-by-size table has been written.

## Symmetry handling

The rule-bit ring has its own physical `D4` orbit. ECA reflection/complement conjugacies are recorded separately after enumeration; they are not added to the allowed local orientation set unless they are literally induced by a physical `D4` transformation of the stored ring.

Rules related by global bit complementation may naturally map satisfying fields to complemented fields; this should be audited after the primary table rather than assumed.

## Interpretation

Passing means only that the local rule-table geometry can be made spatially self-consistent across overlapping 2D neighborhoods up to physical orientation.

It does **not** yet mean:

- that the field evolves under a native 2D rule;
- that the rule representation persists after an update;
- that a unique orientation can be decoded locally;
- that the construction lifts again to 3D;
- or that the property is related to Wolfram Class IV.

If no nontrivial ECA passes, this particular unblocked Moore-ring route is obstructed before dynamics and should not be tuned post hoc to rescue Class IV.

If a selective set passes, the next preregistered test should add the existing selector evolution and ask whether the satisfying subshift is invariant or has long persistence.

## C4 hypothesis relation

The user-supplied strong hope is that dimensional rule closure may characterize Class IV. This overlap census is only an early necessary-condition candidate. We will report its rule set first and compare to frozen class labels second. Failure to isolate Class IV here is not grounds to change the orientation group or ring permutation within this checkpoint.
