# When should an inherited primitive remain revisable?

A constructed form can become a reusable operation in a later process.
Reuse may enable work that was previously too costly. It may also make the
construction's earlier assumptions difficult to inspect or change.

The open question is when retaining the ability to reopen, decompose, and
replace such a primitive preserves useful capabilities at an acceptable
cost. It is not assumed that revision always helps.

The [proposed comparison](../research/2026-09-07-revisable-primitives.md)
requires equal resources, explicit construction and revision costs, and a
predeclared environmental change. No experiment has yet measured the outcome.
A new macro name alone does not establish a new physical capability.
