# Sequential binary lift pilot through 6D

Status: frozen protocol; Myk explicitly overrode Gate 1 before implementation/evaluation.
Authored by: Codex (OpenAI), Myk's dimensional-lift working session, 2026-09-14.
Reviewed by: none.
Protocol review: none at freeze; run authorized by Myk 2026-09-14.
Authorization: in this session, Myk said: "Don't worry about gate 1, I am overriding that requirement and granting approval." This overrides the prospective Gate 1 requirement; independent Gate 2 remains required before merge.

## Question and scope

Myk requests a quick 5D/6D test of the recipes retained in PR #233, under the clarified requirement that a lift's output support faithful recovery and autonomous native evolution before it is lifted again. This pilot tests sequential construction on a declared small invariant input family. It does not test all infinite-source configurations, all 256 rules, arbitrary independent higher-dimensional inputs, or full recursive commutator preservation.

Scientific baseline: PR #233, merge commit 8c3f4081c03cc73a960287494c143f5674aea7df. In particular, the four-field selection in results/binary_lift_20260914/rule_coverage.csv and the common final-eight construction in docs/research/2026-09-14-binary-lift-complements.md.

## Frozen population

All 128 binary states of a longitudinal ring of width 7, with every spatial position and every transverse phase included. These finite tori are the explicit test domain, not cropped approximations to infinite inputs. Exhausting this source set makes it closed under every ECA used below. No random samples, training/holdout inference, or claim of full-shift validity.

Six paths, lifted from 1D through 6D in the order 90, 54, 110, 157, 171, 233:

| Source rule | Fields in order | Mask | P sign | Q |
|---|---|---|---|---|
| 90, 54, 110 | P,D,M,Q | birth | +1 | X(i-1) AND X(i+2) |
| 157 | P,D,M,Q | stay-one | +1 | X(i-1) AND X(i+2) |
| 171, 233 | P,D,A2,M,Q | birth | +1 | NOT X(i-1) AND X(i+2) |

All four-field recipes are the saved all-256 faithful selection. The five-field recipe is the published shared complemented-T2 repair. The primary gates below concern faithfulness, not whether these fixed completions preserve G. Rule 110 is not predicted to fail native/recovery merely because a historical recipe failed G.

## Construction

Each current object contains (a) a fully specified binary native rule, (b) the full finite admissible configuration family for this pilot, and (c) its immutable recipe policy. The initial recipe is selected deterministically by the table above. Retaining that policy is explicit metadata; this does not claim a generator for bare arbitrary unannotated CA truth tables.

For current configuration X, compute Y=H(X), Z=H(Y) using the current native law. Put D=X XOR Y, P=X XOR shifted(X), M=(NOT X) AND D for birth or X AND (NOT D) for stay-one, A2=1 XOR X XOR Z, and Q as specified above. At the first lift the shifts are horizontal. Thereafter the vector crosses horizontally by +1 and across the newest existing transverse axis by +1. Reference offsets -1 and +2 multiply this whole vector. Stack the four or five fields along the new transverse axis, periodically.

Compile one phase-free radius-two native derivative h from all encoded states and their encoded successors, using every full physical 5-by-...-by-5 neighborhood. Equal neighborhood values must have identical demanded flips, pooled across source states, positions, and all phase combinations. Complete every unforced derivative output with zero. Compile an immediate-parent bit decoder from the same native neighborhoods; all unforced decoder outputs default to zero. Decoder targets are pooled across all phases, without row labels.

The child rule is H_child(X)=X XOR h(neighborhood(X)). Once compiled it is immutable. Subsequent levels compute parent evolution through this law, not via the original ECA or an oracle for source trajectories. Parent tables are never re-solved. Unforced zero outputs are a declared pilot completion, not a claim that the archived sparse operators had that completion.

The result is a pure deterministic construction on the finite decorated objects just defined. Data-dependent rule tables are synthesized from the entire declared family; they are not fits asserted to generalize to unseen configurations.

## Gates and predictions

At every level d=2,...,6:
1. Native constraint consistency.
2. Local immediate-parent decoder consistency.
3. Native replay H_child(L(X))=L(H_parent(X)) for every domain X.
4. Decoder replay R_child(L(X))=X for every domain X.
5. Original source recovery by composing already validated immediate-parent decoders.

Immediate-parent decoder radius is two. Composed source recovery may have a larger effective radius; do not report it as radius two. One-step verification over the complete finite invariant family proves every time step on that family; execute two steps as a regression against successor indexing and table plumbing.

Prediction: every declared path passes all five gates through 6D. This is an unverified extrapolation from earlier native/recovery success, explicitly not a G prediction.

For failures save the first conflicting physical neighborhood, the two configurations/coordinates, and opposite target bits; reproduce it with a direct scalar/full-neighborhood implementation. Stop that path at its first failed floor, continue the remaining paths, and do not search for a repair. Budget exhaustion is censored, not failure.

## Exact neighborhood compression and independent checks

The native law observes only binary physical values. Period-four/five transverse repeats can be compressed exactly. An allowed optimization interns recursively ordered tuples of subpatches using equality-checked integer identifiers; no hash digest alone decides equality. Shared dictionary identifiers must have the same meaning across all compiled states and later native evaluation.

For each path and floor, a separately implemented direct binary neighborhood extractor checks the central position for source state indices 0,1,42,85,127 and transverse coordinate tuples all-zero, all-one, and all-(period-1). Compare complete direct neighborhood patterns with their compressed representations. Independently compute reference encoding using the original ECA only in the verifier, and compare the complete encoded states and two native time steps. The production lift must never call that reference.

Controls before the canonical run: compare compressed key equivalence against explicit full 5^d-bit keys on a finite synthetic binary 3D tensor; include patches deliberately equal and deliberately different; confirm a known conflicting forced-output pair is rejected; confirm unset native derivative outputs evaluate to zero. No scientific outcomes were inspected before the recorded user authorization.

## Budget and records

Run outside GitHub Actions. One process, checkpoint after each completed floor, cooperative timing checks, 120-second per-floor budget and 15-minute total budget; 4 GiB resident-memory soft ceiling. A single numerical kernel may finish after its deadline, but start no additional floor after the cap. Record measured wall times, peak RSS, phase counts, state counts, physical neighborhood size, unique keys, key-compression statistics, gates, and any witness/censoring. Timing and resource numbers are measurements, not bitwise-reproducible scientific fields.

Preserve the reviewed protocol commit, implementation commit before evaluation, exact code/input SHA-256s, raw result records and a concise findings note in a gathering PR. Cheap automatic checks only; no scientific replay in automatic CI. Acceptance of the whole unit remains a separate independent Gate 2.
