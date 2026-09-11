# Protocol: wiring as a transformation, neighborhood dilation on the ring — 2026-09-11

**Status:** frozen before implementation and evaluation. Nothing run.
**Program:** [Invariants Across Representation Contracts](../2026-09-10-representation-invariants-program.md), eleventh unit.
**Authored by:** Claude Code, Fable 5.1. **Protocol review:** pending (Codex, gate 1, requested on the gathering PR before implementation).
**Why this unit:** every transformation audited so far acts on the state or on what is observed of it. The interaction-graph framing in B. Rose, *Cellular Automata as Interaction Graphs* (CargoCultResearch preprint, 2026) treats the wiring as the type and the rule table as the invariant, and asks which dynamical properties survive a change of wiring. This unit opens that fourth transformation type in the program's vocabulary with the simplest rewiring of the ring, neighborhood dilation, where a theorem says exactly when the change is a relabeling in disguise. Disclosure: while reviewing that preprint, before this protocol was written, the author checked numerically that dilation by 2 on rings 7, 9 and 11 is conjugate to the standard automaton for all 256 rules; that check is the theorem control W1 below and is not counted as a result.

## 1. The transformation and its costs

For a dilation factor `d ≥ 1` and the `n`-ring, the dilated automaton with rule `r` is `F_r^{(d)}(S)_i = f_r(S_{i−d}, S_i, S_{i+d})`: the same 8-entry rule table read at offsets `{−d, 0, +d}` instead of `{−1, 0, +1}`. The dilated observation `ψ^{(d)}` is defined the same way. Costs: the rule table is unchanged; the radius becomes `d`; the interaction graph changes; the state is untouched. The transformation has two declared transports: **whole-contract dilation**, where the rule and the observation are dilated together, and **partial dilation**, where the rule is dilated and the observation is not.

Lemma (stated, checked before freezing, not a result): if `gcd(d, n) = 1`, the site permutation `P_d(S)_j = S_{dj mod n}` satisfies `F_r^{(d)} = P_d^{-1} ∘ F_r ∘ P_d` for every rule, so whole-contract dilation is conjugation by a site relabeling. If `d` divides `n`, the dilated automaton is `d` independent copies of the standard automaton on the ring `n/d`, interleaved. Corollary for partial dilation with `gcd(d, n) = 1`: `C_ψ(F^{(d)}) = C_{ψ^{(e)}}(F)` where `e = d^{-1} mod n`, so the partial census equals the standard census under an observation rewired to offsets `{−e, 0, +e}`; the same identity holds for `K`, `Z`, `X` and `h_*`.

Domain: rings `n ∈ {6, …, 12}`, factors `d ∈ {2, 3}`, observations `ψ ∈ {232, 4}` with reference censuses from the [eighth](../2026-09-11-block-majority.md) and [ninth](../2026-09-11-isolated-cell.md) units, and the result-1 commutator classification (zero-`G`, one-`G`, varying) as the state-level property. Closure `C`, commuters `K`, collapse `Z`, residual `X` and depth `h_*` are as in the tenth unit.

## 2. Frozen predictions

- **W1 (whole-contract dilation is a relabeling; theorem control).** For every `(d, n)` with `gcd(d, n) = 1` and both observations, the census of the dilated rules under the dilated observation, `C`, `K`, `Z`, `X` and `h_*` for all 256 rules, is identical to the standard census at ring `n` read from the eighth and ninth units' result files, and the result-1 commutator classification of `F_r^{(d)}` on that ring equals the standard classification for all 256 rules. Every property is preserved, exactly.
- **W2 (partial dilation is a change, not an invariance).** For `d = 2` and every odd `n ∈ {7, 9, 11}`, and for both observations, the closed set of the dilated rules under the standard observation differs from the standard closed set. Frozen witnesses: the observation rule itself, `ψ`, commutes with `F_ψ` but is predicted not to commute with `F_ψ^{(2)}`, and to be absent from `K_ψ(F^{(2)})` at every such ring; `{0, 170, 204, 240}` remain in `K` (constants fixing the uniform configurations, identity, and the unit shifts, which commute with every shift-equivariant map). The consistency identity `C_ψ(F^{(2)}) = C_{ψ^{(e)}}(F)` with `e = 2^{-1} mod n` is checked as a control at every odd `n`. Whether the depth table changes, and how, is reported.
- **W3 (even rings split; theorem control).** For `d = 2` and every even `n ∈ {6, 8, 10, 12}`, under whole-contract dilation: a rule is closed on the `n`-ring iff it is closed on the `n/2`-ring, `K`, `Z` and `X` correspond likewise, and `h_*` on the `n`-ring equals `h_*` on the `n/2`-ring, because the refinement of a product partition by a product map is the product of the component refinements. The `n/2`-ring censuses (`n/2 ∈ {3, 4, 5, 6}`) are computed in the unit. Rings below 5 are outside every earlier census; whatever they show is reported, and W3 is scored on the equality only.
- **W4 (`d = 3`).** For rings `n ∈ {7, 8, 10, 11}` (`gcd(3, n) = 1`), W1 holds verbatim. For `n ∈ {6, 9, 12}` the automaton splits into three rings of size `n/3 ∈ {2, 3, 4}`; the whole-contract census at ring `n` equals the `n/3`-ring census, as in W3. Both are theorem controls.
- **W5 (the state-level property under partial dilation; reported).** The result-1 classification of `G` is a property of the rule alone and does not involve the observation; it is therefore preserved by both transports whenever `gcd(d, n) = 1` (W1) and reported on split rings.

## 3. Artifacts

`scripts/verify_wiring_dilation.py`, committed after protocol review and before evaluation; reads `results/block_majority_20260911.json` and `results/isolated_cell_20260911.json` for the reference censuses and provenance hashes; output `results/wiring_dilation_20260911.json` with source hashes, per-`(d, n, ψ)` censuses under both transports, the small-ring censuses used by W3 and W4, the commutator classification per `(d, n)`, and the W1–W5 verdicts with every violation. Registered in `scripts/check_result_integrity.py`; CI carries both tiers. Note under `docs/research/2026-09-11-wiring-dilation.md`; the Program page gains a fourth transformation type and a table row.

## 4. Not claimed

Nothing about rewirings other than dilation of the three-cell neighborhood on a ring; nothing about non-contiguous offset sets in general, 2D lattices, or block or second-order constructions, which the cited preprint also catalogs. Nothing about rings outside 6 to 12 except where the lemma is a theorem. The partial-dilation censuses are exact within the domain and are not claimed to characterize anything. No Class IV, novelty, or renormalization claim.

## 5. Protocol review record

Pending. To be filled with the reviewer's identity, date, reviewed revision, requested checks and binding clarifications before any implementation commit.
