# Frozen protocol: separate temporal cycles from spatial drift

Status: frozen before implementation and evaluation, 2026-09-14.

Authored by: Codex (OpenAI), Myk's dimensional-lift session. Protocol review: pending independent review; Myk's explicit earlier session override of Gate 1 remains authorized. No evaluation has run at this revision.

## Question and fixed scope

Annotate Rule 110's reported two period-91 cycles and Rule 54's reported four period-112 cycles on the binary periodic ring of size 14. The user approved this narrow follow-up, not the brief's proposed ring-size census. Source: the supplied Fable brief `Pasted markdown(4).md`, SHA-256 `d954a378b92a280c8978a3e43c2c80839d30f67770dbdf2386701adfd99d7e22`.

The brief supplies counts, not cycle states. Workspace and main-repository searches did not locate the corresponding raw cycles. Reconstruct the two 16,384-state transition graphs solely to recover and check these cycles. Preserve every cycle found and its period count as provenance, but the six reported long cycles are the primary annotation targets. Do not rerun the halo/gcd test, build any lift, expand ring sizes, or search other rules for a favorable result.

Reported spectra to check, without treating them as independently verified input:

- Rule 110, N=14: {1:1, 7:2, 12:7, 14:1, 21:2, 91:2}.
- Rule 54, N=14: {1:1, 4:49, 112:4}.

## Conventions and quantities

Bit i of the state integer is cell i. ECA update is bit `4*left+2*center+right` of the rule number; boundaries are periodic. Translation is `(tau_a S)_i = S_(i+a mod N)`, so positive a moves the visible pattern toward decreasing indices. The canonical representative of a temporal cycle is its smallest state integer, followed in forward ECA order.

For each primary cycle record p, its ordinary least temporal period; d, the smallest positive spatial translation fixing its representative (d divides N); q, the smallest positive t such that E^t(S)=tau_a(S) for some a; the unique a in 0..d-1; the signed representative of a with ties at d/2 taken positive; and m=d/gcd(d,a). Record the exact witness states, complete cycle and first q steps including the return.

Check the identity p=q*m and the minimality of p, d and q directly. Check d, q and a at every temporal phase of each target cycle. Translation commutes with E, and spatial stabilizers are constant on a periodic orbit; hence these values must agree. Group target temporal cycles by equivalence under spatial translation and temporal advance; preserve the group representative without treating related cycles as independent examples.

The q=13, a=2 example in the preceding conversation was illustrative, not a directional prediction. This is a descriptive exact annotation. Classify q=p as no shortening by rotation and q<p as shortening; report whichever decomposition occurs. A mismatch with a reported spectrum is a finding, not a reason to alter the rule convention or pick alternative cycles. If a target period is missing, mark it absent and retain the discovered spectrum.

## Implementation, controls and budget

Use the repository's vectorized `groovy.ca.apply_rule` for the complete successor graph. When batching words, pad each row with its own periodic boundary cells and discard the padding after the update, so the engine's flattened rolls cannot mix different source words. Independently cross-check every successor for both rules using a literal scalar neighborhood implementation. Extract graph cycles by removing transient vertices using indegree pruning, then following the remaining permutation cycles. Retain all cycle states so their edges and disjointness can be checked independently.

Known-answer controls before the target run: a single 1 under Rule 170 at N=14 has (p,d,q,a)=(14,14,1,1); a single 1 under identity Rule 204 has (1,14,1,0); and a period-two alternating word under Rule 170 has (2,2,1,1). These control translation signs, zero drift and shorter spatial motifs. Check the algebraic period formula in all cases.

Budget: two target graphs, no more than 60 seconds and 512 MiB process RSS. Stop on verification failure or budget exhaustion, preserving the failure and completed work. Do not expand the scope or tune a hypothesis after outcomes. Record implementation SHA, source hashes, UTC time, elapsed time, peak RSS and runtime versions. Commit protocol, implementation and results in that order.

## Interpretation and preservation

For a faithful one-step lift, injectivity and HL=LE imply H^p(L(S))=L(S) iff E^p(S)=S. The beam therefore inherits the same primitive periods. This run studies the source automata directly and makes no new assertion about local lift existence at ring size 14.

Neither large prime factors nor a decomposition involving N establishes a new prime-distribution law. The result concerns these two rules and this one ring. Any rule-size arithmetic census, additive-baseline comparison or Witt-ring investigation is separate future work.

Preserve code, exact cycle data, CSV annotations, execution metadata, a hash-bound canonical account, a short note and knowledge/checkpoint links. If useful, render a static spacetime figure from saved cycle data after evaluation; it supplies no additional evidence. Automatic CI performs only provenance and saved-data accounting, not CA enumeration. Full scalar checks and independent scientific review run locally. Independent exact-head Gate 2 is required before integration into main.
