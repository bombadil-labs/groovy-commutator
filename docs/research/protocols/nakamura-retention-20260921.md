# Frozen protocol: can Rule 110 forget a previous-state distinction?

Status at freeze: unrun. Authored by Codex (OpenAI), 2026-09-21.
Reviewed by: none. Protocol review: none at freeze; run and solo integration
authorized by Myk on 2026-09-21: “Do it! You’re flying solo, set it up however
you’d like and churn on it?” This applies to the case-study and bounded
causal-retention unit in this session, not to future research by default.

## Decision

The representation program asks which distinctions can safely be discarded.
Nakamura's asynchronous simulation supplies a concrete existing interface to
test, rather than a new classifier. Can a pointwise quotient of that simulator
forget any previous-state distinctions while preserving the current bit, the
modulo-three phase, and the exact effect of each permitted cell update?

If a nontrivial quotient survives, report only that it survives the finite
obstruction search; an all-domain congruence proof is required before using
it. If every nontrivial candidate fails on reachable configurations, close
this direct-compression route under the stated interface. Do not respond by
enlarging a census or searching different rules. The alternative of changing
the interface/cadence is already established in the literature.

## Prior art and non-claims

Use the current/previous/age construction in
[Gács, section 3](https://cs-web.bu.edu/faculty/gacs/papers/commut.pdf), credited
to Nakamura's simulation tradition, and the explicit account in
[Lee et al. (2004), section 2](https://doi.org/10.1016/j.physd.2004.03.007).
The former identifies commuting enabled updates and notes that only the old
message field need be retained when that is all neighbours consult. The latter
also supplies a different construction with q²+2q states. Consequently twelve
states is not a general lower bound for asynchronous simulation of a binary
CA. This unit cannot establish novelty or a Class-IV signature.

The spatial six-field lift and its period-three necklace alternative have
different contracts: binary alphabets and an added spatial axis, with exact
synchronous dynamics on their encoded families. No scheduling property or
resource advantage transfers from those existence theorems automatically.

## Fixed mathematical interface

The local alphabet is S = {0,1} × {0,1} × Z/3, with components (current,
previous, age). The spatial neighbourhood is radius one on a ring. A cell
waits when either neighbour is behind: (neighbour.age - cell.age) mod 3 = 2.
Otherwise use each neighbour's current bit at equal age, and previous bit at
age one ahead; apply the source ECA to those bits and the cell's current bit;
save that current bit as previous and increment age. An atomic update reads
one pre-update neighbourhood. Progress under fair scheduling is separate
from the finite safety checks below.

The target source rule is 110. Rule 204 is an identity control only. A quotient
must keep current and age exactly readable at the same site, with no increased
radius, added state, alternative readout, or altered update cadence. Thus the
only possible identifications are the six pairs with fixed (current, age)
and different previous bits. There are 2^6 = 64 equivalence relations, one for
each choice to retain or merge those pairs. The uncompressed identity map is
included. No restriction to an affine/XOR compression is imposed.

For a candidate Q, apply it pointwise to the whole configuration. If Q(s)=Q(t),
every update label i must have the same enabledness in s and t and, when
enabled, must satisfy Q(U_i(s))=Q(U_i(t)). This condition defines an exact
quotient of the labelled transition system. A single conflicting pair refutes
it. This is an elementary operation-wise extension of the existing factor
criterion, not a claim to a new general theorem.

## Frozen finite checks

1. Local construction control: enumerate all 12^4 four-cell windows and test
   both orders of updating the two interior cells whenever both are enabled.
   Compare with their simultaneous update from the original window; also
   check persistence of the other's enabledness. Test both fixed source rules.
   This is the complete local diamond check for adjacent updates; nonadjacent
   updates commute by their disjoint writes and absence of mutual reads.
2. Reachable obstruction domain: ring width five; all 32 source bit strings;
   uniform initial age a in {0,1,2}; previous=current initially; all 32 subsets
   of sites advanced exactly once. Construct each prefix by updating its
   selected sites in increasing order and verify every update is enabled.
   The phase rotations are part of the declared initialization family, not
   arbitrary independently assigned clocks. This is 3,072 prefix records per
   source rule before deduplication. Every subset is legal because no cell is
   more than one step ahead of an unadvanced neighbour.
3. For all 64 quotients, group these reachable configurations by their whole
   observed field. Compare enabledness and the projected successor for each
   of five update labels. A tested successor may lie outside the prefix
   collection; Q is defined on all S^5. Store a replayable initial bit string,
   initial age, prefix update list and final update for each failed candidate.
   Also record whether the difference is visible in current bits themselves.
4. Identity quotient must pass for both source rules. All quotients should
   pass the identity-rule control, since previous=current throughout its
   reachable evolution. Rule 110's compression outcome is open at freeze;
   do not silently omit surviving candidates or reinterpret a timeout.

## Budget, outputs, and stopping rule

One deterministic runner, one canonical JSON, one short interpretation note.
The canonical run has a 60-second timeout; if exceeded, report censored and
stop rather than expanding resources. No random schedules, new ring widths,
further source rules, solver calls, or six-field implementation are authorized
by this protocol. It is a necessary-obstruction search, not a complete search
over all asynchronous CA implementations. A reachable counterexample on the
ring also obstructs the identical local quotient contract on the infinite line
by spatial periodic repetition of the configuration and update pattern.

Record script, protocol and imported CA source hashes. Replay every stored
counterexample from initialization, and compare the canonical report with a
deterministic regeneration. Include a tampered-witness rejection check. Freeze
this protocol in git before implementing/evaluating the runner. A discovered
gap changes the account explicitly; it does not authorize an automatic next
experiment. Land the completed case studies and this bounded outcome, then
leave an agent-readable handoff reflecting what was actually learned.
