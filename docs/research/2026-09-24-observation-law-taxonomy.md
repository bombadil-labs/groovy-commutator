# Observation, laws and rule choice: a working taxonomy

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Status: definitions and research questions, not a new experiment.** This is
the maintained map for asking whether a description has dynamics of its own
and whether that description can help choose future dynamics. The
[current research direction](START_HERE.md) decides what work to schedule;
entries here do not queue a census or a fourth Groovy generation.

## The common contract

Fix a source state space `X`, a synchronous rule `E: X -> X`, and an
`E`-invariant declared domain `A` (possibly all source configurations). An
observer `O: A -> Y` keeps some distinctions and erases others. A proposed
update `F: Y -> Y` is a **factor law on A** when

```
                 O(E(S)) = F(O(S))                 for every S in A.    (1)
```

On `O(A)` the law, if it exists, is fixed by (1); values outside that image
are *completion choices*. A present-only local CA law, a law with stored
history, and a set-theoretic function are different claims. Specify the
geometry, locality/radius, boundary, cadence, memory and domain each time.
If `A` is not invariant, (1) supplies at most a one-step readout until a
separate continuing-domain claim is established.

For Boolean configuration fields, a **candidate-law residual** is
`R[E,O,F](S) = O(E(S)) XOR F(O(S))`. Its zero set answers whether this one
candidate works. Without a candidate, the **intrinsic closure obstruction**
is a pair of valid states with `O(S)=O(T)` but `O(E(S)) != O(E(T))`.
Such a pair rules out *every* present-only deterministic factor law on the
declared domain, regardless of radius. If no pair exists, an induced
set-theoretic law exists on `O(A)`; locality still needs proof. Finite-ring
certificates and infinite-line assertions must be kept separate.

## Objects we must not conflate

| Name | Choices / question | What a result establishes |
| --- | --- | --- |
| **Same-rule Groovy residual** `G_E` | `D_E(S)=S XOR E(S)`, `O=D_E`, candidate `F=E`; `G_E=R[E,D_E,E]`. | `G_E=0` on `A` means *the original* `E` advances the change field on `A`. Nonzero `G_E` rejects that candidate, not every effective law. **G is the residual, not O.** |
| **Observer closure** | Fix `E,O,A`; ask whether *some* `F` satisfies (1), with a declared locality and memory contract. | An exact law is unique on the reachable image. A conflicting indistinguishable pair disproves present-only closure. |
| **Law extension** | Given the forced action of `F` on `O(A)`, choose its unforced local table entries elsewhere. | Extensions that agree on the inherited image describe the same observed source trajectories, but may yield different answers when another operation queries off-image states. |
| **Recursive native Groovy field** | Start `O_0=identity`, `F_0=E`; form `O_(n+1)=G_(F_n) composed with O_n`, then seek `F_(n+1)` satisfying (1) for `O_(n+1)`. | Each generation is relative to a specified law and its completion. Closure on inherited fields need not hold on arbitrary configurations of `F_n`. A history-valued `O_n` needs its own typed state and update. |
| **Driven rule schedule** | `S_(t+1)=E_(r_t)(S_t)` with externally specified `r_t`. | The schedule supplies a clock/program. A period-`p` sequence has a radius-at-most-`p` stroboscopic composition for radius-one rules; intermediate steps also require phase. This is a new system, not a factor of an unchanged `E`. |
| **Observation-controlled rule choice** | Store a rule label `q_t`; advance `S_(t+1)=E_(q_t)(S_t)` and choose `q_(t+1)` from an observation available by time `t`. | This feeds a description back into source dynamics. Declare global versus local selection, observation/acquisition work, selector memory and access cost. Local selectors become an ordinary fixed multitrack CA when labels are included in the state. |

For an affine Boolean evolution `E(S)=L(S) XOR b`, direct expansion gives
`G_E(S)=b=E(0)` for every source. Thus the centered value
`G_E(S) XOR E(0)` is the polarization/additivity defect along `(S,E(S))`;
the raw residual also contains an affine offset. Neither is a universal
complexity statistic or a quantum uncertainty relation.

**Small counterexample to a tempting shortcut.** Rule 255 always outputs
ones. Its change observation `D_E(S)=NOT S` is invertible, so its exact
observed law is the constant-zero rule; yet `G_E(S)=1` everywhere because
applying the *original* constant-one rule to a change field is wrong. See
[representation case A](representation-case-studies.md). This distinguishes
wrong-law disagreement from information loss.

These completed cases anchor different rows of the taxonomy:

| Existing case | What was established | What it does not establish |
| --- | --- | --- |
| [Rule 255](representation-case-studies.md) | A nonzero same-rule residual coexists with an exact, different effective law for `D_E`. | Nonzero `G_E` does not imply loss of observer closure. |
| [Rule 30](2026-09-22-groovy-field-census.md) | The `G_E` field has a local law when three consecutive G rows form the observer state. | The [six-bit next-G readout](2026-09-23-observation-discovery.md) alone is not an autonomous field, and history closure does not supply a one-row rule. |
| [Rules 2/16](2026-09-23-groovy-1d-third-generation.md) | Specific completed inherited 1D chains reach a nonconstant third G. | Other completions fail or remain unresolved; the source becomes a rigid translation after one step. |

## Where the rule-space branches

For a valid field `y` under an effective law `F`, expansion gives

```
G_F(y) = F(y) XOR F(F(y)) XOR F(y XOR F(y)).                (2)
```

The first two `F` evaluations follow inherited trajectories if `F` advances
the image `Y_in=O(A)`. The argument `y XOR F(y)` in the third term need not
belong to `Y_in`. Its local neighborhoods may query unspecified table entries.
When this happens, changing those entries can change the next Groovy field
without changing any original observed trajectory. Membership of
`y XOR F(y)` in `Y_in` is a sufficient way to avoid this particular
off-image ambiguity, not a necessary one: the needed local entries might
already be forced even when the whole configuration lies off-image.

Therefore a proposed “trajectory through rule space” is a graph of **typed
observation/law/extension choices**, not an unqualified list of ECA numbers.
Quotient extensions by their action on inherited trajectories before counting
distinct dynamics; then record whether their *next* observations still agree.
The [Rule-2/16 recursion](2026-09-23-groovy-1d-third-generation.md) already
shows completion-sensitive third-generation closure. Its all-source exact
positives do not establish richer long-term behaviour: those source runs
translate rigidly after one update. The
[Groovy-field census](2026-09-22-groovy-field-census.md) establishes separate
present-only and history-bearing cases, not a single universal 1D rule chain.

The rule graph can *suggest* switching candidates, but an edge `E -> F`
derived from `F(O(S))=O(E(S))` says nothing by itself about applying `F` to
the **base** state. Likewise, a closed observed `G` is a report of the
original dynamics until a specified selector feeds it back.

## A proposed construction question, not a Class-IV claim

Could a small, causal `G`-guided selector sustain mobile structures and
interactions better than the same rules on a fixed schedule? Specify the
behavioural target independently of searched examples. Compare single rules,
periodic/open-loop schedules, and a fixed CA with the same tracks, locality
and memory. Charge the clock or selector, G acquisition, initialization,
updates and storage. A future-dependent `G` computed from a rule that has
not yet been chosen makes a circular policy; use a declared reference rule
or an already available lagged observation. If changing the rule changes
which derivative is meant, explicitly define that time-dependent derivative.

This is a **design question**, not an empirical finding or a definition of
Class IV. An externally supplied rule sequence can carry the organization
being sought. The sharper question is whether a local observer/selector can
maintain the condition for its own future rule changes, under fair baselines.
No search is scheduled until an operation, target, resource bound and
negative-result stopping decision are written down.

Temporally switched CA and memory-enriched ECA have existing research
literatures; changing the rule or adding a clock is not itself a novelty
claim. See [Paul and Das on temporally nonuniform CA](https://arxiv.org/abs/2411.17421)
and [Martínez, Adamatzky and Alonso-Sanz on CA with memory](https://arxiv.org/abs/1406.2277).

## How to extend this page

For each new case, record: (1) source rule and domain, including line versus
ring; (2) observation and its acquisition cost; (3) target/cadence/horizon;
(4) effective law, memory, radius and forced-versus-completed table entries;
(5) exact witness, proof or finite evidence with a dated link; (6) whether a
rule choice is external or locally available; (7) matched baseline and stop
condition. Add a new row only when it asks a genuinely different question.
Put protocols, results and failed predictions in dated notes; link them here
without relabeling a timeout as impossibility or a completion-dependent
branch as source-forced. Update [START_HERE](START_HERE.md) only when the
research priority actually changes.
