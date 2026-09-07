# When does a useful shortcut become a constraint?

**Status: original proposal, now partly implemented.** The
[costed comparison](2026-09-07-costed-primitives.md) and
[all-width audit](2026-09-07-macro-local-equivalence.md) are complete. They
assume given constructions and oracle planning; learning, discovery, and
repeated transitions remain open.

The motivating question: A system can turn an expensive
construction into a reusable primitive. Does that inherited efficiency help
it adapt when conditions change, or make its earlier assumptions harder to
revise?

This is the next larger question in the
[history-and-possibility program](2026-09-07-history-and-possibility.md).
The immediate [future-repertoire probe](2026-09-07-future-repertoire.md) measures
options under fixed actions. This proposal would let the available effective
actions themselves develop.

## Candidate comparison

Begin with the same elementary operations, resource budget, tasks, and initial
conditions. Allow repeated successful constructions to become callable
primitives. Compare a policy that freezes a compiled primitive with one that
permits later inspection, decomposition, and replacement.

Use a common first environment, then a predeclared change in tasks or resource
conditions. Measure initial performance, adaptation cost, retained abilities,
and newly reachable tasks. Include a baseline that retains the original
operations without compiling and a control that permits replacement without
giving access to the primitive's internal construction.

## Fairness problems to solve before freezing a protocol

- Count construction, copying, storage, invocation, inspection, and revision
  costs. Calling a large macro once is not free physical execution.
- Keep total resources and library capacity equal. If one arm simply receives
  a strict superset of free actions, a larger reachable set is built into the
  setup and is not an experimental discovery.
- Permit both arms to train for the same budget. Separate the cost of learning
  a shortcut from the cost of using it.
- Define novelty through held-out tasks and explicit capability tests. A new
  name for an old operation is not automatically new capability.
- Distinguish changed descriptions from changed physical processes. A macro
  can shorten a description without changing the executed elementary actions.
- Specify the environmental change before inspecting comparative outcomes.
  Test cases where revision is useful, unnecessary, and costly.

## What would change our view?

Revisability may preserve capabilities at a measurable cost. It may confer no
advantage when old primitives remain adequate. It may be too costly or permit
harmful loss of useful structure. These are all legitimate outcomes.

The motivating idea is that forms can become useful ground without becoming
immune to inspection. This proposal does not assume that continuous revision
always wins, or that a computational benchmark settles the ethical question
of who should control a relationship's future terms.
