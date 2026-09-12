# Research CI cost boundary — 2026-09-12

**Status:** repository process policy, not scientific evidence.

At Myk's direction, long scientific evaluations and byte-for-byte result replays are no longer routine GitHub Actions work. Automatic pull-request and main-branch CI keeps the fast provenance-integrity tier and bounded smoke/publisher checks. A research run or replay expected or observed to exceed about ten minutes is performed outside GitHub Actions from the pinned implementation and recorded in the unit's provenance; an expensive manual Actions dispatch is exceptional and requires explicit authorization.

This changes execution plumbing only. It does not alter any frozen protocol, canonical result, evidence label, or review requirement. Expensive Actions jobs already running when this policy was stated may finish, but they are not a precedent for automatic reruns. Existing expensive workflows are to be converted before their next execution.
