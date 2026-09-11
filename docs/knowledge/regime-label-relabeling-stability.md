# Regime labels are more stable under relabeling than the statistics behind them

The full sweep classified 32,640 rule pairs from five fixed random seeds. Mapping each pair to its image under reflection or complement conjugation, and comparing the saved labels, gives 95.13% agreement under reflection and 93.94% under complement conjugation, with commute pairs agreeing exactly under both. The raw `final` and `peak` disagreement values agree exactly only 27–28% and 17–22% of the time, because the seeds were not transformed. All label disagreements lie on the drain/structured, drain/noisy, and crystalline/drain boundaries already identified as soft.

This is an exact computation over a sampled result, not an invariance. It bounds how much of the five-regime picture is convention and how much is the pair of maps. See the [audit note](../research/2026-09-11-representation-invariants-audit.md).
