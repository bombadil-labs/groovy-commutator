# One further recursive G for Rules 2 and 16

Frozen before implementation/evaluation, 2026-09-23. Authored by Codex
(OpenAI); Reviewed by: none. Inspected main:
`a8dee2d0510f22e7f992a65346e3167cd64ac2dd`. Existing PR #296 head:
`6628c14577acdba01a363457160add329eedb80c`.

Myk asks whether either of the two nonconstant second-generation positives
extends to another recursive G. This authorizes exactly the next inherited
generation, entirely in 1D. The completed second-generation result and its
implementation remain immutable inputs. Continue on the same gathering PR.

## Decision and candidates

For r in {2,16}, retain both previously fixed first-level completions F
(all missing entries zero or all missing entries one). Read the certified
second update table H from the saved result. Its primary completion fills
missing entries with zero, exactly as in the published explicit rule table.
Also test a fixed sensitivity alternative filling H's missing entries with
one. This gives four primary/sensitivity choices per source, eight cases.
No other completions or source rules are searched.

With O1 = G_r, O2 = G_F composed with O1, and O3 = G_H composed with O2,
the question is whether a present-only local J satisfies

```
J(O3(S)) = O3(E_r(S)) for every binary source S on the integer line.
```

This follows the actual third-generation field from the original source.
The starting family, synchronous cadence one, no burn-in, and no temporal
memory are unchanged. Do not substitute arbitrary starting rows for the
inherited image. No full-descendant-domain census is included.

A nonconstant law means this specified chain extends one more level; a
constant field is recorded separately. A periodic whole-field collision
ends that case with an all-spatial-radii negative. A capped search is
unresolved. No prediction of closure or failure is registered. Also compare
the resulting observable with O2 for exact equality; equality alone does
not establish an indefinitely repeating tower with newly chosen updates.

## Bounded implementation

1. Check hashes of the prior result, its protocol and implementation.
2. Construct the finite truth table of O3, removing unused symmetric outer
   coordinates by exhaustive agreement. Preserve its radius, one-count,
   SHA-256 digest of ascending output bytes, and the defining F/H tables.
   A large observation table may be regenerated instead of duplicated.
3. For a nonconstant O3, screen source periods n=1..12 in order. Stop at the
   first equal whole O3 field with different next field. Save complete sources,
   observations and successors. Periodic extension supplies the line proof.
4. If no collision is found, test J radii 0..4 in order by complete source
   cones. Stream in chunks and cap the cone at 23 bits. Stop at the first
   consistent table and preserve every forced and unforced output entry.
   No collision on small rings alone is never called a positive.
5. Use separate unpacked arithmetic to verify the direct three nested
   commutators over their complete original-source support (at most 21 bits),
   and every positive local identity. Check negatives by direct scalar nested
   G on periodic sources, not just the composed observation lookup table.

Each invocation is limited to 120 seconds and 2 GiB. No automatic radius
increase, memory repair, other source, arbitrary-completion enumeration, or
fourth generation. A timeout is a resource result, not a negative theorem.
If the eight cases end sooner, stop. Algebraic deductions after evaluation
must be identified as such and cannot silently change the tested candidates.

## Publication

Preserve protocol -> implementation -> result commits within PR #296. Save
a new canonical result without altering the second-generation record or
its pinned implementation. Update the plain-language findings, note and
handoff. Existing local checks and a bounded CI replay are verification;
Reviewed by remains none unless an actual separate review occurs. PR #295
is unrelated and remains untouched. No merge is authorized by this question.
