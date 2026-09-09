# Causal witness light cones

This note isolates the locality statement used by Research031. It is independent of the ECA census.

## Setup

Let

\[
G:A^{\mathbb Z}\to A^{\mathbb Z}
\]

be a one-dimensional cellular automaton of finite radius `r`, and let

\[
T:A\to B
\]

be a local target observation. Two configurations `x,x'` are a **single-symbol pair** when they agree everywhere except one site `i`, where

\[
x_i=a,\qquad x'_i=b.
\]

A **target witness at time `t`** is a site `j` for which

\[
T(G^t x)_j\ne T(G^t x')_j.
\]

The least such time over all surrounding contexts is the causal witness horizon of the local distinction `a<->b`, relative to `(G,T)`.

## Theorem 1: every finite-time witness has a finite light-cone representative

For a radius-`r` cellular automaton, the state of site `j` after `t` steps depends only on the initial interval

\[
[j-rt,j+rt].
\]

Therefore if a single-symbol pair is distinguished at `(j,t)`, its differing site `i` must lie in that interval. Restrict both initial configurations to the dependency word

\[
w=x_{j-rt}\ldots x_{j+rt},
\]

of length

\[
\boxed{2rt+1}.
\]

The corresponding restricted word `w'` is identical except at the position of `i`, and evaluating the local rule for `t` steps gives the same two output symbols at the center as the original infinite configurations.

Hence:

> **If a local distinction has any target witness at time `t`, it has one represented by a finite dependency word of length `2rt+1`, with the changed symbol occupying one of those positions.**

Conversely, any such finite dependency-word witness can be extended arbitrarily outside the word to an infinite configuration pair, because those exterior symbols lie outside the causal past of the tested output site.

Thus exhaustive finite-word search is exact for any fixed witness horizon.

## Corollary: existential witness search is local, not periodic

To decide whether symbols `a,b` can be distinguished by time `t`, it is enough to enumerate:

1. every word in `A^(2rt+1)`;
2. every position in that word at which `a` can be replaced by `b`;
3. the target value of the center after `t` local updates.

No periodic boundary condition is required.

This is an existential statement. A short causal witness horizon says that **some** admissible surrounding context exposes the distinction quickly. It says nothing about how common that context is or how long the distinction can remain hidden in other contexts.

## The matched block-3 ECA macro rule

Research031 uses elementary cellular automata, fine radius `r=1`, nonoverlapping blocks of size `b=3`, and cadence `q=3`.

Consider one aligned three-cell output block after three fine ECA ticks. Each output cell has fine causal radius 3. Taking the union of the three output cells' causal pasts gives nine consecutive initial fine cells:

\[
3+2qr=3+6=9.
\]

Those nine cells are exactly three aligned three-cell input blocks. Therefore every ECA rule induces an exact radius-1 cellular automaton on the block alphabet

\[
A=\{0,1,\ldots,7\}:
\]

\[
\boxed{g:A^3\to A.}
\]

One macrostep under `g` is exactly three fine ECA steps followed by aligned block reading. Research031 verifies this identity exhaustively on the 12-cell ring before using the macro rule.

For this matched macro system the light-cone theorem specializes to a dependency word of length

\[
\boxed{2t+1}
\]

at macro-horizon `t`.

## Periodic rings see only a constrained subset of contexts

Let a periodic macro-ring have `m` block sites. A dependency word of length `2t+1` can be realized on the ring only if repeated positions forced equal modulo `m` are compatible with that word.

If

\[
m\ge 2t+1,
\]

every finite dependency word embeds without identifying positions, so periodic and local existential witness searches agree through horizon `t`.

When

\[
m<2t+1,
\]
periodic identification removes admissible finite contexts. The ring therefore searches a subset of the true local witness space.

Consequently:

- a distinction witnessed on the ring is also locally witnessable;
- a distinction absent on the ring may still have a wrap-free local witness;
- the periodic future-context quotient can be **coarser** than the local light-cone quotient because the ring lacks contexts that would separate symbols.

For the four-macroblock ring used in the original block-3 census:

- horizon 1 has dependency width 3, so every local context embeds;
- horizon 2 has dependency width 5, so periodic context loss can begin;
- horizon 3 has dependency width 7, so additional local contexts can be missing.

That is exactly where Research031 finds the first discrepancies.

## What this theorem does not bound

The theorem makes every fixed-horizon search finite, but it does **not** give a system-independent upper bound on the witness horizon. The number of contexts grows exponentially with `t`, and two local symbols can in principle remain interchangeable through many finite horizons before some deeper context separates them.

Research031 searches the complete ECA/block-3 target family only through macro-horizon 3. Finding exact horizon-3 witnesses falsifies the proposed two-step bound, but does not establish that 3 is maximal.

A deeper exact search should replace brute-force word enumeration with a finite-state/de-Bruijn distinguishability construction.