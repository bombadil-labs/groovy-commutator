# The bounded source-recoder recovery is still stuck at 0/8, and here is exactly where

**Date:** 2026-09-14
**Program:** Dynamics of Erased Distinctions
**Status:** recovery campaign status and negative resource finding; the frontier remains open
**Authored by:** Claude Code, Opus 5, session `session_01SobHxxYcFURkku6CFKrhSZ`. **Reviewed by:** none — retrospective review requested on the gathering PR that integrates this note.

## The question and the plain answer

The [program terminus note](2026-09-10-erased-distinctions-terminus.md) can only
become a closure record once the
[frozen exact-recovery protocol](protocols/bounded-source-recoder-exact-recovery-20260910.md)
has classified all eight previously censored seed languages. Did it?

**No.** After a fresh campaign on 2026-09-14 the tally is unchanged:

| quantity | value |
| --- | ---: |
| frontier seed languages exactly classified | **14 / 22** |
| recovery seed languages recovered | **0 / 8** |
| bounded-recoder certificates | **0** |
| structural tuples decided in this campaign | **0** |

Nothing was decided, and nothing was fabricated to look decided. The Program is
**not** marked complete/dormant. `pending` is scheduling state, exactly as the
protocol says; it is not a scientific `censored` outcome and it is emphatically
not a negative result about these eight seeds.

## What was actually run

The frozen recovery implementation
(`scripts/recover_bounded_source_recoder_exact.py`) was run unchanged from this
repository's pinned copy, against the parent audit
`results/bounded_source_recoder_synthesis_20260910.json`, whose SHA-256 was
re-verified as `2d28a4d5e4b668f9a201f3658a986060712a2f9069577810aacd08a49e7f12f2`
before any batch. No frozen scientific parameter was touched: the same 22 seed
languages, `m <= 4`, `t <= 6`, the same `(m,t,j,k,delta)` structural order, the
same deterministic adaptive rail-selection grammar, the same seed-reinsertion
semantics, the same universal equality criterion, the same scalar fine-ECA
replay requirement, and the same 10-second-per-solver operational slice before a
cylinder is split. Solver portfolio order was the frozen `cadical195`,
`glucose4`, `maplechrono`, `minisat22`.

All five of the protocol's controls were reproduced **before** any recovery seed
was interpreted, in this environment, from this implementation:

1. the Rule 5 `m=1,t=3,k=2,j=1,delta=0` partitioned verification closed all
   seven candidate positions exactly;
2. the Rule 35 bounded negatives reproduced — 16 exact-negative control
   structures over `m <= 2`, `t = 3`;
3. a known-SAT verifier query produced a counterexample that passed independent
   scalar fine-ECA replay (`replay_pass: true`);
4. a known-UNSAT query was closed exactly by the partitioned verifier;
5. the operational solver slice was forced to zero on a tiny control, exercising
   the split-to-direct-leaf path and agreeing with ordinary exact verification
   (1 split, 2 direct leaves, exact UNSAT).

Execution was off GitHub Actions, on four cores, in eight resumable per-seed
campaigns driven from the protocol's own checkpoints. Determinism of a *decided*
result is not at issue here, because nothing was decided; what the checkpoints
record is accumulated exact partition evidence.

## Where the recovery is stuck, quantitatively

Every one of the eight seeds is parked at **output position 0 of its first
uncompleted structural tuple**, with the CEGIS example set still empty — that
is, on the very first universal-verification query the parent experiment's
1,200-second wall had cut short.

| seed | rule | pair | tuple ordinal | remaining tuples | `m` | free source-background bits | clauses | DFS depth reached |
| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 122 | 1-5 | 84 | 256 | 1 | 42 | 12,096 | 21 |
| 6 | 154 | 6-7 | 253 | 87 | 3 | 39 | 13,184 | 15 |
| 11 | 161 | 2-6 | 155 | 185 | 2 | 54 | 15,397 | 26 |
| 14 | 164 | 0-4 | 252 | 88 | 3 | 42 | 14,030 | 13 |
| 16 | 166 | 0-1 | 338 | 2 | 4 | 39 | 14,733 | 13 |
| 17 | 180 | 0-4 | 82 | 258 | 1 | 42 | 12,096 | 19 |
| 18 | 210 | 3-7 | 82 | 258 | 1 | 42 | 12,096 | 20 |
| 20 | 218 | 3-7 | 252 | 88 | 3 | 42 | 14,030 | 12 |

The decomposition is exact and it is working as specified — it is just very
wide. With 39 to 54 free background bits, the worst-case cylinder tree under the
frozen split order has up to `2^39` to `2^54` leaves. Recorded totals across the
2026-09-10 and 2026-09-14 campaigns:

| quantity | 2026-09-10 | after 2026-09-14 | added |
| --- | ---: | ---: | ---: |
| recorded portfolio solver-hours | 36.2 | 45.5 | **9.3** |
| exact partition splits | 2,780 | 3,501 | 721 |
| cylinders closed by a solver | 3,326 | 4,041 | 715 |
| per-cylinder portfolio timeouts | 11,301 | 14,197 | 2,896 |
| fully assigned direct-evaluation leaves | 0 | **0** | 0 |

Two features of that table matter more than the totals.

First, **no run has ever reached a direct-evaluation leaf.** The protocol's
logical-termination argument rests on those leaves: at a fully assigned
background the CA equality is decided by scalar evolution, so solver
nontermination can never become a scientific endpoint. The argument is sound,
but the depth-first frontier is 12 to 26 bits into a 39-to-54-bit assignment, so
the guarantee has not yet been exercised on a real seed.

Second, **timeouts outnumber solver decisions roughly three and a half to one.**
Each undecided cylinder costs the full portfolio — four solvers at 10 seconds
each — before it is split, so the dominant cost is paid on cylinders that
produce no verdict, only two children. The frozen slice is explicitly labelled
operational rather than scientific, but this note does not change it: a protocol
parameter is not the sort of thing to retune mid-campaign on the basis of how
the campaign is going.

## What this does and does not establish

It establishes that the recovery's remaining workload is large, that it is
large for a locatable reason, and that the campaign is genuinely resumable
from the committed checkpoints rather than needing a restart.

It does **not** establish:

- that the eight seeds have no bounded finite-state recoder — that is exactly
  the open question, and nothing here bears on it;
- that these instances are intrinsically hard. The program's own
  [established lesson](2026-09-09-symbolic-sofic-image.md) is that a wall in one
  exact encoding said nothing about the dynamics: phase-splice MDD censored all
  twelve Rule 122/161 sentinels, and the same candidates as fine-ECA CNF were
  tiny and completed exactly. This campaign's difficulty is a statement about
  the partition-on-source-bit decomposition at its frozen slice, in this
  environment, on four cores;
- that the recovery protocol is wrong. Its decomposition is exact and its
  controls reproduce;
- that more solver time would or would not finish it. No extrapolation is
  offered, because the DFS frontier gives no reliable basis for one.

## What would move this

Three options, in increasing order of how much they change the question:

1. **More computation, unchanged.** Resume the committed checkpoints. This is
   the protocol's own intent and needs no new authorization.
2. **A better exact backend at the same semantics.** The program has already
   seen one representation wall dissolve under re-encoding. An incremental
   solver reusing learned clauses across sibling cylinders, or a smarter split
   order, would change only the operational layer — but the split order and the
   slice are written into the frozen protocol, so a change needs a recorded
   deviation and review, not a quiet edit.
3. **A structural theorem.** The terminus note's first named continuation is a
   principled bound or impossibility result for source-recoder state. That
   would retire the whole search rather than accelerate it, and is the option
   the program itself points at.

## Reproducing

```bash
pip install -e '.[research-sat]'
python scripts/recover_bounded_source_recoder_exact.py --controls-only \
    --output /tmp/controls.json
python scripts/recover_bounded_source_recoder_exact.py --seed-index 16 \
    --checkpoint-in results/bounded_source_recoder_recovery/checkpoint-seed-16.json \
    --output /tmp/recovery-seed-16.json --batch-seconds 900
```

The aggregate artifacts are
`results/bounded_source_recoder_exact_recovery_20260910_progress.json` and
[the progress table](bounded-source-recoder-exact-recovery-20260910-progress.md),
regenerated by `scripts/aggregate_bounded_source_recoder_exact_recovery.py` from
the eight per-seed checkpoints in `results/bounded_source_recoder_recovery/`.
This campaign runs **off** GitHub Actions; only the fast integrity tier
(`scripts/check_result_integrity.py`) guards the committed bytes, and it
establishes provenance coherence only.
