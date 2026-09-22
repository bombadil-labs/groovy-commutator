# What Rule 110 must remember at a fixed asynchronous interface

Evidence: exact reachable counterexamples and a restricted lower-bound proof.
Authored by Codex (OpenAI), 2026-09-21. Reviewed by: none. Myk authorized this
session to set up, run and integrate the work solo. All verification here is
self-verification; it is not independent review. No novelty claim is made.

## Answer and decision

Nakamura's twelve-state binary simulator cannot be compressed by any
noninjective pointwise encoding **if current bit and modulo-three age remain
exactly readable at each site, the update radius remains one, and the original
atomic-update semantics and cadence are preserved**. For Rule 110, every
possible identification of previous-bit values has a reachable local
counterexample. The uncompressed simulator attains the bound under this
interface, so the restricted alphabet requirement is exactly twelve states.

This is not a lower bound for all asynchronous Rule-110 simulators. Existing
constructions change the protocol and use eight states for binary sources.
The result tells us which cost/semantics constraint must change before claiming
an improvement. The direct quotient search is closed; no larger numerical
search is queued. The dimensional lift has not been given an asynchronous
implementation or an advantage by this result.

## The established baseline and the new comparison

[Nakamura's construction as presented by Lee et al., section 2](https://doi.org/10.1016/j.physd.2004.03.007)
uses local current/previous/age states. [Gács, section 3](https://cs-web.bu.edu/faculty/gacs/papers/commut.pdf)
explains the commuting enabled updates and the possibility of retaining only
an old message field when neighbours need only that field. Operation-based
[CRDTs](https://arxiv.org/abs/0907.0929) provide a useful comparison for
commuting concurrent operations; these CA cells are different pieces of a
computation, not replicas of one shared object.

Here S={0,1}×{0,1}×Z/3 with components (c,p,a). A cell waits if a neighbour
is one phase behind; otherwise it reads the current bit of an equal-age
neighbour or the previous bit of an ahead neighbour. It applies Rule 110,
stores its former current bit as previous, and advances its age.

Suppose Q is a pointwise encoding preserving c and a. Its only possible
identifications are the six pairs (c,0,a) and (c,1,a). Choosing independently
whether to identify each pair gives all 64 candidate equivalence relations.
Mask bit 3c+a is one when the previous-bit distinction is retained. The
candidate alphabet has 6+popcount(mask) states; mask 63 is the identity.

An unrestricted whole-field factor requires equal observed configurations to
have equal observed successors under each enabled update label. A radius-one
factor additionally requires the successor centre to be a function of the
three observed neighbourhood labels. It cannot consult an erased distinction
or an unobserved fourth site. Enabledness must also be well-defined. This is
the operation-wise factor criterion from the
[shared closure account](2026-09-10-shared-closure-account.md), with locality
made explicit rather than assumed.

## Frozen chronology and complete outcomes

The first [protocol](protocols/nakamura-retention-20260921.md) was committed at
`5b54f39` before its runner at `0e5d0e2` and evaluation. It checked all 64
quotients on reachable prefixes of width-five rings: every source bit string,
every uniform initial phase, and every subset of cells advanced once. Previous
equals current at initialization. Each prefix is replayed as an actual legal
update sequence, not inferred from arbitrary phase assignments.

| Check | Rule 110 | Rule 204 identity control |
| --- | --- | --- |
| Four-cell alphabet windows | 20,736 | 20,736 |
| Jointly enabled adjacent-update diamonds | 3,072, all pass | 3,072, all pass |
| Prefix records before deduplication | 3,072 | 3,072 |
| Distinct reachable configurations | 3,069 | 2,976 |
| Reachable local states | 12 | 6 |
| Whole-field quotient candidates | 64 | 64 |
| Whole-field candidates refuted | 56 | 0 |
| Whole-field survivors | masks 56–63 | all 64 |

The local construction control checks both sequential update orders, their
agreement with simultaneous updating, and persistence of enabledness. It
checks the known simulator; it does not establish a novel scheduling theorem.
The first search's survivors were explicitly inconclusive. In particular,
mask 56's nine-state alphabet was not announced as a working simulator.

The separate [locality protocol](protocols/nakamura-local-retention-20260921.md)
was frozen at `bc7741b`, after recording those outcomes, and implemented at
`d41b427`. It reused the identical reachable prefixes and grouped radius-one
observations rather than whole fields. All seven nonidentity Rule-110 survivors
failed. Mask 63 and all eight identity-rule controls passed. This follow-up
was selected because the first check had not resolved the fixed locality
requirement; it is not presented as a prediction made before the first result.

The canonical reports preserve every candidate, including the first run's
survivors: [whole-field audit](../../results/nakamura_retention_20260921.json)
and [radius-one audit](../../results/nakamura_local_retention_20260921.json).
All 63 rejected Rule-110 candidates have replayable witnesses across these
two reports. No timeout or solver outcome is treated as a mathematical result.

## A short proof explaining the enumeration

Write the lagging centre's phase as a, and its ahead right neighbour's phase
as a+1 modulo three. In both examples below, the left neighbour and centre
are at phase a. Both centres are enabled.

First consider identifying previous bits when the ahead neighbour's current
bit is one. The two local neighbourhoods are

$$
((0,0,a),(0,0,a),(1,0,a+1)),\qquad
((0,0,a),(0,0,a),(1,1,a+1)).
$$

The source inputs for the centre are 000 and 001, so Rule 110 outputs zero
and one. These neighbourhoods are reachable: initialize source rings `00001`
and `00011`, respectively, at uniform phase a, update site 3, then consider
updating site 2. Sites are numbered zero through four from left to right.
Every other local component agrees. The whole-field audit already detects
this obstruction, including all three phase rotations.

Now consider identifying previous bits when the ahead neighbour's current
bit is zero. The neighbourhoods are

$$
((1,1,a),(1,1,a),(0,0,a+1)),\qquad
((1,1,a),(1,1,a),(0,1,a+1)).
$$

The source inputs are 110 and 111, requiring centre outputs one and zero.
For the first neighbourhood, initialize ring `00011`, update site 0, and
consider centre 4. For the second, initialize `01111`, update site 3, and
consider centre 2. Translate the second example to align its centre with the
first; the local rule must be translation-invariant. Both are legal prefixes.
The projected three-cell neighbourhoods agree after the proposed merge, but
their required current-bit outputs differ. Information elsewhere in the ring
cannot help a radius-one update. This is exactly the obstruction missed by
the first whole-field grouping.

Uniform phase rotation supplies these two examples at each of the three
ages. Therefore each of the six previous-bit pairs must remain distinct.
Pairs with different current or age were already required to be distinct by
the readout contract. All twelve original states must consequently have
distinct labels under any admissible pointwise encoding. This proves the
restricted bound without extrapolating from finite survival.

Periodic repetition embeds these source/prefix examples on the integer line
with the same local contradiction. More generally, any source domain admitting
these local prefixes inherits it. This is a witness transfer argument, not
an assertion that every finite-ring positive result transfers to the line.

## What the result does and does not buy

The [published q²+2q construction](https://doi.org/10.1016/j.physd.2004.03.007)
is an essential boundary: it reorganizes computation through different stages
and achieves eight states when q=2. It is not a homomorphic quotient preserving
every atomic transition of the twelve-state scheme. Our result therefore
does not make twelve a universal minimum or establish superiority over eight.

Likewise, the [six-field dimensional lift](2026-09-17-affine-oriented-lift-theorem.md)
uses binary cells spread along a new spatial axis. Its spatial phase is an
address in an encoding, whereas the asynchronous age tracks logical progress.
Comparing six binary rows, twelve local labels and eight protocol states as
bare numbers would conceal different resources. Neither the future-derived
fields X XOR E(X), X XOR E²(X) nor an on-beam synchronous theorem by itself
supplies previous-state availability under asynchronous updating.

The useful finding is the locality distinction: an apparent compression
survived a whole-state necessary check and failed as soon as we asked whether
the required operation could be performed with its promised local access.
This is a concrete way to assess what a representation buys. It supplies no
Class-IV discriminator and makes no claim about the project's different
commutator DE versus ED.

## Reproduction and stop

Run `python scripts/verify_nakamura_retention.py --check`, then
`python scripts/verify_nakamura_local_retention.py --check`. Both commands
regenerate the finite audits, replay the stored counterexamples and reject a
changed report. The follow-up imports the first runner's transition and prefix
definitions; this shared dependency is included in its hashes. A separate
malformed-certificate check confirms rejection of tampered outputs.

This closes the fixed-interface compression question. If the lift program is
reopened, the next contribution must choose an operation and a resource
contract that its representation actually improves, while charging spatial
storage, radius, initialization and cadence. Until such a concrete advantage
is proposed, the correct next action is to integrate and explain these results,
not to widen the numerical search.
