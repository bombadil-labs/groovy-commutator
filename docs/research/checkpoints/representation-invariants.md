# Checkpoints: Invariants Across Representation Contracts

Checkpoint log for the third research program. Each section is a
Program-scoped checkpoint: a dated statement of state that adds no evidence.
The most recent unit is first. Add a new checkpoint at the top when a
substantial unit completes; keep the bounded-claim style.

Program page: `docs/research/2026-09-10-representation-invariants-program.md`

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
- Open: the tight cap-shift value; the editorial default for the commutator
  under relabeling; non-injective coarse-graining as the next transformation type.

## Checkpoint 2026-09-11 (fourth unit): first local transformation; recoding is nearly free

- Protocol and verifier committed before the single deterministic run; no
  corrections. Note: `2026-09-11-higher-block-recoding.md`.
- T_beta (2-block recoding): forward radius 1, inverse 0, alphabet 2->4,
  family the consistent-pair subshift. All four predictions held: cap radius
  in [mpr-1, mpr] on all 674 decided cells, unchanged in 665, reduced by one
  in 9 (K 55,109,233; O 73,109,146,182); D and G covariant componentwise on
  rings 8/10 (algebra; control); derivative closure preserved; Research026
  observer family closed under input complement/reversal with 12-ring block
  alignment, hence census summaries covariant (deduction; tables not in repo).
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
