# Checkpoints: Class-IV Refinement

Checkpoint log for the fourth research Program, opened 2026-09-17. Each
section is a Program-scoped checkpoint: a dated statement of state that adds
no evidence. The most recent unit is first. Add a new checkpoint at the top
when a substantial unit completes; keep the bounded-claim style.

Program page: `docs/research/2026-09-17-class-iv-refinement-program.md`

## Checkpoint 2026-09-17 (later): fiber census evaluated

- **Completed:** [the fiber census](../2026-09-17-fiber-census.md), canonical
  `results/fiber_census_20260917/` (summary registered with the fast
  integrity tier). P1–P3 held (fibers differ; fiber(54) both-positive 0.47
  against 0.37/0.25/0.22/0.07 for 22/0/90/204; HighLife and Life typical of
  their fibers), P4 failed (fiber(22) is 72% ballistic, not bimodal). Two
  deviations recorded in the note (a glance at the secondary pass before the
  primary finished; provenance hashes added to the evaluator after the run).
- **Do not infer:** that the base rule carries more than its fixed bits'
  activity (untested); anything about the full plane or about 110.
- **Next, unfrozen:** a 64-fiber census at 128 rules per fiber to separate
  base rule from fixed-bit activity; an anisotropic family for 110.

## Checkpoint 2026-09-17: Program opened from the GPT handoff; fiber census frozen and unrun

Authored by Claude/Fable 5.1. Myk suspended the cross-model review gates on
2026-09-17 (GPT has no GitHub access, no other agent available) and authorized
this session to integrate, self-review and merge; every record below says so.

- **Inherited and recorded (GPT-5.6 Sol, 2026-09-16/17):** the Jev semantic
  scout, Runs 1 and 2 (`2026-09-17-jev-class4-scout-record.md`; raw responses
  and frozen evaluator re-run by Fable, ranks reproduced); the
  selective-persistence × spreading discriminator (`2026-09-17-selective-persistence-discriminator-record.md`;
  report and complete tables survive, the hash-pinned protocols, runner and
  canonical JSON were lost and are reconstructed with explicit non-claims); the
  cross-dimensional 2D panel and the strip spectrum (GPT's notes as written);
  the exact strip restriction (Fable replayed `strip_restriction_exact.json`
  byte-identically). Evaluation preceded review for all of them.
- **Exact facts to build on:** width-one HighLife = ECA 54; Life and B35/S236
  = ECA 22; height-one restriction of the Life-like family is a 12-bit
  quotient onto the 64 reflection-symmetric ECAs (4096-rule fibers); height
  two is injective on the family; the selective-surprisal gap has an exact
  coarse-visible + within-fiber decomposition. Rule 110 has an empty fiber in
  this family (not reflection-symmetric).
- **Frozen and unrun:** the fiber census
  (`protocols/2026-09-17-fiber-census.md`): 512-rule samples of the
  height-one fibers of ECAs 54, 22, 90, 204, 0 at strip height two under the
  starred contract; the bet is that fiber(54) is enriched in the both-positive
  region. Jev Run 3 was acquired the same day by a child session and evaluated:
  J1/J3/J5 reproduce under operational definitions alone, J4 weakens.
- **Do not infer:** a universal Class-IV definition; anything about the full
  plane from finite strips; novelty over the storage × spreading literature;
  hash-level provenance for the 2026-09-16 discriminator; that the
  refinement-depth conjecture is well posed beyond an explicitly restricted
  family (the trivial bolt-on lemma is recorded in the protocol).
