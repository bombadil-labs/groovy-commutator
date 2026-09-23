# A hidden cell becomes visible through time

2026-09-23. Authored by Codex (OpenAI). Reviewed by: none.
This is an exact, finite observation result, with a separate scalar replay
by the same author. It formalizes a small part of a collaborator's proposal
about sensing through damage; it is **not** a model or test of HAVOKSLAM,
audition, unknown noise, cortical object formation, or physical repair.

## The question

Suppose we can read eleven cells of a twelve-cell Rule-54 ring, but the
location of the twelfth cell is known and permanently hidden. Can seeing
later *visible* rows reveal what was hidden? Does it let us answer a task
before it lets us reconstruct the exact original state?

We reused the 52-source family from the integrated
[prediction/repair result](2026-09-23-prediction-repair.md): four rotations
of `(0011)^3` and all their one-bit injuries. These are possible physical
source states, not corruption introduced by the observer. For each of 12
known hidden-cell addresses, the physical CA evolves without intervention;
we observe the other eleven bits at times 0, 1 and (if needed) 2. The task
is to say whether the source reaches the four-state stripe target at time 4.
On this source family and ring, that answer equals whether the *initial*
state was intact. Full reconstruction instead asks for all twelve original
bits. The [frozen protocol](protocols/masked-history-sensing-20260923.md)
fixes these choices and the four predictions.

For any received history `y`, let `F(y)` be every permitted initial state
that could produce it. A task can be answered exactly from `y` if and only
if all members of `F(y)` have the same task outcome: necessity follows because
one deterministic answer cannot be correct for two different outcomes, and
sufficiency follows by assigning each fiber its shared outcome. Recovering
the entire source requires every fiber to contain exactly one state. This
criterion is a finite identifiability statement, independent of which
algorithm reads the sensor.

## Exact result

Each row below accounts for all **52 sources × 12 hidden-cell choices = 624**
source-mask cases. A conflicting case belongs to a fiber containing sources
with incompatible answers. The source column counts any multi-source fiber.

| Visible snapshots | Distinct observations | Task-conflicting fibers / cases | Source-conflicting fibers / cases | Visible bits read per case |
| --- | ---: | ---: | ---: | ---: |
| Time 0 | 576 | 48 / 96 | 48 / 96 | 11 |
| Times 0–1 | 600 | 24 / 48 | 24 / 48 | 22 |
| Times 0–2 | 624 | 0 / 0 | 0 / 0 | 33 |

For example, if cell 0 is hidden, sources 818 (injured) and 819 (intact)
give the same initial visible eleven bits but opposite task answers. At the
next time their visible histories differ. Another pair, 1638 (intact) and
1639 (injured), remains indistinguishable even after the first update and
splits only at the second. Each hidden-cell address has some pair requiring
time 2; all addresses become fully distinguishable then.

The frozen P1–P3 predictions held. **P4 failed:** in this selected family,
there is no tested observation length and missing-cell position for which
every task answer is determined while some original states remain
ambiguous. Every remaining ambiguous pair is precisely the distinction
between an intact stripe and an injury. Task prediction and full source
reconstruction attain sufficiency together here, despite their different
definitions. This is a limit of this corpus and sensor, not a theorem that
tasks always require reconstructing everything.

There is a stronger **post-evaluation consequence** of the audited time-zero
fibers: each has at most two sources, and every two-source fiber has opposing
task labels. Any later observation that *retains* the time-zero view can only
split those fibers, never merge them. Thus task identification and exact
source identification coincide for **any** longer such history, not merely
for the three horizons evaluated. The finite fiber audit supplies the premise;
the refinement argument supplies the all-horizon conclusion under this
declared source domain and fixed mask.

## Cost and interpretation

Time restores information that a permanently missing spatial sensor cannot
provide at one instant: the physical dynamics move evidence of the hidden
bit into visible cells. This costs two update intervals and three eleven-bit
snapshots (33 observed bits plus a four-bit cell address if it must be sent),
versus twelve bits in one direct whole-state snapshot if that sensor is
available. Evolution updates the full twelve-cell ring twice. We have not
shown an information, computation or energy saving. There is no controller
and no new bit is added to the physical system.

Rule-54's full 4,096-state transition map was checked, and an independently
written scalar/string implementation agreed on all 624 source-mask cases,
fiber counts, predictions and witnesses within a 30-second cap. The exact
criterion says what can be inferred under *known erasure on this declared
source family*. With unknown corruption or a larger family, incompatible
clean histories may persist; a generative model could then rank possible
repairs, but could not certify a unique true missing bit without further
assumptions or evidence.

## Decision and provenance

This supplies an inspectable definition for the proposed sensing bridge:
specify a corruption channel, a source family and a task; test compatible
histories before claiming that inpainting recovers truth. The selected
stripe task and exact state identity proved equally hard under this sensor,
so repeating the same experiment with a larger mask or more horizons would
not address the desired task-specific distinction. Further work needs an
independently motivated task or the collaborator's actual operator and loss.

- Inspected main: `69c9121c627b15952d57b179a1bc6b0c95ccb29a`.
- [Protocol commit](https://github.com/bombadil-labs/groovy-commutator/commit/7aaaef3fee531df7e17988bacab00dd58b4bd596), frozen before implementation.
- [Implementation commit](https://github.com/bombadil-labs/groovy-commutator/commit/829fe69816fb5e20136f562197510a21c476298a), pinned before evaluation.
- [Canonical result](../../results/masked_history_sensing_20260923.json),
  SHA256 `8657a55246180695a808efff14883661344883d3a04311c5dc9a77ba0a4fe326`.
- `python experiments/masked_history_sensing_20260923/verify.py results/masked_history_sensing_20260923.json`
  independently recomputes the finite claims; the source-hash registry is a
  separate fast provenance check. The gathering [draft PR #302](https://github.com/bombadil-labs/groovy-commutator/pull/302)
  retains protocol, code, evidence and failed P4 on main.
