# Reusable descriptions: proof and visual comparison

Authored by Codex, 2026-09-23. Reviewed by: none. Myk requested the proposed
interactive CA/arithmetic comparison. Inspected main:
`a8dee2d0510f22e7f992a65346e3167cd64ac2dd`; inspected draft PR #296:
`405c298243ad69f5230e06ac887f83342cd6e0e9`. PRs #295/#296 remain separate.

## Decision and scope

Can the same representation support the operations we want to perform on it?
The useful output is an exact, visible distinction between lost state
information and an unspecified rule outside an invariant image. This is a
proof/explainer unit, using familiar quotient mathematics and explicit worked
examples; it is not an empirical novelty claim, new census, or prime-distribution
hypothesis. A general congruence criterion and the existing shared closure
account are the baseline. Do not call any repair minimal without a lower bound.

## Fixed examples

1. Integers with observation `c_K(n) = min(v_2(n), K)`, defining `c_K(0)=K`,
   and evolution `n -> n+1`. Primary display K=3. Prove that reduction modulo
   `2^K` is the unique coarsest deterministic present-state refinement that
   retains this readout and supports increment for every integer and all future
   steps. Explain its compatibility with addition and multiplication. Numerical
   controls are only K=1,2,3,4 on their complete residue sets. Refinement by
   forward words is a proof construction, not online suffix memory.
2. Source Rule 32 on the full binary line, cadence one, `Q=G_32`. Prove the
   image excludes neighborhood 101 and that Rules 128 and 160 both give its
   exact evolution. They differ only at 101. Use the seven-cell periodic
   source `0101010` to show that `Y XOR F(Y)` can consult that missing entry,
   making native `G_F(Y)` depend on the chosen completion. This is distinct
   from failure of Y to predict its next state. The worked example also holds
   with zero tails, but display the periodic boundary explicitly.
3. As a separate operation contract, test whether source XOR descends through
   Q using the fixed sources `0000000`, `1111111`, and `0101010`. If their
   displayed Q fibers conflict under source XOR, record the exact witness.
   Distinguishing that pair is necessary; no globally sufficient one-bit
   repair is inferred. Native output XOR and transported source XOR differ.

## Implementation and verification

Commit this scope before executable verification. Commit the small Python
verifier and JavaScript model before recording their computed outputs. Use
separate scalar Python and JavaScript implementations of ECA/G arithmetic.
The full-line local identities use their complete length-seven source cones
(128 words); the seven-cell example is a replay, not a ring-size search.
The bounded controls and UI snapshots must agree. Pin the protocol and both
mathematical implementations in a small evidence JSON. Preserve failed checks
and corrections if any are found; do not overwrite published canonical bytes.

Build a keyboard/touch-accessible comparison with direct bit rows and residue
groups. Inspect mobile and desktop layouts and verify the actual controls.
No network data is needed in the interactive view. Publish source, proofs,
verification, findings, and handoff in one gathering PR based on main.

## Bounds and stopping rule

Budget: each mathematical verifier below 30 seconds; no solver, larger radius,
fourth G, additional CA, fitted score, broad prime panel, or costly Actions job.
The unit ends with the exact examples, their limitations, and a working visual.
If a proposed identity fails, preserve the counterexample and narrow the
explanation. No claim of new information, efficiency, unique ambient dynamics,
or a result about the distribution of primes follows.
