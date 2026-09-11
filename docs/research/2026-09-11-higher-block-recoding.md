# What does the higher-block recoding cost, and what does it leave alone?

**Research note, 2026-09-11.** Fourth unit of the [Invariants Across Representation Contracts](2026-09-10-representation-invariants-program.md) program, and the first with a transformation that is not a global relabeling. Authored by: Claude Code, Fable 5.1. Reviewed by: none at evaluation (Codex inactive; Myk driving). Retrospective review: Codex (OpenAI), 2026-09-11, after merge; corrections applied in the follow-up PR and dated below. [Protocol](protocols/higher-block-recoding-20260911.md) frozen and [verifier](../../scripts/verify_higher_block_recoding.py) committed before this single deterministic run; canonical output [`results/higher_block_recoding_20260911.json`](../../results/higher_block_recoding_20260911.json). The on-family cap and covariance checks stand (B1–B3, on the consistent-pair family, and the observer-family-closure part of B4); the ambient-radius declaration and B4's literal-summary consequence required retrospective correction and are not counted as original frozen successes.

## The transformation

`T_β` sends a binary configuration to its 2-block presentation, `S'_i = (S_i, S_{i+1})`. It is injective, its forward locality is radius 1, its inverse is the radius-0 projection, the alphabet grows from 2 to 4 symbols (two stored bits per site instead of one), and the family shrinks from the full shift to the subshift of consistent pairs. The law, derivative, and correction rows transport componentwise. **Deviation (2026-09-11):** the total block law that was executed reads first components and returns `(F(s)_i, F(s)_{i+1})`, which has ambient radius 2 off the family, not the radius 1 the protocol declared; a Rule 170 witness is asserted in the verifier. A componentwise completion (apply the binary rule to each component field) has ambient radius 1, agrees with the executed law on the family for all 256 rules, and B2 and B3 are now reported under both laws with identical on-family results. Costs are declared in the protocol. This is the simplest instance of what Codex flagged in the review of #67: a conjugacy that changes the alphabet.

## Answer

- **B1, cap radius.** In block coordinates the minimum passing cap radius satisfies `mpr − 1 ≤ mpr_β ≤ mpr` in every decided cell (674 cells, K and O, `h ≤ 2`, `R ≤ 4`), with the consistency conditions holding where one side is undecided. The recoding reduces the radius in only 9 cells and leaves it unchanged in 665:

| kind | `h` | unchanged | reduced by 1 |
| --- | --- | --- | --- |
| K | 0 / 1 / 2 | 30 / 127 / 178 | 0 / 1 / 2 |
| O | 0 / 1 / 2 | 30 / 126 / 174 | 0 / 2 / 4 |

The nine cells: K 55 (`h=1`), K 109 and K 233 (`h=2`), O 73 and O 109 (`h=2`), O 146 and O 182 (`h=1` and `h=2`). Two cells undecided at `R ≤ 4` in the original become decided at radius 4 in block coordinates, as the inequality allows.

- **B2, componentwise covariance.** `D'(β S) = β(D S)` and `G'(β S) = β(G S)` for all 256 rules and all states on rings 8 and 10, where `D'` and `G'` are computed natively on the 4-symbol system. This is algebra (`β` is XOR-linear and the block law is defined by `F'∘β = β∘F`) and the run is a control.
- **B3, derivative closure.** Closure of the derivative observation on the image equals closure of the original for all 256 rules at both rings, as conjugacy requires.
- **B4, Research026 observer family.** The static family of all nonconstant Boolean functions of 2-cell and 3-cell blocks is closed under input complement and under input reversal, output-complement pairs are preserved, and the 12-ring block alignment survives reflection for both block sizes. Closure transports maximizers through explicit permutations of observer tables, now recorded by the verifier (for 2-cell blocks, table 1 maps under input complement to table 8, canonical representative 7). By conjugacy, the scalar per-rule summaries of the [possibility-frontier census](2026-09-08-possibility-frontier.md), the optimal values, counts and overlap flags, are identical for a rule, its complement-conjugate, and its mirror, while the named optimal observers correspond under the permutation rather than coinciding literally (corrected 2026-09-11). The per-rule tables of that census are not in the repository, so this is a deduction from a finite check, not a numerical audit.

## Reading for the program

The higher-block recoding never costs cap radius and buys at most one unit, in 9 of 674 cells, while doubling stored bits per site. For the primitives program this is the first calibration of an equivalence notion: two constructions that differ by a 2-block recoding have the same decoded dynamics, closure and commutator, and differ by at most one unit of cap radius. Whether the recoded system counts as a useful new implementation depends on the resource contract, since equivalent computations can have different costs; what a learner should not do is count the recoding as new decoded dynamics (qualified 2026-09-11).

## Limits

One recoding (`k = 2`); nothing about `k > 2`, non-injective recodings, or other observers. Ring results are exhaustive at `n ≤ 10`; cap results are exhaustive over full causal windows within `R ≤ 4`. Where a property is preserved by algebra the run is a control, and the note says so.

## Next

Two transformation types remain undeclared: a change of ambient completion on a shared invariant family, which Codex's [second-lift protocol](2026-09-10-second-lift-completion-protocol.md) already freezes for Rule 32 and which should run under that protocol rather than here, and a non-injective coarse-graining, which is the Erased Distinctions Program's object and where "preserved" must be replaced by "closed". The program's transformation table should be consolidated into a single page before either.

## Correction 2026-09-11, after retrospective review by Codex

Recorded in the [protocol addendum](protocols/higher-block-recoding-20260911.md): the executed law has ambient radius 2 off the family (deviation, with witness); a radius-1 componentwise completion is added and both laws are run; B4 is restated as transport of maximizers with explicit permutations; the cost statement records two stored bits per site and no longer implies that a cheaper-radius recoding is not a useful implementation. On-family numbers unchanged.