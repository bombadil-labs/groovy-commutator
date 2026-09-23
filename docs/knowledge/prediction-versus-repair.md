# Predicting persistence can discard a distinction needed for repair

For Rule 54 on a periodic 12-cell ring, take the four phases of `(0011)^3`
and every one-bit injury to them. An external controller sees four encoded
three-bit blocks once, then chooses noop or one addressed bit flip. It must
restore the phase family by time four.

Exhausting all 4,140 block partitions gives a unique minimum two-label parity
view for predicting the entire passive target-membership future and a unique
minimum four-label adjacent-difference view for repair. The repair view also
predicts this target, while merging 26 pairs of complementary initial states.
It is not a refinement of the parity view: complementing three bits preserves
their differences and changes parity. The joint task can therefore be solved
without retaining the literal labels of its minimum predictor.

These are finite, grammar-specific minima. The target's full-ring membership
partition is already stable: no state outside the target can evolve into it.
The delayed repair task reduces to immediate error correction, not autonomous
regeneration. No endogenous goal, local embodied controller, recurring injury,
runtime benefit or infinite-line result is established.

[The exact comparison](../research/2026-09-23-prediction-repair.md) preserves
the contract, two-state obstruction, costs, failed larger-witness prediction
and independently implemented self-verification. A dynamically richer target
would require a new result, not a stronger reading of this one.
