# Resource addendum: phase-splice source recoders — 2026-09-09

**Status:** frozen after the parent protocol and before implementing or evaluating any Research034 frontier candidate.  
**Parent protocol:** `phase-splice-source-recoder-20260909.md`.

The parent protocol fixes candidate order and resource ceilings but does not prescribe the order of output-position identities inside one candidate. Because wall-time censoring can depend on that operational order, freeze it now:

1. for candidate `(t,k,j,delta,policy)`, list output positions `p in [-t,t]` outside the reinserted seed's future cone `[delta-j,delta+j]` first, in ascending order;
2. then list positions inside `[delta-j,delta+j]`, in ascending order;
3. stop the candidate at the first exact inequality;
4. if every position is equal, the candidate passes;
5. if the MDD node or seed-language wall-time ceiling is reached first, record censoring without changing this order.

This is only an evaluation-order choice. It does not prune a candidate, change the exact identity, alter the frozen `LR/RL` family, or add any scientific hypothesis.
