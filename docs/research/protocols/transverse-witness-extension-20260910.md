# Post-census supplement: extend every radius-one conflict to a full field

Date: 2026-09-10. Status at freeze: planned, not executed. The original transverse-difference census has completed unchanged:6 sources pass radius one,60 fail; the3-by3 periodic test supplies57 full-field conflicts and hides128,232,254. This supplement is an audit of a post-census proof, not an altered rule, observation, or rescue.

## Proof to audit

Each failed radius-one budget supplies two3-by4 source patches with identical nine observed vertical differences and different next central differences. Equality of those nine differences forces the XOR of the two source patches to be constant down each of the three columns. Repeat each patch with periods3 and4. Their entire difference fields are then equal, including the seam between the last and first row. The two causal windows for the next central difference are contained within the original patch, so their different certified outputs persist in the periodic extension.

Thus every radius-one conflict here supplies a full-field obstruction to any deterministic update on T alone. This implication uses the particular observation and complete causal windows; it is not a general upgrade of any failed local budget. Radius-zero conflicts are not upgraded by this argument.

## Frozen certificate replay

Use every failed radius-one first witness from the completed canonical census, in source-rule order. No witness search, selection by outcome, or modification is allowed. For each pair, independently decode the two words as3-by4 periodic fields; verify their XOR is column-constant and their complete T fields agree. Run one unchanged axial macro update using integer lattice passes and an independent Boolean local tree. Compare every output cell and both complete next T fields. Verify their central bits equal the original local witness and differ from each other.

Freeze this supplement and its verifier before replay. Save a separate canonical certificate artifact with the original census SHA-256, every pair and baseline mask, observed and next fields, and counts. Preserve the original census and its3-by3 results unchanged. Report the all-radius classification as the original exhaustive local audit plus this explicit extension proof and separately frozen validation supplement.
