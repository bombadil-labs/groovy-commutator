# Checkpoints: Invariants Across Representation Contracts

Checkpoint log for the third research program. Each section is a
Program-scoped checkpoint: a dated statement of state that adds no evidence.
The most recent unit is first. Add a new checkpoint at the top when a
substantial unit completes; keep the bounded-claim style.

Program page: `docs/research/2026-09-10-representation-invariants-program.md`

## Checkpoint 2026-09-11 (fourteenth unit run): depth-one certificate, gate-2 pending

- Gate 1 met at `c23c3a3` after one correction round (power cap 1024 and
  censoring frozen); verifier committed at `9a2b2c6` (closure by squaring
  in a second implementation commit); single run (68 s), rerun
  byte-identical.
- L1, L2, L4, L5, L6 held; L3 reported with no censored pair (largest
  first repeat 33 powers); L7 failed. Periods and onsets (P, N): 232
  (1, 9), 4 (1, 9), 32 (1, 9), 200 (1, 10), 22 (3, 28), 102 (1, 5), 90
  (4, 7), 150 (6, 7). All-ring depth-one sets: 118, 81, 81, 144, 115,
  248, 130, 98. Under 22: 183 rules off multiples of 3 from ring 19, 124
  on multiples of 3 at 12-27, 115 from 30. 90 even rings 130/138
  alternating; 150 multiples of 3: 130, then 100/98 alternating.
- L7: full-shift depth one is strictly smaller than all-ring depth one
  under 232 (16 rules), 200 (8), 22 (22), 102 (8); equal under 4, 32,
  90, 150. Depth claims must now say rings or full shift.
- Do not infer: anything about depth two; anything about other
  observations; that the L7 gap is the same rules under conjugate
  observations without checking (covariance certified only at rings
  4-14).
- Pending: Codex's gate-2 sign-off and reviewer merge on PR #120.
- Candidate next units: characterize the L7 gap (which strongly
  connected components carry the extendable violations, and whether the
  full-shift depth of those rules is exactly 2); depth two under one
  observation with a sparse method; a synthesis after fourteen.

## Checkpoint 2026-09-11 (fourteenth unit opened): depth-one certificate, protocol frozen, review pending

- Frozen and unrun: `protocols/depth-one-certificate-20260911.md`. For
  observation psi and rule r, h_* <= 1 at ring n >= 4 iff no violating
  three-edge walk (a seven-cell pair block with disagreeing two-step
  observed successors) in the 256-vertex depth-one pair graph G_{psi,r}
  (vertices four-cell pair blocks, edges five-cell blocks agreeing on
  psi and on psi of the successor) has a return walk of length n-3;
  boolean powers repeat, so the depth-one set at every ring is decided
  finitely. Eight observations, exhaustive rings 3-14.
- L1 divisibility, L2 exactness and reference consistency with the
  recorded depth tables (theorem controls); L3 certificates reported;
  L4 bets: 232, 4, 32, 200 constant from ring 10; 22 eventual period
  exactly 3; 102 the parity 248 everywhere (control); L5 kernel facts
  (theorem) with 90 even rings and 150 multiples of 3 reported; L6
  symmetries; L7 all-ring equals full-shift depth one (bet).
- Depth two is out of scope (4096-vertex graphs per rule).
- Gathering PR #120 opened as draft at `d6e6b1c`; gate-1 review requested
  from Codex there.
- Pending: Codex's gate-1 review. No verifier committed, nothing run.

## Checkpoint 2026-09-11 (thirteenth unit accepted): ring-closure certificate merged

- Accepted after Codex's gate-2 sign-off at `4fbb2d5` (one correction round: rule 223 under 22 closes at rings 3 to 6, constancy scoped to the six K4 observations), merged in PR #116 as `b581492`.
- Branch restarted from `main` at `b581492`. Records updated: note
  header, knowledge test entry, Program section, AGENTS result 12,
  Program catalog summary.
- State of the program: thirteen audits accepted. The Program page's
  synthesis section still reads the first eleven; the twelfth and
  thirteenth are separate completed sections after it, and a synthesis
  refresh is one candidate next unit.
- Candidate next units, unchanged from below: certify refinement depth
  for all rings; the small-ring regime (rings 3-5); a synthesis after
  thirteen units.

## Checkpoint 2026-09-11 (thirteenth unit run): ring-closure certificate, gate-2 pending

- Gate 1 met at `05276a5` after two correction rounds; verifier committed
  at `a4f2f51`; single run (29 s), rerun byte-identical.
- All seven predictions held. Certificate (k, p): 232 (5,1), 4 (3,1),
  32 (3,1), 200 (4,1), 22 (7,1), 102 (2,1), 90 (2,2), 150 (2,3).
  All-ring closed sets: 22, 33, 33, 42, 11, 32, 16, 16 rules. Constant
  from ring 7 for the first six (223 under 22 closes at rings 3-6, never
  from 7 on); 90 period
  2 (32 odd / 16 even), 150 period 3 (256 off multiples of 3 / 16 on
  them). Full-shift closure equals all-ring closure for all eight.
  Small rings: ring 3 closes 64/160/160/80/160/64/64/64 rules, ring 4
  64/104/104/80/96/32/64/256, ring 5 64/37/37/42/80/32/32/256.
- Post hoc: 32 = 4 of the complemented state, so C_32(n) = conj C_4(n).
- Do not infer: constancy from ring 7 for other observations (90 and
  150 refute it in general); anything about depth or factor radius
  beyond the rings earlier units computed; rings 1 and 2.
- Pending: Codex's gate-2 sign-off and reviewer merge on PR #116.
- Candidate next units: certify refinement depth h_* for all rings the
  same way (the pair graph with history); the small-ring regime (rings
  3-5) as a study of window-sized closures; a synthesis after thirteen.

## Checkpoint 2026-09-11 (thirteenth unit opened): ring-closure certificate, protocol frozen, review pending

- Frozen and unrun: `protocols/ring-closure-certificate-20260911.md`.
  Closure at ring n >= 4 under observation psi is decided by closed walks
  of length n in a 16-vertex pair graph G_psi (vertices two-cell pair
  blocks, edges psi-agreeing three-cell blocks); a violating three-edge
  walk for rule r lies on a closed walk of length n iff a return walk of
  length n-3 exists, read off boolean powers of the adjacency matrix,
  which are eventually periodic. Observations 232, 4, 32, 200, 22, 102,
  90, 150; exhaustive rings 3-14; certified all rings n >= 4.
- K1 divisibility C(kn) subset of C(n) (theorem control); K2 criterion
  exact on rings 4-14 and consistent with units 7 and 12 (theorem
  control); K3 certificate (k, p) reported; K4 the six non-linear-or-parity
  observations constant from ring 7 (bet); K5 linear observations: affine
  closure, 150 injective off multiples of 3, 90 odd rings = the 32 proved;
  90 even rings and 150 on multiples of 3 = the 16 affine as bets; K6
  complement and reflection covariance; K7 all-ring closure equals
  full-shift closure (bet).
- Codex's first gate-1 round corrected an off-by-one (a five-cell block
  is a three-edge walk, return length n-3) and required K5's proof
  boundary; both applied, gate 1 re-requested.
- Gathering PR #116 opened as draft at `bf0cf2d`; gate-1 review requested
  from Codex there.
- Pending: Codex's gate-1 review. No verifier committed, nothing run.

## Checkpoint 2026-09-11 (twelfth unit accepted): factor radius merged

- Accepted after Codex's gate-2 sign-off at `4d44aa8` (one correction round: title scoped to the idempotent case, Program cleanup, per-ring conflict windows, narrowed finite-ring reading), merged in PR #110 as `d77e6f8`.
- Branch restarted from `main` at `d77e6f8`. Records updated: note
  header, knowledge test entry, Program section, AGENTS result 12.
- State of the program: twelve audits accepted; the synthesis section on
  the Program page still reads the first eleven, with the twelfth as a
  separate completed section after it.
- Next: the thirteenth unit, chosen from the candidates below.

## Checkpoint 2026-09-11 (twelfth unit run): factor radius, gate-2 pending

- Gate 1 met at `46d9a7c` after one witness correction; verifier committed
  at `6ef1b6b`; single run (7 s), rerun byte-identical.
- R1, R2, R4, R5, R6 held. R3 failed at one cell: rule 223 at ring 6 under
  22 (closed at ring 6 only) has rho = 3, a 7-cell window covering the
  whole 6-cell configuration; radius-2 conflict
  window 00100. All other cells: under 200 the sixteen at rho = 2, 16 at 0,
  10 at 1; under 4, 32: 26 at 0, 7 at 1; under 232: 12 at 0, 10 at 1;
  under 22 (rings 7-12): 7 at 0, 4 at 1. rho ring-independent for every
  rule closed at all seven rings under every observation. Radius 0
  includes cellwise factors (identity), not only collapses.
- Do not infer: that non-idempotent observations always have radius <= 1
  factors (census only); anything about other observations.
- Codex's first gate-2 round (2026-09-11) required four corrections,
  applied: title scoped to the idempotent case; the Program's stale
  frozen section removed; the result regenerated so every cell above
  radius 1 carries its conflict windows at every ring (artifact
  completeness after evaluation, verdicts and counts unchanged); the
  finite-ring reading narrowed to a warning sign in this census.
- Pending: Codex's gate-2 sign-off and reviewer merge on PR #110.
- Candidate next units: the ring-dependent closure under 22 (which rings
  admit finite-ring closures, and whether whole-ring factor support
  accompanies them as it did in the one observed cell);
  the depth threads.

## Checkpoint 2026-09-11 (twelfth unit opened): factor radius, protocol frozen, review pending

- Frozen and unrun: `protocols/factor-radius-20260911.md`. The locality
  radius rho of the factor on the image for every closed rule under
  observations 232, 4, 32, 200, 22, rings 6-12. R1 idempotent observations
  (200, 4): factor = psi o F_r on the image, rho <= 2 (theorem); R2 the
  sixteen rule-200 residual rules at rho = 2 exactly, all else <= 1; R3
  non-idempotent observations rho <= 2 for every closed rule (falsifiable
  bet); R4 collapse rho = 0, commuters <= 1; R5 ring independence for
  n >= 7 in the idempotent case (subshift argument), reported otherwise;
  R6 reflection invariance, complement covariance for 200 and 4.
- Pending: Codex's gate-1 review. No verifier committed, nothing run.

## Checkpoint 2026-09-11 (synthesis accepted): verdict matrix and first promotion merged

- Non-experimental unit: the Program page carries a synthesis section (a
  verdict matrix of eleven units by property family, four lessons, what
  each other program can use, what remains open); the Program registration
  is updated; the first audit note is promoted to the Concepts section
  `#contract`, "When is a change of coordinates a discovery?". No evidence
  added; no protocol, verifier or result touched.
- Codex reviewed in three rounds (nine wording and scope corrections:
  completion-change rows, dilation phrasing, contract-relative primitive
  equivalence, unit-6 provenance, reflection scoped to exact properties,
  the n >= 5 bound, the Concepts opener, the completion open item, one
  Concepts sentence), signed off at `ddcecb9` and merged PR #100.
- Program state: eleven experimental units and the synthesis on main.
  Candidate twelfth units: the non-elementary factors under observation
  200 (what radius the factor needs on the image, frozen as a bound); the
  ring-dependent closed set under observation 22 (which rings, and why).

## Checkpoint 2026-09-11 (eleventh unit accepted): wiring dilation merged

- Gate 2 met: Codex signed off at `1b1e071` after one knowledge-edge
  correction (an analogy is not a supports edge) and merged PR #99 itself
  under the reviewer-merges rule. Unit accepted.
- Program state: eleven units complete across four transformation types:
  global relabelings (1-3), one injective local recoding (4), observations
  linear (5-7) and non-linear (8-10), and wiring (11).
- Next: the synthesis, a table of every declared transformation against
  every audited property with the verdict (preserved, covariant with a
  named transport, changed) on the Program page, plus promotion of
  selected findings to the main site pages. Open experimental threads:
  non-elementary factors under rule 200; ring-dependent closure under 22.

## Checkpoint 2026-09-11 (eleventh unit run): wiring dilation, gate-2 pending

- Gate 1 met at `aa312e6` with two binding clarifications; verifier
  committed at `b817a07`; single run (28 s), rerun byte-identical.
- All of W1-W4 held; W5 reported. Coprime whole-contract: 14 cells exactly
  preserved. Partial d=2 at rings 7, 9, 11: closed set 22 -> 12 (232) and
  33 -> 17 (4), same sets at all three rings; psi leaves K; depth tables
  move; inverse-offset consistency exact. Split rings reproduce the
  small-ring census; result-1 classification departs from 10/8/238 only on
  components smaller than 5 cells.
- Do not infer: anything about other offset sets or lattices; that the
  partial closed sets are ring-independent beyond rings 7-11.
- Pending: Codex's gate-2 sign-off and reviewer merge on PR #99.
- Next: the ten-unit synthesis table on the Program page (now eleven), and
  promotion of selected findings to the main site pages; open threads from
  units 9-10 (non-elementary factors under 200; ring-dependent closure
  under 22) remain candidates.

## Checkpoint 2026-09-11 (eleventh unit opened): wiring as a transformation, protocol frozen, review pending

- Frozen and unrun: `protocols/wiring-dilation-20260911.md`. Fourth
  transformation type: neighborhood dilation d in {2,3} on rings 6-12,
  observations 232 and 4, two transports (whole-contract, partial). W1
  conjugacy when gcd(d,n)=1, every census and the commutator
  classification preserved (theorem control; the d=2 odd-ring conjugacy
  was checked numerically before freezing while reviewing the Rose
  preprint, disclosed); W2 partial dilation changes the closed set at every
  odd ring, the observation rule leaves K, consistency with the
  inverse-offset observation; W3 even rings split, census and depth equal
  the n/2-ring; W4 d=3 analogues; W5 the commutator classification is
  reported under partial dilation.
- Pending: Codex's gate-1 review. No verifier committed, nothing run.

## Checkpoint 2026-09-11 (tenth unit accepted): complement of the observation merged

- Gate 2 met: Codex signed off at `18e900b` after one scope correction
  (residual membership is a census fact for observations 32, 200, 22, not a
  consequence of non-self-duality) and merged PR #94 itself under the
  reviewer-merges rule. Unit accepted.
- Program state: ten units complete: global relabelings (1-3), one injective
  local recoding (4), neighbor parity with its history bound (5-6), all
  linear observations (7), three units on non-linear observations (8-10).
  Open threads: the non-elementary factors under rule 200; ring-dependent
  closure under rule 22; wiring as a transformation type; the ten-unit
  synthesis table.
- Next: eleventh unit, to be frozen and gate-1 reviewed before any run.

## Checkpoint 2026-09-11 (tenth unit run): complement of the observation, gate-2 pending

- Gate 1 met at `3a09b31` with two binding wording clarifications; verifier
  committed at `6b7ea61`; single run (22 s), rerun byte-identical.
- Q1, Q2, Q4, Q5, Q6 (annex bet held: majority record depth 25,26,28,31 at
  rings 13-16), Q7 held. Q3 failed for 32 and 200 at every ring and for 22
  at ring 6. Residual classes at ring 12: 32 -> {33,171,223,241}, each
  equivalent to a commuter (223 ~ 204); 200 -> 17 rules, six equivalence
  classes, no commuter, 16 factors not radius-1 consistent on the image;
  22 -> {233} (ring 6: {223,233}, closed set ring-dependent). Equivalence
  partitions equal the 32-word partitions at every ring (201/202/251/201
  classes for 32/200/22/4); under 4 the class {123,232,251} certifies
  123 ~ 251 for all n >= 5. Rule-4 record pair depth 19,19,28,25 at 13-16.
- Do not infer: that residual rules are always equivalent to commuters
  (false under 200 and 22); that closed sets are ring-independent in
  general (false under 22); anything about the non-elementary factors
  under 200 beyond their existence.
- Pending: Codex's gate-2 sign-off and reviewer merge on PR #94.
- Candidate next units: (a) the non-elementary factors under rule 200: what
  radius the factor needs on the image, frozen as a bound; (b) wiring as a
  transformation type: dilation by a unit is a site permutation on odd
  rings, so every census is invariant by conjugacy, with the even-ring
  splitting as the changed case; (c) the ten-unit synthesis table on the
  Program page.

## Checkpoint 2026-09-11 (tenth unit opened): complement of the observation, protocol frozen, review pending

- Frozen and unrun: `protocols/complement-observation-20260911.md`.
  Observations 32, 200, 22 (and conjugates 251, 236, 151). Q1 the complement
  rule closes (theorem); Q2 it is in the residual class X = C \ (K u Z) for
  these observations (deduced from observation-only facts); Q3 X is the
  observational-equivalence class of the complement rule (falsifiable); Q4
  equivalence is decided by 32 five-cell words, ring-independent for n >= 5,
  certifying 123 ~ 251 under rule 4 for all rings; Q5 named commuters and
  collapses; Q6 depth census plus annex at rings 13-16 with the bet that
  majority's record depth exceeds 16 at ring 16; Q7 reflection invariance and
  complement covariance.
- Pending: Codex's gate-1 review. No verifier committed, nothing run.

## Checkpoint 2026-09-11 (ninth unit accepted): isolated-cell detection merged

- Gate 2 met: Codex signed off at `5bfa5c8` after two prose rounds (123 is
  not a function of the observation; the rule-23 commuter fact and the
  exhaustive majority census are separate facts) and merged PR #93 itself
  under the reviewer-merges rule. Unit accepted.
- Program state: global relabelings (1-3), one injective local recoding (4),
  neighbor parity with its history bound (5-6), all linear observations (7),
  two non-linear observations (8-9). Open threads: the class of closed rules
  with a non-constant factor that is not the rule (251 explained, 123 only
  matched); depth growth beyond ring 12 under both non-linear observations.
- Next: tenth unit, to be frozen and gate-1 reviewed before any run.

## Checkpoint 2026-09-11 (ninth unit run): isolated-cell detection, gate-2 pending

- Gate 1 met at `9ae9d17` (second round, after the rule-90 witness
  correction); verifier committed at `fedc0e5`; single run (13 s), rerun
  byte-identical.
- N1, N2, N4-N7 held. N3 failed: C = 33 rules at every ring; K = 9
  {0,4,42,112,170,200,204,232,240}; Z = 24, all collapsing to 0^n; rules
  123 and 251 are closed, neither commuting nor collapsing, factor = rule
  32 on image words. 251 = ¬F_4 is a function of the observation; 123 is
  not (0^n and 1^n share the observation, map to 1^n and 0^n) and only
  shares 251's observed successor on rings 6-12.
  h_* max 6,6,8,14,12,12,22 at rings 6-12 (62/118; 107/121 at ring 8),
  not monotone; 160 rules vary with n. Complement-covariant with the
  observation transported to 223, not invariant. C_4 and C_232 meet in 12
  rules; neither contains the other.
- Do not infer: anything about the closed-set structure under other
  non-linear observations; anything beyond ring 12 about the depth; that 123's
  agreement with 251 holds off the tested rings.
- Codex's first gate-2 round reproduced every number and requested
  wording corrections: 123 is not a function of the observation, and the
  contradicts edge to the majority finding became a depends_on contrast.
- Pending: Codex's gate-2 sign-off on the corrected head and reviewer
  merge on PR #93.
- Candidate next units: (a) characterize the closed rules with a
  non-constant factor that is not the rule: for a given pi, every g o pi
  is one candidate class, with 123 showing it is not the only one; frozen
  as a prediction for a third observation; (b) the depth-growth follow-ups on {106,120,169,225} under
  majority and {62,118} under rule 4 at rings 13-16.

## Checkpoint 2026-09-11 (ninth unit opened): isolated-cell detection, protocol frozen, review pending

- Frozen and unrun: `protocols/isolated-cell-20260911.md`. Rule 4 as an
  observation: non-linear, non-surjective (image 28% -> 8% from n=6 to 12;
  fibers up to 853), not self-dual (conjugate observation 223). Predictions
  N1-N7: commuters close (control; 255 is not a commuter); 255 closes by
  collapse, so C != K is frozen; C = K u Z, commute-or-collapse, is the
  unit's falsifiable question; the eight remaining affine rules do not
  close, witness 0^n against a 11 or 111 block; h_* census; reflection
  invariance and complement covariance to the rule-223 census; CLOSED_32
  not contained in the closed set.
- Codex's first gate-1 round found one blocker: the hand witness for rule
  90 (blocks 11 and 111) was false; N4 re-frozen with one enumerated
  witness per rule (110111 for 90 and 165). Substantive predictions
  unchanged. Gate 1 re-requested. No verifier committed, nothing run.

## Checkpoint 2026-09-11 (eighth unit accepted): block majority merged

- Gate 2 met: Codex signed off at `7c33051` with no blockers and merged
  PR #92 itself under the reviewer-merges rule. Unit accepted.
- Program state: global relabelings (1-3), one injective local recoding (4),
  neighbor parity with its history bound (5-6), all linear observations (7),
  the first non-linear observation (8). Open threads from unit 8: the depth
  growth beyond ring 12 on {106, 120, 169, 225}; whether commute-or-collapse
  is the general shape of closure under a non-linear observation.
- Next: ninth unit, a second non-linear observation (rule 4, isolated-cell
  detection), chosen to test the second thread; protocol to be frozen and
  gate-1 reviewed before any run. The depth-growth thread stays open.

## Checkpoint 2026-09-11 (eighth unit run): block majority, gate-2 pending

- Gate 1 met at `6f4eb6c` before implementation; verifier committed at
  `ade705f`; single run (5 s), rerun byte-identical.
- All frozen predictions held (M1, M2, M4-M7; M3 reported). Closed set = 22
  rules at every ring: 14 exact commuters {0,4,15,23,32,51,85,170,204,223,
  232,240,251,255} plus 8 collapse rules {2,8,16,64,191,239,247,253} with a
  constant factor. The eight remaining affine rules are not closed (witness
  0^n vs one isolated cell holds everywhere). h_* max 2,4,3,4,7,8,16 at rings
  6-12 (rules 106,120,169,225 at 12); 88 rules change depth with n. Neither
  CLOSED_32 nor C contains the other.
- Do not infer: anything beyond ring 12 about the depth growth; that the
  collapse mechanism is the only non-commuting route in general.
- Pending: Codex's gate-2 sign-off and reviewer merge on PR #92.
- Candidate next units: (a) a frozen follow-up on the depth-16 rules
  {106, 120, 169, 225} at rings 13-16 to test the growth; (b) a second
  non-linear observation (rule 4, isolated-cell detection) to test whether
  commute-or-collapse is the general shape of non-linear closure.

## Checkpoint 2026-09-11 (eighth unit opened): block majority, protocol frozen, review pending

- Frozen and unrun: `protocols/block-majority-20260911.md`. Rule 232 as an
  observation: non-linear, non-injective, non-surjective (image 53% -> 26%
  from n=6 to 12; fibers up to 98 states). Predictions M1-M7: exact
  commuters close (theorem control; at least the ten named rules); the
  eight remaining affine rules do not close (M2, falsifiable); closed set vs
  commuters reported; factor radius-1 on the image (M4); h_* census; T_c and
  T_m invariance; CLOSED_32 not contained in the majority-closed set.
- Pending: Codex's gate-1 review. No verifier committed, nothing run.

## Checkpoint 2026-09-11 (seventh unit accepted): linear observations merged

- Gate 2 met: Codex signed off at `953d2dc` with no blockers, independently
  reproducing the post-hoc closed sets and depth maxima, and merged PR #91
  itself under the reviewer-merges rule. Unit accepted.
- Program state: global relabelings (1-3), one injective local recoding (4),
  neighbor parity with its history bound (5-6), all linear observations (7).
  Next: block majority (rule 232 as an observation), the first non-linear
  fiber structure; protocol to be frozen and gate-1 reviewed before any run.

## Checkpoint 2026-09-11 (seventh unit run): linear observations, gate-2 pending

- Gate 1 met at `eb7d2f1` before implementation; verifier committed at
  `e30221c`; single run, rerun byte-identical (25 s).
- All seven predictions held. Complement-pair kernels (60, 102, 90 odd n)
  reproduce the 32 and the certified depths for all 256 rules. Rule 90 even n
  and rule 150 at 3|n: closed set = the 16 affine rules exactly (bounds were
  frozen; the exact value is post hoc). Depths under those kernels reach 4
  within n=12 (90: rules 22, 151 at n=10,12; 150: up to 10 rules at n=12)
  and are ring-dependent (16 and 48 rules respectively).
- Do not infer: that only affine rules close under every observation whose
  kernel omits the all-ones vector (Codex's caution); anything beyond n=12.
- Pending: Codex's gate-2 sign-off and reviewer merge on PR #91.
- Intended eighth unit: block majority (rule 232 as an observation), the
  first non-linear fiber structure.

## Checkpoint 2026-09-11 (seventh unit opened): linear observations, protocol frozen, review pending

- Frozen and unrun: `protocols/linear-observations-20260911.md`. Declares the
  eight linear rules as observations; closure is decided by each kernel:
  {0,1} for 60/102 and 90 at odd n (E3: the fifth unit's 32), period-2
  kernel for 90 at even n (E4: between the 16 affine and the 32), period-3
  kernel without the all-ones vector for 150 at 3|n (E5: affine lower bound,
  no upper bound; the unit's question), trivial kernels (E2), affine rules
  always closed (E1, theorem), h_* by exact partition refinement (E6),
  symmetries (E7).
- Pending: Codex's gate-1 review. No verifier committed, nothing run.
- Intended eighth unit: block majority (rule 232) as the first non-linear
  observation.

## Checkpoint 2026-09-11 (sixth unit accepted): parity history bound merged; workflow housekeeping

- Gate 2 met: Codex signed off at `10fdbe3` after one record correction (the
  per-ring census covers rings 6-12 and 14, not 6-14). Merged via PR #89 at
  `2a58ca2` with a merge commit; five checks green including the 24-minute
  byte-for-byte replay; local rerun byte-identical. Unit accepted.
- Workflow change (Myk, 2026-09-11), in the next gathering PR: the reviewer
  merges on a clean gate-2 sign-off with green checks; result replays split
  into a fast integrity tier on pull requests and the full replay on main.
- Next unit candidates unchanged: a second non-injective map (2-block
  projection or block majority) to test whether the constant-response
  criterion is parity-specific; or which observations admit a finite
  history certificate of this kind.

## Checkpoint 2026-09-11 (sixth unit run): parity history bound certified, gate-2 pending

- Run authorized by Myk before any other-model review (recorded on the
  protocol); Codex's gate-1 sign-off arrived retrospectively at the same
  frozen revision with no change; verifier committed at `c16cee0` before the
  run. Evaluation preceded review; gate 2 not waived.
- All four predictions held. D1 literal: no violating L-admissible 8-word for
  any rule, so h_* <= 2 on every ring (theorem via the frozen lemma). D2:
  depth-2 set exactly {22,73,104,109,146,151,182,233}, realized at n=5. D3:
  rings 7/9/11/14 reproduce 32/216/8. D4: T_c and T_m invariance holds.
- Post hoc, do not promote without a frozen follow-up: 32 non-closed rules
  have no L-admissible 8-word (no pair survives two complementary steps).
- Runtime ~38 min (ring-14 census); CI job limit raised in the workflow only.
- Pending: Codex's gate-2 sign-off on PR #89 at its head. Not accepted until then.
- Next unit candidates: a second non-injective map (2-block projection or
  block majority) to test whether the constant-response criterion is
  parity-specific; or the general question of which observations admit a
  finite history certificate of this kind.

## Checkpoint 2026-09-11 (sixth unit opened): parity history bound, protocol frozen, review pending

- Frozen and unrun: `protocols/parity-history-bound-20260911.md`. Turns the
  fifth unit's post-hoc h_* <= 2 into predictions D1-D4: a finite certificate
  (equal adjacent g∘F² values on every L-admissible 8-word, with a frozen
  lemma extending it to every ring size), the exact depth classification
  (8 rules at depth 2, 216 at depth 1) from 6-word cycle checks, an
  independent exhaustive census at n in {7, 9, 11, 14}, and the T_c/T_m
  invariance of h_*.
- Pending: Codex's gate-1 review. No verifier committed, nothing run. Do not
  infer: that the certificate passes.

## Checkpoint 2026-09-11 (fifth unit accepted): parity coarse-graining merged

- Gate 2 met: Codex signed off at `36be4bc` (one record correction first: the
  ring-12 pair count is 2,046 of 2,048, not 1,022 of 1,024; prose only).
  Merged to main via PR #88 at `48b6cf3` with a merge commit; five checks
  green including the parity replay. Unit accepted.
- State of the program: global relabelings (units 1-3), one local injective
  recoding (unit 4), one non-injective coarse-graining (unit 5) declared and
  audited. Undeclared: change of completion (Codex's second-lift protocol).
- Next unit candidates, in order of preference: (a) freeze h_* <= 2 under
  neighbor parity as a prediction at n in {14, 16} with a proof attempt on the
  complement-response structure; (b) a second non-injective map (2-block
  projection or block majority) to test whether the constant-response
  criterion is parity-specific. Protocol review by Codex before any run.
- Open for Myk, unchanged: the editorial default for the commutator under
  relabeling.

## Checkpoint 2026-09-11 (fifth unit run): parity coarse-graining, final review pending

- Gate 1 met: Codex reviewed the protocol at `9997462` before implementation;
  verifier committed at `163859c`, serialization patch at `8cc0ada` (dated
  deviation, no computation changed), then the single run.
- All five predictions held. Closed set = 32 constant-complement-response rules
  at n in {4,5,6,8,10,12}; elementary factors match the formula; rule 90 fixed;
  pi G_r = G_B pi on rings 8/10; h_*=0 exactly on the closed set; closed set =
  audit self-dual set + complement-invariant set.
- Post hoc, do not promote without a frozen follow-up: h_* in {1,2} for all
  224 non-closed rules at n <= 12 (2 for 22,73,104,109,146,151,182,233); the
  factor map is two-to-one along complement conjugation; fixed points are the
  8 linear rules.
- Pending: Codex's final sign-off on PR #88 at its head. Not accepted until then.
- Candidate next units: a frozen prediction or proof of h_* <= 2 at larger n;
  change of completion (second-lift protocol, Codex's program).

## Checkpoint 2026-09-11 (fifth unit opened): parity coarse-graining protocol frozen, review pending

- The correction unit merged to main via #86 with Codex's final sign-off at
  `cec7422`; the review workflow of #85 is now canon in `AGENTS.md`.
- Frozen and unrun: `protocols/parity-coarse-graining-20260911.md`, the first
  non-injective transformation (`π` = rule 102 as an observation). Predictions
  C1–C5 are stated there; the verifier is not yet committed, by design: the
  workflow now requires other-model protocol review before implementation.
- Pending: Codex's protocol review on the gathering PR. Do not infer: any
  result of C1–C5; that the 32-rule closure set has been checked at any `n`.
- Open for Myk, unchanged: the editorial default for the commutator under
  relabeling.

## Checkpoint 2026-09-11 (corrections): Codex retrospective review of units 1–4 applied

- Review arrived after merge, not at freeze; all four protocols carry dated
  addenda and the frozen text is unchanged. Verifiers were corrected and the
  four canonical JSONs regenerated in dependency order; every previously
  reported number is unchanged.
- Unit 1: P6's boundary clause was unscored; now scored, unsupported
  (28.46%/26.19% on the named boundaries). P5's 22 = 4 genuine h=0
  violations + 18 right-censored cells; 696 identical, 54 differ finite.
  Self-duality iff proved by the five-cell local check; full-gradient
  criterion qualified (constant complement response, admits 0 and 255).
- Unit 2: domain described as flagged entries; "budget artifact" restricted
  to the 18 censored cells; window width 2·max(h+1+R,h+2)+1 clarified.
- Unit 3: half-decided cells can refute the shift bound (lower bound 5−a)
  and are now reported; X5 implements its declared predicate; no data change.
- Unit 4: executed block law has ambient radius 2 off the family (deviation,
  witness asserted); componentwise radius-1 completion added, both run,
  identical on-family results; B4 restated as transport of maximizers with
  explicit permutations; costs record two stored bits per site.
- Process change from Myk: both sides now PR into a gather branch and the
  gather is PR'd for review by the other side; meaty sub-PRs may request
  review before joining the gather. This program's next unit follows that.
- Transition, agreed with Codex on #85 (2026-09-11): PR #86 (branch
  `claude/review-github-issues-wf15ni`) is this correction unit's gathering
  PR despite its harness-assigned prefix. It is pending Codex's final
  sign-off at its current head before merge into main; a second review
  round (headline and P6 boundary wording) was applied at `8a1e54b`. Do
  not describe the unit as accepted until that sign-off is recorded.
- Open: the tight cap-shift value; the editorial default for the commutator
  under relabeling; non-injective coarse-graining as the next transformation type.

## Checkpoint 2026-09-11 (fourth unit): first local transformation; recoding is nearly free

- Protocol and verifier committed before the single deterministic run; no
  corrections at evaluation; retrospective corrections dated 2026-09-11 in
  the note and protocol addendum. Note: `2026-09-11-higher-block-recoding.md`.
- T_beta (2-block recoding): forward radius 1, inverse 0, alphabet 2->4,
  family the consistent-pair subshift. B1-B3 held on the family: cap radius
  in [mpr-1, mpr] on all 674 decided cells, unchanged in 665, reduced by one
  in 9 (K 55,109,233; O 73,109,146,182); D and G covariant componentwise on
  rings 8/10 (algebra; control); derivative closure preserved; Research026
  observer family closed under input complement/reversal with 12-ring block
  alignment (B4 closure part held). B4's frozen consequence, literally
  identical census summaries, was corrected after review (2026-09-11) to
  scalar summaries identical and optimal observers covariant under the
  table permutation (deduction; tables not in repo); the executed block law
  had ambient radius 2, not the declared 1 (recorded deviation).
- Do not infer: anything about k>2 recodings, non-injective recodings, or
  radii above 4; that the deduction has been numerically run.
- Open for Myk: default reading of the commutator under relabeling
  (state-transport of the derivative), editorial.
- Next: consolidate the program's transformation table into one page; then
  either run Codex's second-lift protocol for the completion type (Codex's
  to run) or declare the non-injective coarse-graining type against the
  Erased Distinctions closure object. Codex review of all four protocols
  is still outstanding.

## Checkpoint 2026-09-11 (third unit): shift census over all rules; global relabelings exhausted

- Protocol and verifier committed before the single deterministic run; no
  corrections. Note: `2026-09-11-cap-shift-census.md`.
- All six predictions held at R<=4: census reproduced (4,608); reflection
  exact for K and O; K shift <= h+1 (observed max 2, at 132/222, 160/250,
  h=2); O shift 0 and O pass table complement-invariant at every radius;
  zero half-decided cells (862 undecided on both sides).
- Post hoc, exact within budgets: the 30 rules with a depth-0 cap of either
  kind are exactly the 30 rules whose derivative observation closes on
  rings n<=10 (both say D∘F is a local function of D).
- Do not infer: anything above radius 4; that h+1 is tight (observed max at
  h=2 is 2); that these two global transformations exhaust admissibility.
- Open for Myk: default reading of the commutator under relabeling (state-
  transport of the derivative), an editorial decision.
- Next: declare a transformation of a different type (local recoding with a
  locality budget, or change of completion on a shared family) and audit an
  Erased Distinctions observer result against it. Review of the three
  protocols by Codex is still outstanding.

## Checkpoint 2026-09-11 (second unit): cap-census extension confirms the corrected bound

- Protocol and verifier committed before the single deterministic run; no
  corrections. Note: `2026-09-11-cap-census-complement-extension.md`.
- All four predictions held on the 22 cells at R<=6: reproduction exact;
  caps on both sides, every former None at radius 3; bound holds; shift
  never exceeds h+1 (1 in 18 cells, 2 in 4: 132/222 and 160/250 at h=2).
- Reading: the first audit's P5(b) failure was a budget artifact. The bound
  is loose (up to 6, observed at most 2). Radius budget is part of the contract.
- Do not infer: the tight shift value; anything about O coordinates, radii
  above 6, or the 696 unchanged cells.
- Open for Myk: whether state-transport of the derivative becomes the default
  reading of the commutator under relabeling (editorial, not computational).
- Next candidates: (a) shift census over all 256 rules at h<=2, R<=4 to test
  `shift <= h+1`; (b) declare local recodings with a locality budget and
  completions as the next transformation types and audit the Erased
  Distinctions observer results against them.

## Checkpoint 2026-09-11: first audit run; one frozen prediction failed

- Verifier committed at a2a5fe5 before evaluation; run once, deterministic
  JSON, no implementation corrections. Note: `2026-09-11-representation-invariants-audit.md`.
- Held: P1 (reflection preserves commutator class, 256/256), P2 (complement
  images exactly as predicted; 4↦223 and 200↦236 leave the zero-G set),
  P3 (native commutator complement-covariant for exactly the 16 self-dual
  rules at n=6,8,10, no spurious passes; state-transport covariant for all
  256; reflection covariant for all 256), P4 (derivative closure preserved;
  same 30 closed rules at all three rings), P5(a) (reflection preserves all
  4,608 cap budgets), P6 (labels 95.13%/93.94% stable; commute exact).
- Failed: P5(b). Frozen radius bound `h` omitted the target row's recoding
  and radius composition. Corrected bound is post hoc; at h=0 it is 1 and
  every observed h=0 shift is exactly 1. 22 of 768 (rule,h) cells differ
  within R<=2; the census budget cannot decide the corrected bound for h>=1.
- Do not infer: that the corrected bound is established; that label
  stability is an invariance; that three transformations exhaust admissibility.
- Next: freeze a census extension at R<=4 on the 22 cells with the corrected
  bound as prediction; decide editorially whether state-transport of the
  derivative is the default reading of the commutator under relabeling.

## Checkpoint 2026-09-10: program opened; first audit protocol frozen, unrun

- Program registered as `representation-invariants`. Thesis: properties of a
  represented dynamics are classified as preserved, covariant with a declared
  transport, or changed, relative to a declared transformation with declared
  costs. No single group; no intrinsic invariant; not the beam.
- First counterexample recorded before any protocol: complement conjugation
  sends Rule 0 to Rule 255 and the commutator from `G ≡ 0` to `G ≡ 1`. The
  derivative is a difference and is relabeling-invariant; the law acts on
  labeled states. Established result 1 stands; its bias is not invariant.
- Frozen: `protocols/representation-invariants-audit-20260910.md`. Two global
  transformations (complement conjugation, reflection) and their composite;
  six audited properties with predictions. Implementation to be committed
  before evaluation. Nothing run.
- Do not infer: that the audited transformations exhaust admissible
  re-interpretations; that a preserved property is intrinsic; that the sweep's
  regime labels, which depend on fixed seeds, should be exactly invariant.
- Next: implement `scripts/verify_representation_invariants.py`, commit, run,
  write the results note, register it, add knowledge entries, and update this
  log. Reviewer for the protocol: none yet; Codex inactive at freeze time.
