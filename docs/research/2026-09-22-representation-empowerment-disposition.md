# Representation empowerment: an endpoint proof stops the census

2026-09-22. This is a prospective protocol audit and scheduling decision, not
a numerical evaluation of the frozen
[representation-empowerment protocol](protocols/representation-empowerment-20260910.md).
No intervention channels or primary-rule outcomes were generated.

## What we wanted to learn

The proposed census asked whether a lossy observation that leaves many stable
futures possible is also the observation under which a controller can select
among those futures. It would compare Research026's stable-future repertoire
with channel capacity under two actions, `noop` and one flip of cell 0.

That is a sensible distinction in general. Before paying for a 247-rule
census, however, the declared channel has to survive its simplest controls.

## The primary endpoint answers itself

The primary outcome is the stable future class of the post-action state,
`C_infinity(a(S_0))`. In the frozen protocol that class includes the initial
post-action observation. Stable future classes therefore refine the current
observation: if `P(S_0)` differs from `P(flip_0(S_0))`, the two outcomes are
already distinct before the dynamics has demonstrated any persistence.

For the identity observation, conditioning on `y=P(S_0)` identifies the exact
microstate. `noop` and `flip_0` then produce two different initial identity
observations, hence two disjoint deterministic outcome rows. By the protocol's
own disjoint-support control,

```text
E_C_infinity(identity) = 1 bit
```

for every ECA rule. One bit is the upper bound for a binary action channel, so
identity is a rule-independent global maximizer. Research026's future
repertoire for identity is zero because an identity macrostate leaves no
hidden state. The two score functions are therefore already nonidentical by an
exact endpoint argument. This does not decide the registered maximizing-set
prediction: a repertoire maximizer might also attain one bit.

The same shortcut classifies many block observers without any trajectory.
For a block truth table `h`, let `d_0 h(x)` say whether toggling the input bit
containing physical cell 0 toggles the observed block bit. If `d_0 h` is
always one, the immediate-inclusive action supports are disjoint and capacity
is one. If it is always zero, the flip permutes every observation fiber and
the two rows are identical under the uniform-fiber prior, so capacity is zero.
This fixes 6 of the 14 nonconstant block-two tables and 30 of the 254
nonconstant block-three tables independently of the ECA rule.

## Why the remaining census would not repair the question

The primary denominator contains exactly the 247 rules with some observer of
positive future repertoire. This excludes nine endpoint cases that would
necessarily count against the registered separation prediction, while
identity remains a capacity maximizer in all 256 rules. The resulting majority
count is a valid statistic of the declared catalog, but it is not a clean test
of dynamical revisability.

The comparison also changes several things at once. The observation determines
the controller's information and the distinctions counted in the outcome;
identity and block observers use different physical cadences; and the fixed
flip site selects one block phase and one truth-table argument. A pass or fail
would describe those representation/clock/action/readout bundles. It would not
select a representation for a named task or change a current project decision.

## Cost and provenance audit

The implementation is possible but is not a small pending replay. Using
output-complement representatives still requires 34,816 stable partitions and
about 11.8 million macrostate-conditioned channels across the seven registered
outcomes. A streaming implementation is likely a multi-core-hour,
multi-gigabyte off-Actions computation; naive exact Python could take days.

The repository also lacks the full Research026 per-pair tables, per-rule
optimizer summary and saved stable-class labels required by the protocol's
blocking reproduction gate. Only aggregates and selected independent checks
remain. Numeric rationalization, directed-rounding precision and the sparse
result schema were never prospectively pinned. These are recoverable
engineering gaps, not negative scientific evidence, but there is no reason to
repair them for a primary endpoint already settled analytically.

## Disposition

**Park the frozen census unrun.** Preserve the protocol as a careful record of
the proposed channel; do not implement or evaluate it under its current primary
endpoint. This is not a claim that empowerment or intervention-relative
representation design is impossible.

A new control study would need a new, independently reviewed protocol. It
should name a consumer and cost budget, hold the physical cadence and future
target fixed across representations, exclude immediate action detection from
the primary outcome, and control action site/block phase. The action-changing
question would be whether a lossy representation provides delayed,
action-addressable variation that beats direct source access or the cheapest
sufficient baseline. If immediate leakage or direct-source dominance explains
the score, stop.

This audit used two independent read-only reviews: one checked the scientific
endpoint and one checked provenance and computational cost. The disposition
creates no result artifact and changes no historical protocol bytes beyond a
dated status notice.
