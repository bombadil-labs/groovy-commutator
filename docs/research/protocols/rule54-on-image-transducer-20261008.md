# Prospective bounded gate: Rule-54 J5 on-image symbolic transducer

**Frozen 2026-10-08, before running this gate's numerical/implementation checks.** This is a constructive follow-up to draft PR #329, not a prospective test of its earlier factor theorem. Author: GPT-6 (OpenAI). Independent external review remains pending.

## Wondered

Can we implement the induced Rule-54 J5 evolution by a finite-state, **on-image** input/output relation with explicit size and a practical local decoder, avoiding a fictitious unrestricted 32^13 jet-symbol truth table? This is a *symbolic transducer*, not necessarily a minimized deterministic automaton, compression scheme, or asynchronous streaming implementation.

## Frozen construction

Use Rule 54 H on the bi-infinite binary full shift, A0=I xor H, Ak+1=Ak∘H xor H∘Ak, J5=(A1..A5). For each length-15 binary source word w, label it with the center input 5-bit jet J5(w) and central missing bit A6(w); use the usual length-14 prefix/suffix overlaps as automaton vertices.

The candidate NFA has 2^14=16,384 source-window states, 2^15=32,768 directed edges, jet input alphabet at most 32 symbols and one-bit A6 edge outputs. Reconstruct the full next five-track output via
J5'(i)=(H(G)(i) xor Q(i), H(Q)(i) xor R(i), H(R)(i) xor A4(i), H(A4)(i) xor A5(i), H(A5)(i) xor A6(i)),
where H operates independently on each binary field. This triangular calculation only uses jet neighbors and the transducer's A6 output.

Because the earlier exact full-line factor certificate shows all bi-infinite source lifts with the same entire J5 have equal A6, the restricted bi-infinite edge relation *should* be functional on the admissible jet image. Do not claim a bare NFA produces a deterministic output on all finite jet words, or that arbitrary off-image jets are accepted.

## Frozen execution and pass/fail

1. Implement a standalone no-dependency reproducer, rebuilding local Boolean jet tables directly. Verify the 16,384/32,768 graph sizing and that each edge's input-output label matches direct source evolution on its width-15 window. Freeze Rule 54 only.
2. Exhaustively enumerate cyclic source rings n=8,10,12, compute J5 before/after native H and compare with the candidate edge-transducer's cyclic input/output labels for every ring and every source. For every J5 image on these rings, confirm any multiple source lifts have **one** next jet. Report image count, fiber count, conflicts and mismatch counts. These are finite-ring implementation checks, **not** a new full-line proof.
3. For a reproducible short-window decoder, process a fixed set of 32 length-13 jet blocks (from deterministic periodic source words with n=24, covering multiple phases; no random seeds) using forward source-context dynamic programming over source width-15 edges, constrained by all 13 observed jet symbols. For each block, compute the set of possible central A6 bits; require it to be a singleton and match native A6. Count maximum/median live source contexts. The earlier radius-six certificate, not finite sampling, supplies the all-image guarantee.
4. Give one explicit failure/limitation of off-image or shorter-window use if directly available; otherwise report untested. Do not search other rules, additional jet depths, arbitrary branch minimization, or a 65-bit Boolean table.

If a gate fails, preserve its counterexample and report honestly. Record source hash, exact method, reproducibility command and provenance.

## Stop condition

Once one working finite-state implementation plus these bounded checks are documented, stop this experiment and update a **new self-contained** HTML report edition (do not overwrite Edition 7 if blocked), plus a brief dated research note, on draft PR #329. No merge and no costly CI dispatch.
