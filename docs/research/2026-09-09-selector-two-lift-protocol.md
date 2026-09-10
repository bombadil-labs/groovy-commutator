# Frozen two-rail selector protocol

Frozen on 2026-09-09 before the numerical census. This is a control construction for the [dimensional program](2026-09-09-dimensional-closure-program.md), following the [correction-coordinate note](2026-09-09-correction-future-coordinates.md). No Wolfram-class labels enter construction or selection.

## Question and scope

Can one explicit local program constructor retain every source instruction, remain well typed through two lifts, and preserve dynamics on a globally consistent geometric encoding?

Here a program becomes **static routing instructions**, not eight mutable truth-table cells. This weaker test is intentional and declared before evaluation: passing it will establish a recursively typed routing control, not settle the original shared-state/program conjecture. The constructor also does not claim to realize the ternary L/R/C roles.

## Frozen grammar

Let G_1 be the 256 binary radius-one ECA programs, with address q = 4l + 2c + r and output bit (rule >> q) & 1. Define G_(d+1) = { Rail(p) : p in G_d }. One constructor, one binary alphabet, radius one, one tick per source tick; no clock, tags, changing block size, or additional internal state.

If p denotes F on d-dimensional configurations, Rail(p) denotes H on dimension d+1:

    b = F(central d-dimensional slice)(x)
    H(X)(x,k) = X(x,k+1) if b = 0, else X(x,k-1).

The source program is executed as the routing control; its two terminal values become instructions to read the positive or negative new-axis neighbor. Recursion preserves this exact syntax. No source-specific fitting is permitted.

## Frozen spatial encoding and resource budget

    E_d(S)(x,k) = 0 for k > 0,
                 S(x) for k = 0,
                 1 for k < 0.

Decode by restricting to k = 0. The source-dependent preparation radius is zero: no future trajectory, derivative tower, or nonlocal function of S is prepared. Two infinite homogeneous half-spaces and a distinguished interface are supplied. This is an interface encoding, not a translation-equivariant block encoding in every target direction, a finite-support encoding, or an intrinsic-simulation claim.

All sites, including the background, subsequently obey the same autonomous CA. Background layers are not externally clamped. Periodicity may be used within source directions, never across the two opposite transverse backgrounds.

One source bit flip is encoded by flipping the corresponding interface site. Through two lifts it is a single-site flip at the intersection of the two interfaces. No robustness to arbitrary background damage is presumed.

## Deductions to audit

These predictions follow algebraically from the fixed definitions, before enumeration:

1. Both lifted local-map families retain all 256 source programs distinctly. Setting the new positive/negative neighbors to 0/1 recovers the preceding program pointwise, so changing any source table bit has a witness at each level.
2. H E_d = E_d F for every source configuration if and only if F(0) = 0 and F(1) = 1, where these denote uniform configurations. For ECA this predicts exactly 64 rules: bit 0 = 0, bit 7 = 1.
3. Every H = Rail(F) preserves both uniform configurations, regardless of F. Consequently every first descendant passes the second interface, on arbitrary two-dimensional fields. Full source-to-second-descendant commuting chains still require the first interface and therefore number 64.
4. The same implication gives all further lifts for any source that passes the first interface. This is a theorem to prove, not an extrapolation from two finite grids.
5. The two failed endpoint conditions have concrete one-tick witnesses on the background layer adjacent to the interface. A correct data plane alone is insufficient for preservation of the full encoding.

## Fixed computational checks

Use a dependency-free JavaScript audit with deterministic, recursively sorted JSON output.

- Enumerate all 256 sources on all 32 effective five-input patches at the first lift and all 128 seven-input patches at the second. Compare an AST interpreter with direct scalar multiplexer formulas.
- Verify distinct truth tables at both levels and counterfactual witnesses for each of the eight source instructions.
- Enumerate first-interface one-tick comparisons on all eight source neighborhoods at transverse positions -2 through 2. Enumerate second-interface comparisons on all 32 effective source neighborhoods at the same five transverse positions. Compare complete encoded patches, including both adjacent background layers.
- Test four evolving ticks for every successful first-interface rule and all 32 states on a source ring of width five. Use an initial transverse interval [-5,5], shrink it by one site at each step, and compare every remaining site with the encoded source evolution.
- Test three evolving ticks for every first descendant and all 512 states on a 3 by 3 source torus. Lift into an initial interval [-4,4], shrink after each tick, and compare every remaining site. This tests the second interface on arbitrary two-dimensional source fields, not merely images of the first encoding.
- Test the full composed encoding for all successful source rules and all width-five source states through four ticks on initial transverse square [-5,5]^2, shrinking both open directions after each tick. Repeat with one matched source/site flip before each tick, at horizontal coordinate t modulo 5.
- Do not change the grammar, encoding, pass criteria, or census bounds after results. Any implementation correction or protocol deviation must be recorded.

## Reporting rule

Publish the exact if-and-only-if proof, the endpoint failure witnesses, the complete passing-rule list, reproducible audit output, and the distinction between recursive routing syntax and active mutable program data. Do not infer a dynamical-class discriminator, a preferred dimension, or impossibility for other encodings from this test.
