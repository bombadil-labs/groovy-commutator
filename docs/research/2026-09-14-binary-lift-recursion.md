# Every ECA has a faithful binary path through 3D; recursive G remains incomplete

Status: retrospective exhaustive selected-path computation; independent Gate 2 review pending. Recipe selection and retained alternatives are reported separately.

Authored by: Codex (OpenAI), dimensional-lift local working session, 2026-09-14. Reviewed by: none.

## Question and answer

Does the [four-reference family](2026-09-14-binary-lift-family.md) repeat once while preserving native evolution and local source/parent recovery for every ECA? **All 256 selected paths pass.** Of the 220 selected paths with a first-floor G carrier, 200 preserve their selected recursive-G diagnostic. Earlier alternatives raise best-known 3D G coverage to 206 source rules.

Myk approved the Gate 1 exception. Evaluation preceded independent review; the [retrospective record](protocols/binary-lift-retrospective-record-20260914.md) preserves the adaptive history and deviations.

## Repeating the recipe

Let X be a prepared parent configuration, E(X) its compatible native evolution, and ΔX=X XOR E(X). Keep the first-floor mask, row order, sign s, reference offsets a,b and Boolean reference function q.

Let v move horizontally by s and across the newest existing transverse axis by +1. Define

\[
P(X)=X\oplus\tau_vX,\qquad D(X)=\Delta X,\qquad
M(X)=m(X,\Delta X),\qquad
Q(X)=q\!\left(\tau_{asv}X,\tau_{bsv}X\right).
\]

The Q shifts therefore move horizontally by a or b and transversely by as or bs. Repeat these four fields along the newly added axis in the same order. This is a repeat on the prepared parent family; the input X is not an arbitrary independently specified 2D configuration.

The child native derivative must update every field autonomously from its 5×5×5 binary neighborhood. Source recovery and parent recovery are separate local consistency gates. First-order targets on prepared states come from the source evolution and do not depend on an arbitrary off-image parent completion.

## Selection and exact domain

Select one recipe per source rule using only first-floor data: prioritize original G, then centered G, and apply the recorded deterministic layout/reference/mask tie-breaks. Choose one member of each reflection pair and reflect its partner's entire recipe. Self-reflecting rules use a signed orientation convention.

The census accounts for all 256 paths, reusing 53 identical prior cases and computing 203 new cases. The dependency windows have width 13 with the origin chosen for the left/right reference placement. Every one of their 8,192 binary assignments is tested. The packed 80-bit key contains every distinct bit of the full 125-bit neighborhood on the period-four prepared family; the independent verifier uses the full physical neighborhood.

| Selected-path gate | Passing source rules |
|---|---:|
| Uniform native evolution | **256/256** |
| Local source recovery | **256/256** |
| Local parent recovery | **256/256** |
| Selected recursive-G diagnostic | **200/220 eligible** |
| Original-G selected paths | 115 |
| Additional centered-G selected paths | 85 |

The other 36 rules have no first-floor G carrier in this family. They are not counted as newly failing a 3D G test.

## Completion freedom and physical G

The parent rule's M/Q commutator values are not prescribed by the first-floor carrier. The recursive solver retains the relevant unforced parent outputs as GF(2) variables. It tests compatibility with the child's native/probe constraints and every admissible centered all-zero choice. It does not fix missing parent outputs to zero and then attribute a resulting failure to the lift.

For successful paths of Rules 157 and 199, the solution imposes a rank-one relation on previously free parent outputs. Their success is therefore conditional on compatible parent completion. This corrects the earlier observation that successful extensions appeared to leave every parent completion free.

The physical G guarantee is on nested P/D layers. It is not an all-channel covariance theorem, and it is not the equation G_up L = L G for the full nonlinear L.

## Selected outcomes versus best-known alternatives

The selected G failures are 6, 14, 20, 74, 78, 84, 88, 92, 110, 124, 134, 142, 148, 173, 202, 206, 212, 216, 220 and 229. Previous successful alternatives for 14, 84, 110, 124, 206 and 220 remain valid. Keeping them gives **206 best-known 3D G paths: 121 original-G plus 85 additional centered-G paths**.

Thus 14 eligible source rules still have no saved successful 3D G path: 6, 20, 74, 78, 88, 92, 134, 142, 148, 173, 202, 212, 216 and 229. A failed selected recipe does not prove that every recipe for that ECA fails.

## Historical 4D boundary

An earlier fixed selection tested 113 paths in 4D. All passed native evolution and both recovery gates; 105 passed recursive G (75 original and 30 centered). Rules 14, 84, 110, 124, 140, 193, 206 and 220 failed G on those fixed paths. Rule 110 therefore has a known G-preserving 3D path but its tested 4D continuation fails.

This historical 4D population differs from the later all-256 3D selection. It supplies no 4D result for the other 143 rules and no dimension-induction theorem. Its records and targeted checks are included as a clearly separated baseline.

## Verification, costs and next question

The primary new census took 26.19 seconds. Targeted independent author implementations covered 64 eligible rules, all 36 no-carrier native/recovery cases, 300 first-order gate decisions, 106 GF(2) branch decisions and 5,636,096 direct physical-G cell outputs, including the two parent-completion supplements. The total recorded verification time is 34.03 seconds. The 53 cached paths retain their earlier checks. Original records and cumulative reporting are preserved rather than presented as an independent-agent replay.

The alphabet stays binary and native radius stays two on every axis. Two period-four transverse axes carry 16 prepared fields per source site. This is faithful evolution through two lifts of a 1D source, not arbitrary independent higher-dimensional information. Exact one-step intertwining extends through time at each verified floor; induction over dimension remains open.

The [canonical account](../../results/binary_lift_20260914.json), [per-rule table](../../results/binary_lift_20260914/rule_coverage.csv) and [replay bundle](../../experiments/binary_lift_20260914/README.md) expose each distinction. The next useful condition for induction is derivative-neighborhood sufficiency plus compatibility with native evolution. The [collision diagnosis](2026-09-14-binary-lift-g-obstructions.md) tests that condition at the first floor before another dimensional extension.
