# Bounded adaptive source-recoder synthesis — compact report

## Final checkpoint outcome

- Outcome: **terminal-inconclusive-due-to-censoring**
- Machine class: deterministic adaptive rail selector with at most **4 proof states**
- Search horizon: `t<=6`
- Seed languages: **22**; target questions: **170**
- Seed statuses: `{'censored': 8, 'no-bounded-recoder-through-4': 14}`
- Exact permanence resolutions: **0**
- Exact bounded-negative questions: **30**
- Scientific-censored questions: **140**
- Infrastructure-censored questions: **0**
- First canonical certificate: `None`
- Completed-state distribution: `{'0': 3, '1': 1, '2': 3, '3': 1, '4': 14}`

## Interpretation

This is the final new source-recoder family in the current Dynamics of Erased Distinctions program. Exact negatives apply only to the frozen `m<=4`, adaptive rail-selection class through `t<=6`. Censoring remains representational/computational evidence only. Regardless of outcome, the next step is the program-level synthesis and terminus note, not a larger selector family.

## Controls

- Rule 5 positive synthesis control: **pass**
- Rule 35 bounded negative synthesis control: **pass**

## Provenance

- Full durable audit: `results/bounded_source_recoder_synthesis_20260910.json`
- Full SHA-256: `2d28a4d5e4b668f9a201f3658a986060712a2f9069577810aacd08a49e7f12f2`
- Frozen protocol: `docs/research/protocols/bounded-source-recoder-synthesis-20260910.md`
