# A retained trace can pay for a nearby change

**Exact under the declared oracle cost model.** Among useful inherited
constructions, all-width programs make revision cheaper than replacement
for 364 of 384 one-letter target changes at the primary prices. The mean
saving is 0.802 units. For larger literal changes it wins 91 of 1,056 cases
but costs 1.902 units more on average.

A one-letter patch costs three, a replacement eight, and the upfront trace
reserve four. Any single-transition revision advantage over replacement is
bounded by five minus the reserve, hence by one unit at these prices. The
high nearby-change win rate must be read alongside this small margin.

The [experiment](../research/2026-09-07-costed-primitives.md) and
[local-map audit](../research/2026-09-07-macro-local-equivalence.md) state the
bounds. This is an exact resource model with free oracle planning, not an
empirical learning law or a reason to preserve every construction forever.
