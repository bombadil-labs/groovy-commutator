# Dimensional compatibility and axis order are separate constraints

In the fixed axial ECA family,24 of256 sources have commuting operators on distinct axes. A complete512-patch plane test and the adjacent-transposition proof establish axis-permutation equivariance in every dimension. All16 affine rules pass; eight additional rules are AND/OR functions.

Exactly14 also preserve the literal-replication beam:0,128,136,150,160,170,192,204,238,240,250,252,254,255. They are constants, copies, ternary parity, and AND/OR functions. A further52 sources preserve replication while depending on axis order. Rule90 commutes but fails replication; Rule232 preserves replication but has72 axis-order disagreements.

This concerns permutations of axes, not reflection invariance or arbitrary higher-dimensional rules. Simple or degenerate controls remain in the count. Full ambient Rule128/150/254 respectively take AND/parity/OR over the entire3^d block, so guard-free compatibility is not restricted to one-site copies.

See the [checkpoint](../research/2026-09-10-guard-free-axial-lift.md) for exact lists, witnesses, proof, and independent reproduction. No novelty or Class-IV inference is made.
