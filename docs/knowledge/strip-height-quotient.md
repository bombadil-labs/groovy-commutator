# Height-one strips quotient the Life-like rule space; height two is injective

A binary outer-totalistic Life-like rule on a periodic strip of height `k` is
exactly a radius-one 1D CA over the `2^k` column symbols. At `k = 1` only the
six local conditions B0, B3, B6, S2, S5, S8 are reachable, so the induced ECA
is `r = B0 + 18 B3 + 32 B6 + 4 S2 + 72 S5 + 128 S8`: a 12-bit-forgetting
quotient from the 262,144 Life-like rules onto exactly the 64 reflection-
symmetric ECAs, each with a 4096-rule fiber (HighLife → 54; Life and B35/S236
→ 22; Day & Night → 178). At `k = 2` all eighteen conditions are reachable, so
the restriction is injective on rule identity. Exact by exhaustive
enumeration (GPT-5.6 Sol, 2026-09-17; Fable replayed the result file
byte-identically). Rule 110 is not reflection-symmetric and has an empty
fiber. The statement is about local-rule identity, not about dynamics on the
plane.

Source: [strip spectrum](../research/2026-09-17-strip-spectrum.md), [cross-dimensional panel](../research/2026-09-17-cross-dimensional-class4.md).
