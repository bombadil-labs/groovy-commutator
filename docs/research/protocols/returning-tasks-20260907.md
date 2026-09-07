# Returning tasks: frozen sequence extension

A revision that helps now may change the cost of an earlier ability when it
is needed again. This extension uses the
[all-width local kernels](../2026-09-07-macro-local-equivalence.md), retaining
all prices from the [costed comparison](../2026-09-07-costed-primitives.md).
Its [configuration](returning-tasks-20260907.json) is committed before running
the new task sequences.

Eight old-task jobs of WW establish the inherited construction. Then blocks
of VV and WW alternate for one, two, or four cycles. Each block contains one,
four, or sixteen jobs. There is still one macro slot. The editable trace
belongs to the current macro; changing back to an earlier macro is not free.
Its reserve is paid once, so repeated changes can amortize it differently
from a single transition.

Compare primitive-only and frozen baselines with replacement and revision.
For each adaptable library policy, compute a full-sequence oracle optimum
and two reactive policies. The reactive policies optimize only the current
block, with either lexicographic ties or a preference to keep the current
macro when tied. They know the current task and its duration, but do not use
subsequent tasks or learn the repeating schedule.

The oracle's advantage is therefore a hindsight/planning benchmark, not
proof that one learning algorithm is better. The comparison asks whether
local cost minimization and available revision options are sufficient to
preserve low costs over a sequence. Both positive and absent regret are valid
outcomes. Tie effects are declared in advance because a locally equivalent
choice can leave a different construction for the next block.

An exact dynamic program optimizes over the sixteen possible current macros.
For two blocks it must agree with direct enumeration of all 256 macro paths.
Selected paths are replayed with separate cost accounting. The one-transition
revision-saving bound generalizes conservatively to at most 10 times the
number of cycles minus the trace reserve: each cycle has two management
opportunities, each saving at most five units relative to replacement.
