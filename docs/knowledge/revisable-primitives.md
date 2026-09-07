# When should an inherited primitive remain revisable?

A construction can become a reusable operation in later activity. Reuse may
enable work that was too costly, while making earlier assumptions difficult
to inspect or change.

**Partly answered, 2026-09-07.** A
[costed oracle comparison](../research/2026-09-07-costed-primitives.md) and
[all-width audit](../research/2026-09-07-macro-local-equivalence.md) show a
narrow benefit for nearby changes under specified resource prices. The
retained trace can cost more than replacing the construction. Macros do not
add physical operations when their full execution is charged.

The [returning-task experiment](../research/2026-09-07-returning-tasks.md) now
shows how a locally cheap revision can increase a returning task's cost, and
how repeated changes can repay the trace. Open questions include learning
useful primitives, paying for search, and changing the operation vocabulary. The
[original proposal](../research/2026-09-07-revisable-primitives.md) remains
a source of those questions. No conclusion about ethical alignment follows
from the finite cost model alone.
