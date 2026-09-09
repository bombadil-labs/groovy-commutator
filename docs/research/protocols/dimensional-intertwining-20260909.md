# Protocol: dimensional intertwining

## Question

Can a one-dimensional cellular automaton with update `F1` be embedded into a two-dimensional cellular automaton with its own local update `F2` so that evolution commutes exactly with the embedding?

The target identity is

$$
F_2 E = E F_1.
$$

For binary systems, the corresponding cross-dimensional residual is

$$
K_E(s)=F_2(E(s))\oplus E(F_1(s)).
$$

The first goal is existence, not selectivity: construct explicit families with `K_E=0` for every source state. A later question is whether nonzero residual structure distinguishes interesting dynamics.

## Distinctions fixed before evaluation

We will keep three notions separate.

1. **Exact commuting lift.** `E` is injective, its image is invariant under `F2`, and `F2 E = E F1`.
2. **Geometrically two-dimensional local law.** The essential input offsets of `F2`, measured from the updated cell, linearly span two spatial directions. This excludes a rule that merely ignores one coordinate after a rotation or shear.
3. **Two-dimensional encoded degrees of freedom.** The encoded family itself supports independent variation in two dimensions. The diagonal-stripe construction below does not satisfy this stronger condition; it has one logical degree of freedom per anti-diagonal.

A result for (1) and (2) must not be reported as a result for (3).

## Fixed embedding

For a one-dimensional configuration `s : Z -> {0,1}`, define

$$
E(s)(x,y)=s(x+y).
$$

Thus encoded configurations are constant on anti-diagonals and satisfy

$$
X(x+1,y)=X(x,y+1).
$$

This encoding is fixed before examining any ECA class labels.

## Construction A: active stencil lift

For an elementary rule `f(l,c,r)`, define

$$
F_2^{\mathrm{active}}(X)(x,y)
=f\bigl(X(x-1,y),X(x,y),X(x,y+1)\bigr).
$$

On the encoded family these three cells represent logical offsets `-1, 0, +1`, respectively. The local identity should therefore hold for all 256 elementary rules.

We will compute which source rules have both left and right inputs essential. For exactly those rules, the essential nonzero offsets `(-1,0)` and `(0,1)` are linearly independent, so the lifted rule is geometrically two-dimensional under the fixed criterion.

No Wolfram class labels will be loaded for this count.

## Construction B: defect-gated two-dimensional extension

For an elementary rule `f`, define the horizontal base update

$$
B_f(X)(x,y)=f\bigl(X(x-1,y),X(x,y),X(x+1,y)\bigr).
$$

Encoded states satisfy `X(x+2,y)=X(x+1,y+1)`. Define

$$
F_2^{\mathrm{gate}}(X)(x,y)
=B_f(X)(x,y)\oplus X(x+2,y)\oplus X(x+1,y+1).
$$

The added term vanishes on every encoded state, so this construction should intertwine every ECA exactly. Its two added offsets `(2,0)` and `(1,1)` are linearly independent and are not read by the horizontal base rule, so they should remain essential for every source rule. This should give a geometrically two-dimensional extension for all 256 ECAs, including constant and one-sided rules.

This construction deliberately permits the extra two-dimensional dependence to be dormant on the encoded subspace. It is therefore weaker than requiring irreducible two-dimensional coupling to remain active on encoded states.

## Checks

The verifier will:

- enumerate all 256 ECAs and all 8 local source triples;
- verify the local intertwining identity for both constructions;
- compute the essential logical inputs of each ECA;
- compute the directional rank of essential physical offsets for the active lift;
- independently enumerate the truth table of the gated lift over its five distinct physical inputs and verify that `(2,0)` and `(1,1)` are essential for every rule;
- verify global commutation on square periodic tori for selected rules and all source states at widths 3 through 6;
- save a machine-readable JSON summary.

The algebraic identities, if correct, are the primary evidence. Exhaustive computation is an audit of the implementation and the finite examples, not the basis for extrapolating the theorem.

## Interpretation boundary

A positive result establishes a cross-dimensional intertwiner: the same temporal dynamics occurs inside an invariant family of a higher-dimensional CA. It does not establish that the encoded family has intrinsically two-dimensional state complexity, nor that every natural 1D-to-2D projection admits such a closing rule.

The next research question after existence is to characterize a fixed encoding `E` for which a local `F2` exists at all, and then to ask what minimum two-dimensional state complexity or active coupling can coexist with exact commutation.
