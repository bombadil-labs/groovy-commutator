# The complete Rule-54 G field retains the repair decision

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Exact information-sufficiency result on one finite ring, not a cheaper or local controller.**

## Question and frozen comparison

The [previous route gate](2026-09-24-rule54-glider-route-gate.md) found 68
injuries that a one-site hold rescues, and observed afterward that holding
the originally injured address matches the full-state maximum. We asked
whether the causal, *reference-rule* G field at the two-step decision time
loses a distinction needed to choose the hold. This information gate comes
before searching for a distributed local policy.

The [protocol](protocols/2026-09-24-rule54-g-sensor-gate.md) fixed the
source result, 34-cell ring, 1,156 trials, time-eight route target, and
35 possible actions unchanged. It defines
`G54(s)=E54(s) XOR E54(E54(s)) XOR E54(s XOR E54(s))` on the current state
**before** the action. Each observer picks one action for all trials that
look identical to it; the exact domain score adds each observed fiber's
best action count. This is an oracle-calculated information ceiling, not
a trained policy on new states.

| Observation at time two | Distinct observed words | Best successes / 1,156 |
| --- | ---: | ---: |
| No observation, fixed action | 1 | 340 |
| Entire raw current state | 1,054 | 408 |
| Entire reference-rule G field | 850 | **408** |

Our prospective P1 predicted that G would lose at least one of the 408
successes. **P1 failed.** It merges distinct current states without
making any of this task's successful action choices incompatible. P2, that
deterministic G cannot outperform the raw state from which it is computed,
holds by direct factorization and is verified on this finite domain. The
result does not identify a local decision rule, infer the injury site in
general, or establish out-of-domain accuracy.

## What the apparent compression costs

Both full-field observations require access to all 34 current source bits.
Raw readout needs no additional Rule-54 update; calculating G from this
snapshot requires three full-ring Rule-54 evaluations and intermediate
fields/XORs. **Cost clarification after the local follow-up:** the first
`E(s)` evaluation can be shared with the next physical update if that
output is available before selecting the hold; this leaves two *additional*
passes, rather than three additional passes. A central selector must still
communicate a hold/noop flag
and one of 34 addresses (six bits suffice) and gather information across
the ring. Using a literal 34-bit key and six-bit action per observed word
would give uncompressed tables of 42,160 bits for raw states and 34,000
bits for G states. These are **not** minimal circuit sizes or total resource
costs, and a local G cache cannot be treated as free to initialize or
maintain. Fewer observed words do not establish a computational advantage.

The next justified question is a separately frozen local interface: does
any G-based site selector achieve a useful repair score with less *total*
source access, computation, controller state and address coordination than
a raw local selector with a matched footprint? Each `G_i` depends on at
most five current raw bits (radius two); a raw site selector with those
same five bits can compute exactly the same feature. A benefit would need
to survive this baseline and all acquisition and maintenance costs. If
the raw controller ties at equal or lower cost, park the proposed G-specific
advantage. Do not enlarge the seed, scan other ECAs or relabel the task to
manufacture one.

## Evidence and boundaries

- Inspected main: `88abe0bc02835b987619202d6484ff4e26ada556`.
- Frozen protocol on gathering branch: `749e694dbacae5986de698cfe2ee812d6b9b7d42`.
- Pinned runner and independent bit-parallel G verifier:
  `fcabee9be1a1f1d3db4e9bcaee07fb1af7fe3528`, before evaluation.
- New [canonical result](../../results/rule54_g_sensor_gate_20260924.json):
  SHA-256 `b2ebab4806922360f570b39ce0f1701df4a90cfc3704b8239bc671e604c661af`.
  It binds the unchanged earlier result SHA-256
  `b390b49d3506b5e78e45fbcbd3de710bdcad60b3b0a6d21054e1dc276d166f75`.
- Run `python experiments/rule54_g_sensor_gate_20260924/verify.py
  results/rule54_g_sensor_gate_20260924.json` for the independent G and
  observation-fiber audit; run `python scripts/check_result_integrity.py
  results/rule54_g_sensor_gate_20260924.json` for provenance coherence.

The outcome labels come from the previous exact route evaluation, whose
own independent verifier separately checked all 40,460 action outcomes.
Our independent bit-parallel evaluator rechecks G and the exact observation
groups. Neither script constitutes an independent peer review. The ring
adaptation remains a one-shot finite target inspired by published glider
encodings, not a glider-persistence proof or a Class-IV result.

**Subsequent local decision:** the [frozen one-trigger gate](2026-09-24-rule54-local-sensor-gate.md)
found that `G_i=0/1` never uniquely selects a site, while one raw
five-bit source pattern rescues 34 further trials under identical
address arbitration. The complete G field remains sufficient in the
original information sense; a one-bit G trigger is insufficient in
this specified local policy grammar.
