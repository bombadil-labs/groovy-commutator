# Protocol: perturbations around the six-cell Rule-90 encoding

Frozen before evaluation. Keep the ternary 2D interpreter and the code from
Research 015 fixed: rows (s,1), (0,1), (0,1 XOR s), repeated vertically.
Park the proposed exceptional role of three spatial dimensions. No dimension
comparison, Class-IV classification, or feedback-law intervention is included.

## Inputs and perturbations

Exhaust all 64 XOR masks on the six cells of logical block zero, bit index
2*y+j. Include zero and the matched logical-flip mask 33. For each mask use
two distinct physical interventions: repeat it in every vertical period, or
apply it only in rows 0..2. The latter is one finite defect in the infinite
2D field, not a height-three torus intervention. Compare each to its own
undamaged encoded background. No repairs or fitted observation frames.

Fine times are 0, 2, and 4 (stationary Rule-90 sampling). Exhaust all 512
assignments to logical input positions -4..4. For time at most four, every
possibly changed physical cell is in rows -4..6, columns -4..5 for an isolated
mask; periodic masks have the same horizontal bound and vertical period three.
Assess complete aligned blocks in rows -6..8, columns -4..5. That rectangle
covers the isolated defect's entire possible support and complete blocks.

The output rectangle's four-tick causal expansion is rows -10..12, columns
-8..9. Encode the nine logical input bits in that rectangle, initialize the
specified mask, and shrink the window at each physical update. This removes
all artificial boundary conditions. At earlier times crop to the same output
rectangle. Outside the affected support the field agrees with undamaged
evolution. Consequently validity and response claims cover every extension
of the nine-bit input to an infinite logical row. Periodic mode can use the
same rectangular computation; duplicate vertical periods are not independent
observations.

## Measurements

At each sampled time classify each mask/background as identical to undamaged
evolution, valid code with different content, or outside the code. Validity
means the WHOLE field is in the same global encoding E: all vertical copies
of each logical bit must agree as well as satisfying the six-cell code.
For isolated defects, unchanged vertical copies outside the finite affected
strip fix the logical content. Thus isolated recovery to this globally
periodic code necessarily equals undamaged evolution; locally valid blocks
alone are insufficient. Also record local block validity separately so that
this distinction is visible, not hidden by the global criterion.

For every mask count distinct full response fields across backgrounds and
total changed cells in the declared output rectangle. Counts over the 512
contexts use the uniform local-bit enumeration, not a claim about a natural
invariant measure. Report periodic and isolated modes separately.

Let delta_M = F^t(E(s) XOR M) XOR F^t(E(s)). For all 15 pairs of distinct
single-cell masks measure delta_(A XOR B) XOR delta_A XOR delta_B. Nonzero
means the pair response fails XOR superposition at this background and time.
This measures ambient nonlinear interaction, not gliders or logical gates.
Record the number of backgrounds with a nonzero interaction and its full-field
hash. For the repeated mask33, verify its response against encoding a logical
flip and Rule-90 evolution, independent of background.

## Audit and records

Save all 384 mask/mode/time aggregate records, response hashes, compact
per-background classifications, 90 pair-interaction records, source hashes,
and deterministic witnesses. Complete responses are reproducible from the
instruments; hashes refer to little-bit-order np.packbits of a C-order array
shaped (512 backgrounds, 15 rows, 10 columns).

An independent Boolean truth-set implementation must recompute every response
without importing the primary update/encoder. Check response hashes, local
and global validity counts, background dependence, and all pair records.
The exact horizon is four fine ticks; no claim of eventual healing or persistent
structures follows from a four-tick survivor. Any later horizon extension or
derived mechanism must be identified as a follow-up.
