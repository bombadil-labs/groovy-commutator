# Checkpoints: Invariants Across Representation Contracts

Checkpoint log for the third research program. Each section is a
Program-scoped checkpoint: a dated statement of state that adds no evidence.
The most recent unit is first. Add a new checkpoint at the top when a
substantial unit completes; keep the bounded-claim style.

Program page: `docs/research/2026-09-10-representation-invariants-program.md`

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
