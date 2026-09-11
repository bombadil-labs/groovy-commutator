# Protocol: a finite certificate for the history bound under neighbor-parity coarse-graining — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md), sixth unit.
**Authored by:** Claude Code, Fable 5.1. **Protocol review:** pending; requested from Codex (OpenAI) on the gathering PR before any implementation or evaluation, per the [gathering-branch workflow](../../../AGENTS.md#gathering-branches-and-cross-model-review).
**Why this unit:** the [fifth unit](../2026-09-11-parity-coarse-graining.md) found, post hoc and unpredicted, that every non-closed rule has refinement depth `h_* ∈ {1, 2}` under neighbor parity at every ring `n ≤ 12`. A post-hoc bound must be frozen before it can be promoted. This protocol turns it into a prediction with a finite certificate that, if it passes, proves the bound for every ring size, and an independent exhaustive check at rings the fifth unit did not visit.

## 1. Objects (fifth-unit definitions, unchanged)

`π(S)_i = S_i ⊕ S_{i+1}`; fibers `{S, ¬S}`; complement response `g_r(l,m,r) = r(l,m,r) ⊕ r(¬l,¬m,¬r)`. For a ring state `X` write `g_r(X)` for the ring of window values `g_r(X_{i−1}, X_i, X_{i+1})`. A pair `(F^t X, F^t ¬X)` is unsplit at `t+1` iff `g_r(F^t X)` is constant on the ring: all-zero means the pair becomes equal (absorbing), all-one means it stays complementary. `h_*` is the largest first separation time over complement pairs, `0` if none separates.

Define, per rule, the sets of ring states

- `W_1 = { X : g_r(X) ≡ 1 }`, states whose pair stays complementary for one step,
- `W_0 = { X : g_r(X) ≡ 0 }`, states whose pair becomes equal,
- `L = W_1 ∩ F^{−1}(W_1)`, states whose pair stays complementary through two steps.

`W_1` is a subshift of finite type with allowed 3-windows `A_1 = g_r^{−1}(1)`; `L` is a subshift of finite type with 5-cell constraints (a 3-window of `F(X)` reads five cells of `X`).

**Lemma (frozen, with proof).** If for a rule every state of `L` on every ring has `g_r(F²(X))` constant, then `h_* ≤ 2` on every ring. Proof: let the pair of `X` be unsplit through steps 1 and 2 with `X ∈ L`. Then `F²X ∈ W_0 ∪ W_1`. If `F²X ∈ W_0` the pair becomes equal and never separates. If `F²X ∈ W_1`, then `FX ∈ W_1` and `F²X ∈ W_1` give `FX ∈ L`, so the hypothesis applies to `FX` and `F³X ∈ W_0 ∪ W_1`; by induction the pair never separates. Pairs that are unsplit at step 1 but not through step 2 separate at `t = 2` or become equal at `t = 1`. Hence every separating pair separates at `t ≤ 2`.

**Finite check of the hypothesis.** `g_r(F²X)_i` is a function of the seven cells `X_{i−3} … X_{i+3}`. Constancy of `g_r(F²X)` around a ring follows from equality of adjacent values, `g_r(F²X)_i = g_r(F²X)_{i+1}`, which reads the eight cells `X_{i−3} … X_{i+4}`. An 8-word is *`L`-admissible* when every 5-subword satisfies `L`'s constraints (all 3-windows of the word in `A_1`, and all 3-windows of the word's `F`-image in `A_1`). Every 8-cell window of a ring state in `L`, wrapped or not, is an `L`-admissible 8-word, so if every `L`-admissible 8-word has equal adjacent values the hypothesis holds on every ring `n ≥ 1`. The converse direction (a violating 8-word that lies on a cycle of `L`'s de Bruijn graph yields a ring state in `L` with a nonconstant `g_r(F²X)`) is used only to interpret failures, not asserted as a prediction.

## 2. Frozen predictions

- **D1 (certificate).** For every one of the 224 non-closed rules, every `L`-admissible 8-word has equal adjacent `g_r∘F²` values. Consequence, by the lemma: `h_* ≤ 2` for all 256 rules on every ring size. Any failing rule is listed with a violating 8-word and whether that word lies on a cycle of the `L` graph (a genuine ring counterexample) or not (a boundary word with no ring realization).
- **D2 (exact depth for all `n`, from local checks).** Define the analogous 6-word check for depth 2: `h_* ≥ 2` on some ring iff some `W_1`-admissible 6-word (all 3-subwindows in `A_1`) has unequal adjacent `g_r∘F` values and lies on a cycle of `W_1`'s de Bruijn graph. Prediction: exactly the 8 rules `{22, 73, 104, 109, 146, 151, 182, 233}` satisfy this, so their `h_*` is 2 on every ring where such a cycle fits, and the remaining 216 non-closed rules have `h_* = 1` on every ring `n ≥ 6`. The smallest ring on which each of the 8 reaches depth 2 is reported (a cycle length), not predicted.
- **D3 (independent exhaustive check at unvisited rings).** The fifth unit's exact pair census, code unchanged, at `n ∈ {7, 9, 11, 14}` reproduces the certified depths: `h_* = 0` on the 32 closed rules, `1` on the 216, `2` on the 8. This is the only computationally heavy step; `n = 14` has 8,192 pairs per rule.
- **D4 (symmetry, theorem control).** `h_*` is invariant under complement conjugation and reflection: `π(¬S) = π(S)` makes the pair census of `r̃` the census of `r` with the roles of `X` and `¬X` exchanged, and reflection commutes with `π` up to a shift. The certified depth sets are closed under both maps; the 8 depth-2 rules are four complement-conjugate pairs of mirror-symmetric rules.

## 3. Artifacts

`scripts/verify_parity_history_bound.py`, committed after protocol review and before evaluation; reuses `refinement()` from `scripts/verify_parity_coarse_graining.py` by import for D3 and reads `results/parity_coarse_graining_20260911.json` for the closed set and the `n ≤ 12` depths; output `results/parity_history_bound_20260911.json` with source hashes, per-rule certificate verdicts and any violating words, the D2 classification with smallest depth-2 ring, the D3 depths per ring, and the D4 orbit check. CI replays it byte-for-byte. Note under `docs/research/2026-09-11-parity-history-bound.md`; the knowledge finding `parity-closure-constant-response` gets its post-hoc clause upgraded to a certified statement only if D1 passes, with the fifth unit's wording preserved as history.

## 4. Not claimed

Nothing about other coarse-grainings or cadences; the bound is specific to neighbor parity at cadence one. `L`-admissible words that fail the check but lie on no cycle are not counterexamples and are reported as such. No claim about the infinite line beyond what the finite certificate implies for arbitrary finite rings. No Class IV, novelty, or renormalization claim. If D1 fails for some rule with a genuine ring counterexample, the bound is refuted for that rule and the failing ring size is the result; the fifth unit's `n ≤ 12` data stand unchanged.
