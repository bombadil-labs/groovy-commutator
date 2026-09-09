# Width-k reachable-language invariants for one-defect paired cellular automata

This note records the exact finite-language construction used by Research034 and its relation to the Research033 nearest-neighbor invariant.

## Setup

Let

\[
g:A^3\to A
\]

be a radius-1 one-dimensional cellular automaton on a finite alphabet `A`, and let

\[
\widehat g:(A\times A)^3\to A\times A
\]

be the paired rule obtained by evolving two configurations componentwise.

Fix a target observation

\[
T:A\to O
\]

and a target-hidden seed pair

\[
s=(a,b),\qquad T(a)=T(b).
\]

Write

\[
B=A\times A,
\qquad
D=\{(x,x):x\in A\}.
\]

The admissible initial configurations are arbitrary diagonal backgrounds with one occurrence of `s`.

## 1. Width-k languages

For integer `k >= 1`, a width-k language is a set

\[
W\subseteq B^k.
\]

It defines the shift

\[
X_W=\{x\in B^{\mathbb Z}:\text{every consecutive length-k word of }x\text{ lies in }W\}.
\]

Let `W_0^(k)` be the set of all length-k words that appear in an admissible one-seed initial configuration. Equivalently, it consists of all-diagonal words plus words containing the seed exactly once and diagonals elsewhere.

For width 3 in the Research034 alphabet `|A|=8`,

\[
|W_0^{(3)}|=8^3+3\cdot 8^2=704.
\]

The shift `X_W0` is already an overapproximation of the exact one-defect initial set because it can splice locally admissible words into rows containing multiple well-separated defects. This is acceptable for a sufficient safety certificate.

## 2. One closure step

For a radius-1 CA, a length-k output word depends on a length-(k+2) input word.

Call

\[
p_0p_1\ldots p_{k+1}
\]

admitted by `W` when each consecutive length-k subword belongs to `W`.

Its output word is

\[
q_i=\widehat g(p_i,p_{i+1},p_{i+2}),
\qquad i=0,\ldots,k-1.
\]

Define the monotone operator

\[
\Phi_k(W)
=
W\cup\{q_0\ldots q_{k-1}:p_0\ldots p_{k+1}\text{ is admitted by }W\}.
\]

Because `B^k` is finite, iterating from `W_0^(k)` stabilizes at a least fixed point

\[
W_*^{(k)}.
\]

## 3. Reachability overapproximation theorem

### Theorem 1

Every length-k word appearing at any time in any admissible one-seed paired trajectory lies in

\[
W_*^{(k)}.
\]

### Proof

At time zero the claim holds by definition of `W_0^(k)`.

Assume every length-k word in one row lies in the current closure language. Any length-k word in the next row depends on a consecutive length-(k+2) input word. Every one of its consecutive length-k subwords is admitted by the current language, so the closure operator adds the corresponding output word. Induction over time proves the claim. ∎

## 4. Forward-invariance theorem

### Theorem 2

At the fixed point,

\[
\boxed{\widehat g(X_{W_*^{(k)}})\subseteq X_{W_*^{(k)}}.}
\]

### Proof

Take any row in `X_W*`. Every consecutive length-(k+2) word has all of its length-k subwords in `W_*`. Since `W_*` is a fixed point of `Phi_k`, the corresponding output length-k word also lies in `W_*`. Hence every consecutive output k-word is admitted and the image row lies in `X_W*`. ∎

## 5. All-time safety certificate

A paired symbol `(u,v)` is target-visible when

\[
T(u)\ne T(v).
\]

### Corollary

If no paired symbol occurring anywhere in any word of `W_*^(k)` is target-visible, then

\[
\boxed{w_T(a,b)=\infty.}
\]

The exact one-seed trajectories are contained in a target-safe forward-invariant shift, so no causal witness can ever occur.

## 6. Hierarchy in window width

Increasing window width retains weakly more spatial compatibility information.

Let `pi_k` project a length-(k+1) word to its consecutive length-k subwords. The initial width-(k+1) language projects into the width-k initial language, and the CA image operation commutes with taking consecutive subwords. By induction over closure rounds, every width-k subword of a word in

\[
W_*^{(k+1)}
\]

belongs to

\[
W_*^{(k)}.
\]

Therefore every paired symbol admitted at width `k+1` is admitted at width `k`.

Consequently, the safety certificates are monotone:

\[
\boxed{
\text{safe at width }k
\Longrightarrow
\text{safe at every width }k+1,k+2,\ldots
}
\]

and a larger window can add certificates but cannot invalidate an earlier one.

Research033's nearest-neighbor edge language is exactly the width-2 member of this hierarchy. Research034 evaluates width 3.

## 7. Why failure remains inconclusive

For every finite `k`, `X_W*^(k)` can still contain rows assembled by splicing individually admitted k-words in combinations that never arise from the one-seed initial condition.

Thus target visibility somewhere in `W_*^(k)` does not imply a finite witness exists. It only says that this finite-window overapproximation is too coarse to certify permanence.

The sequence

\[
X_{W_*^{(1)}}\supseteq
X_{W_*^{(2)}}\supseteq
X_{W_*^{(3)}}\supseteq\cdots
\]

is therefore a hierarchy of finite-state outer approximations to the true reachable defect language.

Whether that hierarchy stabilizes at finite width for a particular paired CA/seed, or whether a smaller sofic automaton can capture the reachable language more efficiently, remains open.
