# What we have learned

Running plain-language summary, updated 2026-09-22. This is a synthesis of
existing evidence, not a new experiment or independent review. Each entry
links to the technical account that states its assumptions and verification.
“Complete” means the stated investigation has ended, not that every related
mathematical question is solved. The [program survey](2026-09-22-program-survey.md)
explains what deserves work next.

## 1. A disagreement can mean we chose the wrong law

We were curious whether the Groovy commutator detects information lost when
we describe a system by its changes instead of its full state. We compared
“evolve, then describe” with “describe, then apply the original rule.”

We found that these can disagree everywhere even when the description loses
no information. Rule 255 provides a tiny exact example: its change mask is
just the original bits reversed, but the correct update for that mask is a
different rule. A large commutator is therefore not, by itself, evidence of
failed prediction or complexity. First ask whether a suitable update law
exists at all. **Complete: exact counterexample and general factor criterion.**
[Case A and the criterion](representation-case-studies.md).

## 2. Some erased information comes back to matter

We were curious which hidden differences can safely be forgotten. We grouped
states by what an observer sees, then separated groups whenever their observed
futures differed. On finite systems this gives the exact distinctions needed
to determine the observer's entire future.

We found that information hidden now divides into information that eventually
matters and information this observer never needs. Under Rule 106, the same
initial hidden defect stays invisible forever in one finite context and
becomes visible after 51 steps in another. Its surroundings change its fate.
These forward-future partitions are not automatically an online observer's
memory requirement. **Complete examples and finite constructions; no universal
memory bound.** [Erased distinctions synthesis](2026-09-08-dynamics-of-erased-distinctions.md).

## 3. Repairing a description can require a seemingly useless first step

We were curious whether repeatedly adding the most immediately helpful
distinction finds the cheapest predictive description. We compared greedy
repair with exact optima in small, fully enumerated observation families.

It worked in all 1,590 nonclosed two-cell cases. In the three-cell study it
failed in four of 30,856 cases, all in the Rule-24/231 family. In a verified
counterexample, a distinction with essentially no immediate predictive benefit
makes a later distinction much more valuable. The failure also survives a
fresh ring size. **Complete within the tested families:** a concrete reason
that immediate information gain need not find the cheapest representation.
[Repair and predictive synergy](2026-09-08-block3-representation-design.md).

## 4. Coordinates can change the answer unless the observer changes too

We were curious which measurements describe the dynamics and which describe
our chosen notation. We reversed directions, exchanged binary labels,
repacked cells, changed wiring and changed rules away from a preserved family.

We found exact examples of all three possibilities: a quantity stays the
same, transforms predictably, or really changes because the observation was
held fixed while the system changed. In particular, a native commutator
value is not automatically an intrinsic signature of a rule. The observer,
decoding rule and permitted local access belong in the claim.
**Completed audits, now a shared method rather than a standing census.**
[Transformation synthesis](2026-09-10-representation-invariants-program.md#synthesis-after-eleven-units).

## 5. Even every finite ring can miss an infinite-line obstruction

We were curious whether small-ring results reveal how much observed history
determines the next observation. We built finite graphs of pairs of possible
states and checked paths and cycles, producing certificates rather than
extrapolating simulation plots.

We found both late size effects and a stronger domain difference. Rule 58
under observation 232 has a depth-one certificate on every finite ring, yet
fails that property on the infinite line. An explicit pair with periodic tails
shows why. Elsewhere, a certified depth-three ring pattern only settles into
its eventual behavior at size 65. **Complete for the certified contracts:**
small-ring agreement is insufficient, and even all-ring agreement does not
automatically answer the infinite-line question. These are forward observed-word
depths, not universal suffix-memory requirements.
[Executable case C](representation-case-studies.md);
[depth-three certificate](2026-09-14-depth-three-onset.md).

## 6. Every binary finite-memory CA can be represented one dimension higher

We were curious whether one construction could lift arbitrary binary cellular
automata and then lift its own results again. We developed the affine-oriented
six-field construction, a general proof and finite verification cases.

The existence and every-finite-depth recursion question is settled under that
construction's assumptions. The encoded states evolve exactly as the source
and permit local recovery. This is a substantial completed mathematical result.
It does not determine what happens outside the encoded family, establish an
infinite-dimensional limit, or make the construction optimal. A simpler
period-three encoding also meets the broad existence requirement. The open
value question is what the six fields make cheaper or easier to access.
**Existence program complete; resource advantage unestablished.**
[Theorem, verification and simpler baseline](2026-09-17-affine-oriented-lift-theorem.md).

## 7. Sharing a representation is a question about constraints

We were curious when two lifted rules can inhabit one native rule. We compared
the table entries actually forced by their encoded states, keeping unspecified
entries separate from zeros or any other default.

In the specified width-seven/eight cache, 20,944 of 32,640 root pairs admit a
common completion, although no pair has identical individually completed tables
under the four default policies tested. Compatibility is not equality of
arbitrary completions. Rule 0 has more compatible partners than the two core
Class-IV examples, so the raw count does not isolate them. A 54/110 conflict
appears at width eight that width seven misses. **Complete finite audit and
constraint-counting formulas; no global cohabitation or Class-IV theorem.**
[Partial cohabitation](2026-09-15-partial-cohabitation.md).

## 8. Asynchronous computation makes the cost of forgetting concrete

We were curious whether the CRDT-like commuting-update idea lets an
asynchronous CA store less history. We took the established Nakamura simulator
and tested every way of merging its previous-bit distinctions while preserving
current-bit and phase readout, radius-one access and each atomic update.

For Rule 110, all 63 nontrivial mergers fail. Seven passed the first whole-field
necessary check but failed when the update had to use only its local neighbors.
Two reachable examples, rotated through the three phases, prove the restricted
twelve-state requirement. Existing eight-state protocols change the interface;
this result does not rule them out. **Fixed-interface question complete.**
[Causal-retention proof](2026-09-21-causal-retention.md).

The analogy supplied a useful question, not a new equivalence theorem. These
cells compute different pieces of a state, whereas CRDT replicas maintain a
shared object. Commuting asynchronous updates and CRDT convergence already
have established theories: [Gács](https://cs-web.bu.edu/faculty/gacs/papers/commut.pdf)
and [Letia, Preguiça and Shapiro](https://arxiv.org/abs/0907.0929).

## 9. We found a promising finite discriminator, not a definition of Class IV

We were curious whether selective persistence together with disturbance
spreading picks out complex behavior. A frozen statistic separated the 54/110
core from the declared undisputed negatives across five fresh conditions in
the surviving tables: 10 positive decisions and no positives among 420
undisputed negative decisions.

That is a scoped empirical success. It has only two core positive families,
depends on the declared observations and ensembles, and does not settle
disputed cases or generalize to arbitrary CA. Some original protocol and runner
bytes were lost; reconstructed files are not the originals. **Finite benchmark
frozen; universal classification unestablished.** Further threshold hunting on
the same examples would not supply the missing external test.
[Surviving evidence and provenance limits](2026-09-17-selective-persistence-discriminator-record.md).

## 10. Refinements have local mechanisms, but the broad story did not hold

We were curious whether simple lower-dimensional rules predict structured
behavior in families of richer rules. We studied narrow strips, rule families
with the same restriction, and the survival or healing of small defects.

We found exact restriction relationships, finite family differences and useful
local defect mechanisms. Several stronger specificity and transfer predictions
failed. The final held-structures record contains 2,112 rows; a later audit
invalidated three healing-predictor scores because inputs were shifted by one
time step. Nine other scores held and nine failed under their stated tests.
Three corrected witnesses diagnose the bug; they do not repair the full study.
**Paused with retained findings and explicit invalidations; no automatic next
unit or general explanation of Class IV.**
[Program](2026-09-17-class-iv-refinement-program.md);
[completion and correction](2026-09-21-held-structures-account.md).

## 11. Ring arithmetic matters, but its predictive value is uneven

We were curious whether prime factors and divisibility organize relationships
between rules. We enumerated whole-state relations and tested selected
arithmetic associations on held-out sizes.

Most first-study associations reversed sign. A better-balanced follow-up with
arithmetic interactions beat both simpler models in 88 of 252 tasks, but gains
were uneven; for the 54/110 pair it won only on basin relations. This is limited
predictive value, not an arithmetic explanation of Class IV. **Both bounded
studies complete; broader mechanism open and parked.**
[Initial study](2026-09-15-rule-ring-structure.md);
[balanced follow-up](2026-09-15-factor-balanced-interactions.md).

## 12. Failure to find a proof is not proof of impossibility

We were curious whether small machines could certify that hidden defects stay
hidden forever. Several exact encodings and bounded certificate grammars were
tried. Changing the encoding sometimes made a previously difficult finite
question easy, showing that computational cost can belong to the proof method.

The final source-recoder search found no certificate: 14 of 22 seed languages
were ruled out within the frozen grammar, while eight remained unresolved.
Those eight are not negatives. Separately, predictive assembly support has
preserved code and a protocol but no recovered canonical result. **Both are
archived incomplete, not scientifically closed.** Neither creates an obligation
to spend indefinitely just because a finite question remains decidable.
[Recoder account](2026-09-10-erased-distinctions-terminus.md);
[integration dispositions](2026-09-21-research-reset.md).

## 13. A useful readout cache is not yet a dimensional advantage

We were curious whether the six-field lift makes the original Rule-110 Groovy
field cheaper to read than ordinary storage. We compared explicit formulas,
charging initialization, update work, storage and local access rather than
running another census.

The lift's fast readout uses two difference fields. A three-track recoding of
ordinary stored time slices supplies the same four-bit readout and can maintain
it with a local update. The six-field geometry is unnecessary for that marked,
named-track operation. This does not replace its phase-free binary interface:
finding the right row without an address is a different cost. **Bounded design
complete; no-go for a broad benchmark of this proposed advantage.** A real
consumer requiring phase-free geometry would justify a different comparison.
[Derivation and cost contract](2026-09-22-groovy-readout-cost.md).

## 14. No current caller needs the lift's phase-free geometry

We were curious whether some existing operation still required the six-field
lift's address-free binary layout after the marked Groovy readout advantage
disappeared. We audited the active code, site, research registry and current
documentation, separating downstream uses from tools that study the lift
itself.

The public code has no lift caller. The scripts that really consume
unknown-phase windows are verifiers, finite-beam replayers or measurements of
the construction itself. Other open motivations do not declare a workload
that needs spatial phase. **Repository audit complete; leave the dimensional
application question dormant.** This is not an impossibility theorem. A real
future consumer can reopen it by stating its output, geometry, cadence and
full cost contract and by beating ordinary storage, the three-track cache and,
where relevant, the simpler period-three necklace.
[Consumer audit and reopening contract](2026-09-22-phase-free-consumer-audit.md).

## 15. “Recursive G” was three different questions

We were confused by records saying both that Groovy transports through the
lift and that recursive G remains open. We traced each claim to its exact
object instead of treating the shared name as a contradiction.

Ancestral source G already transports exactly through every finite lift depth
using two marked beams. Native descendant cellwise G is a different operation
and is generally completion-dependent. Compressing the two-beam construction
to one marked point beam plus a typed vector sector is still open. The older
P/D carrier census is a narrower finite construction with no induction proof.
**Terminology audit complete; no experiment follows.** The open compression
question stays dormant because the consumer audit found no caller for it.
[Exact boundary and corrected status](2026-09-22-recursive-g-boundary.md).

## 16. The planned empowerment census leaked the action at its endpoint

We were curious whether a representation that leaves many futures possible is
also the representation under which a controller can choose among those
futures. We audited the frozen no-op/flip protocol before implementing its
247-rule census.

Its primary future class includes the observation immediately after the
action. Under identity observation, the controller knows the exact state and
the two actions produce different identity observations, so their outcome rows
are disjoint. Identity therefore has the maximum one bit of capacity for every
rule, while its hidden-future repertoire is zero. This exact endpoint contrast
does not decide whether a repertoire-maximizing observer could also tie at one
bit. It does show that the registered score is not a clean test of dynamical
persistence. The run would also mix controller information, sampling cadence
and outcome semantics and lacks the full saved baseline required by its own
reproduction gate.
**Protocol audit complete; census parked unrun.** A new study would need a
delayed fixed target, common cadence, action-phase controls, a named consumer
and a representation-cost baseline.
[Endpoint proof and disposition](2026-09-22-representation-empowerment-disposition.md).

## 17. More retained differences restore some closure, at an explicit cost

We were curious whether departures from a replicated dimensional beam could
evolve autonomously without retaining the underlying binary field. We first
kept only differences between neighboring transverse slices, then kept both
horizontal and vertical differences.

The transverse-only observation closes for 6 of 66 declared source laws. For
the other 60, complete observed fields can agree while their next observations
differ, so no larger neighborhood of that observation can repair the loss.
The two-component full gradient admits four additional nonlinear laws, for 10
of 66 total, but costs two bits per site and still leaves 56 complete-field
obstructions. A completed follow-up proves that eight nonconstant self-dual
laws preserve periodic loop bits while constants erase them. **Exact
observation-relative sequence complete.** This is a lesson about which state a
factor needs, not compression, intrinsic dimension or spontaneous organization.
[Transverse result](2026-09-10-transverse-difference-closure.md);
[full-gradient result](2026-09-10-full-gradient-closure.md);
[loop invariant](2026-09-10-gradient-loop-invariants.md).

## 18. Pulse shape changed the boundary signature, not the bounded fate

We were curious whether changing the logical shape of two colliding Rule-90
strip pulses would produce extinction, exact reassembly, fold-in or fan-out.
We exhaustively tested eight normalized four-site shapes on each strip, all 64
ordered pairs and 25 relative displacements: 1,600 declared encounters.

Every case acquired exact persistent top and bottom boundary certificates, and
none annihilated or reconstituted as separated strips. Shape still mattered:
the run found 16 paired outgoing boundary signatures. **Frozen four-site family
answered; wider shapes and other geometries remain open.** The aggregate and
audit summaries survive, but the 6.9 MB raw primary file does not and this
legacy lineage is not registered by the current integrity checker.
[Bounded pulse-shape result](2026-09-08-pulse-shape-scattering.md).

## 19. A second correction lift stayed local without becoming spatial

We were curious whether Rule32's second correction lift stays local because of
its inherited family or merely because of one arbitrary total completion. We
exhaustively compared two completions, correction and future coordinates,
inherited and ambient domains, depths zero through two and cap radii zero
through two, using independent evaluators and retained conflict witnesses.

Every inherited case has exact minimum cap radius one under both completions,
while storage grows from 2 to 4 to 6 bits per site. Every declared ambient case
conflicts through radius two. **Bounded comparison complete.** The closure
belongs to the organized inherited family, but the construction remains
product-alphabet state on a one-dimensional lattice. Larger ambient radii and
depths above two remain open.
[Completed second-lift comparison](2026-09-11-second-lift-completion.md).

## 20. Absential compressibility did not add a Class-IV shortcut

We were curious whether the off cells next to live cells separated informally
complex behavior more clearly under the same compression score than the
evolving state itself.
An initial 1D comparison was inconclusive, so we tried the idea where it was
actually motivated: seven Life-like rules on 60-by-60 tori, eight random seeds
per rule, a settled-window comparison, and separate still-life and glider
probes.

In every tested condition, absential-field compressibility tracked the raw
state's compressibility rather than cross-cutting it. For example, Life,
HighLife and the III/IV Day & Night case occupied the same middle region in
both views, while the still-life and glider probes stayed paired. **The
declared separation test is a completed negative, not an open question.** This
is a finite result for one compression score and a small hand-selected rule
set, not an impossibility theorem or a general classifier of CA behavior.
Runtime, observation and storage costs were not compared, so “cheaper” remains
untested.
[Runner and frozen setup](../../scripts/experiment_absential_2d.py);
[published aggregate](../../site/src/data/absential_2d.json).

## Keeping this useful

After a completed or stopped unit, update its entry or add one short account:
what we wanted to know, what we tried, what we found, the domain where it holds,
and what decision it changes. Link to the evidence. Preserve failed predictions,
missing results and corrections. Change an earlier conclusion visibly when
evidence changes it. Do not append every run, reproduce the technical ledger,
or call a parked question solved.
