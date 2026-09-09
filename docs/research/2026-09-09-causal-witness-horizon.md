# The ring hid the third-step witness

Research030 found a striking finite-ring fact: across every nonclosed block-3 ECA target on the periodic 12-cell ring, the final local future-context quotient appeared by macro-horizon 2, even while global predictive memory reached `h*=23`.

Research031 asks whether that two-step bound belongs to the local dynamics or to the topology of the experiment.

The answer is exact:

> **The two-step bound was a finite-ring artifact.**

When periodic wrap is removed and local distinctions are tested in their exact causal light cones, four symmetry-related cases contain a distinction whose **first possible target witness occurs at macro-horizon 3**. The four-block ring cannot realize the surrounding context that exposes it.

The earlier Research030 result remains correct for its declared periodic system. Research031 changes its interpretation: a small torus can underestimate the local vocabulary of future-relevant distinctions by deleting admissible causal contexts.

## From fine ECA to an exact block light cone

For an elementary cellular automaton, fine radius is 1. Research028–030 use block size 3 and cadence 3.

After three fine ticks, one aligned three-cell output block depends on nine fine input cells. Those are exactly three aligned input blocks. Therefore every ECA induces an exact radius-1 macro-CA

\[
g:A^3\to A,
\qquad A=\{0,\ldots,7\}.
\]

One macrostep is exactly three fine ECA steps under the aligned block encoding.

That gives a clean local witness geometry. At macro-time `t`, one output block depends only on a word of

\[
2t+1
\]

initial macro-symbols. To ask whether two local symbols `a,b` can ever matter by time `t`, it is therefore enough to enumerate every such dependency word and every position at which `a` can be replaced by `b`.

The proof is in `docs/research/proofs/causal-witness-light-cone.md`.

## Causal witness horizon

Fix the induced macro dynamics `g` and a binary block target `T`.

For two local block symbols `a,b`, define their **causal witness horizon** as the least macro-time `t` for which there exists some finite surrounding context, identical except for `a` versus `b`, whose target future differs by time `t`.

This is deliberately existential.

It does **not** ask how long a distinction can survive invisibly in a particular context. Research025 already showed that the same hidden defect can have different fates in different surroundings.

Instead it asks:

> **How deep must the light cone be before the future has any context capable of reading this distinction?**

That is a different timescale again from both hidden-mode lifetime and global predictive memory.

## Frozen exact census

The protocol was frozen before evaluation over:

- all 256 ECA rules;
- all 127 canonical nonconstant binary block-3 targets;
- the exact induced eight-symbol radius-1 macro rule;
- wrap-free local causal contexts through horizons 0, 1, 2, and 3;
- the corresponding four-macroblock periodic-ring quotient as a topology control.

That is **32,512 rule/target cases**.

The primary sharded run was Actions run `34330667980`. Its exact aggregate is committed at

`results/causal_witness_horizon_20260909_summary.json`.

## Finding 1: the ring first loses contexts at horizon 2

At horizons 0 and 1, the wrap-free local quotient and the four-block periodic quotient agree in every case:

\[
\boxed{0\text{ mismatches at }h=0,1.}
\]

That is the expected light-cone control. A horizon-1 dependency word has length 3, which embeds freely in a four-block ring.

At horizon 2 the dependency width is 5, larger than the four-block ring. Periodic identification now constrains the surrounding context.

Exactly

\[
\boxed{54}
\]

rule/target cases have different local and ring quotients at horizon 2.

So even before the headline horizon-3 counterexample, the torus is already hiding real local distinctions.

## Finding 2: exactly four distinctions are born at horizon 3

Across the full wrap-free search, local quotients continue refining from horizon 1 to 2 in **1,394** rule/target cases.

Only **four** target cases refine again from horizon 2 to 3. Each contains exactly one symbol pair whose first target witness is horizon 3:

| Rule | Target | Pair first separated at `h=3` | Local quotient chain `h=0..3` |
| ---: | --- | --- | --- |
| 35 | `00000001` | `2 <-> 6` | `00000001 -> 01234325 -> 01234526 -> 01234567` |
| 49 | `00000001` | `2 <-> 3` | `00000001 -> 01223445 -> 01223456 -> 01234567` |
| 59 | `01111111` | `1 <-> 5` | `01111111 -> 01232145 -> 01234156 -> 01234567` |
| 115 | `01111111` | `4 <-> 5` | `01111111 -> 01123345 -> 01234456 -> 01234567` |

Thus

\[
\boxed{4}
\]

symbol-pair/target distinctions are first born at horizon 3 in the frozen domain.

All four rules are Class II in the repository taxonomy, but that count is not four independent mechanisms. They are exactly one standard ECA symmetry orbit under reflection and black/white conjugacy:

\[
\boxed{\{35,49,59,115\}}.
\]

So the census found one essential horizon-3 mechanism, appearing in four symmetry-related forms.

## Finding 3: the four-block ring misses the third-step witness completely

For each of the four cases, the local quotient becomes the full eight-symbol identity at horizon 3.

The four-block ring does not make that final split. Its quotient stalls at the horizon-2 value.

For Rule 35, for example:

\[
Q^{local}: 00000001\to01234325\to01234526\to01234567,
\]

while

\[
Q^{m=4}: 00000001\to01234325\to01234526\to01234526.
\]

The missing distinction is `2 <-> 6`.

This is the direct falsification of the tempting Research030 extrapolation:

\[
\boxed{d_Q\le2\text{ is not a topology-independent local bound.}}
\]

## Independent witness reconstruction

After the primary census, the four cases were frozen before a separately written scalar audit.

The audit does not import the primary vectorized light-cone helper. It reconstructs the eight-symbol macro rule directly from the fine ECA and then, for each frozen pair:

1. exhausts every possible context at horizons 0, 1, and 2 and finds no witness;
2. finds an explicit seven-symbol dependency word with a target difference at horizon 3;
3. replays the same witness directly under the original fine ECA for nine fine ticks.

All four pass.

One explicit Rule-35 witness is

`[0,0,0,2,1,5,2]`

versus

`[0,0,0,6,1,5,2]`.

After three macrosteps the center output block is `3` versus `7`. Under target `00000001`, those map to `0` versus `1`.

The independent fine-ECA replay gives the same block outputs after nine fine ticks.

The exact audit is committed at

`results/causal_witness_horizon_20260909_audit.json`.

## Finding 4: five blocks are already enough to restore the witness

A second frozen protocol checked the four cases on periodic rings of 4, 5, 6, and 7 macroblocks—fine widths 12, 15, 18, and 21.

The preregistered endpoints pass:

- 4 blocks: the frozen pair remains merged through horizon 3;
- 7 blocks: the pair separates at horizon 3.

The unpredicted middle sizes are more informative:

\[
\boxed{m=5,6,7\text{ all recover the horizon-3 split in all four cases}.}
\]

So a full seven-block dependency word is sufficient to embed every possible horizon-3 context, but these particular witnesses need less freedom: a five-block periodic ring already admits a compatible one.

The exact size-control artifact is

`results/causal_witness_horizon_sizes_20260909.json`.

## What changed about Research030

Research030 established an exact and useful separation on a fixed topology:

- local representation discovery could finish at horizon 1 or 2;
- global state resolution could require dozens of history steps.

Research031 does not erase that result. It inserts another layer:

\[
\boxed{\text{observed quotient-discovery time depends on which causal contexts the topology admits}.}
\]

On the four-block ring, some contexts literally do not exist. The ring can therefore declare two local symbols interchangeable even though a larger or open system contains a context that eventually reads their difference.

This is the same general theme that has appeared repeatedly in the project:

> **the causal fate of an erased distinction belongs to the distinction plus its admissible context.**

Here the context restriction is not a local background state but the global topology itself.

## Three different timescales

The current research now separates at least three notions that had initially looked like one kind of “memory”:

1. **hidden-mode lifetime** — how long a particular erased difference remains active before it becomes visible or dies;
2. **causal witness horizon** — how deep some admissible context must be before it can prove that a local distinction matters at all;
3. **global state-resolution depth** `h*` — how much observed history is required to determine the complete predictive state.

They can be radically different.

A distinction may have a very short existential witness horizon but remain hidden for a long time in a particular context. And a system may reveal its complete local vocabulary quickly while its global predictive state remains unresolved for much longer.

## What is exact now

Within the declared block-3 ECA family:

- three fine ECA ticks induce an exact radius-1 eight-symbol macro CA;
- every horizon-`t` local witness has an exact finite dependency-word representative of length `2t+1`;
- the complete local search through horizon 3 finds 54 local/ring quotient mismatches at horizon 2 and 58 at horizon 3;
- exactly four rule/target cases contain one symbol-pair distinction first witnessed at horizon 3;
- those four rules form one ECA symmetry orbit;
- an independent scalar implementation verifies no witness through horizon 2 and an explicit horizon-3 witness for all four;
- direct fine-ECA replay verifies the same witnesses after nine fine ticks;
- four-block rings miss all four, while 5-, 6-, and 7-block rings recover all four at horizon 3.

## What remains open

Research031 does **not** establish that horizon 3 is maximal.

The exact brute-force context search grows like

\[
8^{2t+1},
\]

so simply extending the same census becomes the wrong instrument quickly.

It also does not claim that horizon-3 contexts are typical, only that they exist.

And it does not yet characterize why the `{35,49,59,115}` macro-rule orbit alone supports the delayed witness.

## Next question

The next target is now computationally and mathematically clear:

> **Can causal witness search be converted into a finite-state distinguishability problem so that horizons 4, 5, ... can be explored without enumerating every light-cone word?**

A de-Bruijn or paired-state automaton should be able to represent the growth of left/right context and ask whether a target-distinguishing output is reachable. That would let us compute shortest witness horizons—and possibly permanent local equivalence—without exponential context enumeration.

Only after that should we ask for the actual maximum witness horizon of the block-3 ECA family.

The light cone has made the next station visible.