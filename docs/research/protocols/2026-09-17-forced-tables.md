# Protocol: first-floor forced tables for all 256 ECAs, full input, with cohabitation and a pair-regime bet

**Status:** FROZEN before implementation and evaluation.
**Date:** 2026-09-17.
**Author:** Claude/Fable 5.1, Myk's session.
**Program:** Dimensional Closure and the Commutator Lift (dataset unit after the lift theorem).
**Protocol review:** none at freeze. Myk's 2026-09-17 suspension of the
cross-model review gates remains in force; this session runs, self-reviews
and merges. The results note must say evaluation preceded review.

## 1. Purpose

The lift theorem makes the first-floor forced table of every ECA a
ring-free, exact, once-and-for-all object: the set of 35-bit child windows
that some source configuration produces, with the native output, the
recovered source bit and the phase each forces. The repository's existing
caches were built on ring-7/8 source families; this unit computes the
full-input tables for all 256 rules, records their completion-independent
invariants, reproduces the numbers GPT-5.6 Sol reported in proof section 37
(currently unverified), and turns pairwise cohabitation into a cached graph,
metric and family structure. One frozen bet connects the lift-induced metric
to the pair-divergence regimes of established result 4, so the dataset is
asked a question rather than only cached.

## 2. Objects

For each rule `r`, with the affine-oriented six-field lift at entry
(`v± = ±e`, phase-saturated), the **forced table** `T_r` maps each 35-bit
window (rows `−3..3` of the period-six axis × positions `−2..2`, packed
row-major) to `(output, source bit, phase)`, where phase is the field index
of the window's centre row. Its domain is the set of windows produced by all
512 nine-bit source words at all six centre rows; a ring of width nine
realizes every window exactly once per (word, row), so the table is computed
on that ring and is ring-free. Within-rule consistency (equal keys never
demand different values) is asserted, not assumed.

Per-rule invariants, all exact:

- `|T_r|`; the six per-phase sheet sizes; the completion count
  `2^(2^35 − |T_r|)` as an exponent.
- Affine hull dimension of the key set in `F₂^35`, and per phase sheet.
- `h₂(r,p)`, `h₃(r,p)`: the GF(2) rank of all monomials of degree at most 2
  and 3 in the 35 window bits evaluated on phase sheet `p`.
- Minimal ANF degree (over the forced domain) of the output function, the
  recovery function and the phase decoder (three indicator bits of the
  binary phase index; the decoder's degree is the maximum over them).

Pairwise, for every unordered pair `{r, s}`: shared keys
`|dom T_r ∩ dom T_s|`; conflicts (shared keys with different outputs);
compatible iff conflicts = 0; nonvacuous iff compatible with at least one
shared key; added pins `|dom T_s \ dom T_r|`. Conflict count is the
lift-induced metric (it equals the minimum Hamming separation of the two
completion families, proved 2026-09-15).

Families: the compatibility graph and the nonvacuous graph on 256 rules;
conflict-graph components and degree distribution; for named candidate
sets, whether they are cliques (the 16 affine rules; each of the 88
reflection/complement orbits; the result-1 zero-G and one-G classes);
maximal cliques of the nonvacuous graph by Bron–Kerbosch with pivoting under
a ten-minute cap (censored if exceeded, with the greedy clique-number lower
bound reported either way).

D3 panel: for `{0, 4, 30, 54, 90, 106, 110, 184}`, the full-input second-
floor forced table (7×7×5 window, diagonal rails, source dependency fifteen
bits, computed on a ring of width fifteen), its size, and D3 pairwise
shared/conflict/compatible counts for the 28 pairs. Note, stated here so it
cannot be mis-sold later: a forced table at any floor is a function of the
source rule, and the source rule is readable from `T_r`'s domain, so
"higher floors are determined by D2" is trivially true per rule. The
non-trivial question is pairwise, below.

## 3. Frozen predictions

- **P1 (section 37 reproduces exactly):** for every rule the six phase
  sheets have equal size and the full hull dimension is 30 (codimension 5,
  the five equalities between the `−3` and `+3` rows); `(hull dim, h₂, h₃)`
  is the same on every phase sheet of a rule; output degrees distribute
  4 affine / 51 quadratic / 201 cubic, recovery 95 / 161 (quadratic /
  cubic), phase decoder 55 / 201; compatible pairs 30,320 and nonvacuous
  17,926; 54/110 compatible with 36 shared keys; 106/110 incompatible with
  564 shared keys; the triple `(h₂, h₃, nonvacuous partner count)` takes 88
  distinct values on the 88 orbits. Any deviation is reported as a
  correction to the handoff, not smoothed.
- **P2 (the lift metric predicts the pair regime beyond the truth table):**
  joining the 32,640 pairs to `results/sweep_full_classified.parquet`,
  (a) commute pairs are nonvacuously compatible at a strictly higher rate
  than the other four regimes pooled; (b) conflict count differs across
  the five regimes (Kruskal–Wallis, `p < 0.01`, descriptive) with commute
  pairs having the lowest median; (c) for commute-versus-rest, the AUC of
  conflict count exceeds the AUC of plain truth-table Hamming distance
  (number of the eight table entries on which `r` and `s` differ) by at
  least 0.05. (c) is the bet; (a) and (b) are expected to hold and are
  weaker.
- **P3 (symmetry and the affine block):** cohabitation is exactly
  reflection-invariant (`compatible(r,s) ⇔ compatible(mirror r, mirror s)`
  with equal shared and conflict counts) and the 16 affine rules are a
  clique of the compatibility graph. Complement covariance is reported
  descriptively (the affine marker is not complement-symmetric).
- **P4 (D3 panel, pairwise):** on the 28 panel pairs, every D2-compatible
  pair is D3-compatible, and nonvacuity agrees between floors. A D2-
  incompatible pair may become D3-compatible only vacuously; report it.

## 4. Outputs

`results/forced_tables_20260917/`: `tables_d2.npz` (per rule: sorted keys
as uint64 and packed values), `invariants.json` (per rule), `pairs.npz`
(256×256 shared, conflict, added-pins), `families.json`, `regime_join.json`,
`d3_panel.json` (sizes, SHA-256 of each panel table, pairwise counts; the
D3 tables themselves are reproducible in minutes and not committed), and
`summary.json` with predictions and a `source_hashes` block registered in
the fast integrity tier. Runtime expected under thirty minutes off Actions.

## 5. Use by later units, and a leakage caution

The per-rule invariants and the cohabitation matrix are label-free,
completion-independent primitives suitable for Jev-style anonymous probes.
Because the section-37 triple identifies the symmetry orbit injectively, a
probe must receive coarse summaries (ranks, quantiles, degree counts, graph
statistics), never the raw identifying triple, or the anonymity is
nominal. Any protocol drawing on this dataset states which columns it
exposes and why they are not identifying.

## 6. Non-claims

Nothing about completions' dynamics or ambient class; nothing above D2
beyond the eight-rule panel; families are descriptive except the named-set
clique checks; P2 is one contract (the sweep's) and one metric.
