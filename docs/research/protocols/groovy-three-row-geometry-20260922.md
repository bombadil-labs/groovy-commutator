# Three raw Groovy rows as binary spatial geometry

Status: frozen before implementation and evaluation, 2026-09-22.
Authored by: Codex (OpenAI), this Myk-directed session. Reviewed by: none.
Inspected main: `a8dee2d0510f22e7f992a65346e3167cd64ac2dd` (PR #294).

## Decision

Myk asked whether the three temporal layers of Rule 30's autonomous Groovy
history can instead be spatial rows governed by one uniform binary 2D rule.
The uncertainty is whether forgetting the row labels loses information needed
for advancement. This tests the raw representation itself; the known marked
history rule and the six-field lift do not settle that question. A law would
justify studying this smaller geometric encoding. A collision would identify
the missing distinction and end this encoding's existence test. No derivative
tower, all-rule census or dimensional-performance claim is part of this unit.

## Exact contract

- Source: elementary Rule 30, all binary configurations on the integer line,
  synchronous evolution E, no burn-in or restricted attractor assumption.
- Observable: D(S)=S XOR E(S), G(S)=E(S) XOR E^2(S) XOR E(D(S));
  write G_j(S)=G(E^j(S)). Original-source G, never descendant-native G.
- Encoding: L(S)(x,y)=G_{y mod 3}(S)(x), with residues 0,1,2. The three
  rows are repeated vertically to obtain a binary configuration on Z^2.
  This period-three closure is an explicit representation choice, not a
  conclusion about a finite strip with boundary markers or a full history.
- Include all three vertical translates: R_p L(S)(x,y)=L(S)(x,y+p).
- Target: one translation-equivariant binary 2D CA Phi, with no external
  row/phase label or retained source, satisfying
  Phi(R_p L(S))=R_p L(E(S)) for every S and p in {0,1,2}.
  One new CA update equals one original-source update. The new displayed
  rows must therefore be G_1,G_2,G_3, with the same spatial phase.
- First local stencil: horizontal offsets -6..6 and vertical offsets -1..1.
  This is 39 bits, matching the certified marked Rule-30 history radius.
  No isotropy or radius-one requirement. Larger finite vertical radii provide
  repeated rows on the encoded domain, rather than new information.
- Required correctness is on the phase-saturated encoded family. Any positive
  local table must declare its off-image completion; no ambient claim follows.

## Bounded evaluation and stopping rule

1. Search horizontal periods n=1..12, source words in binary integer order,
   phase p=0,1,2. Compare entire phase-shifted three-row inputs and required
   successor arrays. Stop at the first equal input with unequal target. Save
   both sources, phases, all G_0..G_3 rows, and a differing coordinate. Their
   spatial periodic extensions give an exact infinite-plane obstruction to
   any deterministic map on the phase-saturated encoding, regardless of
   neighborhood radius. Absence through n=12 is only bounded search evidence.
2. Only if step 1 finds no obstruction, exhaust all 2^21 source words for the
   13-by-3 local test. The input rows G_0,G_1,G_2 have source radii 2,3,4;
   their width-13 window fits in 21 source cells. Output G_3 at the center has
   radius 5 and also fits. Include all three phase roles and retain a conflict
   pair if a neighborhood requests both output bits. A local conflict only
   excludes this stencil unless a separate whole-plane certificate exists.
   A consistent table proves a local law for every valid source, by complete
   cone coverage; store its ordered table digest and a replayable definition.
3. Stop after the first decisive negative or the completed positive test.
   Total evaluation cap: 120 seconds and 2 GiB. A cap/error is an explicit
   unresolved outcome. Do not expand radius, periods, rules or memory here.

For a negative, independently replay the retained certificate with a scalar
Rule-30 formula and explicit periodic indexing; test full row equality and
the required output disagreement. For a positive, use an unpacked independent
cone implementation before making a certified claim. Integrity hashes pin the
protocol and implementation; they do not replace mathematical verification.
Retain skipped stages as not evaluated with reasons.

## Predictions and interpretation

No directional prediction: an exact marked memory-three law is known, but
phase compatibility of the raw three-row representation is untested here.
A negative does not rule out labelled rows, a different binary encoding,
an enlarged alphabet, boundary markers, another cadence, a restricted source
family, or another 2D evolution target. It would show that this specific
forgetting of temporal roles is not a dynamically valid gauge equivalence.

## Publication

Use gathering branch `gather/groovy-three-row-geometry` and a draft PR. Preserve
this protocol commit before the implementation commit and evaluation record.
Publish a concise note, canonical certificate, executable verifier and handoff;
update FINDINGS when the unit ends. Do not alter prior canonical results.
