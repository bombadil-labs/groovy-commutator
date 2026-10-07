# The realized commutator jet is sofic, but its grammar does not stabilize through A5

**Evidence:** exact labeled de Bruijn construction, exact DFA
determinization/minimization and exact finite block counts; spatial entropy is
derived numerically from the exact minimized integer presentation.

**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-07. **Reviewed by:** none.

The intrinsic jet unit showed that

\[
G,\;Q,\;R,\;A_4,\ldots
\]

is a natural same-lattice hierarchy of transport residuals, but finite-ring
prefixes rapidly become nearly source-injective.

That leaves a different possibility: perhaps the **set of allowed jet
configurations** has a compact symbolic grammar even when individual jet fields
collectively retain almost all source information.

This unit computes that grammar exactly for fixed jet prefixes.

Protocol:
[commutator jet language](protocols/commutator-jet-language-20261007.md).  
Runner:
[experiment_commutator_jet_language.py](../../scripts/experiment_commutator_jet_language.py).  
Result:
[commutator_jet_language_20261007.json](../../results/commutator_jet_language_20261007.json).

## Construction

For a prefix ending at \(A_m\), the largest source radius is

\[
r=m+1.
\]

Use the binary source de Bruijn graph on \(2r\)-bit source contexts. Each source
edge is labelled by the current sitewise jet symbol

\[
J_m=(G,Q,\ldots,A_m).
\]

Because \(J_m\) is a sliding-block code of the binary full shift, this labelled
graph presents its exact sofic image.

We then:

1. determinize from the set of all source contexts;
2. add an implicit rejecting sink;
3. minimize the deterministic finite-word language automaton;
4. count allowed blocks exactly through length 16;
5. derive the Perron eigenvalue and spatial entropy numerically from the exact
   integer transition graph.

The minimized DFA is a minimal recognizer for the finite block language. It is
not automatically claimed to be the Fischer cover or another stronger
canonical bi-infinite presentation.

## Rule 110 fills source entropy by R

| Prefix | realized site symbols | minimal DFA states | largest recurrent SCC | spatial entropy |
| --- | ---: | ---: | ---: | ---: |
| \(G\) | 2 | 26 | 22 | 0.835023 |
| \(G,Q\) | 4 | 74 | 29 | 0.986745 |
| \(G,Q,R\) | 8 | 131 | 60 | **1.000000** |
| \(G,Q,R,A_4\) | 16 | 280 | 152 | **1.000000** |
| \(G,Q,R,A_4,A_5\) | 32 | 621 | 383 | **1.000000** |

The Perron value for the \(G,Q,R\) presentation is numerically

\[
2.0000000000000036,
\]

so its topological entropy is one source bit per site to numerical precision.

Thus the first three residual fields already support as much asymptotic
spatial word growth as the original binary full shift.

This does **not** mean the factor is one-to-one. It means no asymptotic entropy
rate is lost.

The exact number of allowed \(G,Q,R\) words grows:

\[
8,\;51,\;160,\;358,\ldots,\;1{,}552{,}530
\]

for lengths 1 through 16.

## Rule 62 approaches full entropy more slowly

| Prefix | realized site symbols | minimal DFA states | largest recurrent SCC | spatial entropy |
| --- | ---: | ---: | ---: | ---: |
| \(G\) | 2 | 5 | 5 | 0.650900 |
| \(G,Q\) | 4 | 42 | 35 | 0.977704 |
| \(G,Q,R\) | 7 | 93 | 62 | 0.994186 |
| \(G,Q,R,A_4\) | 14 | 271 | 148 | 0.998755 |
| \(G,Q,R,A_4,A_5\) | 27 | 698 | 317 | **1.000000** |

The A5-prefix Perron value is numerically

\[
2.000000000000002.
\]

So Rule 62 also reaches the full one-bit source entropy within the tested jet,
but only after two additional residual levels.

This mirrors the previous finite-ring diagnostic:

- Rule 110's G-anchored finite prefixes closed by \(G,Q,R\);
- Rule 62 required fields through \(A_5\) at the larger tested rings.

The two measurements are different -- one is a spatial full-line factor
language, the other finite-ring future separation -- but they point to the
same ordering of how quickly the jet recovers hidden source distinctions.

## The symbolic presentation does not settle to a fixed small grammar

Minimal DFA accepting-state counts are

\[
26,\;74,\;131,\;280,\;621
\]

for Rule 110 and

\[
5,\;42,\;93,\;271,\;698
\]

for Rule 62.

There is no stabilization through \(A_5\).

So the raw jet does not reveal a fixed tiny hidden-state machine merely by
adding successive residual fields.

The finite presentations are still substantially smaller than their raw source
de Bruijn presentations at the deeper levels. For example:

- Rule-110 \(G,Q,R\): 131 minimal DFA states versus 256 source de Bruijn
  contexts;
- Rule-62 through \(A_5\): 698 versus 4,096 source contexts.

That is **presentation compression**, not information-rate compression.

## A sharp source-context asymmetry

The subset construction also tracks which source de Bruijn contexts remain
compatible with a finite observed jet word.

For Rule 110, every tested prefix has some finite jet words that synchronize
the compatible source context to a singleton. Median compatible-context count
falls from 5 for \(G\) to 3 by \(G,Q,R\).

For Rule 62, no tested prefix through \(A_5\) has a singleton compatible source
context. The minimum remains exactly two.

At the deepest tested prefix:

| Rule | source contexts in raw de Bruijn graph | minimum compatible | median compatible |
| ---: | ---: | ---: | ---: |
| 110 | 4,096 | **1** | 3 |
| 62 | 4,096 | **2** | 16 |

This is a statement about finite-word source-context synchronization, not a
global two-to-one theorem for bi-infinite configurations.

A post-hoc scratch check suggests the Rule-62 minimum pairs differ in the
newest boundary source bit when words are read left-to-right, while the reverse
reading direction can synchronize. That directional observation is not part of
the canonical result and needs its own exact unit before interpretation.

## Another local contrast

Rule 110 realizes the complete point alphabet at every tested prefix:

\[
2,\;4,\;8,\;16,\;32.
\]

Rule 62 already has forbidden **single-site jet symbols** at \(G,Q,R\):

\[
2,\;4,\;7,\;14,\;27
\]

rather than \(2,4,8,16,32\).

So Rule 62's jet remains locally constrained longer, even as its spatial
entropy approaches one bit/site.

## What this says about the latent-state idea

The result does not produce the hoped-for fixed small machine.

Instead it gives a different picture:

> **successive jet levels transfer hidden source entropy into the observable
> residual language.**

For Rule 110, \(G,Q,R\) already carries full source entropy rate.
For Rule 62, the transfer is more gradual and reaches full rate only through
\(A_5\) in this bounded tower.

This is compatible with the interpretation

\[
A_{k+1}
=
\text{the source information still needed to transport }A_k,
\]

but it sharpens the cost: enough residual levels eventually recover the full
spatial information rate.

The remaining compression question therefore cannot be solved just by stacking
raw residual bit fields.

## Next structural target

The finite-language automata contain more structure than the scalar entropy.

A particularly interesting unresolved distinction is **directional
synchronization**: whether a finite jet word determines its hidden source
context when scanned from the left or from the right.

The scratch asymmetry between Rules 110 and 62 suggests that the remaining
latent state may behave like an oriented phase carried along a spatial
boundary rather than an independent pointwise field.

A clean next unit would construct the left- and right-resolving source-pair
covers of the jet language and ask whether their residual ambiguity is a small
finite-state phase variable.

That would directly test the desired "latent complement as hidden state"
picture without adding another source-derived field.
