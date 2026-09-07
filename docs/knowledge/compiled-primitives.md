# Compiled primitives and their resource costs

A macro makes a sequence of existing operations callable as one instruction.
Its invocation can save dispatch work while executing every underlying
physical operation. Construction, storage, dispatch, physical execution,
inspection, and revision are distinct resource costs.

The [costed experiment](../research/2026-09-07-costed-primitives.md) uses one
four-letter macro slot, an eight-physical-tick job cap, and a prepaid reserve
for an editable construction record. These are declared toy-machine prices.
A trace is charged even when it goes unused; a macro does not get free
physical execution.

The oracle knows the dynamics and target and does not pay a search cost.
This definition therefore does not describe a learned skill or establish
that a new name for a construction creates a new physical operation.
