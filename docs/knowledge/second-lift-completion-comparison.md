# Rule32's inherited second-lift tuples close at radius one through depth two

**Status: completed exact bounded experiment.** The [frozen protocol](../research/protocols/second-lift-completion-comparison-20260910.md) was implemented before primary evaluation and is reported in the [result note](../research/2026-09-11-second-lift-completion.md).

For both H128/H160 completions, both K/O coordinate systems and every tested depth `h=0,1,2`, the inherited Rule32 first-image family conflicts at `R=0` and closes at `R=1` and `R=2`. Thus the minimum local cap radius is exactly one throughout the frozen second lift, while the represented tuple cost grows from 2 to 4 to 6 bits per site. All 36 full-four-symbol ambient controls conflict through `R=2`.

The theorem-backed completion comparison behaves as expected: inherited O tables are literally identical across H128/H160; K tables can differ while exhaustive local triangular recodings preserve the fixed-depth whole-field fibers and the same minimum radius. On the finite `n=8` inherited diagnostic, 255 distinct first-image states map to 254 tuple states at every tested depth, leaving one size-two fiber under the uniform-distinct-state measure.

Scope: Rule32, one inherited family, two completions, K/O, `h,R≤2`. The spatial lattice remains one-dimensional; this is product-alphabet correction closure, not a new spatial dimension. Ambient failure is bounded to radius at most two.
