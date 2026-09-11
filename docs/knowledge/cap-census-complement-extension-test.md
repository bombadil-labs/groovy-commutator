# Extend the cap census to R ≤ 6 on the cells that disagreed with their complements

Completed 2026-09-11. Frozen protocol, verifier committed before evaluation, single deterministic run, CI replay. On all 22 differing `(rule, h)` cells: reproduction of the saved census at `R ≤ 2` exact; caps exist on both sides, every former `None` passing at radius 3; the post-hoc bound `mpr(r̃,h) ≤ max(mpr(r,h), h+1) + h(h+1)/2` holds; the observed shift never exceeds `h + 1` (values 1 or 2). See the [extension note](../research/2026-09-11-cap-census-complement-extension.md).
