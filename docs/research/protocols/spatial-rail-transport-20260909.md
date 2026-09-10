# Frozen extension: state-gated transport of spatial Rail programs

Date: 2026-09-09. Frozen after the retained-program audit passed and before this extension is evaluated. The original protocol, script, and result are retained unchanged. This extension is motivated by the existing nonuniform source model, not by a dynamical class.

## Single change to the complete logical dynamics

Retain exactly the same native Rail grammar, data update, five-symbol layout, radius-nine geometry, and separate guard g=204. Replace program retention by

    P'_x = P_(x-e1) if S_x=1, else P_x.

Data and programs update simultaneously from the old state. The new rule transports complete eight-bit program words; it does not modify the fixed Rail wrapper syntax.

## Uniform physical program-cell update

Keep the previous data-cell update and blank retention. At a P cell z:
- inspect z-j e_d for j=1,...,8;
- if exactly one of those sites has a D tag, it is the owner datum;
- if that datum is D1 and z-9e1 has a P tag, copy that neighbor's program symbol;
- otherwise retain the center P symbol.

On the canonical layout the owner is unique and all eight bits of one word see the same old datum. They therefore move coherently. This rule is defined for malformed fields as well, without an error-correction claim. The radius remains nine.

## Prediction and proof obligation

The separate guard program is spatially constant within every guard layer, so copying its left neighbor retains it for either data value. On the central data interface, both program and state dependencies are exactly the source dependencies. Therefore the complete programmed dynamics should commute through both lifts, including autonomous program transport and finite matched payload edits.

More generally the guard must be stable under the declared program update on both uniform data backgrounds, in addition to providing the needed state selectors. Failure of that joint condition would be a failure of this guard architecture, not of all spatial-program lifts.

## Frozen audit

- For dimensions 1,2,3, all eight program slots, both own/left payload bits, and both owner data bits: exhaust the physical program-cell update (192 local cases).
- Check missing/multiple owners, bad neighbor types, and blank retention.
- Test 16 deterministic heterogeneous width-five source fields through four ticks, comparing complete physical source/first-lift/second-lift fields after each tick. Apply one local data edit and one local instruction edit before each tick.
- Test 32 deterministic arbitrary 3-by-3 two-dimensional source program/data fields through three ticks and a third-dimensional lift, with the same matched action rule.
- Initialize enough open transverse guard layers to retain core [-2,2] after shrinking. Compare every retained data/program symbol and the canonical blank complement.
- Record autonomous program changes separately from external edits, and require at least one autonomous change in each field-audit family.
- Keep the retained-program audit as the exhaustive data-law check. Save a separate canonical JSON result and reproduce both in CI.

No program synthesis, unrestricted self-modification, marker self-organization, optimized storage, or binary radius-one result is claimed.
