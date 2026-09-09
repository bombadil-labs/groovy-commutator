# Provenance completes the dimensional shell

The dimensional-lift search had an apparently unused center cell. A natural proposal is to put there the **local derivative bit that produced the present lower-dimensional center value**.

For a binary trajectory, write

\[
\delta_t = c_{t-1}\oplus c_t.
\]

The proposal is not to treat this as decorative metadata. The center stores local provenance: together, `(c_t, delta_t)` recovers `c_{t-1}`.

## The first exact coincidence

An unrestricted elementary cellular automaton has eight truth-table output bits. A radius-one 2D Moore neighborhood has eight shell cells plus one center.

Therefore

\[
8\text{ rule bits}+1\text{ derivative bit}=9=3^2.
\]

With any fixed bijection `sigma` from the eight ECA truth-table entries to the eight shell positions, define the completed spatialization

\[
P_{1,\sigma}(R,\delta)\in\{0,1\}^{3\times3}
\]

by placing `R` on the shell and `delta` at the center.

This is an exact bijection

\[
\{0,1\}^8\times\{0,1\}\cong\{0,1\}^9.
\]

Equivalently,

\[
\{\text{256 ECAs}\}\times\{0,1\}\cong\{\text{512 binary 3x3 patches}\}.
\]

This is a representation identity, not yet a dynamical closure result. A trajectory-derived derivative is constrained by the lower-dimensional past; the bijection only says that the *representation type* has no unused states.

## A recursive shell-coded rule language

The coincidence suggests a dimension-independent type.

A radius-one Moore neighborhood in dimension `d+1` has

\[
3^{d+1}
\]

cells. Its shell has

\[
s_d=3^{d+1}-1
\]

cells.

Define a candidate shell-coded `d`-dimensional rule description to contain `s_d` bits, with one additional derivative/provenance bit completing the next-dimensional neighborhood:

\[
\mathcal R_d^{\mathrm{shell}}=\{0,1\}^{3^{d+1}-1},
\]

\[
\mathcal R_d^{\mathrm{shell}}\times\{0,1\}
\cong
\{0,1\}^{3^{d+1}}.
\]

The first sizes are

| source dimension | shell-coded rule bits | completed next-dimensional neighborhood |
| ---: | ---: | ---: |
| 0 | 2 | 3 |
| 1 | 8 | 9 |
| 2 | 26 | 27 |
| 3 | 80 | 81 |
| 4 | 242 | 243 |

The `d=0` term is already an ordinary unrestricted rule space: a binary zero-dimensional deterministic system updates one bit from its current value, so its truth table has two entries. The `d=1` term is also ordinary and unrestricted: its eight bits are exactly the full ECA rule table.

Thus the recurrence is not introduced only after seeing the ECA coincidence. It begins

\[
\text{all binary 0D rules}\to\text{all binary 1D ECA rule codes}\to\text{candidate 26-bit 2D shell rules}\to\cdots
\]

with the first two rule spaces already standard.

At `d=2`, the ansatz proposes a 26-bit native rule language, much smaller than the 512-bit unrestricted Moore truth table. This is potentially the missing recursive compression mechanism.

## A natural selector semantics for shell rules

The shell cardinality also suggests a uniform *form* for the local rule, even though the required address maps are not yet known.

Let

\[
S_{d+1}=\{-1,0,1\}^{d+1}\setminus\{0\}
\]

be the set of shell offsets, so `|S_{d+1}|=3^{d+1}-1`.

A shell-coded rule `r` is a bit assignment

\[
r:S_{d+1}\to\{0,1\}.
\]

If there exists a fixed, rule-independent address map

\[
A_d:\{0,1\}^{3^d}\to S_{d+1},
\]

then the corresponding `d`-dimensional local update can be written as the selector

\[
F_r(x)=r(A_d(x)).
\]

At `d=0`, the input neighborhood has one bit and there are two shell positions in 1D, so `A_0` can be a bijection.

At `d=1`, there are eight 3-bit input patterns and eight shell positions in 2D, so `A_1` can again be a bijection. This is exactly the existing ECA truth-table-to-Moore-ring selector family, modulo the choice of spatialization.

At `d=2`, the first genuine compression problem appears:

\[
A_2:\{0,1\}^{9}\to S_3,
\]

mapping 512 binary 2D Moore neighborhoods to only 26 shell directions in 3D.

So the recursive-lift problem can be sharpened further:

> **Find a dimension-uniform, rule-blind family of address maps `A_d` whose first two members reproduce ordinary unrestricted 0D and 1D rules and whose higher members give composable shell-coded rules.**

The derivative completion may be relevant precisely because every `d`-dimensional neighborhood in this shell language can be parsed recursively as a lower-dimensional shell rule plus one provenance bit:

\[
\{0,1\}^{3^d}
\cong
\mathcal R_{d-1}^{\mathrm{shell}}\times\{0,1\}.
\]

Therefore an address map may equivalently be sought in recursive form

\[
\widetilde A_d:\mathcal R_{d-1}^{\mathrm{shell}}\times\{0,1\}\to S_{d+1}.
\]

This does not yet determine `A_d`, but it turns the higher-dimensional input from an undifferentiated `3^d`-bit pattern into exactly the pair suggested by the construction: **a lower-dimensional rule code plus the derivative/provenance bit at its center**.

## Why the derivative is structurally natural

For an ECA address `q=(L,C,R)` with output `R(q)`, the local derivative of the center under that transition is

\[
\Delta_R(q)=C\oplus R(q).
\]

Thus every ECA also has a canonically associated eight-bit derivative truth table. In Wolfram-number bit ordering this is

\[
\Delta R = R\oplus 204,
\]

because Rule 204 is the identity rule `C`.

There are therefore two related but distinct uses of derivative information:

1. **event derivative:** the single realized `delta_t` stored at the completed patch center;
2. **rule derivative:** the eight-bit table `Delta R`, a rule-independent transform of the whole rule table.

The present dimensional-shell proposal is primarily about the first. The second is retained as a candidate ingredient for the lift semantics rather than silently conflated with it.

## The operator target becomes sharper

The shell identity gives a representation type but not yet the lift operator.

We seek one rule-blind construction, fixed before class labels, of the form

\[
L_d:\mathcal R_d^{\mathrm{shell}}\rightharpoonup\mathcal R_{d+1}^{\mathrm{shell}}.
\]

A promising closure equation would use a fixed next-dimensional update `F_{d+1}` and the completed embedding `P_d`:

\[
F_{d+1}(P_d(R,\delta))
=
P_d(L_d(R),g_d(R,\delta)),
\]

for both derivative values whenever `R` lies in the domain of `L_d`.

This equation would mean:

- the shell evolves autonomously to the next rule code `L_d(R)`;
- the center carries the updated derivative/provenance bit;
- no hidden external decoder is needed;
- the same `F`, completion convention, and extraction rule apply across source rules.

This is an ansatz, not an established law. In particular, the existing eight-bit selector supplies one concrete `d=1` local architecture, but there is not yet a canonical dimension-independent address map that turns an arbitrary 9-bit 2D Moore neighborhood into one of 26 shell directions in 3D.

That missing semantic rule is now the central operator-discovery problem.

## Relation to the earlier table-size obstruction

The unrestricted truth-table ladder explodes:

\[
2^{3^d}
\]

output bits would be required to describe an arbitrary binary radius-one Moore rule in dimension `d`.

The shell-coded language instead grows geometrically:

\[
3^{d+1}-1.
\]

So the proposal does not make the old obstruction disappear; it replaces the unrestricted native-rule family with a recursively typed compressed family whose first two members coincide with ordinary unrestricted binary rule spaces in dimensions zero and one.

This produces three mutually exclusive possibilities worth distinguishing:

1. a canonical shell-rule semantics exists and gives a uniform lift operator across a nontrivial domain;
2. several natural semantics exist, giving a frozen operator family whose closure domains can be measured;
3. no nontrivial recursive semantics can satisfy locality, overlap compatibility, provenance completion, and rule-blindness simultaneously.

Any of these is a useful result.

## Immediate next test

Do **not** join Wolfram classes yet.

First search for a rule-independent local semantics for shell codes satisfying the `d=0` and `d=1` ordinary-rule behavior and admitting a well-typed `d=2` rule family. Candidate semantics should be ranked only by structural requirements fixed in advance:

- locality;
- translation equivariance;
- compatibility with rotations/reflections up to coordinate conjugacy;
- no rule-specific decoder;
- the completed center has derivative/provenance semantics;
- the output shell can be extracted without trajectory-specific fitting;
- composability from 0D to 1D to 2D to 3D.

Only after one or more operators are frozen should their closure domains be compared with Class-IV labels.
