# Rule54 J5 local source-bit inverse census (frozen locally before execution)

**Provenance:** Same-author follow-up to Edition 11, October 8, 2026. The complete protocol was frozen locally before running experiments (SHA-256 `84a477590830b392f4d21f8beb137f846354e5c6124b74847f49806e6c2b1243`). This abbreviated repository copy is committed after the local run and is not independent timestamp evidence.

Question: Is symbol-1's radius-one inverse representative of the other 16 jet-visible globally certifying symbols? How do they compare with the 11 symbols occurring in exceptional ambiguous source pairs?

Lock: ECA54 with A0=S XOR HS, A{k+1}=A{k}(HS) XOR H(A{k}(S)), J5=(A1..A5). Exhaustively test all 8192 length-13 source windows (radius zero), all 32768 length-15 windows (radius one), and, **only if a member of the 17 certifying symbol set remains locally undecodable at radius one**, all 131072 length-17 windows for that symbol (radius two). Report the 28-symbol census, opposite-source center-bit conflicts, and complete negative results; stop at radius two. Crosscheck control symbol 1: 352 central 13-bit windows, 36,864 ordered opposite-bit pairs at R0, 1408 15-bit windows, 20 observed triples, zero R1 conflicts. Independent ring controls; no additional rule, lift, class census, CI, or general compression claim.

The global uniqueness marker classification from Edition 11 remains conditional on external review of the 4316v/8460e equal-jet pair SCC certificate. Finite-window conditional local-bit decoders are separate exact brute-force statements. The complete locally frozen protocol and hash must accompany the bounded experiment artifact.
