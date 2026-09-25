# Rule 184 → 232: a costed prior-art calibration

**Status:** literature reconstruction and decision, 2026-09-25. No new
experiment, original theorem, or computational performance claim. Inspected
main `e4647fbe86ab4d561247159dfb79cae681ecddf8` after PR #313; no open
PRs or issues. Reviewed by: none.

**Same-day correction:** [the observer/readout audit](2026-09-25-density-observer-readout.md)
adds the omitted 1996 result of Capcarrere, Sipper and Tomassini: Rule 184
alone classifies density when the output is the surviving `11` or `00`
block language. The 1997 Rule-232 stage makes the answer available as a
homogeneous majority endpoint. Composition is needed for that *output
contract*, not to make the density distinction first exist. The following
theorem and cost accounting remain valid under their stated contract.

## Why this is the right external example

Our selected three-rule permutations changed finite-ring cycles, but supplied
no task requiring their intermediate rows. A real, independent task is the
finite-ring density classification problem. Land and Belew proved the
impossibility of a **single, fixed, uniform two-state CA** perfectly
classifying all binary strings by converging to a **uniform binary output**.
Fukś then proved that a **length-timed two-rule program** solves that
output task. The latter changes the model by supplying a rule switch and
the ring length to an external controller. The earlier 1996 result changes
the output interpretation instead. Neither refutes the impossibility
theorem. This is prior art, not a discovery of this project.

Primary sources: [Fukś, *Physical Review E* 55, R2081 (1997), Proposition
4](https://arxiv.org/pdf/comp-gas/9703001) ([journal
record](https://doi.org/10.1103/PhysRevE.55.R2081)); [Land and Belew,
*Physical Review Letters* 74, 5148
(1995)](https://doi.org/10.1103/PhysRevLett.74.5148). The first source also
analyzes the critical density 1/2 and its infinite random-configuration
order parameter. That asymptotic analysis is distinct from the finite-ring
classification theorem used here.

## Exact task and factorization

Let `s` be an arbitrary periodic binary ring of length `L ≥ 2`, with `N1`
ones, `N0` zeros, and density `ρ=N1/L`. Updates are synchronous and radius
one; the endpoint is the **whole ring**. Set

`n = floor((L-2)/2)`, `m = floor((L-1)/2)`, and
`T_L(s) = E_232^m(E_184^n(s))`.

Fukś's Proposition 4 proves for *every* such source: `T_L(s)=0^L` when
`N1<N0`; `T_L(s)=1^L` when `N1>N0`; and an alternating ring (one of its two
spatial phases) when `N1=N0`. The tie only occurs for even `L`. The exact
number of updates is `n+m=L-2`.

What the two stages do, under the paper's propositions:

| Stage | Retained or created distinction | Sufficient local cue for the next stage |
| --- | --- | --- |
| Rule 184 for `n` rounds | Conserves `N1`. Eliminates every `00` if ones are the majority, every `11` if zeros are the majority, and both if tied. It reorganizes, rather than calculates and stores, the count. | A majority side has a same-symbol adjacent pair of its own kind; the opposite pair is absent. A tie has neither pair. This is a property of the whole intermediate ring, not a claim that each cell can already read the global answer. |
| Rule 232 for `m` rounds | A three-cell majority update preserves absence of the disfavored pair, grows the surviving majority domains, and leaves a perfectly alternating tie intact. | At the deadline the whole ring is homogeneous 0, homogeneous 1, or alternating. |

For the no-`11` case, Fukś reduces the reachable Rule-232 dynamics to
Rule 32: the only `m`-step precursor of an output 1 is the alternating
`2m+1`-cell word starting and ending in 1. Its dual covers no `00`. Together
with Rule 184's finite elimination bound, this explains why the deadlines
suffice. The paper supplies the proof; this note has not independently
formalized it.

## Resource and observer contract

| Implementation | External information and state | Work, access, output |
| --- | --- | --- |
| Fukś schedule | Two fixed 8-entry rule tables; `L` must be known to schedule the switch after `n` rounds and stop after `m`. An external stage bit and a counter sized with `L` are one realization; selecting/broadcasting the active rule is a real control channel. One binary cell per ring site. | `L(L-2)` binary-site updates (for `L≥2`), each reading a radius-one triple and writing a bit. Approximately `3L(L-2)` logical input incidences, with overlapping reads. Latency `L-2` synchronous rounds. Endpoint is distributed across all cells; count the external clock and any observation/readout costs. |
| Central count and write | A processor reads `L` source bits, keeps a counter with `ceil(log2(L+1))` bits (plus control), and knows `L`. A tie output needs an arbitrary spatial parity origin for one of the two alternating phases. | One pass of `L` reads to count and `L` output writes; access is global or sequential and the processor is not a radius-one uniform binary CA. Its wall-clock latency depends on the access model. It uses asymptotically fewer operations than the CA's aggregate site updates in a model with cheap global/sequential access; it cannot be called a local-communication baseline under a model that forbids that access. |
| Single fixed binary CA | No externally staged rule choice or length-dependent switch; uniform local law and one bit per site. | Perfect classification *by convergence to the uniform majority state* on all lengths/sources is ruled out under the classical contract, irrespective of how long one waits. The different Rule-184 block readout succeeds under another output contract. |

The external controller may store `L` and a round counter once globally. If
instead each cell must autonomously know when to switch, merely adding a
three-valued periodic phase track (as for our fixed three-step schedule) is
**not** an implementation of this length-dependent one-shot switch. A
distributed timer, marked origin, extra states, or another protocol would
need its own construction and cost. We have not established a lower bound
against every such construction.

For a *fixed* length `L`, `T_L` is itself a CA map whose obvious composed
radius bound is `L-2`; that is a different rule family for each `L`, not a
single fixed-radius binary rule for all lengths. Our PR #313 theorem about
repeating three fixed rules and reading every third row does not remove
this `L`-dependent control. Direct table size or minimum radius for `T_L`
has not been proved here. Repeating 184 and 232 after classification is not
part of the contract.

## Decision

This is a known successful **task-specific transformation of a global count
into a local defect language**, followed by amplification to a homogeneous
majority output (the tie stays alternating). The first stage alone already
supports a perfect classifier under
the 1996 observer contract. This is a useful
calibration for how to state observer, clock, memory and locality constraints
when a schedule seems to outperform one CA. It gives no Groovy-specific
advantage, Class-IV discriminator, prime result or complexity-theoretic
shortcut. In particular, its roughly quadratic aggregate binary-site work
is not evidence of fast general constraint solving.

**Stop here for this unit.** Do not sweep ECA pairs to rediscover 184/232.
Further work needs an action-changing question such as a *specific* bounded
implementation of length-dependent switching using local state with a
matched controller/access cost, or an independent task in which the
intermediate defect representation is a useful consumer. Compare both with
central count where that access is available. The present literature
reconstruction is sufficient to correct our composition agenda.
