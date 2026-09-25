# Frozen order-image gate: one seven-bit causal cone

**Frozen before new evaluation.** Inspected main `bf938190b9c492e8017dd530bdf498d5b02caa4e`
(PR #311 integrated); no open issues or PRs. Motivation: the previous
finite-ring cycle comparison does not itself prove full-line equality or
difference of the composed *local maps*. Test the exact distinction, not
more recurrent statistics or a rule-space census.

## Fixed contract

- Binary ECA on the full two-sided 1D line; synchronous uniform rules.
- Fix the order pair `B=E_54`, `C=E_110`. For one fixed first rule `A`,
  compare `C∘B∘A` with `B∘C∘A` after exactly three source steps.
- Preselected prefixes: identity `E_204`; Rule 30 (the PR #311 witness);
  Rule 90 (simple additive, locally surjective control); Rule 54 (candidate
  nontrivial image filter); constant Rule 0 (erasing control). No extra rule
  may be added based on these results.
- **Primary:** enumerate all 128 seven-bit patches in ascending numeric
  order, with bit 3 the center and bit 0 the leftmost site. Record the
  Boolean difference table at the center, Hamming weight and first differing
  patch for each prefix. Equality of tables is an exact all-configuration
  full-line equality for these compositions; nonzero is a full-line witness.
- **Mechanism:** enumerate all 32 five-bit intermediate patches for
  `K_(B,C)(u)=C(B(u)) XOR B(C(u))` at the center. Record which of those
  patches can be the middle five bits after `A` acts on one seven-bit patch,
  and how many `K`-positive patches each prefix's image admits. The exact
  identity is difference-after-prefix `K_(B,C)(A(s))`.
- **Control/predictions:** Rule 0 should remove the discrepancy because
  both selected rules preserve all-zero states. Rule 204 retains the raw
  discrepancy; Rule 30 retains at least one witness from the saved n=8
  result. Predict Rule 90's five-bit local image is all 32 patterns; the
  result for Rule 54 is intentionally open. Preserve predictions even if
  they fail.
- **Independent check:** a scalar truth-table implementation on seven-bit
  source patches and a separate vectorized ring implementation on an
  11-cell ring must agree at its center for all 128 patches, for both
  all-zero and all-one exterior bits (radius three prevents outside impact).
  Compare actual output bits, not just XOR totals. Verify the identity via
  the enumerated intermediate patch.
- **Action:** publish one exact certificate and an explicit finite word
  witness or an all-128 equality proof for each prefix. If Rule 54 erases or
  partially filters a distinction, record the exact boundary without adding
  favorable prefixes. Otherwise stop with the negative. Neither result
  establishes a better dynamical controller or complexity measure; no
  additional orbit simulations, ring widths or schedule search follow.

The baseline is the directly fused radius-three truth table of each
three-step schedule. Counting a seven-bit read and three ECA evaluations
versus one fused seven-bit lookup is required before any efficiency claim.
The present unit makes no performance claim.
