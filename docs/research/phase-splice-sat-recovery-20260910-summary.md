# Phase-splice SAT recovery — compact report

## Recovery outcome

- Recovery backend: **Minisat22 / manual fine-ECA CNF**
- Previously censored sentinel seeds: **12**
- Status counts: `{'no-phase-splice-through-6': 12}`
- Exact negative recoveries: **12**
- Certificates: **0**
- Remaining censored seeds: **0**
- Same per-seed wall as primary MDD census: **1200 seconds**
- Backend recovery hypothesis: **pass**
- Overall phase-splice completion: **complete-exact-negative-22-of-22**

## CNF cost

- Maximum variables in one exact position query: **1314**
- Maximum clauses in one exact position query: **9943**

## Provenance

- Full recovery audit: `results/phase_splice_sat_recovery_20260910.json`
- Full recovery SHA-256: `0540fc2a4bf3801e7cd5f8dad9514022c120bda773d2591fcc78d6a17d0aa90f`
- The original 10 Class-II seed languages remain exact negatives from the frozen MDD primary census; this recovery changes only the backend for the 12 previously censored Rule-122/161 sentinels.
