# Recovery protocol: exact completion of bounded source-recoder synthesis — 2026-09-10

**Status:** frozen before any recovery evaluation under this protocol.  
**Parent protocol:** `bounded-source-recoder-synthesis-20260910.md`.  
**Canonical parent result:** `results/bounded_source_recoder_synthesis_20260910.json`, SHA-256 `2d28a4d5e4b668f9a201f3658a986060712a2f9069577810aacd08a49e7f12f2`.  
**Role:** remove computational censoring from the already-frozen final recoder class; this is backend recovery, not a new recoder family.

## Why recovery is required

The parent experiment fixed a 1,200-second wall per seed language. It returned 14 exact bounded negatives and eight scientifically censored seed languages, with no certificates and no infrastructure censoring. Every censored seed stopped specifically during universal verification of a synthesized machine.

The wall was a legitimate preregistered resource limit for that experiment, but it is not a mathematical boundary. The underlying machine class and horizon are finite. The program therefore does **not** terminate on the phrase `terminal-inconclusive-due-to-censoring`.

The recovery objective is:

> **Classify all 22 Research034 frontier seed languages exactly for the already-frozen adaptive rail-selector class with `m<=4` and `t<=6`.**

The 14 exact negatives from the parent result remain exact. Only the eight censored seed languages are recovery cases.

## Frozen recovery set

Use exactly these parent-result censored seeds:

| seed index | ECA rule | ordered seed pair |
| ---: | ---: | --- |
| 1 | 122 | `1-5` |
| 6 | 154 | `6-7` |
| 11 | 161 | `2-6` |
| 14 | 164 | `0-4` |
| 16 | 166 | `0-1` |
| 17 | 180 | `0-4` |
| 18 | 210 | `3-7` |
| 20 | 218 | `3-7` |

Do not add seeds based on apparent difficulty and do not remove any of these cases after recovery begins.

## Scientific quantities are unchanged

The recovery inherits without modification:

- the exact block-3 / cadence-3 macro dynamics;
- the one-defect source language;
- the deterministic adaptive rail-selector machine grammar;
- state budgets `m=1,2,3,4`;
- macro horizon `t<=6`;
- the same `(m,t,j,k,delta)` structural tuples and order;
- the same left-to-right machine scan and initial proof state;
- the same seed reinsertion semantics;
- the same output-position order;
- the same universal equality criterion;
- the same fine-ECA scalar replay requirement for every SAT counterexample;
- the same Rule 5 positive and Rule 35 negative semantic controls.

No larger state budget, longer horizon, additional symbol-repair action, alternate source language, or changed certificate theorem is permitted.

## Parent progress reuse

The parent full result is authoritative for structures already completed as `exact-negative`. Recovery may skip those structures after verifying the parent result hash and matching its frozen source hashes.

The compact parent structure records intentionally do not contain the full accumulated CEGIS counterexample list. Therefore the first censored structural tuple for each recovery seed is restarted from an empty CEGIS example set rather than reconstructing hidden state. This can repeat work but cannot change the answer.

A recovered certificate stops that seed exactly as in the parent protocol. A recovered exact-negative structural tuple advances to the next frozen tuple. A seed is globally exact-negative only after every remaining structural tuple has been proved exact-negative.

## Exact verification recovery: partition instead of censor

For a fixed synthesized machine and output position, the verifier asks whether there exists a finite source-background assignment producing a mismatch. This is an ordinary finite SAT question.

Use the same manual fine-ECA CNF as the parent verifier. For each query maintain a queue of partial assignments to the **shared source-background bits**. Each queue item denotes a disjoint cylinder of the original finite background space.

For one queue item:

1. try the exact SAT portfolio below under the item's assumptions;
2. SAT means a concrete mismatch candidate; recover the full model and scalar-replay it before accepting the counterexample;
3. UNSAT closes that cylinder exactly;
4. if no portfolio solver decides within its operational slice, split that cylinder on the next unfixed background bit and enqueue the `0` and `1` children;
5. if all background bits are fixed, decide the leaf directly with scalar fine-ECA evolution and the fixed machine, without relying on SAT termination.

The whole verifier query is SAT as soon as one replayed mismatch is found. It is UNSAT only when every cylinder in the queue has been closed. This preserves the original universal semantics exactly.

### Frozen split order

Exclude the origin seed bits, which are fixed. Order free source-background bits by

1. increasing `abs(q)` of the macrocell coordinate;
2. then increasing signed `q`;
3. then macro-symbol bit `0,1,2`.

Always split on the first unfixed bit in this order. This order is operational only and has no scientific status.

## Solver portfolio

For each SAT cylinder, try available PySAT solvers in this fixed preference order:

1. `cadical195`;
2. `glucose4`;
3. `maplechrono`;
4. `minisat22`.

Unavailable backends are recorded and skipped. `minisat22` is required because it is already part of the parent environment.

Each solver receives **10 seconds per cylinder** before the cylinder is split. This is an operational decomposition threshold, not a scientific wall: exceeding it never produces `censored`, `negative`, or `positive`; it only causes exact partition refinement.

SAT results from any backend require the same independent scalar replay. UNSAT closes only the current assumption cylinder. A complete UNSAT verifier result is the union of all closed cylinders.

## Synthesis side

The parent censoring set contains no synthesis-wall cases. Synthesis therefore first uses the same finite machine constraints with the solver portfolio above. If a synthesis query itself fails to decide under the portfolio, it must be made resumable by an analogous partition of the finite machine-table assignment space; it may not be reported as scientific censoring.

At a fully specified machine-table leaf, evaluate all accumulated concrete CEGIS examples directly. Thus backend nontermination cannot become a scientific endpoint there either.

## Checkpointing and infrastructure

Recovery is a **completion campaign**, not a fixed-wall performance experiment.

Implementations may use bounded infrastructure slices, but every slice must write a deterministic checkpoint containing enough information to resume without changing the search:

- seed identity and parent-result hashes;
- current structural tuple and its frozen ordinal;
- accumulated scalar-replayed CEGIS examples;
- synthesized machine, if currently in verification;
- current output-position ordinal;
- pending verification cylinders / partial assignments;
- exact-negative structures completed in recovery;
- solver/backend availability and per-cylinder outcomes.

An infrastructure timeout or batch boundary has status `pending`, never `censored`. Subsequent runs resume the same checkpoint. No scientific conclusion is emitted until the seed is `bounded-recoder-certified` or `no-bounded-recoder-through-4`.

The finite direct-evaluation leaves make this recovery logically terminating if enough computation is supplied. No claim is made that the worst-case workload is practically small.

## Controls

Before recovery seeds are interpreted:

1. reproduce the parent Rule 5 `m=1,t=3,k=2,j=1,delta=0` certificate;
2. reproduce the parent Rule 35 exact negatives for the declared `m<=2,t=3` control structures;
3. take at least one parent verifier query known to return a SAT counterexample and require the partitioned verifier to recover a replaying counterexample;
4. take at least one parent verifier query known to be UNSAT and require the partitioned verifier to close it exactly;
5. force the operational solver slice to zero on a tiny control so the split-to-direct-leaf path is exercised and agrees with ordinary exact verification.

A control disagreement blocks recovery interpretation.

## Exact completion and independent audit

For each of the eight seeds, the only final statuses are:

- `bounded-recoder-certified`, with the first certificate in the inherited structural order; or
- `no-bounded-recoder-through-4`, after every inherited structural tuple has exact-negative status.

No `censored` final status exists in this recovery protocol.

Any fresh frontier certificate must still receive the parent protocol's independent Z3 or separately implemented Boolean audit before publication.

For a recovered all-negative seed, retain enough partition evidence and solver statistics to reproduce the exact CEGIS path. The final program synthesis must distinguish solver UNSAT evidence from direct fully assigned leaf checks.

## Program decision rule

The Dynamics of Erased Distinctions program remains open until all eight recovery seeds are classified exactly under this protocol.

After exact completion:

- if any certificate exists, audit it independently and report the minimum inherited proof-state budget at which it occurs;
- if all 22 seeds are exact-negative, report the complete bounded negative for `m<=4,t<=6`;
- in either case, proceed to the program-level synthesis and terminus note;
- do **not** respond by enlarging `m`, `t`, or inventing another selector family inside this program.

The recovery changes the backend and scheduling semantics only. It does not revise the parent hypothesis after seeing the result.