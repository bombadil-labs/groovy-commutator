# Full-entropy commutator jets leave only zero-entropy phase ambiguity

**Evidence:** exact full-line source-pair de Bruijn graphs, exact bi-infinite
support pruning and SCC decomposition; Perron values are computed from the
exact finite graphs.

**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-07. **Reviewed by:** none.

The parent jet-language unit found that successive residual fields recover the
binary source's full spatial entropy at different depths:

- Rule 110 by \((G,Q,R)\);
- Rule 62 by \((G,Q,R,A_4,A_5)\).

Full entropy does not imply injectivity. This unit therefore studies the exact
fiber product of those sliding-block maps:

\[
\mathcal F_\pi=\{(X,Y):\pi(X)=\pi(Y)\}.
\]

The result is sharp:

> **Immediately before full entropy, both rules retain a positive-entropy
> mixed hidden fiber. At the first full-entropy jet prefix, that extensive
> hidden fiber disappears. Every surviving recurrent off-diagonal ambiguity is
> a finite periodic phase/gauge cycle; the remaining nonperiodic ambiguity is
> carried by finitely presented interfaces between those sectors.**

This is an infinite-line symbolic result for the fixed jet factors below, not a
finite-ring inference.

Protocol:
[commutator jet fibers](protocols/commutator-jet-fibers-20261007.md).  
Runner:
[experiment_commutator_jet_fibers.py](../../scripts/experiment_commutator_jet_fibers.py).  
Result:
[commutator_jet_fibers_20261007.json](../../results/commutator_jet_fibers_20261007.json).

## Exact pair graph

For a fixed jet factor \(\pi\), use the binary source de Bruijn graph at the
factor's source radius.

The pair graph has vertices \((u,v)\) of source contexts and retains exactly
those paired source edges whose jet labels agree.

After pruning to states with both infinite left and right continuation, the
remaining graph presents all bi-infinite source pairs with identical entire jet
fields.

The diagonal \(X=Y\) is always present. Off-diagonal recurrent SCCs describe
persistent hidden ambiguity. Transient essential pair states describe
interfaces connecting recurrent sectors.

## Rule 110: R kills the positive-entropy hidden fiber

For the shallower control

\[
(G,Q),
\]

the pair graph has a mixed recurrent SCC with

\[
\rho\approx2.0378403041,
\qquad
h\approx1.027041\text{ bits/site}.
\]

Since the source diagonal already contributes one bit/site, the hidden pair
language carries a positive excess entropy

\[
\boxed{h_{\rm pair}-1\approx0.027041}.
\]

The mixed SCC contains both diagonal and off-diagonal states, so there is an
extensive family of distinct source pairs producing the same \(G,Q\) field.

After adding \(R\),

\[
\boxed{(G,Q,R)},
\]

that mixed component disappears.

The exact pair graph then has:

- one diagonal full-shift component with \(\rho=2\);
- **eight** recurrent non-diagonal SCCs;
- every non-diagonal recurrent SCC is a simple directed cycle with
  \(\rho=1\), hence zero entropy;
- 68 additional non-diagonal bi-infinite-support vertices lie on interfaces
  between recurrent sectors.

Therefore the non-diagonal recurrent ambiguity of the first full-entropy
Rule-110 jet has

\[
\boxed{h_{\rm hidden}=0}.
\]

Representative persistent phase pairs include

\[
0^\mathbb Z\leftrightarrow1^\mathbb Z,
\]

\[
(01)^\mathbb Z\leftrightarrow(10)^\mathbb Z,
\]

and the period-four pair

\[
(0111)^\mathbb Z\leftrightarrow(1101)^\mathbb Z.
\]

The exact pair graph also contains phase-to-diagonal interfaces. One shortest
representative has XOR word

\[
111111111100000000,
\]

the same half-line-complement/domain-wall motif that appeared earlier in the
parity-plus-Groovy obstruction.

So \(R\) does not make the source factor injective. It changes the nature of
what remains hidden: from an extensive source language to phase sectors and
domain walls.

## Rule 62: the same transition occurs only at A5

For the shallower control

\[
(G,Q,R,A_4),
\]

the pair graph still contains a positive-entropy mixed SCC:

\[
\rho\approx2.0034064513,
\]

\[
h_{\rm pair}-1
\approx
\boxed{0.002455145\text{ bits/site}}.
\]

So an extensive hidden ambiguity remains, although its entropy density is
already small.

Adding \(A_5\),

\[
\boxed{(G,Q,R,A_4,A_5)},
\]

removes that mixed recurrent fiber.

The first full-entropy Rule-62 jet has:

- the diagonal full-shift component;
- **15** recurrent non-diagonal components;
- every one is a simple directed cycle with zero entropy;
- 20 additional non-diagonal interface states.

The recurrent phase sectors include periods 1, 2, 3 and 6.

Thus Rule 62 shows the same qualitative transition as Rule 110, but two jet
levels later:

\[
\boxed{
\text{positive-entropy hidden field}
\;\longrightarrow\;
\text{zero-entropy phase/gauge ambiguity}.
}
\]

## Direction matters

The one-sided subset automata expose a further matched-rule difference.

For Rule 110 at \(G,Q,R\):

- a finite jet word can synchronize the source context to one state scanning
  left-to-right;
- a finite jet word can also synchronize to one state scanning right-to-left.

For Rule 62 at \(G,Q,R,A_4,A_5\):

- right-to-left reading can synchronize to one source context;
- left-to-right reading never reaches fewer than **two** compatible source
  contexts in the exact subset automaton.

This is not a proof of a globally two-to-one factor.

It does show an exact **oriented residual phase ambiguity** in the finite-word
presentation: one spatial direction retains a two-context uncertainty that the
opposite direction can resolve.

That asymmetry is a natural target for a finite-state phase coordinate.

## Full entropy still does not give a bounded local inverse

Even after the hidden recurrent entropy collapses to zero, neither primary jet
factor determines the central source bit from a small symmetric current jet
window.

Exact local inverse tests fail for radii

\[
0,1,2,3,4
\]

for both primary factors.

So the source information rate is present in the jet language, but is not
organized as a trivial bounded-radius source decoder.

This is precisely the distinction between:

- carrying the full entropy rate;
- having only zero-entropy global ambiguity;
- and possessing a small local inverse.

They are different statements.

## What this says about the latent complement

The residual complement is not behaving like an endless sequence of
independent one-bit fields.

At the first full-entropy jet depth, the **extensive** hidden field is gone.
What remains is a zero-entropy object:

- periodic phase sectors;
- phase/gauge relabelings;
- interfaces/domain walls between them.

This gives a more precise candidate for the latent complement:

> **the remaining \(Q\)-like state may be a finite-state spatial phase process,
> not another positive-entropy pointwise field.**

The commutator jet appears to consume the extensive latent information level by
level until only a phase/gauge skeleton remains.

That interpretation is exact for the two fixed factors studied here. It is not
a universal theorem about all CA or all jet depths.

## Next target

Do not add another residual field immediately.

Instead, quotient the off-diagonal pair graph itself into a **phase automaton**:

1. recurrent zero-entropy phase sectors become latent states;
2. heteroclinic pair paths become phase-boundary transitions;
3. determine whether that latent phase process has a local/update law coupled
   to the observable jet;
4. test whether it can be represented as a same-lattice binary field with a
   low-entropy realized subshift.

That would finally operationalize the user's original idea of a hidden
same-configuration-space complement without confusing ambient binary capacity
with actual information rate.
