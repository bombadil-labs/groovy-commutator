# Exact symbolic causal-witness automata and congruence certificates

This note records the two general mathematical controls used by Research032.

The reduced multi-valued decision diagram is standard symbolic machinery. The statements here establish that the particular witness queries used in the research are semantically exact.

## 1. Local light-cone function

Let

\[
g:A^3\to A
\]

be a radius-1 one-dimensional cellular-automaton rule on a finite alphabet `A`.

For every `h>=0`, define

\[
F_h:A^{2h+1}\to A
\]

to be the center symbol after `h` applications of `g` to a finite dependency word.

The standard causal-cone argument makes `F_h` exactly equal to the corresponding infinite-configuration output at that site and time.

## 2. Ordered multi-valued decision diagrams

Fix variables

\[
x_0,\ldots,x_{2h}
\]

and a fixed order on them.

A nonterminal node is a pair

\[
(v;c_0,\ldots,c_{|A|-1})
\]

that evaluates variable `x_v` and follows the child indexed by its value.

Leaves are symbols in `A`.

Research032 applies two semantic-preserving reductions:

1. if all children are equal, replace the node by that child;
2. share any nodes with identical `(v, children)` tuples.

Neither reduction changes the represented function.

Therefore a reduced ordered MDD is simply a shared canonical representation of a deterministic finite function under the chosen variable order.

## 3. Exact symbolic composition

Represent each input variable `x_i` by its one-node MDD.

Suppose symbolic roots `u,v,w` represent functions of the ordered variables. Define `Apply_g(u,v,w)` recursively.

- If all three roots are leaves, return the leaf `g(u,v,w)`.
- Otherwise let `k` be the earliest variable tested by any root.
- Branch all roots consistently on each value of `x_k`, recursively apply `g`, and reduce/hash-cons the result.

### Lemma

`Apply_g(u,v,w)` represents the pointwise function

\[
x\mapsto g(u(x),v(x),w(x)).
\]

### Proof

Induct on the number of remaining variables.

The leaf case is immediate.

Otherwise every complete assignment has exactly one value `a` for the earliest tested variable `x_k`. The recursive child chosen for that value represents the three restricted functions under the same assignment `x_k=a`. By the induction hypothesis the child computes their pointwise `g`-composition. The constructed parent therefore computes the desired function for every assignment. Reduction preserves semantics. ∎

Applying this operation across one symbolic row shrinks its number of roots by two. Repeating `h` times leaves one root.

By induction on macro-time, that root represents exactly `F_h`.

## 4. Restriction is exact

Let `R` represent a function `F` and fix variable `x_k=a`.

Recursively replacing every node testing `x_k` by its `a` child and reducing all affected ancestors gives a root representing

\[
F|_{x_k=a}.
\]

This follows directly by induction over the ordered DAG.

## 5. Synchronous paired traversal preserves same-context semantics

Fix two restricted roots

\[
R_a=F_h|_{x_k=a},
\qquad
R_b=F_h|_{x_k=b}.
\]

Traverse the pair `(R_a,R_b)` synchronously:

- if both roots are leaves, record their leaf pair;
- otherwise choose the earliest variable tested by either root;
- assign the **same value** of that variable on both sides;
- recurse over all values.

### Theorem

The reachable leaf pairs are exactly

\[
\{
(F_h(c[k:=a]),F_h(c[k:=b]))
:
c\in A^{2h+1}
\}.
\]

### Proof

Every synchronous root-to-leaf path assigns one common value to every non-fixed variable and therefore defines one shared surrounding context. Its two leaves are the two function values in that context.

Conversely, every shared surrounding assignment chooses exactly one branch at every synchronous traversal step, yielding its corresponding leaf pair.

Thus there is a bijection at the semantic level between shared assignments and paired evaluation paths, modulo DAG sharing of equivalent subcomputations. ∎

For a target map

\[
T:A\to B,
\]

there exists a causal witness at axis `k` and horizon `h` iff a reachable leaf pair `(u,v)` satisfies

\[
T(u)\ne T(v).
\]

OR over every possible changed axis to recover the exact horizon-`h` existential witness relation.

## 6. Why the symbolic representation can be exponentially smaller

The explicit table of `F_h` contains `|A|^(2h+1)` inputs.

The MDD merges input prefixes/suffixes that induce the same remaining function. Its size therefore depends on the number of distinct symbolic residual functions, not the number of complete context words.

There is no promise that the reduction is polynomial. Some local functions can still produce exponentially large ordered decision diagrams. Research032's frozen node ceiling treats such growth as censoring rather than evidence about the witness relation.

## 7. Target-respecting congruence certificate

Now fix target

\[
T:A\to B
\]

and its kernel

\[
K_T=\{(a,b):T(a)=T(b)\}.
\]

For a relation `R` on `A`, define `Phi(R)` to contain `(a,b) in K_T` iff for every `x,y in A`,

\[
g(a,x,y)\;R\;g(b,x,y),
\]

\[
g(x,a,y)\;R\;g(x,b,y),
\]

and

\[
g(x,y,a)\;R\;g(x,y,b).
\]

Starting with

\[
R_0=K_T,
\]

iterate

\[
R_{n+1}=\Phi(R_n).
\]

## 8. The refinement remains an equivalence relation

Assume `R` is an equivalence relation.

Reflexivity of `Phi(R)` follows from reflexivity of `K_T` and equality of each paired rule output.

Symmetry follows because each compatibility test is symmetric in `a,b`.

For transitivity, suppose

\[
a\,\Phi(R)\,b
\quad\text{and}\quad
b\,\Phi(R)\,c.
\]

The target kernel is transitive, so `(a,c) in K_T`.

For every fixed context and argument position, the corresponding outputs for `a` and `b` are `R`-related, as are the outputs for `b` and `c`. Transitivity of `R` therefore relates the outputs for `a` and `c`.

Thus

\[
a\,\Phi(R)\,c.
\]

Hence every `R_n` is an equivalence relation.

Because `A` is finite and the sequence only deletes pairs, it stabilizes after finitely many rounds at some `R_*`.

At the fixed point, one-coordinate substitutivity holds in all positions. By sequentially replacing coordinates, `R_*` is a congruence of the ternary algebra `(A,g)`.

## 9. All-time invisibility theorem

Suppose

\[
a\,R_*\,b.
\]

Take any two infinite configurations identical except that one contains `a` and the other `b` at one site.

At time zero, corresponding sites are `R_*`-equivalent: diagonal positions by reflexivity and the changed position by assumption.

If two configurations are componentwise `R_*`-equivalent at one time, every corresponding radius-1 input triple is componentwise related. Congruence compatibility therefore makes the next output symbols `R_*`-equivalent.

By induction, the two complete configurations remain componentwise `R_*`-equivalent forever.

Since

\[
R_*\subseteq K_T,
\]

their target values agree at every site and every time.

Therefore

\[
\boxed{
a\,R_*\,b
\Longrightarrow
w_T(a,b)=\infty.
}
\]

## 10. Why the certificate is not complete in general

The congruence theorem quantifies over **every** local context whose corresponding symbols lie in `R_*`.

But the pair dynamics generated by one non-diagonal seed may realize only a strict subset of those contexts.

A pair can therefore be permanently target-invisible for dynamical reachability reasons even when arbitrary algebraic substitution would break the relation.

So failure of the congruence certificate does not imply a finite witness.

The unresolved non-congruence cases motivate a richer invariant over **languages of reachable pair configurations**, rather than a relation on single symbols alone.
