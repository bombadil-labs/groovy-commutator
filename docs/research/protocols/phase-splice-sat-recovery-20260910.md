# Protocol: phase-splice SAT recovery — 2026-09-10

**Status:** frozen after the primary phase-splice census and before evaluating any previously censored Rule-122/161 seed with the recovery backend.  
**Branch:** `research/relational-source-recoder-20260909`.  
**Working identity:** `phase-splice-sat-recovery`; this is a backend recovery of the already-frozen phase-splice family, not a new public research note or certificate family.  
**Dependency:** the frozen phase-splice protocol/addendum, the committed primary aggregate `results/phase_splice_source_recoder_20260909.json`, and Research032's independent fine-ECA SAT audits.

## Why this recovery exists

The frozen cross-phase `LR/RL` census completed exactly for all ten Class-II frontier seed languages but censored on wall time for all twelve Rule-122/161 Class-III sentinel seed languages. No seed hit the five-million-node MDD ceiling; the largest observed MDD had 1,747,841 nonterminal nodes. The unresolved question is therefore computational representation, not a change in the mathematical certificate.

This recovery keeps the source-recoder family unchanged and replaces only the MDD equality backend with an independent Boolean/CNF encoding of the original fine ECA.

## Frozen recovery domain

Recover exactly these twelve previously censored seed languages:

- Rule 122: `(1,4)`, `(1,5)`, `(3,6)`, `(3,7)`, `(4,5)`, `(6,7)`;
- Rule 161: `(0,1)`, `(0,4)`, `(1,4)`, `(2,3)`, `(2,6)`, `(3,6)`.

These are the twelve Rule-122/161 sentinel seed languages underlying the twelve censored target questions in the primary aggregate. Do not add or remove seeds after recovery outcomes are inspected.

## Frozen candidate family and order

For each seed, use exactly the primary phase-splice family:

- `2 <= t=k+j <= 6`;
- `k>=1`, `j>=1`;
- `delta in [-k,k]`;
- policy in `{LR,RL}` only;
- increasing `t`, then increasing `j`, then `delta` by `(abs(delta),delta)`, then `LR` before `RL`;
- output positions outside the reinserted seed's `j`-step future cone first, ascending, then inside the cone ascending;
- stop a candidate at the first exact counterexample;
- stop a seed at the first exact passing candidate.

No `LL/RR` frontier search is introduced.

## Independent fine-ECA SAT encoding

For one `(seed,candidate,p)` query, let `t=k+j` and use the exact wrap-free source window of `2t+1` macroblocks `[p-t,p+t]`, represented as `3(2t+1)` fine bits.

Create two initial fine rows. Away from macro-coordinate zero they share the same arbitrary background bits. At coordinate zero the left rail is fixed to seed symbol `a` and the right rail to `b`.

Encode the original ECA truth table directly in CNF for `3k` fine ticks on both rails. The resulting rows contain exactly `2j+1` aligned macroblocks and represent `z^L=G^k(x^L)` and `z^R=G^k(x^R)` on `[p-j,p+j]`.

Build the recoded source row directly from those Boolean values:

- at `q=delta`, reinsert terminals `a` and `b` on the two candidate rails;
- elsewhere choose the common three-bit block from `z^L_q` or `z^R_q` according to the frozen `LR/RL` policy.

Continue the actual `z^L/z^R` rows for `3j` fine ticks and independently evolve the recoded rows for `3j` fine ticks. Add one clause requiring at least one of the six final output bits (three per rail) to differ.

Interpretation:

- **SAT** means the candidate fails at position `p`; extract the arbitrary background, reconstruct the macro source, and scalar-replay the original ECA and recoder before accepting the failure.
- **UNSAT** means exact equality at position `p` for every admissible background.
- a candidate passes iff all required positions are UNSAT.

The recovery implementation must not import the MDD builder or use MDD roots to decide any primary query.

## Frozen controls

Before sentinel recovery:

1. reproduce the disclosed Rule-5 positive control, seed `0-2`, `(t,k,j,delta,policy)=(3,2,1,0,LL)`, by proving the mismatch formula UNSAT at all seven required positions;
2. reproduce the Rule-35 negative control, seed `2-6`, by finding a scalar-replayed SAT counterexample for every fresh `LR/RL` candidate with `t<=3` (22 candidates).

Any control failure blocks recovery evaluation.

## Resource envelope

Preserve the primary wall-time comparison:

- **20 minutes maximum wall time per sentinel seed language**;
- the external CI wrapper enforces the same 1,200-second limit even if an individual native solver call does not return;
- one matrix job is used per seed, so one hard seed cannot consume another seed's budget.

No MDD-node ceiling applies because the recovery does not construct MDDs. Record CNF variables, clauses, solver time, candidates tested, and the first failure witness or certificate as applicable.

A seed is:

- `phase-splice-certified` if a frozen candidate passes;
- `no-phase-splice-through-6` if every frozen candidate has an exact scalar-replayed SAT counterexample;
- `censored` if the 1,200-second seed wall is reached before either outcome.

## Recovery hypothesis

Before evaluating the twelve censored seeds:

> **The independent fine-ECA SAT backend completes all twelve previously censored Rule-122/161 phase-splice seed languages under the same 20-minute-per-seed wall.**

This is a representation/backend hypothesis, not a new dynamical certificate hypothesis. The primary phase-splice hypothesis remains whatever the completed recovery implies.

## Fresh positive certificate audit

If SAT recovery finds a phase-splice certificate, freeze the first canonical success before interpretation and independently re-encode its negated identities with Z3 (not PySAT/CNF) over the same fine-ECA cones. Every required position must be UNSAT. A disagreement invalidates the certificate and blocks publication.

If all candidates fail with scalar-replayed SAT models, no separate negative audit is required.

## Outputs

Persist:

1. a per-seed recovery artifact for all twelve seeds;
2. a durable combined audit result;
3. a compact JSON summary and short Markdown report, each carrying hashes/provenance for the full recovery output.

The combined summary must state completed/censored seeds, exact certificates, recovered target-question classification, maximum CNF size, and whether the recovery hypothesis passed.

## Decision rule

- If all twelve recover exactly and none certifies, the complete 22-seed `LR/RL` family is an exact negative through `t<=6`; broaden next to a finite rail-selector mask or synthesized local repair transducer.
- If any seed certifies, independently Z3-audit the first canonical certificate before publication.
- If some seeds remain censored, preserve the family and investigate solver/BDD representation rather than enlarging the recoder or the wall-time ceiling.
