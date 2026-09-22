# Completion-independent relations survive some lifts, but do not isolate Class IV

Authored by: Codex (OpenAI), /root, 2026-09-15. Independent prospective
protocol and physical-result review: Codex (OpenAI), /root/relations_review.
Final integration is tracked by the gathering PR. Evidence: exact within the
declared finite contracts; the Class-IV interpretation remains negative.

The preceding audit found that an unspecified local rule entry can change a
lifted commutator bit without changing evolution on the beam. Two bits querying
the same unspecified entry nevertheless have a fixed parity. This test asks
whether those relations remain after translated copies are removed, and
whether they persist into the next lift.

**Some relations survive, but the proposed discriminator fails its basic
controls.** Rules 54 and 110 have no remaining relations between ambiguous G
values at D3 or D4 on seven-cell source rings. Eight-cell rings retain
relations that persist from D3 to D4; controls 18 and 126 show the same
higher-floor counts and transport. Color-complemented representatives also
change the signature. These are properties of this finite representation and
completion contract, not a Class-IV characterization.

## What was recovered and tested

The prior context-full session left an unrun frozen protocol with SHA-256
`7ae1ff9d736e5c6efdd5ded582f2d9ec1297fc76757cf02f01b5670d11feed0b`.
The resumed session preserved it unchanged and obtained independent review
before implementing and evaluating the test. The signed review and two
pre-implementation clarifications are retained in
[the recovery record](../../experiments/commutator_relations_20260915/recovery.md)
and [Gate 1 review](../../review/gate1-review.md).

The [frozen protocol](../../experiments/commutator_relations_20260915/protocol.md)
specifies an algebraic reanalysis of all 2,048 prior contracts: every ECA root,
source widths seven and eight, finite D2–D4 tables, and the additional complete
first-lift D2 table. A physical panel covers roots
0, 4, 18, 30, 54, 90, 110, 124, 126, 137, 147, 193 and 204 at both widths and
all three floors: 78 physical records and 104 symbolic contracts. It includes
every reflection/color-complement variant of the two core families.

There is no new lift synthesis, trajectory simulation, fitted threshold or
selection among readouts. The exact input archive and D2 tables from
[the preceding audit](2026-09-15-commutator-completion.md) are immutable.
The complete first-lift constraint table is only available for D2; D3 and D4
freedom is relative to each width's finite family.

## The observable and translation quotient

Write the native commutator family as

$$G_i=c_i\oplus u_{q_i}.$$

Here a forced query is absorbed into the fixed constant; otherwise its
physical neighborhood identifies a free Boolean variable. Distinct free keys
are independent under unrestricted compatible local completions. A pair of
ambiguous endpoints has fixed parity precisely when it shares a variable.

An event contains source word, transverse coordinates and a pointed
longitudinal position. Simultaneously translating the source and pointer is
a free width-$w$ action. Selecting longitudinal position zero retains one
event per orbit. If the original census has $M$ ambiguous events, $U$ free
variables, and equal/opposite pair counts $E,O$, the quotient has

$$R=M/w-U,\qquad E'={2E-M(w-1)\over 2w^2},\qquad O'=O/w^2.$$

Every division was checked to be exact and nonnegative. The physical panel
then compares the **entire pointer-centered configuration Y**, using exact
packed bytes, to remove any remaining transverse translation copies. Equal
local patches or equal difference fields alone do not define this quotient.
Every merged class has the same symbolic variable and affine constant.

In this panel, the additional full-state quotient reduces fixed-event copies
but does not reduce the ambiguous relation ranks. This is a measured panel
fact, not a statement for all roots or widths.

## Relation counts after all spatial translations are removed

The entries below count independent parity relations among ambiguous
endpoints. Fixed individual G values are recorded separately in the data.
D2 uses the complete first-lift table; D3/D4 use the finite family table.

| Root | Width 7: D2 / D3 / D4 | Width 8: D2 / D3 / D4 |
| --- | --- | --- |
| 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| 4 | 0 / 0 / 1296 | 0 / 0 / 7128 |
| 18 | 0 / 0 / 0 | 138 / 108 / 648 |
| 30 | 0 / 0 / 0 | 0 / 0 / 0 |
| 54 | 6 / 0 / 0 | 96 / 108 / 648 |
| 90 | 0 / 0 / 0 | 0 / 0 / 0 |
| 110 | 18 / 0 / 0 | 138 / 72 / 432 |
| 124 | 18 / 0 / 0 | 138 / 72 / 432 |
| 126 | 0 / 0 / 0 | 120 / 72 / 432 |
| 137 | 23 / 35 / 215 | 149 / 107 / 647 |
| 147 | 5 / 35 / 215 | 83 / 143 / 863 |
| 193 | 23 / 35 / 215 | 149 / 107 / 647 |
| 204 | 0 / 0 / 0 | 0 / 0 / 0 |

The all-256 longitudinal census also shows that nonzero relations are common:

| Contract | Roots with relations, width 7 | Roots with relations, width 8 |
| --- | ---: | ---: |
| D2 finite | 198 | 239 |
| D2 complete first lift | 198 | 239 |
| D3 finite | 163 | 215 |
| D4 finite | 157 | 201 |

These all-rule counts remove longitudinal copies only. The full spatial
quotient was independently reconstructed on the fixed 13-root panel.

## What persists into the next lift

The declared address map retains the source word and old coordinates and
chooses one of six new-axis phases. All 312 individual phase maps respect the
full-state quotient and are injective. Seven readouts were fixed beforehand:
each individual child G bit and the XOR of child phases four and five.
No native-G transport theorem is assumed by choosing this address map.

For two parent orbit classes sharing a free variable, child parity is fixed
exactly when the child expressions have equal variable supports. The audit
separates fixed child expressions from expressions sharing a nonempty support,
and tests whether the resulting parity agrees with or reverses the parent.

For 54/110 and the following controls, **each of the seven readouts gives the
same counts** in this table. These are unordered pairs, not independent ranks.

| Width | Root | D2→D3 surviving / eligible pairs | D3→D4 surviving / eligible pairs |
| --- | --- | --- | --- |
| 7 | 54 | 0 / 6 | Not applicable: no parent relations |
| 7 | 110 | 0 / 18 | Not applicable: no parent relations |
| 8 | 18 | 36 / 162 | 216 / 216 |
| 8 | 54 | 36 / 114 | 216 / 216 |
| 8 | 110 | 12 / 144 | 72 / 72 |
| 8 | 126 | 12 / 126 | 72 / 72 |

All surviving pairs in this table retain nonempty child variable support and
agree with parent parity. They are therefore real relations between uncertain
values, rather than pairs of already-fixed child outputs. The complete data
also retains the complement variants, where the XOR readout can cancel the
shared child variable and become fixed. No observed surviving parity reverses
its parent, across the full panel and all seven readouts.

## A bounded obstruction stronger than seven failed readouts

For width-seven roots 54 and 110 at child floors D3 and D4, every ambiguous
event after longitudinal quotienting has its own independent variable. Every
six-phase sibling block is either wholly free or wholly fixed; there are no
mixed blocks. Distinct all-free blocks consequently use disjoint variables.

A nonconstant Boolean function on six free bits can attain either output.
Because separate blocks have independent inputs, any fixed nonconstant
sibling-only Boolean readout can vary independently on those all-free blocks.
It cannot produce a completion-independent parity between two such blocks.
This rules out more than the seven particular readouts in that verified
domain. The condition is on the **child** floor, not the parent floor.

This does not apply to fixed outputs, mixed blocks, overlapping spatial
readouts, additional constraints on completions, or arbitrary widths and
dimensions. Width eight does not satisfy the distinct-variable condition for
these two roots.

## Gauge structure, partition shape and an untested gluing question

After evaluation, Myk shared a proposal to treat completion choice as gauge
freedom and study the partition's structure instead of its magnitude. The
finite algebra supports a precise version. If $A$ is the incidence matrix
with one column per distinct queried free key, the commutator family is

$$\mathcal G=c+\operatorname{im}A,\qquad g\mapsto g+A v,\quad v\in\mathbb F_2^U.$$

The columns have nonempty disjoint supports, so this action is free and
transitive on the family: it is a torsor for $\mathbb F_2^U$. Each free-query
block has two allowed bit patterns with every relative parity fixed. This is
the set-level free/transitive notion of a
[torsor](https://stacks.math.columbia.edu/tag/04TV); no sheaf or bundle has been
constructed by the experiment. Fixed G cells remain anchored outside those
free blocks.

Among ambiguous endpoints, pairwise differences are invariant exactly within
the same free block. Fixed–fixed differences are invariant as well.
For a linear parity $b^Tg$, invariance is exactly $A^Tb=0$:
each free block contributes an even number of selected endpoints. Within a
block the signed edge value is $c_i\oplus c_j$, so its sum around every loop
already vanishes. Any nontrivial gluing obstruction would therefore have to
come from additional compatibility data, such as spatial overlaps, dynamics
or cross-floor identifications. Calling it a cohomological obstruction before
specifying those maps and conditions would exceed the result.

The full partitions, constants and physical addresses were preserved and
compared independently. **Equal relation counts or equal survival totals do
not establish isomorphism of the spatially or temporally structured
partitions.** The unembedded same-query graph alone is a union of cliques;
its unlabeled topology is determined by block sizes. A richer shape question
needs to retain how those blocks sit in space, evolution and lift addresses.
That analysis was not performed or scored by this protocol. At width seven,
the D3/D4 ambiguous partitions for 54/110 are entirely singletons even before
the remaining spatial quotient; that stronger negative survives any mere
change of graph summary. Fixed vertices or extra spatial/dynamical edges
would be additional structure, not a relation measured by this test.

The gauge interpretation is relative to the partial beam and the queried
observable. Different completions can define different ambient dynamics off
the beam. Complement conjugation is a distinct relabeling operation; treating
it jointly with completion freedom requires transporting the law, lift,
difference operation and address maps consistently. The experiment does not
identify those two operations as one gauge group.

## Interpretation and stopping point

The relational object is well-defined and sometimes persists through a lift.
It fails as the sought Class-IV marker under this protocol: the core
representatives disappear at one tested width, controls share the positive
higher-floor signatures at the other, and color-complemented representatives
have different counts. The latter is a failure of representation invariance
for this signature, not evidence that the underlying conjugate dynamics
belong to different classes. These tests do not rule out a discriminator based
on the richer, untested partition structure described above.

The phrase “identity without essence” motivated inspecting relational
invariants; this finite result neither establishes nor refutes that broader
interpretation. The calculation establishes which parity relations belong to
this completion family. It has not shown that they identify persistent
interactions, memory, adaptation, or a class boundary.

Stop this bounded test. A useful future question would explain which
difference-neighborhood collisions generate the surviving relations and why
they depend on width and bit convention, before treating their recurrence as
a new discriminator. No further experiment is frozen or running here.

## Verification, preservation and provenance

The primary evaluation completed all 78 physical records, 2,048 census rows
and 52 adjacent-floor comparisons in **44.08 seconds**, peak RSS 189,092 KiB.
Independent direct-coordinate reconstruction took **148.97 seconds**, peak
RSS 125,324 KiB. It imports none of the primary keyer, quotient or transport
code. Both runs stayed within the frozen ten-minute and 2 GiB process limits,
outside GitHub Actions. The existing archive made this reanalysis far cheaper
than rebuilding the previous census.

The independent comparison checks all **1,317,888 pointed symbolic events**
across 104 contracts, comparing equality partitions and constants rather than
arbitrary numeric variable IDs. It also checks all spatial orbits, 2,048
census rows, 546 contract/readout summaries, and the sibling-block conditions.
See [signed physical review](../../review/physical-replay-review.md) and
[comparison certificate](../../review/comparison.json).

The [compact public result](../../results/commutator_relations_20260915.json)
includes column-labeled tables for every panel contract and readout. The
[raw archive manifest](../../experiments/commutator_relations_20260915/raw-archive.json)
identifies the complete 336-member bundle: unchanged full input archive and
manifest, full D2 table, all primary and independent per-event outputs,
examples, source code, execution records and reviews.
[Reproduction instructions](../../experiments/commutator_relations_20260915/REPRODUCE.md)
explain how to replay without overwriting the preserved results.

Code lives in [the primary audit](../../scripts/commutator_relations.py),
[independent replay](../../review/replay_relations.py),
[path-only replay launcher](../../review/replay_portable.py),
[artifact comparison](../../review/compare_relations.py), and
[public summarizer](../../scripts/summarize_commutator_relations.py).
The author cross-reviewed the independent replay, comparator and launcher;
the reviewer independently reviewed the primary implementation. Final
publication review is pinned to the gathering head. Automatic CI only
compiles and checks provenance plus the ordinary site tests/build; it does
not rerun the scientific experiment.

Publication correction: the recovered prior-summary JSON had one extra
trailing newline relative to the unchanged repository file. CI detected the
byte-hash mismatch. The parsed JSON is identical. The bundle and execution
record preserve the actually evaluated bytes and hash; the public source hash
now points to the exact repository bytes. The [normalization certificate](../../experiments/commutator_relations_20260915/publication-normalization.json)
records both hashes. No scientific values or frozen inputs were rewritten,
and no scientific evaluation was rerun for this packaging correction.
