# Checkpoints: Invariants Across Representation Contracts

Checkpoint log for the third research program. Each section is a
Program-scoped checkpoint: a dated statement of state that adds no evidence.
The most recent unit is first. Add a new checkpoint at the top when a
substantial unit completes; keep the bounded-claim style.

Program page: `docs/research/2026-09-10-representation-invariants-program.md`

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
