# Future-context quotient: canonical uniform local sufficiency

This proof is independent of the Research029 block-3 census. It concerns an arbitrary finite deterministic target label on a tiled product space.

## Setup

Let `A` be a finite local alphabet, let `m >= 1`, and let

\[
C:A^m\to Q
\]

be any deterministic target label.

A **uniform local encoder** is a map

\[
z:A\to Z
\]

applied independently in every coordinate. It is sufficient for `C` when there exists a map `b` such that

\[
C=b\circ z^m.
\]

Define local future-context equivalence by

\[
a\equiv_C b
\]

iff, for every coordinate `j` and every exact assignment of all other coordinates, substituting `a` for `b` at coordinate `j` leaves `C` unchanged.

Write

\[
q:A\to A/{\equiv_C}
\]

for the quotient map.

## Lemma 1: contextual equivalence is an equivalence relation

Reflexivity and symmetry are immediate. If `a equiv_C b` and `b equiv_C c`, then in every coordinate and exact context,

\[
C(\ldots,a,\ldots)=C(\ldots,b,\ldots)=C(\ldots,c,\ldots),
\]

so `a equiv_C c`. Hence `equiv_C` is transitive.

## Theorem 1: the quotient is sufficient

Suppose

\[
q^m(x)=q^m(y).
\]

Then `x_i equiv_C y_i` for every coordinate `i`. Transform `x` into `y` one coordinate at a time. Each single-coordinate substitution preserves `C` by definition of contextual equivalence. Therefore

\[
C(x)=C(y).
\]

So `C` is constant on every fiber of `q^m`, and there is a well-defined map `bar C` with

\[
\boxed{C=\bar C\circ q^m.}
\]

## Theorem 2: universal characterization of uniform local sufficiency

For any uniform local encoder `z:A -> Z`,

\[
\boxed{C\text{ factors through }z^m\iff \ker z\subseteq\equiv_C.}
\]

### Necessity

Assume `C=b circ z^m`. If `z(a)=z(b)`, place `a` and `b` in any one coordinate with all other coordinates held to an arbitrary exact context. The two global tuples have identical `z^m` encodings, so sufficiency gives identical `C` labels. Since the coordinate and context were arbitrary,

\[
a\equiv_C b.
\]

Thus

\[
\ker z\subseteq\equiv_C.
\]

### Sufficiency

Assume `ker z subseteq equiv_C`. If

\[
z^m(x)=z^m(y),
\]

then `z(x_i)=z(y_i)` for each coordinate, hence `x_i equiv_C y_i` for each coordinate. By the coordinate-substitution argument from Theorem 1,

\[
C(x)=C(y).
\]

Thus `C` is constant on every fiber of `z^m` and factors through it.

## Corollary 1: unique coarsest uniform local sufficient partition

A local encoder is sufficient exactly when its partition refines the contextual quotient partition. Therefore

\[
\boxed{A/{\equiv_C}\text{ is the unique coarsest uniform local sufficient partition}}
\]

up to relabeling of quotient classes.

This is a universal property, not an empirical fact about ECA.

## Corollary 2: unique minimum-information local sufficient encoder under full support

Let the local fine symbol have a full-support distribution. If `z` is a strict refinement of `q`, then

\[
H(z(U))=H(q(U))+H(z(U)\mid q(U))
\]

with strictly positive conditional term, because at least one positive-probability quotient class is split. Hence every strict sufficient refinement has strictly greater local encoder entropy than `q`.

For the uniform ensemble on `A^m`, the coordinates are independent and uniform, so

\[
H(z^m(S))=mH(z(U_A)).
\]

Thus `q` is the unique minimum-entropy uniform local sufficient encoder, up to output relabeling.

The partition theorem itself is measure-free; only the strict entropy corollary uses full support.

## Theorem 3: exact characterization of refinement-only greedy failure

Let `P_0` be an initial local target partition coarser than the contextual quotient `Q*=A/equiv_C`. Consider any path that only refines the current local partition and stops at the first sufficient partition.

Call a current partition **Q-compatible** when `Q*` refines it. Call a refinement step **safe** when the child remains Q-compatible and **unsafe** otherwise.

Then:

\[
\boxed{\text{the path is globally minimum-information}\iff\text{it never takes an unsafe step}.}
\]

### Safe path

If every step remains Q-compatible, the terminal partition `P` is still coarser than or equal to `Q*`. Because `P` is sufficient, Theorem 2 says `P` must also refine `Q*`. Therefore `P=Q*` as partitions, so the path terminates at the unique global information optimum.

### Unsafe path

An unsafe refinement splits at least one class that `Q*` keeps merged. Refinement-only dynamics can never undo that split. Every later partition is therefore a strict refinement of `Q*` whenever it becomes sufficient. Under a full-support ensemble, Corollary 2 makes its information cost strictly greater than the optimum.

So the first unsafe refinement is an irreversible certificate of eventual greedy regret.

## Safety margin and two kinds of fatal synergy

At a Q-compatible nonclosed partition `P`, let

\[
G_s(P)=\max_{P'\,\mathrm{safe}}g(P\to P'),
\qquad
G_u(P)=\max_{P'\,\mathrm{unsafe}}g(P\to P'),
\]

for the frozen closure-gain function, and define

\[
M(P)=G_s(P)-G_u(P).
\]

Then:

- `M(P)>0`: every maximum-gain choice is safe;
- `M(P)<0`: every greedy rule based only on maximum immediate gain must choose unsafe — **strict fatal predictive synergy**;
- `M(P)=0`: safe and unsafe maxima coexist, so correctness depends on the tie-break — **tie-sensitive fatal predictive synergy**.

Generic increasing returns or synergy does not imply greedy failure. Greedy failure requires the chosen maximum-gain edge to leave the canonical quotient-compatible region.

Research029's frozen block-3 census tests whether the four Research028 failures are all tie-sensitive and whether any strict negative-margin example exists in that finite domain.

## Relation to established mathematics

The construction is structurally analogous to context-equivalence / minimal-quotient arguments such as Myhill–Nerode: indistinguishability under all admissible contexts induces a canonical coarsest quotient. It is also a deterministic minimal-sufficiency construction: the quotient is a function of every sufficient uniform local encoder.

No novelty claim is made here for the abstract context-equivalence argument. The Groovy-specific object is the choice of `C` as a complete dynamical future-equivalence label together with the uniform local-encoder constraint and the resulting representation-repair geometry.
