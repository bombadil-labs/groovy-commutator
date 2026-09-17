# A frozen persistence × spreading statistic selects the 54/110 core phenotype

`S = max(0, R_7) · max(0, M_8)` (same-window selective retention at block
width 7 times held-out eight-step history gain) with the rule `select iff
S > 0.20 and α_512 > 0.50` (α the doubling exponent of single-bit disturbance
support from t = 256 to 512) was frozen before fresh simulation and, across
five fresh width/density conditions, selects 54 and 110 in 10/10 decisions,
no undisputed Class I–III representative in 420, neither disputed 41 nor 106,
and neither a radius-two rare-correction adversary nor a pure shift. Margins:
minimum positive `S` 0.205, minimum positive `α` 0.683; every fast-spreading
negative has `S = 0`; the strongest-spreading high-`S` negative is rule 62 at
α = 0.499.

Status: exploratory. The result is prospective and finite (two positive
families, dependent conditions), and its protocol, runner and canonical JSON
bytes were lost with the GPT session; the report and complete tables survive
and a reconstruction is recorded with explicit non-claims. Prior art covers
the two-axis idea (Langton; Wuensche; Feldman, McTague and Crutchfield;
Borriello and Walker; Mediano et al.; Mirza 2026). Not a Wolfram-class
classifier.

Source: [recovered discriminator record](../research/2026-09-17-selective-persistence-discriminator-record.md).
