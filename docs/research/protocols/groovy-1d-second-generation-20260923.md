# One-dimensional second-generation Groovy closure

Frozen before implementation/evaluation, 2026-09-23. Authored by Codex
(OpenAI); Reviewed by: none. Base main: `a8dee2d0510f22e7f992a65346e3167cd64ac2dd`.

Myk asks: among rules whose G field follows its own 1D rule, where does
that rule's G field also follow its own rule? No spatial encoding or lift
is involved. This unit first resolves the present-only binary case. The
Rule-30 three-observation case is outside this unit, not a negative result.

## Decision and prior information

The preserved 2026-09-22 census reports 36 present-only laws. Thirty-three
have radius zero; only sources 2 and 16 (radius two) and 32 (radius one)
need a spatial derived update. A pointwise binary update is affine, and
its native G is constant. Therefore the informative work is concentrated
in three descendants, not a new all-rule or memory census. Record and
recheck the 36 first-stage local laws, then stop after this second generation.

Positive closure, an exact counterexample or an explicit resource limit
will decide whether a nonconstant recursive example exists under this
contract. Constant collapse is a positive but uninformative closure.
No prediction of a nonconstant positive is registered.

## Objects and domains

All configurations are on the full binary integer line. Updates are
synchronous, cadence one, with no burn-in. For a total 1D update F,
`G_F(Y) = F(Y) XOR F^2(Y) XOR F(Y XOR F(Y))`.

For each of the 36 source ECA rules r, reconstruct its smallest-radius
forced local factor table F from the old census radius, checking all
source words covering its complete causal support. Verify smaller radii
fail when the radius is nonzero. Record every forced and unforced entry.
The primary total F sets unforced entries to zero. For the three nonpointwise
cases, also test the explicitly fixed alternative setting all unforced
entries to one. Do not select a completion after observing its outcome.

Distinguish two questions for each declared F:

1. Full descendant domain: does `G_F(F(Y)) = H(G_F(Y))` hold for all binary Y?
2. Inherited domain: with `O(S) = G_F(G_r(S))`, does
   `O(E_r(S)) = H(O(S))` hold for every original source S?

A full-domain positive implies an inherited positive, but a full-domain
negative alone says nothing about the inherited case. Compare the two
completions' O truth tables to identify any completion dependence. This is
native G under the derived F, not repeated application of the original
G_r observation with its old source update.

## Bounded algorithm and certificates

Use explicit finite truth tables for composition; remove unused symmetric
outer coordinates only after exhaustive agreement. For each nontrivial
closure question, first screen periods n=1..12 in increasing order and
stop at the first whole-field collision. Preserve both sources, identical
complete observed words and different successor words. Periodic extension
makes such a witness an infinite-line negative at every spatial radius.

If there is no periodic witness, test output radii R=0..4 in order by
exhausting the complete source cone. Stop at the first consistent local
table. Cap source cone length at 21 bits. Preserve forced keys/outputs or
their exact compact truth table and digest, support size, and domain.
Finite periodic absence is not a proof; an unsuccessful capped search is
unresolved, not a no-law result. Check constant observations algebraically.

Verify retained witnesses and positive tables with a separate unpacked
Boolean/scalar implementation. No experiment changes after results appear.
Each invocation is capped at 120 seconds and 2 GiB; no invocation over ten
minutes is permitted. No search for more memory, greater radius, other
source rules, or a third generation follows automatically.

## Publication

Preserve protocol -> implementation -> result commits and old canonical
bytes. Publish on `gather/groovy-1d-second-generation` with a draft PR.
Record code/input hashes, exact outcomes and verification in a new result,
plus a plain-language note and handoff. Update the running findings and
current scheduling pointers. Tests/CI are self-verification, not independent
review. PR #295 is separate concurrent work and is not modified or merged.
