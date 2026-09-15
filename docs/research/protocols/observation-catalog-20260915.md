# Observation catalog: a bounded structural search

Status: frozen proposal, not implemented or evaluated. Authored by Codex
(OpenAI), /root, 2026-09-15. Independent protocol review: pending.

## Question and intent

Can a mechanically enumerated family of observations, especially joint
observations, reveal distinctions that survive changes of width and lift?
Myk authorized this search in the current conversation on 2026-09-15.
This is an exploratory comparative atlas, not a new definition of Class IV.
The prior lift search motivates enumerating projections and their combinations.
The prior completion-relation result motivates retaining partitions and their
spatial/dynamical incidence, rather than only their sizes.

The repo's run calculus calls an observation a gauge: Q(F^t(S)). This remains
distinct from a symmetry action or the freedom to complete a partial native
rule. No observed field is iterated as an autonomous CA in this experiment.

## Frozen catalog

Use x increasing to the right and B_j(S)(x)=S(x+j). Let F be the root rule,
X=S, U=F(S), V=F^2(S), D=X XOR U. Primitive order is fixed below:

0. state: X
1. future1: U
2. future2: V
3. change1: X XOR U
4. change2: X XOR V
5. space_left: X XOR B_-1(X)
6. space_right: X XOR B_1(X)
7. space_two: X XOR B_2(X)
8. move_left1: X XOR B_-1(U)
9. move_right1: X XOR B_1(U)
10. move_left2: X XOR B_-2(V)
11. move_right2: X XOR B_2(V)
12. birth: (1 XOR X) AND U
13. death: X AND (1 XOR U)
14. sensitivity_left: F(S)(x) XOR F(S XOR e_(x-1))(x)
15. sensitivity_center: F(S)(x) XOR F(S XOR e_x)(x)
16. sensitivity_right: F(S)(x) XOR F(S XOR e_(x+1))(x)
17. absential: (1 XOR X) AND (B_-1(X) OR B_1(X))
18. commutator: U XOR V XOR F(D)
19. motif000: indicator that (B_-1(X),X,B_1(X))=(0,0,0)
20. motif010: corresponding indicator for (0,1,0)
21. motif101: corresponding indicator for (1,0,1)
22. motif111: corresponding indicator for (1,1,1)
23. persistence: X AND U

There are 24 singles followed by all 276 unordered pairs in lexicographic
primitive-index order: 300 nominal observations. For a single, Z is the
three-bit word Q(S)(x-1),Q(S)(x),Q(S)(x+1), encoded with x-1 least significant.
For pair (i,j), Z=Z_i+8 Z_j. Retain the full Z event labels and constituent
fields, so partitions, transition multiplicities, refinements, and witnesses
can be reconstructed. No higher compositions are admitted this round.

Exact algebraic redundancy is checked on every 11-bit source context for each
ECA. All primitive three-site words depend on positions -5 through 5 at most.
Canonicalize partition labels by first occurrence, so color-name permutations
do not count as different partitions. Preserve aliases and the 300 attempted
names. This checks equality of pointed observation partitions on that local
domain, not equality of whole-field factors or dynamics across different rules.
Reflection/complement rule orbits are recorded; no unproved covariance of
same-named native G or of the catalog is assumed.

## Root event domains and common measurements

Discovery: every state on periodic widths 7 and 8, every ECA 0..255. Each
state is a pointed event at x=0; this quotients simultaneous longitudinal
translation of the source and point, without weighting spatially periodic
states differently. Uniform mass over source states is the stated ensemble.
Successor and spatial-shift maps are retained along with observation arrays.
At each event use Z0=Q(S), Z1=Q(FS), Z2=Q(F^2S), and Zright=Q(S) at x=1.
The common target Y is the raw three-site word of F(S) centered at x=0.

For every observation record seven numbers, with base-2 entropy:

1. H(Z0), observed-symbol entropy.
2. H(Z1|Z0), one-step observed uncertainty.
3. H(Z2|Z1)-H(Z2|Z0,Z1), two-step refinement gain.
4. I(Z0;Zright), spatial mutual information.
5. H(Y|Z0), uncertainty about the common raw future target.
6. Mass of events whose Z0 block has more than one Z1 successor symbol.
7. For pairs, min(H(Y|Zi),H(Y|Zj))-H(Y|Zi,Zj), complementary prediction gain;
   singles receive null, not a success or failure.

All are exploratory summaries of retained labeled objects. In particular,
future1/future2 are retrospective observables with anticipatory support, not
online predictors. Future1 can encode the common target directly. Its apparent
predictive success is a tautological baseline, not evidence of organization.
Pairs have a larger observation budget; complementary gain alone does not
prove synergy beyond that resource increase. Entropy gain is not a count of
independent physical mechanisms. No threshold is treated as a theorem.

## Mechanical discovery shortlist and sealed confirmation

Use existing labels.json, preserving its disputed 41/106 orbits. Positives are
the complete reflection/complement orbits of 54 and 110. Undisputed negatives
are the distinct symmetry orbits in classes 1..3; neither symmetry copies nor
the two widths count as independent rules.

For each candidate and each of the seven measurements separately, form the
closed interval spanning all core-positive values at both discovery widths.
Count a negative orbit as overlapping if ANY member at EITHER width lies in
that interval. Rank by this overlap count, then interval width divided by the
full discovery range of that measurement (zero range -> width zero), then
candidate index. Comparisons use tolerance 1e-10; rounding the normalized width
to 12 decimals fixes tie behavior. For each measurement retain its best
candidate: seven fixed measurement/observation slots, possibly fewer than seven
distinct observations. Print the full search table, attempted multiplicity,
aliases and disputed-orbit outcomes. There are no significance claims.

Commit the generated shortlist and its discovery hashes BEFORE confirmation.
Confirm those exact slots on width 9, all states, all 256 ECAs. Keep discovery
intervals fixed and report core retention, negative-orbit overlap and disputed
cases. Do not replace unsuccessful slots. No confirmation-derived ranking.

Also test the fixed slots on longer ring trajectories for rules
0,4,18,30,41,54,73,90,106,110,124,126,137,147,193,204 and the unclassified
radius-two challenge F(S)(x)=S(x+2) XOR product(S(x-2)..S(x+1)). For the latter,
left/center/right sensitivities perturb offsets -1,0,+1; extreme offsets are
not added. Seeds 2026091501 and 2026091502, numpy PCG64, independent iid fair-bit
initial states, width 1021, burn 1024, then 1024 scored rows plus four lookahead
rows. Sample eight equally spaced sites floor(k*1021/8), k=0..7, on every
scored row. Use the same event rows/sites for every candidate and all lags.
Trajectories are periodic rings and samples are dependent. No binomial confidence
intervals, infinite-line claim, or class label for the radius-two example.
These are finite scale/ensemble stress tests, not new independent Class-IV rules.
All inference concerns the declared iid initialization and finite horizon.

## Native lift views and completion-relation provenance

Use the immutable uniform six-field archive with SHA-256
766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1,
and the preserved commutator-relations arrays from PR259. Panel: roots
0,4,18,30,54,90,110,124,126,137,147,193,204, widths 7/8, floors D2..D4.

Decode each stored grid recursively with phases 4 XOR 5 and verify its source
ordering. Native on-family successors are the same stored encoding at the
root successor, as certified by the previous archive audit. Use X=Y, U=H(Y),
V=H^2(Y); longitudinal shifts keep every transverse coordinate fixed.
Evaluate the 20 primitives except sensitivities and G, and their 190 pairs.
For each floor inspect all six phases on the newest axis with every older
transverse coordinate zero, x=0, three longitudinal cells. Compare each
resulting source-state partition to all 300 root partitions at the same width.
Retain every match and aliases. This is a bounded native-view search against
root partitions, not full transverse coverage, an intrinsic recognition
theorem, or a guarantee that transitions match merely because partitions do.
Also record a common partition's transition relation using the shared source
successor; matching partitions then transport the observed transition graph.
Do not call a decoded-root copy independent discovery. Mark omitted native
sensitivities/G as completion-dependent, rather than evaluate a zero completion.

For the latter G, use the existing symbolic partition and constants instead.
On each contract's fully spatially quotiented free-event blocks, annotate
unordered pairs by: same source state; equal one-step source successor; same
eventual source cycle/basin; both sources of full spatial period. Compute these
counts combinatorially within each shared-free-key block. Retain event-to-source
maps and source functional graphs. These categories overlap and are not causal
explanations. Fixed events are excluded from free-pair denominators. No-free-pair
outcomes are NA. This is a provenance audit, not another raw-rank classifier.

## Budget, predictions, review and preservation

Each primary stage (discovery, confirmation, lift/provenance) has a 600-second
wall budget and 2 GiB RSS limit. Stop and record censored coverage if exceeded;
do not shrink the catalog after seeing scores. Scientific runs and independent
replay occur outside GitHub Actions. CI compiles and checks pinned hashes only.
Save exact source bytes, protocol, discovery shortlist, execution provenance,
all primitive event data and maps, full metric/selection tables, lift matches
and completion annotations. Package raw data with reproduction commands.

Expect substantial exact redundancy and incomplete class separation; these
are expectations, not pass criteria. A completed comparison map with negative
results is successful execution. Any confirmed separation remains bounded and
exploratory, with only two core positive symmetry families. Native-view matches
are a separate axis of evidence and cannot rescue a failed class claim.

Independent Gate 1 must precede implementation and evaluation. Independent
verification must reconstruct primitive definitions, partitions and all common
measurements on an independently chosen fixed panel at minimum, check every
selection/confirmation verdict from the saved tables, and inspect lifted-view
and provenance witnesses directly. Record verification coverage and discrepancies.
Gate 2 reviews the complete argument and the exact publication head.
