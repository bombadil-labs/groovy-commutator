# Fanout turns dimensional role closure back into the Groovy commutator

The derivative-completed lift suggested a three-role table `[rule | state | derivative]`. Several increasingly permissive role-algebra controls now show exactly what is missing from the naive version.

## One-to-one role rows are too strict

The [selector-only protocol](protocols/role-algebra-closure-20260909.md) checks all 162 fixed selector/permutation algebras on the eight one-dimensional center-independent totalistic source rules. Only the constant-zero source closes.

Allowing each role row either ordinary evolution or its own derivative increases the frozen family to 1,296 candidates, but the [Groovy role-algebra protocol](protocols/groovy-role-algebra-20260909.md) still finds no nonconstant source. Constants zero and one survive.

The obstruction is partly representational: these searches require `rule` itself to occupy and reproduce a physical state row, even though the lifted rule table already contains it.

## Fan out state and derivative instead

The [fanout protocol](protocols/fanout-role-algebra-20260909.md) therefore uses three physical rows carrying only state `S` and derivative `D`, with both roles represented and one duplicated. Each row may choose any of the three lifted rule blocks and either evolve or differentiate under it.

On the three-cell totalistic control family, nonconstant closure reappears exactly for source tables `(0,1,0)` and `(1,0,1)`, the ECA Rule-90 / Rule-165 pair.

For Rule 90 the simplest successful algebra is:

- encode `S,S,D`;
- evolve every row under the original source rule.

Because Rule 90 is linear,

\[
F(S)=S^+
\]

and

\[
F(D)=F(P\oplus S)=F(P)\oplus F(S)=S\oplus S^+=D^+.
\]

The derivative row therefore closes for exactly the same reason the original Groovy commutator vanishes.

## The full 256-rule ECA census

The preregistered [all-ECA fanout protocol](protocols/eca-fanout-role-algebra-20260909.md) freezes the same six `S/D` row encodings and the same 216 operation triples per encoding, but uses the existing eight-bit ring substrate in which every pattern can be read as either an ECA rule table or an eight-cell state.

Across all 256 source rules and all 256 predecessor states, exactly eleven source rules admit at least one fanout algebra:

\[
\boxed{0,4,51,60,90,102,150,170,200,204,240}.
\]

Ten of these are exactly the complete zero-Groovy-commutator family on this substrate:

\[
\boxed{0,4,60,90,102,150,170,200,204,240}.
\]

The equality is exact, including the previously known nonlinear zero-commutator Rules 4 and 200. The earlier correction note already established that zero commutator does not imply linearity.

Rule 51 is the only extra fanout source. It maps every state to its bitwise complement, so its outgoing derivative is always the all-ones pattern. That constant derivative can be retained by derivative-mode transport (or by decoding the derivative pattern itself as the constant-one ECA rule), even though Rule 51's Groovy commutator is the constant-one field rather than zero.

Thus the full structural result is

\[
\boxed{\text{fanout-role closure}=\{G=0\}\cup\{51\}}
\]

for this frozen eight-bit architecture.

This candidate is therefore not the Class-IV dimensional razor. Canonical Class-IV exemplars such as Rules 54 and 110 are absent. The result instead provides a baseline: exact parallel transport of state and derivative recovers the same compatibility measured by the Groovy commutator.

## The next object is forced by the failure

For a fixed evolution `F`, let

\[
D(S)=S\oplus F(S)
\]

and

\[
G(S)=D(F(S))\oplus F(D(S)).
\]

Then identically

\[
D(F(S))=F(D(S))\oplus G(S).
\]

So when the derivative cannot be evolved as an ordinary state, the commutator is exactly the correction field needed to transport it.

Apply the same reasoning to `G`:

\[
G(F(S))=F(G(S))\oplus H(S),
\]

where

\[
H(S)=G(F(S))\oplus F(G(S)).
\]

This generates a canonical correction hierarchy. Zero-commutator rules terminate immediately; more general rules may terminate later, recur, or continue producing genuinely new correction roles.

The next class-blind question is therefore whether the **commutator tower** has a finite or low-complexity closure, and whether that closure depth supplies the missing role budget for a recursive dimensional lift.
