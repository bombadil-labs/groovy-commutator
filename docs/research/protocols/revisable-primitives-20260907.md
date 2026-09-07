# Revisable primitives: frozen resource-accounting protocol

The [configuration](revisable-primitives-20260907.json) fixes the panel and all
prices before evaluation. This implements a bounded part of the
[revisable-primitives proposal](../2026-09-07-revisable-primitives.md).

## What is constructed

A four-letter word W in {A,B} becomes a callable macro. Calling it still
executes all four elementary CA ticks, but needs one dispatch rather than
four. Every system keeps access to primitive A and B. There is one macro
slot; preserving an editable construction record consumes an additional,
prepaid resource reserve. This reserve is charged whether revision is used
or not.

Before the change, eight independent jobs ask for transformation WW. After
it, K jobs ask for VV. Each job must work on **every** initial state of the
finite ring using a single open-loop program. We enumerate all inherited W
and all targets V rather than choosing helpful examples. The task changes;
the elementary dynamics does not.

A job can use at most eight physical ticks. We enumerate all 511 primitive
words of length zero through eight and compare their transformations exactly.
Equivalent programs may be shorter than the literal target. For a given
macro, dynamic programming finds the fewest dispatches that encode each
word. Cost is physical ticks plus d times dispatches. The macro does not
execute faster at the physical level.

## Four resource policies

All compilation costs include four units to write a specification and four
to construct it. Replacement costs the same eight units. A retained
construction record permits a patch at cost 1+2 times the number of changed
letters: one access, then one write and one construction unit per changed
letter. Full replacement is also available if cheaper. These are declared
prices of a toy machine, not measurements of real hardware or cognition.

| Policy | Inherited macro | Later management | Upfront trace reserve |
| --- | --- | --- | --- |
| Uncompiled | None | Use primitive operations | 0 |
| Frozen | W, costing 8 to compile | Keep W | 0 |
| Replace | W, costing 8 to compile | Keep W or replace for 8 | 0 |
| Revisable | W, costing 8 to compile | Keep W, patch, or replace | t |

The reserve t is charged before the target changes. Giving revisability a
free superset of choices would guarantee weak dominance under oracle planning;
t=0 is included as that structural control, not treated as a discovery.
Replacement also weakly dominates freezing because it may keep W at no cost.
The comparison of interest charges for the retained trace and includes the
uncompiled baseline. Same overall resource budget means different policies
may spend it on storage, management, or execution; it does not mean these
components are all free or identical.

The primary prices are d=1 and t=4, with K=4 changed-task jobs. Sensitivities
include d in {0,1,2,4}, t in {0,2,4,8}, and K in {1,4,16}. Keep ring widths and
literal unchanged/near/far task shifts separate. Also report whether the
inherited compilation paid for itself during the eight prechange jobs;
that distinction is defined before seeing postchange results.

## What this can establish

At d=0 a macro cannot improve execution cost: expanding it gives the same
primitive computation at the same physical cost. Any apparent physical gain
would be an implementation error. With positive dispatch prices, a history
can change which transformations fit a **total resource budget**, even though
it adds no elementary operation. We compare exact costs, not a scalar
measure of freedom or a claim of intrinsic adaptation.

The planner has complete dynamics and current-task knowledge and can optimize
without paying a search cost. No macro discovery or learning process is
modeled. Equivalent literal words, finite-ring coincidences, and the declared
resource prices may explain apparent revision advantages. The full data and
selected witnesses must make those limits inspectable.
