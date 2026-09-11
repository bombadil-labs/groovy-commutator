# Two steps of history are always enough under neighbor-parity coarse-graining

**Research note, 2026-09-11.** Sixth unit of the [Invariants Across Representation Contracts](2026-09-10-representation-invariants-program.md) program. Authored by: Claude Code, Fable 5.1. Protocol review: none at freeze; run authorized by Myk 2026-09-11; Codex (OpenAI) signed off on the frozen revision retrospectively, after the verifier was committed and the run had started, with no change to the frozen text ([protocol](protocols/parity-history-bound-20260911.md), Section 5). **Evaluation preceded other-model review.** Verifier committed before the single run; canonical output [`results/parity_history_bound_20260911.json`](../../results/parity_history_bound_20260911.json), replayed byte-for-byte in CI. All four frozen predictions held; D1 held in its literal, stronger form. Final review of the completed unit: pending on the gathering PR.

## The question

The [fifth unit](2026-09-11-parity-coarse-graining.md) observed, post hoc, that under neighbor parity `π(S)_i = S_i ⊕ S_{i+1}` every rule's refinement depth `h_*` is at most 2 at rings `n ≤ 12`. Is that a bound for every ring size, and which rules need the second step?

## Method

For a rule with complement response `g_r`, a complement pair stays complementary for one step exactly on the states `W_1` where `g_r ≡ 1` around the ring, and for two steps on `L = W_1 ∩ F^{−1}(W_1)`. The frozen lemma says: if every state of `L` has `g_r(F²X)` constant, then `h_* ≤ 2` on every ring, because a pair unsplit through two steps either becomes equal (absorbing) or remains in `L` one step later. Constancy is a local matter: adjacent values of `g_r∘F²` read eight consecutive cells, so it suffices that every `L`-admissible 8-word has equal adjacent values, and wrapped windows on small rings are such words too. Depth 2 on some ring is likewise decided by `W_1`-admissible 6-words that lie on a cycle of `W_1`'s de Bruijn graph, and the shortest closing path gives the smallest realizing ring. Codex confirmed the lemma, the exactness of the 6-word criterion, and the scoring before the run finished.

## Answer

- **D1, certificate.** For every one of the 224 non-closed rules, every `L`-admissible 8-word passes; there is no violating word at all, cycle-embedded or not, so the literal prediction holds and the lemma gives `h_* ≤ 2` for all 256 rules on every ring size. The 32 closed rules pass trivially. Post hoc: 32 non-closed rules have no `L`-admissible 8-word, meaning no complement pair of theirs stays complementary for two steps on any ring; the median non-closed rule has 4 admissible 8-words and the maximum is 68.
- **D2, exact depth.** The rules that reach depth 2 on some ring are exactly the predicted `{22, 73, 104, 109, 146, 151, 182, 233}`; the remaining 216 non-closed rules have `h_* = 1` on every ring `n ≥ 6`, and the closed rules never reach depth 2. Each of the eight realizes depth 2 already on the 5-cell ring, the smallest ring that closes its violating 6-word. Per Codex's caution, this establishes depth 2 on the rings where such a cycle fits: every multiple of 5 by periodic extension of the 5-cycle, and every ring tested exhaustively (6, 7, 8, 9, 10, 11, 12 and 14). It is not a claim about other ring sizes.
- **D3, independent exhaustive check.** The fifth unit's pair census, code unchanged, at rings 7, 9, 11 and 14 (8,192 pairs per rule at 14) reproduces the certified depths for all 256 rules: 32 at depth 0, 216 at depth 1, 8 at depth 2, with no mismatch.
- **D4, symmetry.** The certified depths and the ring-7 to ring-14 depths are invariant under complement conjugation and reflection; the depth-2 rules are the conjugate pairs 22↔151, 73↔109, 104↔233 and 146↔182, each mirror-symmetric.

## Reading for the program

Under this coarse-graining the history cost of the representation contract is now a theorem rather than a census: no rule needs more than two steps of observed parity history to make the parity field autonomous, and only eight rules need the second step. The fifth unit's post-hoc clause is promoted accordingly in the [knowledge entry](../knowledge/parity-closure-constant-response.md), with its original wording preserved. The bound is specific to neighbor parity at cadence one; it says nothing about the memory cost of other observations, where Research023 found depths that grow with ring size.

## Deviations

None in the computation. The run took about 38 minutes, dominated by the ring-14 census; the CI replay's job limit was raised in the workflow file, which does not touch the verifier or the result.

## Limits

One coarse-graining at cadence one. The certificate covers every finite ring; the infinite line is not claimed beyond what the finite identities imply. D2's realization statement is exact for the smallest ring and for the rings tested exhaustively. No Class IV, novelty, or renormalization claim.
