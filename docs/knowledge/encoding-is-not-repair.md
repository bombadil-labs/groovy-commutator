# Restoring a valid encoding need not restore its content

A matched logical flip acts on every differing cell of its codeword. A single
physical cell flip can instead leave the encoded family. In the tested Rule-23
two-row code on a 2x7 torus, 28 of 128 logical initial states return to valid
code after four ticks of a fixed one-cell perturbation; only 18 agree with the
undamaged evolution. Ten regain valid form with changed logical content.

These are finite periodic damage tests, distinct from the exact preservation
of arbitrary sequences of matched logical actions. See the
[experiment and witnesses](../research/2026-09-08-column-compatibility.md).

## Update, 2026-09-08: isolated defects in the Rule-90 code

The [finite-cone experiment](../research/2026-09-08-encoded-defects.md) removes
the tiny-torus limitation for isolated perturbations of the new six-cell code.
None of the initially invalid periodic or isolated mask/background cases
returns at sampled fine times two or four. Local block validity is also
distinguished from agreement among the global code's vertical copies.

This adds a bounded non-recovery result, not a contradiction of the earlier
Rule-23 examples: the code, intervention, and ambient geometry differ.
