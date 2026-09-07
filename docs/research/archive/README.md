# Recovered conversation artifacts

These two Markdown files are unchanged research artifacts recovered from
**Analysis of Collusion Wiki** on 2026-09-07. They preserve the path of the
investigation, including provisional language subsequently qualified. The
source manifest records the hashes of the recovered notes, CSVs, and patch ZIP.
Targeted conversation retrieval was available; the complete transcript was not.

The patch's script is integrated as
[`scripts/experiment_history_repairability.py`](../../../scripts/experiment_history_repairability.py).
Its two CSVs and summary JSON are in `results/`. Running the original recovered
script against the repository's CA engine reproduced every table value to
1e-12 tolerance on 2026-09-07, after normalizing its `wclass` column name to the
archived CSVs' `class` header. The summary JSON reproduced byte for byte. The integrated script adds repository import setup and
method/source qualifications; its numerical algorithm is unchanged.

Read the original comparison as an exploratory record. The later nonclosure
note supersedes the simple proposal that history repair identifies Class IV.
In particular, Class II also repairs strongly, and the statistic depends on
projection, sampling cadence, trajectory ensemble, and predictor family.

Additional qualifications established during recovery:

- The canonical parity dataset ends at **h=3**, while the majority dataset ends
  at **h=4**. The earlier comparison's separate pilot tables use other depths.
- The stored canonical label for Rule 41 is II, but the full table labels it IV.
  The cited Borriello & Walker paper also describes Rule 41 as IV. Preserve
  the old CSV for provenance; do not treat this discrepancy as independently
  validated class membership. Rule 106's III/IV status is explicitly disputed
  in Alfaro & Sanjuan (2024).
- Error is empirical next-bit misclassification, not conditional entropy or
  proof that the entire projected state lacks a Markov description.
- The original script already used independent training and test seeds.
  It assigned 0 to unseen/tied contexts and used slightly different target
  windows across history depths. The follow-up validation controls these choices.
- Original raw compression uses a separate n=301 trajectory and rowwise byte
  padding; prediction uses n=300. Neither compressor ratio nor class enrichment
  constitutes a general complexity theorem.
- The comparison's Rule-90 damage count requires an infinite lattice or a time
  before wraparound; its exact dyadic identities have the boundary conditions
  stated in the accompanying proof/checks.

Sources: [Borriello & Walker](https://arxiv.org/abs/1609.07554),
[Alfaro & Sanjuan](https://arxiv.org/abs/2407.06175).
