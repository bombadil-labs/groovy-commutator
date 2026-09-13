# Dynamics of Erased Distinctions: synthesis and research terminus

**Date:** 2026-09-10  
**Program:** Dynamics of Erased Distinctions  
**Status:** provisional program synthesis; exact recovery of the eight bounded-recoder verification censorings is active  
**Scope:** the matched block-3/cadence-3 ECA observer and one-defect frontier developed in Research022 onward. Claims below inherit the domains and caveats of their cited checkpoints; they are not statements about arbitrary cellular automata or arbitrary coarse-grainings.

## The question that survived the program

The program began with a simple observation-relative problem: if a representation `P` identifies two concrete states now, when can the erased distinction matter again?

For a fixed forward-invariant source family, dynamics `F` at cadence `q`, and observation `P`, let

```
R_0 = {(s,s') : P(s)=P(s')}
R_t = intersection_{0<=j<=t} (F^q x F^q)^(-j)(R_0)
R_infinity = intersection_{t>=0} R_t.
```

Closure is the special case in which the initial observational equivalence already respects the dynamics: `R_0 = R_1`, equivalently a deterministic factor law exists on `im(P)`. When closure fails, the descending chain records exactly when previously erased distinctions become visible.

The later source-recoder work sharpened a second question. Finite visibility is not the same as an all-time permanence proof. If an attached distinction has not reappeared through a finite horizon, what finite proof object, if any, certifies that it never will?

That second question is where this research line terminates.

## What is established

### 1. Erasure is dynamical, not merely informational

A distinction can be invisible under the present observation while remaining causally active. Research022--026 separate observational closure, finite visibility time, permanently shielded information, latent information, and future repertoire. The same macrostate can therefore carry hidden distinctions with different dynamical fates.

The exact history-lift relation gives a finite-time hierarchy of repaired observations. This is not an appeal to visual similarity: it is the refinement required to make formerly ambiguous future observations distinguishable.

### 2. Finite visibility and all-time permanence need different proof objects

The Research032 causal-witness MDD solves finite target visibility symbolically on exact local causal cones. Across the later frontier there were no new witness births at macro-horizons 4--6; the 12 hard Rule122/161 horizon-6 cases were independently recovered as UNSAT with both Z3 and PySAT.

But the absence of a finite witness through `h=6` is not an all-time theorem. The permanence problem was therefore converted into exact orbit inclusion for the one-defect source language.

Research036 established the relevant symbolic-dynamics fact: the paired one-defect source language is sofic; sliding-block images remain sofic; and an inclusion of the form

```
X_{t+1}(s) subseteq union_{j<=t} X_j(s)
```

together with target safety on the finite prefix gives an all-time permanence certificate. An exact target-visible label supplies a finite counter-witness when inclusion fails.

This theorem separates *what would prove permanence* from *how expensive that proof representation is*.

### 3. Presentation complexity and dynamical complexity are different

The direct exact sofic construction hit a representation wall. The 170-question frontier remained unresolved through the frozen explicit graph budgets even though compressed graph presentations stayed modest. Raw finite-horizon construction grew from 17 transitions at `h=0` to more than six million required transitions by `h=3`, exceeding the frozen five-million ceiling.

Research037 then represented exact local dynamics as reduced ordered 8-valued MDD functions. This cleared the explicit graph wall, and recovered a genuine control identity for Rule5, `G^3 = G`. Yet all 170 frontier questions had no same-source recurrence certificate through `h<=6`.

The important negative was structural: compact exact local dynamics did not automatically produce a compact reachability certificate.

The next experiment made that distinction sharper. Phase-splice MDD evaluation censored all 12 Rule122/161 sentinel languages under the frozen wall, but the *same mathematical candidates* encoded directly as fine-ECA CNF were tiny and completed exactly. Minisat22 recovered all 12 as negatives with at most 1,314 variables and 9,943 clauses.

So difficulty in one symbolic representation was not itself evidence of intrinsically hard dynamics. Throughout this program, censoring is treated as a statement about the chosen proof representation and resource envelope unless an independent mathematical obstruction is supplied.

### 4. Changed provenance is necessary to ask the general inclusion question, but simple provenance repair is insufficient

Same-source recurrence was too restrictive. Exact orbit inclusion may represent a later paired output by a *different admissible source row* because the one-defect source language contains arbitrary common background outside the defect.

The next proof-state hierarchy therefore allowed the recoder to change provenance while preserving the one-defect source contract.

The first fresh family used a single phase cut: choose the evolved left rail on one side and the evolved right rail on the other (or conversely), reinsert the original seed, then continue evolution. Across the complete 22-seed / 170-question frontier, fine-ECA SAT recovered an exact negative for every fresh LR/RL candidate through `t<=6`. No censoring remained.

That result rules out one global bit of left/right provenance phase as a sufficient universal repair on this frontier.

A two-switch `LRL/RLR` island family was then frozen as the last hand-designed selector geometry. Its purpose was diagnostic: test the smallest additional spatial selector freedom without beginning an endless hierarchy of three, four, five, ... explicit cuts. Infrastructure instability prevented a clean canonical census under the original workflow; this rung is not promoted as an exact mathematical classification. It motivated the terminal generalized synthesis instead.

### 5. The terminal experiment searched proof-state, not hand-designed geometry

The final substantive experiment replaced explicit cut patterns with bounded adaptive source-recoder synthesis.

A deterministic Mealy-style selector scans the evolved paired source, carries at most `m` hidden proof states, chooses which evolved rail supplies each recoded background symbol, updates its proof state, reinserts the original defect seed, and then asks for exact equality after continued evolution. SAT/CEGIS proposes a machine from accumulated concrete counterexamples; a separate universal fine-ECA CNF verifier attacks the proposal over all admissible backgrounds. Replayed counterexamples are returned to synthesis.

The frozen terminal ladder was `m=1,2,3,4`, `t<=6`, with a 1,200-second wall per seed language. No larger machine class is authorized by this program.

The controls passed: Rule5 supplies a positive synthesis control and Rule35 supplies bounded negative controls.

Initial bounded-synthesis checkpoint:

- seed languages: **22**;
- target questions: **170**;
- bounded adaptive certificates found: **0**;
- exact-negative seed languages through four proof states: **14**;
- scientifically censored seed languages: **8**;
- infrastructure-censored seed languages: **0**;
- exact-negative target questions: **30**;
- scientifically censored target questions: **140**;
- checkpoint outcome: **inconclusive under the original per-seed wall; exact recovery required before program closure**.

All eight censored seeds reached the frozen scientific wall during universal verification. Their censoring is not converted into a negative result.

The durable audit is `results/bounded_source_recoder_synthesis_20260910.json`, SHA-256 `2d28a4d5e4b668f9a201f3658a986060712a2f9069577810aacd08a49e7f12f2`. The compact companion is `results/bounded_source_recoder_synthesis_20260910_summary.json`.

### 6. Resource censoring triggered backend recovery, not program termination

The 1,200-second wall was preregistered to keep the original synthesis experiment interpretable. It is not a mathematical boundary. Because all eight unresolved cases stopped during universal verification, the machine grammar itself need not be enlarged to continue the exact question.

A separate recovery protocol therefore holds fixed every scientific parameter of the terminal search -- the same 22 seed languages, `m<=4`, `t<=6`, deterministic adaptive rail-selection grammar, source semantics, structural order, and exact certificate criterion -- and changes only the verification backend.

Hard universal-verification SAT queries are solved by an exact resumable decomposition. A solver portfolio first attempts the whole query. If it does not decide the query within an operational slice, the remaining finite background assignment space is partitioned on a source bit. Subproblems are solved independently and may be partitioned again. At fully assigned leaves the CA equality is evaluated directly, so repeated solver timeout cannot become a scientific terminal state. Work queues are checkpointed and resumed across infrastructure runs.

Under this recovery regime, an unfinished batch is reported only as **pending**. The recovery terminates scientifically only when each of the eight previously censored seed languages is either supplied an exact bounded-recorder certificate or exhausted as an exact bounded negative.

The required program-level finish condition is therefore:

```
22 / 22 frontier seed languages exactly classified
for the frozen m <= 4, t <= 6 adaptive recoder class.
```

No larger machine state budget, longer structural horizon, new selector geometry, or relaxed certificate semantics is introduced by this recovery.


## The proof-state hierarchy

The source-recoder sequence can now be read as a bounded hierarchy of proposed permanence witnesses:

```
same-source temporal recurrence
    < changed source provenance
    < one spatial phase cut
    < two-cut diagnostic selector
    < bounded adaptive finite-state selector (m <= 4).
```

This is not claimed to be a universal complexity hierarchy. It is a controlled sequence of increasingly expressive proof grammars for one exact frontier.

What the sequence establishes so far is more modest and more useful: no positive frontier certificate appeared before the terminal finite-state rung, the one-cut family is exactly negative on the full frontier, and the initial generalized finite-state run proved 14 seed languages negative while identifying eight exact-verification cases that require backend recovery. Their mathematical status remains open until the recovery completes.

This suggests a quantity worth future formalization but not claimed here as an established invariant: the **proof-state complexity of erased distinctions** -- the minimum additional state or representation complexity needed to restore an exact closure/permanence argument after an observation erases a distinction. The current program measures lower bounds and representation barriers for one concrete family; it does not yet prove that such a minimum is well-defined or representation-independent in general.

## What the program did not establish

The following are deliberately *not* conclusions of this work:

- that the eight censored terminal seeds have no finite-state recoder;
- that four states is a mathematically privileged universal bound;
- that failure through `t<=6` implies failure at all later structural horizons for the synthesized recoder family;
- that SAT/MDD/sofic difficulty measures intrinsic computational complexity of the underlying CA;
- that the tested block-3 observer is optimal or canonical;
- that Class IV behavior is selected by these criteria;
- that coarse-graining, differentiation, renormalization, or dimensional lifting are interchangeable constructions;
- that the proposed proof-state complexity is a general invariant.

The program repeatedly found reasons to keep these distinctions explicit rather than collapse them into one narrative.

## Why exact recovery now precedes the terminus

Increasing `m`, increasing `t`, or inventing further selector geometries would enlarge the scientific hypothesis. That remains outside this program.

Changing the backend for the eight already-frozen cases is different. Their question is finite and exact, and the earlier phase-splice recovery already demonstrated that a representation wall can disappear under another exact encoding. Ending the program merely because an arbitrary wall expired would therefore mistake an implementation budget for a mathematical conclusion.

The current recovery is consequently part of finishing the existing experiment, not a new rung of the selector hierarchy. It has no scientific timeout outcome: infrastructure slices may end, but unresolved work is checkpointed as pending and resumed.

Once all eight cases are decided, the program has a principled stopping point. At that point every frontier seed language will have an exact classification for the declared `m<=4`, `t<=6` adaptive-recorder class. Any subsequent increase of machine state, horizon, or proof grammar would require a newly motivated research question rather than being an unfinished obligation.

Future work may still reopen qualitatively new questions:

1. prove a structural theorem giving a principled bound (or impossibility result) for source-recoder state;
2. change the proof object qualitatively -- for example an invariant, order-theoretic abstraction, or another exact quotient -- rather than merely enlarge the present selector grammar;
3. study intervention-relative revisability/empowerment or adaptive observation as separate representation questions under their own frozen protocols.

Those remain separate continuations.

## Program conclusion

The durable result is therefore not a single positive recurrence formula. It is a separation of several notions that initially looked interchangeable:

- **erased now** versus **causally irrelevant**;
- **finite witness absence** versus **all-time permanence**;
- **compact local evolution** versus **compact reachability proof**;
- **mathematical obstruction** versus **representation/resource censoring**;
- **same provenance** versus **admissible changed provenance**;
- and, finally, **hidden causal information** versus the **proof-state required to make that information dynamically manageable**.

Within the declared frontier, the program has pushed each distinction to an exact theorem or exact negative except for the eight bounded-recorder verification cases now under exact backend recovery. Those cases must be classified before this note becomes the program's final closure record.

**Recommendation after recovery:** publish this synthesis with the completed source-recoder classification, mark *Dynamics of Erased Distinctions* **complete / dormant**, preserve the frozen empowerment and online-observer continuations as separate planned work, and do not silently resume the selector-state ladder.
