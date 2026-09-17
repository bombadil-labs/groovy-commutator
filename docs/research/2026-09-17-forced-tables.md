# Every ECA's first-floor forced table, full input: a ring-free dataset, section 37 verified, and a failed bet

The lift theorem makes the first-floor forced table of an elementary rule a
finite, ring-free object: the set of 35-bit child windows that some source
configuration produces, with the output, source bit and phase each one
forces. This unit computes those tables for all 256 rules from every
nine-bit source word, records their completion-independent invariants,
verifies every number GPT-5.6 Sol reported in section 37 of the proof state
(all reproduce exactly), caches pairwise cohabitation as a graph and a
metric, and asks one question of it. The question's bet failed: the
lift-induced conflict metric predicts the full sweep's pair regimes no
better than plain truth-table distance, although every one of the 1,164
commuting pairs cohabits and commuting pairs are nonvacuously compatible far
more often than the rest. On an eight-rule panel, second-floor cohabitation
agrees with first-floor cohabitation on all 28 pairs.

Evidence: exact for the tables, invariants, cohabitation counts and the
panel; exploratory for the regime join (one contract, one metric).
Protocol frozen before implementation
(`protocols/2026-09-17-forced-tables.md`); builder committed before the run;
evaluation preceded review under Myk's 2026-09-17 suspension of the
cross-model gates. Authored, run and integrated by Claude/Fable 5.1.
Dataset unit of the [Dimensional Closure Program](2026-09-09-dimensional-closure-program.md),
building on the [lift theorem](2026-09-17-affine-oriented-lift-theorem.md).

## The tables

For rule `r`, the affine-oriented first lift (`v± = ±e`, phase-saturated)
forces, at each window of rows `−3..3` on the period-six axis and positions
`−2..2`, an output bit, the recovered source bit and the phase. A ring of
width nine realizes every window exactly once per source word and centre
row, so the table is computed there and is ring-free; no key ever demanded
two different values (zero collisions over all 256 rules). Sizes run from
768 (18 rules, among them 0 and 204) to 3,072 (16 rules, among them 90),
and 110 forces 1,374, 54 forces 1,200. The completion count of rule `r` is
`2^(2^35 − |T_r|)`.

Invariants, all exact and all as section 37 stated: every rule's six phase
sheets have equal size; the key set has affine hull dimension 30 in `F₂³⁵`
for every rule (codimension 5, the five equalities between the `−3` and
`+3` rows); `(hull, h₂, h₃)` is the same on every phase sheet; the ANF
degree of the output over the forced domain is affine for 4 rules,
quadratic for 51, cubic for 201; recovery quadratic 95 / cubic 161; phase
decoder quadratic 55 / cubic 201; the `(h₂, h₃)` values for 41, 54, 106,
110 are (111, 265), (105, 184), (94, 218), (98, 202); and the triple
`(h₂, h₃, nonvacuous partners)` takes 88 distinct values on the 88
symmetry orbits. **P1 held in full.** Section 37 is no longer "reported."

## Cohabitation

Two rules cohabit when their tables agree on every shared key. Over the
32,640 pairs: 30,320 compatible, 17,926 nonvacuous (compatible with at
least one shared key), 2,320 conflicting; 54/110 cohabit on 36 shared keys,
106/110 conflict on 8 of 564. Conflict count is the lift-induced metric
(the minimum Hamming separation of the completion families). The conflict
graph has one component of 218 rules and 38 isolated rules that conflict
with nothing; rule 0 is compatible with all 255 others, rule 170 has the
most nonvacuous partners (216), rule 9 the fewest (52).

**P3 held.** Cohabitation is exactly reflection-invariant with equal
counts, and, not bet but found, exactly complement-covariant as well (zero
mismatches). The 16 affine rules form a compatible clique, though not a
nonvacuous one; so do the ten zero-`G` rules, nonvacuously; the eight
one-`G` rules compatibly. Of the 80 nontrivial symmetry orbits, 65 are
compatible cliques and 52 nonvacuous ones.

**Families as maximal cliques are uninformative.** The nonvacuous graph is
55% dense, and Bron–Kerbosch with pivoting found about twenty million
maximal cliques of size up to 61 before the 300-second cap (the count under
censorship varies with machine speed; the first, memory-exhausted attempt
found thirty million in ten minutes). A greedy clique of 61 rules exists.
Any "family classification" from this graph needs the metric and a
clustering choice, which this unit deliberately does not make.

## The bet, and what survived it

Joining to `results/sweep_full_classified.parquet` (established result 4):

| regime | pairs | compatible | nonvacuous | mean conflicts | mean table distance |
| --- | ---: | ---: | ---: | ---: | ---: |
| commute | 1,164 | 1.000 | 0.885 | 0.00 | 3.88 |
| drain | 4,009 | 0.957 | 0.667 | 0.13 | 4.00 |
| crystalline | 7,302 | 0.947 | 0.551 | 0.27 | 3.92 |
| structured | 14,751 | 0.935 | 0.518 | 0.29 | 4.06 |
| noisy | 5,414 | 0.852 | 0.471 | 0.83 | 4.08 |

- **P2a held:** commuting pairs are nonvacuously compatible at 0.885
  against 0.537 for the rest pooled. Stronger than bet: every commuting
  pair is compatible.
- **P2b held** in its stated form (Kruskal–Wallis on conflict count across
  regimes, p ≈ 10⁻¹⁴⁶; commute's median is lowest), but vacuously so: the
  median conflict count is zero in every regime, since 93% of all pairs
  conflict nowhere. The means order commute < drain < crystalline <
  structured < noisy.
- **P2c, the bet, failed.** For commute-versus-rest the AUC of conflict
  count is 0.537 and that of truth-table Hamming distance 0.527: a gap of
  0.010 where 0.05 was required. Both are near chance. The lift metric does
  not predict the divergence regime better than the table does.

Reading: cohabitation is a compatibility relation, and almost everything is
compatible; it separates commuting pairs perfectly at the "no conflict"
end but carries nearly no ordering elsewhere, and what ordering it carries
is already in the eight table bits. "Rules X and Y intersect in 2D rule
space" is therefore a weak signal on its own. The nonvacuous-rate
differences by regime (0.89 down to 0.47) are the one gradient worth
keeping, and they concern how often beams *meet*, not whether they agree.

## The D3 panel

Full-input second-floor tables for {0, 4, 30, 54, 90, 106, 110, 184} on
a ring of width fifteen (1,179,648 windows each, no collisions) have
18,432 to 294,912 entries (rule 90 largest). On all 28 pairs, D3
compatibility equals D2 compatibility and nonvacuity agrees; the three
D2-conflicting pairs (30/54, 54/90, 106/110) conflict at D3 too (3, 4, 10
conflicts), and no D2-incompatible pair became D3-compatible vacuously.
**P4 held.** As the protocol notes, a per-rule table at any floor is a
function of the source rule, which is readable from the D2 domain, so the
non-trivial content here is pairwise: on this panel the second floor adds
no cohabitation structure the first floor lacked.

## Use and caution

`tables_d2.npz` (per rule: sorted uint64 keys and packed values),
`invariants.json`, `pairs.npz` (shared, conflict, added pins), and
`families.json` are label-free, completion-independent per-rule and
per-pair primitives. Because the `(h₂, h₃, partners)` triple identifies the
symmetry orbit, any anonymous probe (Jev included) must receive coarse
summaries of these files, never the raw triple, and must say which columns
it exposes. The D3 tables are reproducible in minutes from the builder and
are not committed; their sizes and SHA-256s are in `d3_panel.json`.

## Deviations

The first canonical attempt stored every maximal clique and was killed by
memory before the D3 panel; the enumerator was changed to keep only the
count and the largest clique, the cap reduced to 300 s, and the whole build
rerun from scratch. The deterministic outputs of the first attempt's
finished phases were identical to the rerun's.

## Next

The bet's failure closes "the lift metric predicts pair dynamics" as a
line. What remains open is the nonvacuous-meeting gradient by regime and
whether a *weighted* cohabitation (agreement measured on the keys both
beams visit often under their own dynamics, not on the raw key set)
recovers the ordering the unweighted relation cannot. Off-beam sampling of
completions stays the place where new information lives.

## Files

`scripts/forced_tables_20260917.py`; `results/forced_tables_20260917/`
(`tables_d2.npz`, `invariants.json`, `pairs.npz`, `families.json`,
`regime_join.json`, `d3_panel.json`, `summary.json` with source hashes).
