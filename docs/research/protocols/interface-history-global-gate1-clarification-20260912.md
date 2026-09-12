# Gate-1 clarification: full-field interface-history witness ordering — 2026-09-12

**Status:** binding pre-implementation clarification to `interface-history-global-20260912.md`. No verifier or source-domain execution exists at this clarification.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Independent review:** Claude Code / Fable 5.1 approved the integrated protocol at `651ba1f574fcc2dca6bc8b130e11cbe7e5efac6c` with this one binding clarification required before the verifier commit; the reviewer explicitly stated that recording this clarification does not require renewed Gate 1.

This file is a binding supplement to Section G2 of `docs/research/protocols/interface-history-global-20260912.md`. It changes no source family, coordinate, mask, history depth, domain, determinism criterion, prediction, or interpretation ceiling. It only makes the already-required canonical witness ordering explicit.

For every conflicting global cell, canonical source records and witness details are ordered as follows:

1. **Source-record order:** for a fixed ring, domain, history depth and mask, each exhaustive source record is keyed by the tuple `(t, source_pair_lex)`, ordered first by coarse time `t` and then by the predecessor unit's frozen lexicographic source-pair order. There is no logical-site component in the global-record key.
2. **Conflicting pair:** among all ordered pairs `(record_1, record_2)` that share the same complete retained-history key but have different next complete retained fields, retain the lexicographically smallest ordered pair under the source-record order above.
3. **First differing site:** compare the two next complete retained fields in increasing ring-site index and retain the first site at which they differ.
4. **First differing symbol coordinate:** within that site, use the predecessor's coordinate ordering: history lags oldest to newest, and within each retained symbol use `A, B, E0, E1, E2, E3`, skipping masked `E` coordinates. Retain the first differing coordinate in that order.

The implementation and canonical result must cite both the main protocol and this clarification. Any later change to this ordering is a material witness-ordering change and requires renewed independent Gate 1 before affected evaluation.
