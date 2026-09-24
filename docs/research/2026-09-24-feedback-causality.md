# A Groovy-guided rule needs its rule chosen first

2026-09-24. Authored by Codex (OpenAI). Reviewed by: none.
**Evidence: elementary exact construction and a causal interface specification;
no feedback experiment or maintenance result.**

## The question

The [observer-orbit preflight](2026-09-24-observer-orbit-preflight.md) counts
apparent recurrence under one fixed Rule 30. To test the program's H3, we
would have to use an observation to choose a future rule. Which `G` is
available *before* that choice, and what dynamics does it describe?

For a uniform candidate rule `E_r` on binary configurations, write
`D_r(s)=s XOR E_r(s)` and
`G_r(s)=D_r(E_r(s)) XOR E_r(D_r(s))`. `G_r` is indexed by the rule: it is
not a stored property of `s` independent of `r`. The phrase “choose `r`
from `G_r(s)`” asks us to solve the implicit equation
`r=F(G_r(s))`. It need not define a deterministic update at all.

## An exact obstruction at every ring width

Take the two uniform elementary rules `E_0(s)=0^n` and
`E_255(s)=1^n` on an arbitrary periodic ring of width `n>=1`. For a
constant rule `E_c(s)=c^n`,

`D_c(E_c(s)) = c^n XOR c^n = 0^n`, while
`E_c(D_c(s))=c^n`. Hence `G_c(s)=c^n` **for every source state**.

Name the two candidate rules by bits `r=0,1` and read any specified site
of their candidate `G` fields. If `F(g)=1-g`, the equation `r=F(G_r(s)_i)`
reduces to `r=1-r`: **no next rule exists**. If `F(g)=g`, it reduces to
`r=r`: **both rules qualify** and no unique next state is specified.
These are two concrete counterexamples to treating a simultaneous selector
as a CA; they make no claim that every `G` policy is ambiguous. The same
argument works for a global selector reading one designated G bit. A direct
finite-table check for all states at widths 1..7 corroborates the algebra,
but the proof does not depend on that bound.

## Two causal contracts worth distinguishing

1. **Fixed-reference, counterfactual G.** Declare a reference rule `B`
   before the run. At time `t`, obtain `G_B(s_t)`, select local modes
   `r_t(i)=F(m_t|_{i-q..i+q},G_B(s_t)|_{i-q..i+q})`, then use the selected candidate
   neighborhood table to produce each `s_{t+1}(i)`. Update finite memory
   `m_{t+1}` by a specified local rule. This is causal; `G_B` predicts two
   steps under *B*, not the actual switched continuation. Generic acquisition
   requires `B(s)`, `B(B(s))`, and `B(s XOR B(s))` plus XOR operations. If
   `B` has radius `b`, its G bit uses at most radius `2b` of the current
   source. Declare reuse of intermediate fields and all reads, storage and
   rule evaluations in the cost comparison. Local modes per site make a
   spatially nonuniform choice, even when all candidate tables are ECAs.
2. **Retrospective, realized-path residual.** Store three actual consecutive
   source rows and earlier rule choices. At time `t`, the value
   `C_{t-2}=(s_{t-1} XOR s_t) XOR
   E_{r_{t-2}}(s_{t-2} XOR s_{t-1})` is already known and can choose
   `r_t`; its first difference was produced by `r_{t-1}`, its second term
   uses `r_{t-2}`. If these two rules coincide it is the original
   `G_{r_{t-2}}(s_{t-2})`; otherwise it is a *mixed-rule residual*, not
   native G under either candidate. Charge the two-update latency, stored
   rows/rule identity and the residual calculation. An alternative using
   stored differences needs its own explicit memory accounting.

For an autonomous, translation-equivariant **local** finite-alphabet
selector with finite memory, either causal contract composes into one fixed
CA on the source plus controller tracks. For the reference version with
candidate radius `a`, selector radius `q` on G, and any additional memory
update radius `p`, a straightforward implementation has bounded radius at
most `max(a, q+2b, p)` when `p` includes any controller dependencies.
This is a representability observation, **not** an efficiency theorem or a
reduction to a binary radius-one ECA. A whole-ring selector, an externally
supplied schedule or unbounded memory has a different locality contract.
Calling the result “endogenous” therefore demands a specified controller
and a measured advantage over matched fixed, clocked and full-information
controllers, not just a complex-looking trajectory.

## Decision for H3

Before searching a rule pair or selector, choose one of those contracts;
state whether modes are global or per-site; declare an independently
motivated target and perturbation process; and verify that a full-state
controller with the same actions and timing can improve on passive dynamics.
Then freeze a policy class, horizon, initial states and matched fixed-rule,
periodic-schedule and controller-track baselines. Count rule/selector tables,
initialization, retained rows, local reads, update operations and any phase
clock. An objective tuned to the candidate G policy would not be independent.

The existing [Rule-54 delayed repair](2026-09-23-delayed-repair-feasibility.md)
is a useful *negative gate*: at its two-step decision time a full-state
one-flip controller cannot improve on doing nothing. Do not recycle that
contract for H3 or change its endpoint to manufacture a success. This exact
causality result clears up the policy definition; it does not itself supply
the missing organization target or justify a selector experiment.
