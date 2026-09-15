# Independent verification: whole-state relations across ring arithmetic

Reviewer: Codex / OpenAI, session `/root/selector_review`, 2026-09-15.
The reviewer authored none of the study implementation or scientific protocol.

Gate 1 approved the clarified protocol at
`db2be505e4120259b649bf03967facd6b882a809`, before implementation or evaluation:
https://github.com/bombadil-labs/groovy-commutator/pull/264#issuecomment-5687700172

The primary implementation was pinned at
`60766e4fa4b7636db4707f3223cb2b50caf784b5`. Discovery selection and result were
committed at `6b0fc61adf188a8deeaa468c3104893d8b7ffa35`; confirmation seal was
committed at `9a4a73050baeec821ef9cbc7871d85cd28e756f4`. The reviewer did not
evaluate confirmation widths until the author confirmed that seal.

## Independent construction

`oracle.py` was written from the protocol before reading the author's study
implementation. Its original SHA256 is
`7927a1fb0dcd9a134cd518df4e9d98202a6a696e89f8c9ed86db97d16f5e5abb`.
It uses literal per-cell ECA updates, indegree peeling and explicit cycle walks,
Python `Counter` entropy/VI counts, and an independent GF(2) column-rank
calculation for Rule90. The graph algorithm independently chosen by both
implementations is the same standard peeling method; the code was not copied.

`verify.py` reconstructs every declared case. `check_readouts.py` independently
rebuilds the arithmetic descriptors, comparison scores, means, NumPy Pearson
coefficients, rounded discovery selection and confirmation sign decisions.
No author study functions are imported into these verifiers.

## Coverage and findings

- All 104 successor maps match exactly: 1,048,448 source-successor entries.
- All 936 partition arrays match, with basin labels compared up to relabeling:
  9,436,032 label entries. Cycle length and transient distance match literally.
- Every block count, partition entropy, maximum transient and maximum cycle
  length matches. Every source-state alignment and VI normalization is checked.
- All 3,276 within-ring relations match independently counted entropies, joint
  entropies, raw VI and VI per source bit; maximum error is below 8.9e-15.
- All 78 Rule90 horizon/ring entropies match independent GF(2) ranks. Its
  horizon-16 map is constant precisely at widths 4, 8 and 16 in the panel.
- All 19,656 final four-case comparison rows, all 702 ring responses, all 774
  stage associations and all 27 selection/confirmation decisions match.
  Maximum numeric error in this readout check is below 3.4e-15.
- All four source references in every final evidence row resolve to the
  correct saved rule/ring/observation and exact NPZ SHA256.

The selected confirmation outcomes are four matching signs, 21 opposite signs,
and two undefined signs. The undefined cases are `div4.n` for `future_1` and
`future_2`: the smaller endpoint of a pair wholly in widths 13–16 is one of
13, 14, 15, so this feature is constant. This is a support limitation of the
selected descriptor, not a new dynamical conclusion.

## Interpretation

No mathematical or implementation blocker was found. The controls establish
the expected arithmetic dependence in a known additive rule. The exploratory
first-order associations selected on widths 4–12 do not transfer consistently
to this particular four-width confirmation panel. Six held-out ring pairs,
shared endpoints, overlapping descriptors, ordinary size effects and the
eight-rule panel limit the interpretation. No universal relation, arithmetic
mechanism, Class-IV specificity or absence of prime-factor structure follows.

The instrument preserves raw whole-state partitions and exact graph maps, so
these scalar readouts do not exhaust the retained structure. This review does
not authorize an automatic follow-up experiment. Final Gate 2 remains pinned
to the completed PR head after reviewing publication, integrity and archive
preservation.

## Reproduction

After both scientific stages and the discovery seal are present, run locally:

```bash
python review/rule_ring_structure/verify.py discovery
python review/rule_ring_structure/verify.py confirmation
python review/rule_ring_structure/check_readouts.py
```

The three verification JSON files record counts, errors and verifier hashes.
The independent relation JSON files preserve all reconstructed within-ring
values. The review does not rerun the author's study scripts or overwrite any
scientific result.
