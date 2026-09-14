# One complemented temporal row closes first-floor centered G for all 256 ECAs

14 September 2026. Authored by Codex (OpenAI), continuing Myk's authorized local working session. Gate 2 accepted 2026-09-14 (Claude/Fable, exact head a641df751bc81b50947b8ea7bd1c4d9d2ae8203f, PR #233). Protocol review: none at freeze; run authorized by Myk 2026-09-14. Evaluation preceded independent review. This construction continues the DT2 cycle, whose temporal-depth hypothesis was supplied by Claude/Fable via Myk; the census domain, implementation and evaluation here are this session's.

**All eight remaining first-floor holdouts have faithful binary centered-G carriers after complementing the two-step change row.** One shared recipe works for all eight. Retaining the previous verified recipes gives cumulative coverage of **256 faithful / 156 original G / 256 centered G** at native radius two. This closes the first-floor centered-G existence question across the ECA sources; recursive closure remains open.

## The shared repair

Use the derivative table `r XOR 204` and integrate by XOR: `E(S)=S XOR D_r(S)`. For each of rules 171, 187, 233, 235, 241, 243, 249 and 251, repeat the five rows

\[
\boxed{P,\quad D,\quad A_2,\quad M,\quad Q}
\]

with

\[
P_i=S_i\oplus S_{i+1},\qquad D=D_r(S),\qquad
A_2=1\oplus S\oplus E_r^2S,
\]
\[
M_i=(1-S_i)D_i,\qquad Q_i=(1-S_{i-1})S_{i+2}.
\]

A2 is the complement of T2: a bit is one when that source site agrees with its value two steps later. It is not `D(D(S))`. The five-field order, mask, direction, reference formula and complemented field are the same for every one of the eight; the primitive derivative and compiled native tables still depend on r.

One phase-free binary 5x5 rule evolves the prepared image exactly and admits a local source decoder at every row. First-floor parent recovery is the same gate. The centered physical commutator is prescribed on the true P and D rows only: P_s(G_centered) on P, G_centered on D. A2/M/Q carrier outputs remain unspecified.

Both native zero choices work for this shared recipe. Concrete sparse derivative tables and decoders are exported for all eight using h(0)=0; all unlisted outputs remain free. The exports contain 1,273 to 2,963 forced derivative keys out of 2^25 possible keys.

## Why the complement helps

For a fixed row-polarity vector epsilon, define `L_epsilon(S)=L(S) XOR epsilon`, repeated with the row period. Its native derivative and commutator probe are unchanged:

\[
L_\epsilon(S)\oplus L_\epsilon(ES)=L(S)\oplus L(ES)=U.
\]

But the native neighborhoods of L_epsilon(S) change. A row complement can therefore remove a native/probe collision without changing the probe's retained information or demanded output.

For the shared A2 recipe, the complete observed native and probe key sets are **disjoint for each of the eight rules**. This is an exhaustive statement at the declared radius and prepared family. The carrier constraints are independently consistent after centering. The algebra explains how the repair is possible; the finite census establishes that this particular encoding succeeds. No general theorem that complements always separate the two domains is claimed.

This changes the relevance of an earlier negative result. Complementing a row cannot separate two identical temporal probes, because its complement cancels from the probe. It can separate the native domain from the probe domain. T2 and row polarity address different obstructions.

## The eight-rule background cluster

All eight satisfy f(000)=f(111)=1 and f(010)=0, f(101)=1: uniform states reach all ones and checkerboards have a two-cycle. These are particular trajectories, not Wolfram-class assignments for arbitrary initial states. Their color-conjugate partners are 42,34,104,40,112,48,96,32 respectively; those partners already have original-G carriers in the cumulative results. Reflection groups the eight into 171/241,187/243,235/249 and self-mirror 233/251. Color conjugation does not automatically transport our derivative/carrier convention, so it was motivation for this test, not a shortcut to success.

## Complete census and verification

The experiment accounts for all eight source rules, four masks, both P signs and all cyclic row orders. It tests all 16 polarity vectors for P/D/T2/M and all 32 for P/D/T2/M/Q, with all four previous Q formulas. No earlier rejection is inherited after changing the encoding.

| Family, tested on the eight holdouts | Cases | Faithful | Original G | Centered G |
|---|---:|---:|---:|---:|
| P/D/T2/M, all polarities | 6,144 | 7 | 0 | 7 |
| P/D/T2/M/Q, all polarities | 196,608 | 8 | 0 | 8 |
| Union | 202,752 | 8 | 0 | 8 |
| Auxiliary-only polarities, subset of union | 50,688 | 8 | 0 | 8 |

Rule 233 still needs Q for recovery in this domain. Original and centered counts both require native evolution and recovery in the same recipe. Every G carrier still uses the unchanged P/D convention, even when a tested encoding complements P or D.

The primary sparse computation finished in 14.82 seconds, plus 1.60 seconds compilation. It uses all 2^11 source assignments in [-5,+5] for probes, and the complete 2^9 assignments in [-4,+4] for native patches whose outer two source bits are irrelevant. Duplicate identical constraints are compressed while retaining witness payloads.

All 6,528 zero-polarity gate vectors matched the preceding DT2 census. The separate cropped-source implementation then passed:

- All **633,592** saved negative certificate pairs.
- Reflection checks over **202,752** recipe records.
- **31,820** exact gate comparisons on **6,364** selected records.
- **20,488,192** direct physical-G and **51,101,696** native next-cell evaluations.

This check took 47.26 seconds. The concrete shared recipe received an additional export/verification on all eight rules and both zero branches: **65,536** physical-G, **327,680** native next-cell and **81,920** decoder evaluations. Its native/probe overlap is zero in every rule. These are independent implementations within the author session, not independent-agent review or a second full census.

The common recipe was selected after inspecting the completed census. Its simplicity is a post hoc compression result, not a predeclared prediction. The census also contains many alternative successes.

## Why original G cannot be universal with this carrier

This is an algebraic obstruction, stronger than the recipe census. Suppose the source has a fixed configuration S* and `E_r(0)=1`. Faithful native evolution makes X*=L(S*) a fixed configuration of H. Therefore

\[
G_r(S_*)=E_r(0)=1,\qquad G_H(X_*)=H(0).
\]

A uniform binary CA sends the all-zero configuration to a uniform bit. But the prescribed P/D carrier of the constant-one field is zero on P and one on D. H(0) cannot equal that mixed carrier. No encoding complement, larger radius or free-output completion can solve this under the same faithfulness and original P/D-carrier contract.

Every one of the eight satisfies `f(000)=f(111)=1`, so S*=all ones supplies the obstruction. The same argument covers all 64 ECA rules with those two truth-table bits, and more generally any source with the stated fixed-point and zero-background properties.

Centering subtracts the background values on both sides: `G_r_centered=G_r XOR E_r(0)` and `G_H_centered=G_H XOR H(0)`. Both vanish at the fixed configuration, removing this contradiction. Original-G coverage remains **156**; it is not silently renamed universal. A universal original-G theorem would require changing the carrier contract or source domain.

## Scope and next question

The cumulative family is a union of the earlier four-reference recipes, the T2 recipes that repaired 28 holdouts, and the complemented-T2 repair for the final eight. A single parameter-free five-row recipe has not been tested for all 256 rules. The generator still chooses a source-dependent recipe and leaves off-image native outputs nonunique.

Alphabet: one bit per cell. Native radius: two in both axes. Preparation: source radius two. Transverse period: four or five, with only source-line independent information. The extra polarity is a fixed encoding convention, not a per-cell input label. G remains constrained only on P/D. No all-channel covariance, independent area information, or nontriviality follows merely from faithful evolution.

No new recursive run was performed. Earlier 3D G coverage remains 206 and the historical 4D sample remains 113 faithful / 105 G. The next question is whether the now-complete centered-G first-floor family can be selected and reused under the full symbolic-parent recursive contract. The bridge's three determined lineage types are a weaker contract and must remain separately labeled. Source preparation radius may increase under H^2 even when native radius stays two.

The completed complement census is retired as an unchanged experiment. The original-G fixed-point obstruction is not retried unchanged. Further dimensional testing should address recursive compatibility, not merely add a dimension to the headline.

## Reproduction artifacts

The checkpoint contains `audit_row_complements.cpp`, `run_row_complements.py`, `verify_row_complements.py`, and `export_complement_carriers.py`, together with their pinned DT2 dependencies. `runs/row_complements_8/` contains the pre-run protocol, manifest, every recipe and negative certificate, verification records, the shared recipe, and eight compressed sparse rule/decoder exports. Runs remain off CI; repository integrity checks validate preserved bytes and regenerated accounting.


Repository evidence: [extension guide](../../experiments/binary_lift_20260914/EXTENSION.md), [canonical accounting](../../results/binary_lift_20260914_extension.json), [all-rule current coverage](../../results/binary_lift_20260914_extension/rule_coverage.csv), and [authorization/deviations](protocols/binary-lift-extension-record-20260914.md). The earlier [four-reference](2026-09-14-binary-lift-family.md) and [3D/4D](2026-09-14-binary-lift-recursion.md) datasets retain their original scopes.
