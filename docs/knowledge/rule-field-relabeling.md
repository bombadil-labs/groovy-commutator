# Local relabeling must transform table transport

For a fixed site mask c, transform the state by XOR with c and conjugate each local truth table by the three input masks and its output mask. Substitution proves that frozen-field evolution commutes with this relabeling when the decoder transforms too.

For the synchronous live-gated transport, the gate reads the decoded **old** state. A table copied from j to i must first be converted out of j's convention and then into i's. This proves exact equality of the decoded joint state/rule trajectory. Both updates use old arrays.

[The research account](../research/2026-09-10-rule-field-relabeling.md) separates this all-state proof from the archived seeded checks and finite orbit count. Plain transport differs in the supplied sample, while c=0 is an equality control. Convention-dependent popcount and quiescence statistics do not establish a selection mechanism.
