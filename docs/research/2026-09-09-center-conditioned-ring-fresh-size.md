# The Rule-54 overlap lead resolves into a period-four crystal

A fresh-size transfer test was preregistered after the exploratory `4x4` center-conditioned rule-ring discovery. The six ordered rule-orbit pairs were frozen exactly as discovered:

`(14,31), (39,54), (54,39), (85,170), (91,41), (187,17)`.

They were then tested without retuning on periodic `5x5` and `6x6` fields.

## Result

No frozen pair has a valid `5x5` field.

On `6x6`, only two pairs survive:

| pair | valid fields | geometry |
| --- | ---: | --- |
| `(85,170)` | 2 | the two checkerboards |
| `(187,17)` | 4 | alternating full rows or alternating cells in every row |

The pairs containing Rule 54 have no valid `5x5` or `6x6` fields.

The exact row-transfer solver is `scripts/experiment_center_conditioned_ring_fresh.py`; the frozen protocol is `protocols/center-conditioned-ring-fresh-size-20260909.md`.

## The transfer graphs explain the discovery

The fresh result is not merely a size-specific disappearance. Inspecting the exact row-pair transitions shows that the entire exploratory `4x4` family is crystalline.

- `(85,170)` supports the period-two checkerboard and therefore survives even sizes.
- `(187,17)` supports period-two horizontal/vertical stripe patterns and therefore survives even sizes.
- `(14,31)` has a four-step row cycle built from all-zero/all-one rows, so square fields require height divisible by four.
- `(91,41)` has the analogous four-step row cycle built from alternating rows, again requiring the appropriate period-four commensurability.
- `(39,54)` and `(54,39)` require horizontal period four; their `4x4` witnesses can tile any size divisible by four, but not widths five or six.

Thus Rule 54 appeared in the exploratory `4x4` census because one of its ring geometries participates in a **period-four spatial crystal**. There is no evidence here that its Class-IV dynamics are responsible.

This is exactly the kind of false-positive the fresh-size protocol was meant to detect.

## Inherited selector dynamics

The surviving `6x6` structures are also simple under the existing selector:

- both `(85,170)` checkerboards leave the frozen center-conditioned family after one step on either selector axis;
- all four `(187,17)` stripe fields remain in the same pair on a horizontal period-two selector cycle, but leave after one vertical step.

The persistent cases are therefore short periodic crystals, not complex higher-dimensional rule ecologies.

## Consequence for the Class-IV hypothesis

This particular interpretation of dimensional closure is falsified as a Class-IV discriminator.

Neither

1. storing the same rule ring at every site up to physical orientation, nor
2. allowing a center-conditioned pair of stored rule rings

produces the hoped-for signal. The first collapses to Rules 0/255; the second produces only small-period crystals.

This does **not** falsify the broader dimensional-projection idea. It falsifies the assumption that the projected rule must be redundantly stored in every overlapping Moore neighborhood of one 2D configuration.

That assumption may be stronger than the user's intended question. The next formulation should return to the original dimensional observation itself: the lower-dimensional truth table occupies the boundary of one higher-dimensional neighborhood, and we should ask whether the *resulting boundary-to-boundary transformation* can be recognized as a native next-dimensional rule without requiring every site to carry a complete copy of the lower-dimensional program simultaneously.

In other words, the next target should be **rule transformation across dimension**, not static rule-field tiling.
