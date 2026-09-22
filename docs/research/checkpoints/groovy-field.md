# The Groovy Field: checkpoint

Updated 2026-09-22. Program page: [The Groovy Field](../2026-09-22-groovy-field-program.md).
Results: [census note](../2026-09-22-groovy-field-census.md).
Branch `claude/relaxed-shannon-o7cl11`; no PR opened yet (Myk decides).

## State

Stages 1–4 of the program are complete: Rule 110 repairs, the all-rule
census, one-step burn-in and the Rule 110 repaired system. The suite reruns
in about 25 minutes on four cores; every recorded verdict is certified except
108 memory-1 laws whose tables exceed radius 8 (marked decider-only).
Myk opened this program directly on 2026-09-22 and asked to skip protocol
ceremony; results are exploratory-exact, not preregistered predictions.

## Open questions, in priority order

1. **Towers.** The repaired systems are CAs on several bit-tracks. Does the
   Groovy field of a repaired system (componentwise XOR) again close with a
   small repair? Needs the decider generalized to multi-track, larger-radius
   sources.
2. **The 109 rules without a short-memory law.** Is there any finite memory,
   or a proof that none exists (the Rule 110 memory-3 witness suggests
   background-tail constructions)? A family of witnesses indexed by k would
   settle a rule.
3. **Beyond one-bit, radius-one repairs.** The universal repair keeps nearly
   the whole source. Is there a universal repair that forgets strictly more
   than the D0 bit, for example a background-and-phase marker of larger
   radius?
4. **Two-step burn-in** is censored by the 15M-edge cap for 118 rules; a
   leaner decider would be needed before interpreting it.

## Cautions

- Finite rings are only a consistency check here; Rule 110 shows they can
  agree unanimously and still be wrong about the line.
- "No law with memory ≤ 4" is not a no-go theorem.
- Retaining the source always closes; do not describe these repairs as
  compression.
