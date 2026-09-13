# Closed violating walks decide all-ring depth three; the finite/full-shift gap survives every periodic ring under six observations

**Research note, 2026-09-13.** Nineteenth unit of the [Invariants Across Representation Contracts](2026-09-10-representation-invariants-program.md) program. Protocol: [closed violating walks at depth three](protocols/closed-violation-depth-three-20260913.md). Gate 1 was approved by OpenAI GPT-5.6 Sol after two pre-evaluation correction rounds, the last at exact protocol head `3cfac143a24ae7a998d3823b9fc8bbeba0179f13`; the implementation-only correction landed before evaluation at exact gathering head `320d3ae7dc9d6c761c1fae307c0d32cf16fcca0a`. Myk ran the canonical source-domain evaluation locally from that pinned head, outside GitHub Actions under the 2026-09-12 CI-cost boundary. The component timings printed to stdout sum to about 53 minutes. The canonical output is [`results/closed_violation_depth_three_20260913.json`](../../results/closed_violation_depth_three_20260913.json), local SHA-256 `e2c961a9111d9094505beec84b5efcbef2a091eda045f4b0cb580b0d71d85a6e`; evaluation-only PR #223 merged it into the gathering lineage as `bc9131d07c3c3803c698bab9b904160dd8b2b4d7`, with the fast result-integrity registration and no automatic full replay. **A full second execution for the frozen byte-for-byte determinism check is still required before Gate 2 can close.**

## The question

The eighteenth unit found, post hoc at depth two, that the all-ring set was exactly the rules whose violating three-edge walks never close inside a strong component. The nineteenth unit first proved that this is not a depth-two accident. For every depth `h` and observation `ψ`, if a violating walk ends at `(v_0,v_3)` inside one strong component, the component supplies a positive return walk `v_3 ↝ v_0`; the ring criterion then realizes a violation at some finite ring `n=m+3`. Together with the earlier pruning direction,

`D^h_ψ^∞ = { r : V^h_cl = ∅ }`.

At depth three the pair graph has 65,536 vertices, so this theorem replaces the matrix-power certificate the eighteenth unit declared impractical. Strong components decide the all-ring set; breadth-first return distance gives each deep rule's first failing ring `n_min`; component periods and cyclic classes give the eventual membership residues and period. The onset beyond which the eventual pattern holds is **not** computed.

The main scientific question is then exact rather than sampled: after taking the intersection over **every finite periodic ring**, which rules still look depth-three-predictable although they fail depth three on the full shift?

## Answer

### Q1 — theorem and predecessor controls: held

Every frozen control passed. At depths one and two, the closed-violation criterion reproduces the certified all-ring sets exactly under all eight observations; the recorded depth-two closed-violation counts agree; every least failing ring is reproduced, including the hard control that the twelve observation-22 rules which first fail at ring 24 have `m_min = 21`; and the certified depth-two periods `1, 2, 2, 1, 12, 1, 4, 6` are recovered. At depth three, every frozen `FS³` control sample has no closed violation. This is the unit's implementation/theorem stop condition and it passed.

### Q2 — the all-ring depth-three gap: the main existence bet held; one location bet failed

The all-ring/full-shift gap `Γ³_{ψ,∞} = D³_ψ^∞ \\ FS³_ψ` is nonempty under exactly the six live observations predicted:

- `232`: 8 rules — `58, 78, 92, 114, 141, 163, 177, 197`;
- `4`: 10 rules — `9, 25, 41, 45, 65, 67, 79, 93, 97, 101`;
- `32`: 10 rules — `13, 61, 69, 75, 89, 103, 107, 111, 121, 125`;
- `200`: 6 rules — `135, 137, 149, 157, 193, 199`;
- `22`: 8 rules — `140, 141, 162, 163, 176, 177, 196, 197`;
- `90`: 4 rules — `41, 97, 107, 121`;
- `150`: empty; `102` is empty by the inherited full-shift theorem.

So the collection of **all finite periodic-ring tests together** still fails to decide the full-shift depth-three property for those six observations. This is stronger than the earlier rings-3-to-14 result and does not mean membership on an individual ring is undecidable: every finite ring has an ordinary exact answer.

The secondary window bet was only partly right. The rings-3-to-14 window does overstate the all-ring gap somewhere, but **not under observation 22**, so frozen Q2(c) fails. The surprise occurs under observation 200: rules `41, 97, 169, 225, 233` pass through ring 14 and first fail at **ring 16**. Their conjugates `104, 106, 107, 120, 121` do the same under observation 236. Under 22, by contrast, the eight-rule rings-3-to-14 gap was already the exact all-ring gap at depth three.

### Q3 — first failing rings: held

The first-failing-ring construction agrees with every recorded ring 4–14 control. Among source observations, the largest first failing rings are:

`232: 13`, `4: 13`, `32: 13`, `200: 16`, `22: 13`, `90: 10`, `150: 9`.

No depth-three rule in the computed domain first fails later than the depth-two record of ring 24. The ring-16 failures under 200 are the only source-observation cases that escape the earlier 3–14 window.

### Q4 — eventual periods: theorem controls held; most numerical bets failed

The exact depth-three eventual periods are

`P³_232 = 1`, `P³_4 = 2`, `P³_32 = 2`, `P³_200 = 1`, `P³_22 = 1`, `P³_90 = 2`, `P³_150 = 6`.

Thus the bets `P³_232=P³_200=1` and `P³_150=6` held. The bets `P³_4=P³_32=1`, `3 | P³_22`, and `P³_90=4` failed. In particular, the arithmetic dependence can simplify when one more level of observed history is retained: observation 22 falls from depth-two period 12 to depth-three period 1, and observation 90 from 4 to 2. No monotonicity of period with refinement depth is supported. The frozen kernel theorem controls for 90 and 150 had zero exceptions. The artifact serializes the **full** eventual sets over all 256 rules, with the deep-domain projection kept separately, as required by the pre-evaluation I2 correction.

### Q5 — closed-violation structure: theorem held; the diagonal-anchor bet failed

The corrected theorem control held: no eventually oscillating rule has a closed violation in a component containing a constant-diagonal self-loop. General diagonal anchoring was reported only, not forbidden.

The preregistered structural bet — every eventually-out rule under 232, 200 and 22 is generally diagonal-anchored — fails under 232 and 200 and holds under 22. The eventually-out rules without any diagonal anchor are:

- under `232`: `94, 133`;
- under `200`: `33, 41, 97, 161, 169, 225, 233`;
- under `22`: none.

A post-hoc coincidence worth preserving but **not promoting to a result**: all five observation-200 rules whose rings-3-to-14 membership was a false all-ring positive (`41, 97, 169, 225, 233`) lie inside that seven-rule off-diagonal set. Rules 33 and 161 show the converse is false. A separately frozen future unit could ask whether absence of a diagonal anchor predicts longer minimum return cycles or later first failing rings.

### Q6 — complement and reflection transport: held exactly

The corrected pre-evaluation reflection theorem is borne out. Complement conjugation and reflection transport `|V³_cl|`, `n_min`, rule period, residue set, component sizes/periods and anchoring with no mismatches on the computed domain. Under reflection the return-length residue set is **equal**, not negated: graph transposition and the violating-endpoint swap cancel. The explicit frozen graph-correspondence samples all pass, the all-ring sets/gaps/periods transport under complement, and `D³_32^∞` computed directly equals the transported `D³_4^∞`.

## Reading for the program

The eighteenth unit's post-hoc identity has become a theorem at every refinement depth: finite-ring failure is equivalent to the existence of a violating walk whose erased distinction can **close back on itself** in the pair graph. That gives the program a finite structural divider between two kinds of full-shift obstruction. Some full-shift violations have closed representatives and therefore appear on some finite periodic ring; others are bi-infinitely realizable without any periodic closure and remain invisible to **every** finite ring.

Depth three shows that the second kind is not rare in this finite census: six of the eight source observations retain a nonempty all-ring/full-shift gap. The periodic approximation is therefore not merely too small when it disagrees with the full shift; for these rules, increasing the ring size forever does not repair the representation.

The failures also weaken two tempting structural simplifications. Ring-size arithmetic is not monotone with refinement depth — periods can collapse — and general diagonal anchoring is not necessary for eventual finite-ring failure. The graph's strong-component return structure is the exact object; simple summaries of that structure may or may not explain the remaining variation.

## Limits

This unit does **not** give a full depth-three ring certificate. It decides the all-ring intersection, every deep rule's least failing ring, and the eventual residue pattern, but it does not compute the onset beyond which that pattern is valid; individual rings between the recorded window and the unknown onset are not all enumerated. It does not compute full-shift depth four, and it reads `FS³` from the sixteenth/seventeenth units with hashes rather than recomputing it. Nothing is claimed for observations outside the frozen family and its conjugates/mirrors, or for rings 1–3 under the strong-component criterion.

The all-ring/full-shift gap is a property of this declared observation/refinement contract, not intrinsic dimension, universality, Class IV, physical spacetime, self-assembly, endogenous control, consciousness, metaphysics, or any prime/`8n+1` claim. The post-hoc observation about off-diagonal ring-16 witnesses under 200 is a candidate for a future protocol only.

## Review state

Protocol-before-evaluation ordering is preserved. Gate 1 preceded implementation; I1/I2 were corrected before any canonical result existed; implementation and evaluation returned through separate sub-PRs; the canonical run was off GitHub Actions from the pinned reviewed head; automatic checks are bounded and the expensive replay remains manual-only. Evaluation PR #223 is integrated into gathering PR #218. **The frozen full second execution for byte-identical determinism is still pending. Gate 2 and reviewer merge of #218 must wait for it.**
