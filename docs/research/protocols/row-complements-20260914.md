# Row complements for the eight remaining first-floor G holdouts

Protocol review: none at freeze; run authorized by Myk 2026-09-14.

Authorization: Myk requests solving the remaining complement question before integrating the post-PR findings into PR #233: “Let's do that ... We are just missing some complement somewhere.” This is explicit local implementation/evaluation authority under the continuing exception. No independent review is claimed; evaluation precedes that review. Integrating into the existing gathering PR is also authorized; merge into main remains independently gated.

## Question and prediction

Can a state-independent complement on each prepared row separate native neighborhoods from the unchanged temporal-XOR probe and supply the missing original or centered carrier? The positive prediction is that some holdouts improve. Universal success is a hypothesis, not a scoring assumption.

Ranked questions: (1) does the row-complement family repair all eight; (2) do complements restricted to auxiliary T2/M/Q rows suffice; (3) what certified conflicts remain?

## Fixed domain

Source rules: 171, 187, 233, 235, 241, 243, 249, 251. All four masks, both P signs, all cyclic row orders with P fixed first. Families are P/D/T2/M (six orders) and P/D/T2/M/Q (four previous Q formulas, 24 orders). For p fields, test every polarity vector epsilon in {0,1}^p. All 16 four-row and all 32 five-row vectors, including the prior all-zero control, are accounted for: 6,144 four-row and 196,608 five-row recipes, total 202,752. Do not carry over old admission failures after changing the encoding.

Define L_epsilon(S)_{i,j}=L(S)_{i,j} XOR epsilon_{field(j)}. The native derivative remains L(S) XOR L(ES). The probe U_epsilon=L_epsilon(S) XOR L_epsilon(ES)=L(S) XOR L(ES) is unchanged. On the exact P and D fields, the prescribed carrier is unchanged: P_s(G) and G. Thus h(U)=L(S) XOR L(E²S) XOR c(G) remains the original-G demand. Centered source and native-zero corrections are unchanged, with both shared h(0) branches. Complementing a P or D encoding row does not complement a carrier output or change the source commutator.

## Exact gates and dependency bounds

Keep native evolution, source recovery (also parent recovery at this floor), original G, centered-zero=0, and centered-zero=1 separate. Native tables and decoders see full 5x5 binary keys with no row labels. Unspecified keys remain free. Source derivative table is r XOR 204; integration is XOR. T2=S XOR E²S, not D(D(S)).

Enumerate the same complete source interval [-5,+5]. Native patches depend only on [-4,+4], and their required flip and source output use no outer bit; one representative per 2^9 native window is sufficient. Probe patches require all 2^11 source assignments. Deduplicate identical constraints only after retaining a concrete witness payload. Native-key polarity masks must depend on center row phase; probe keys and demands must remain independent of epsilon.

Reuse previous zero-polarity records as exact controls. Check all 6,528 zero-polarity gate vectors against the prior DT2 records. Verify new failures via independent cropped-source certificate reconstruction, and directly evaluate native next steps and physical G for successful selections spanning every rule/mode and polarity/geometry used. If a representative packing risk appears, resolve it rather than repeating unchanged full censuses.

## Budget and interpretation

Use sparse exact keys, a cycle lease, bounded workers and whole-rule checkpoints. Target approximately two minutes total compute; checkpoint any unfinished declared domain. Costs stay one bit per cell, period four/five, native radius two and source preparation radius two. The polarity bits are fixed recipe parameters, not per-cell side-channel inputs or an independent data field.

Report full-domain family counts and best-known cumulative first-floor counts separately. The auxiliary-only subset has epsilon_P=epsilon_D=0 and is reported separately. Prior 3D/4D guarantees do not change. No recursion, additional temporal depth, relaxed carrier, radius expansion, off-beam trajectory completion, or further candidate family is authorized by this protocol.

After the run, retire unchanged exact failures, reassess the complement hypothesis, and preserve positive recipes plus negative certificates. The report must distinguish new empirical results, elementary identities, and conjectured general mechanisms.
