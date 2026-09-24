# Frozen protocol: can a one-step G observer invent a cycle?

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
Freeze this file on the gathering branch **before** implementing and
evaluating the experiment. Do not alter predictions or expand bounds in
response to results. Link any correction as a dated amendment.

## Question and domain

Source: synchronous ECA Rule 30, `f(l,c,r)=l XOR (c OR r)`, periodic ring of
exactly **six cells**, all 64 binary source configurations. Site `i` uses
neighbors `(i-1,i,i+1) mod 6`; encode a ring by integer `0..63` with cell
`i` in bit `i`. No burn-in. `D(s)=s XOR E(s)` and the whole-field observer is
`g(s)=D(E(s)) XOR E(D(s))`. It is the original source G, not a descendant G
under an independently completed effective rule.

For each source `s` create one boolean graph edge
`g(s) -> g(E(s))`, retaining an example source for each edge. Include edges
from transient states: that is the whole point of testing a one-step
observer graph. Node names are six-bit whole-field integers. Let `A` be this
boolean adjacency matrix over the realized `g` images, in ascending order.
For each `k=1..6` record `C_k=tr(A^k)` (rooted closed observed walks).

Decompose the full 64-state source transition map into directed cycles and
transient trees. A true observed `k`-periodic word is a rooted length-`k`
word that occurs forever along **one source cycle**, including rotations
and allowing source cycles longer than `k` if their observed word has a
period dividing `k`. Count the distinct such words as `R_k`. Report
`P_k=C_k-R_k`, plus counts of source cycles, source transient states,
observed graph nodes and boolean edges. If any `P_k>0`, save the
lexicographically least **primitive** phantom word at the smallest such
period (canonicalize rotations), its one-edge source witnesses and the
list of all real source-cycle observed words. If a phantom word first
appears as a repetition, save its primitive root and verify it is phantom.

Controls: (a) identity observer `O(s)=s` on the same map must yield
`P_k=0` for all `k<=6`; (b) the valid three-row source-G history observer
`H_3(s)=(g(s),g(E(s)),g(E^2(s)))` must yield `P_k=0` for `k<=6`.
`H_3(s)` describes a legal history ending at `E^2(s)`, available only after
two source steps and three six-bit observations. Its successor is
`H_3(E(s))`. It is a **history calibration**, not a free time-zero sensor;
all its observed graph edges must arise from a single legal source history.
No need to compare graph sizes as a compression claim.

## Frozen predictions and interpretation

- **P1 (prospective):** `P_k>0` for at least one `k<=6` for one-row `g`.
  This is a concrete finite-ring hypothesis, not a theorem implied by
  known full-line failure of one-row G closure.
- **P2 (prior-result control):** every `P_k=0` for `H_3` at `k<=6`.
  The existing exact third-order Rule-30 G law implies a deterministic
  update on valid histories; a finite factor cannot have a phantom
  periodic word on that valid inherited domain.
- **P3 (implementation control):** identity has every `P_k=0`.

If P1 fails, report that exact bounded negative and stop the example: no
post-hoc changes to ring size, observer or period. If P2 or P3 fails,
withhold scientific interpretation until the code/contract discrepancy is
resolved. P1 success establishes only that the declared observer graph
overcounts recurrent words; it does not establish Class IV, quantum
uncertainty, feedback benefit, or a novel zeta theorem.

## Verification and cost limit

Run once with a pinned implementation revision and write to a new canonical
JSON path under `results/` without overwriting it. Save the source revision,
full graph edges, source transition table and cycles, counts, all prediction
statuses and any phantom witness so another implementation can check them.
Use an independently written scalar Rule-30/G replay and an independent
closed-walk enumeration or matrix calculation to audit the canonical JSON.
Time cap 30 seconds, memory cap 256 MiB; no expensive Actions run. Charge
64 source states and up to six graph powers; site/observer computation costs
are recorded if a later controller uses them, not treated as a benefit here.
The retained result stays finite-ring evidence even though the Rule-30
history law used as a control has a separate full-line proof.
