# A physically stored finite correction cap closes indefinitely, without general repair

Date: 2026-09-10. Evidence: exact local identities and scoped exhaustive physical/intervention audits.

**The Rule32 two-row correction system now has a complete physical realization under the existing interpreter.** It needs no additional future correction rows. Every matched instruction/data edit also executes faithfully as an edit of the native program/data field. Neither property guarantees that the edited system continues to represent the original source, or repairs itself.

The frozen odd-ring data-damage tests recover, but all their undamaged trajectories become zero. A separate deductive counterexample on a persistent background shows an expanding error from one top-row data or instruction edit. Recovery is not a general property of this cap.

## Frozen experiment and provenance

The [physical-cap protocol](protocols/rule32-physical-cap-20260910.md) was frozen in commit `f65a63ea5a96824cbed850043b286ad0e5b7c3be`, following the [logical-cap census](2026-09-10-local-correction-caps.md). The [implementation](../../scripts/verify_rule32_physical_cap.py) was committed as `1edb7f77321734074e5939a7d79b5b287f2d1e06`. Pre-execution review caught a one-site offset in the three derivative test windows; commit `4d71ba01a1574917abb94bf7a841bdb44646d425` corrected their centering before any evaluation. This correction is retained in the [canonical result](../../results/rule32_physical_cap_20260910.json). There were no protocol deviations or changes to the ambient interpreter.

The result contains all 40 baseline trajectories, all 1,360 edit trajectories and per-tick predicates, the first zero-cap failure, and resource/count metadata. CI reruns the verifier and compares exact JSON. Counts are exhaustive cases within declared budgets, not independent statistical samples.

## The finite physical strip

For fixed homogeneous Rule32 on the full infinite horizontal binary lattice, define D=I xor F, A_0=D and A_1=D F xor F D. Write U=A_0(S), V=A_1(S). The previously established identities give

\[
U'=F_{32}(U)\oplus V,\qquad V'=F_{128}(V).
\]

Use the unchanged five-symbol H_2 interpreter, in hold-program mode, with four occupied logical rows:

| Logical row | Initial data | Stored two-word program | Role |
| --- | --- | --- | --- |
| -1 | 0 | (204,240) | Lower guard |
| 0 | A_0(S) | (32,60) | Derivative transport |
| 1 | A_1(S) | (128,240) | Closed top correction |
| 2 | 0 | (204,240) | Upper guard |

Each logical site has one data symbol and sixteen program symbols in the existing scale-nine layout. Every other physical site is blank. Program60 computes first-stage output xor the positive vertical neighbor. Program240 selects the first-stage output and ignores vertical data. The top still needs occupied vertical neighbors because the interpreter validates their presence before evaluating either table. Guard data freeze because their outward required neighbor is absent.

## Complete-field, all-time identity

Let E(S) be the four-row native field above and J its existing physical encoding. Then

\[
\boxed{H_2\,J E(S)=J E(F_{32}(S))\quad\text{for every }S.}
\]

The proof checks all symbol roles, not just row0:

- Row0 executes F_32(U) xor V=A_0(F_32(S)).
- Row1 executes F_128(V)=A_1(F_32(S)), by the seven-bit local identity.
- Both guard rows retain zero because of their missing outward data inputs.
- Every program bit is held. Blank is absorbing regardless of its neighbors.

These cases exhaust the physical field. The resulting field is exactly freshly prepared for F_32(S), so induction establishes every nonnegative time. Preparation reads the current source within radius at most two; it does not require future observations, an infinite correction stack, or external updates. This is a realization of the represented pair, not a claim that the encoding recovers the original S or represents every possible physical state.

## Audit coverage and the retained failed cap

An independent shrinking-window evaluator checks 384 semantic identities on all 128 seven-bit source windows. The physical rule is checked on all 32 five-bit data neighborhoods for each active program: 64 cases, plus 64 missing-neighbor guard cases and 1,024 held local program-symbol checks.

The complete-field runs use horizontal ring widths3 and5, every source word, and ticks0 through40. At every timepoint they compare the physical field with independently indexed native execution and with fresh preparation of the evolving source. No native update calls the physical selector implementation.

The same runs replace the top program with (32,240) as the frozen zero-cap control. This fails: the first witness is width5, initial source integer11, tick1. The correct pair is (U,V)=(28,8), whereas the zero-cap pair is(28,0). Ring bit x has weight 2^x. Across all40 controls and their41 timepoints there are10 pair mismatches. The original cap is not dispensable merely because many finite trajectories soon die out.

Including baseline, zero-cap and edited runs, 15,520 complete-field timepoints compare 4,854,656 occupied symbols and 29,857,376 explicit blank positions. Sparse-field equality and absorbing blank also account for the infinitely many omitted exterior blanks. Explicit blank counts cover one horizontal period, the strip and a one-macrocell vertical halo, plus a remote exterior check; they are not a count of all sites of the infinite lattice.

## Edits execute correctly; semantic recovery is separate

For every one of40 initial source words, each of32 active instruction bits and each of2 active data bits is separately flipped at horizontal site0. All1,360 edits change exactly one physical symbol. Through ticks0..8, every complete physical field agrees with independently executed edited native dynamics. This is Contract A: faithful editing of the native field, not an implicit edit of the original homogeneous Rule32 source law.

Contract B measures three different predicates: equality with the undamaged active data pair, membership in the fixed-Rule32 K_1 image of the same finite ring, and equality of the stored program field. The result retains every predicate at every tick, including repeated exits and re-entries.

| Edit type | Cases | Ever differ from undamaged data | Ever leave ring image | Match undamaged data at tick8 | Same programs at tick8 |
| --- | --- | --- | --- | --- | --- |
| Instruction bit | 1,280 | 260 | 145 | 1,116 | 0 |
| Active data bit | 80 | 80 | 62 | 80 | 80 |

Program bits cannot revert in hold mode. A program-edited run can temporarily match the undamaged data and diverge again: from the all-zero width3 source, changing bottom leaf bit0 makes the active pair alternate (0,0),(1,0),(0,0),(1,0),... through the tested horizon. The pair remains in the finite-ring represented image throughout these recorded ticks. Thus image membership, trajectory agreement and program recovery are not interchangeable, and tick8 agreement does not mean permanent recovery.

All data-only edits match the undamaged pair by tick5 (by tick3 at width3). However, every undamaged baseline in this odd-ring panel is already the all-zero pair by tick3. This is extinction-confounded recovery, not evidence that the representation maintains arbitrary persistent structure. Finite-ring image membership is also not full-shift image membership.

## Deductive persistent-background non-repair witness

The following is a post-audit deduction from the exact local law, not an expanded experimental panel or a rewritten protocol.

Take an alternating full-lattice source S. Rule32 exchanges its two phases, so D(S)=1 everywhere. D(F(S))=1 and F_32(1)=0, hence A_1(S)=1 everywhere too. The represented pair (U,V)=(1,1) is therefore a fixed point, arising from a non-extinguishing source orbit.

Flip just the top datum V_0 from1 to0, keeping every instruction intact. Since the top row follows

\[
V_x(t+1)=V_{x-1}(t)V_x(t)V_{x+1}(t),
\]

induction gives V_x(t)=0 exactly when |x|<=t, and1 elsewhere. The top disagreement interval grows forever. This is one allowed native data edit and exactly one physical D-symbol edit; it never returns to the undamaged pair.

A corresponding one-instruction witness changes top leaf bit7 at x=0, replacing its word128 by0. The top datum at that site becomes0 at tick1 and is held at0 by the changed table thereafter. All other top sites still apply Rule128. At tick t>=1 the top zeros occupy exactly |x|<=t-1. One physical P-symbol edit therefore also causes permanently expanding data disagreement on this valid persistent background.

These deductions do not claim that the damaged pair always lies outside the represented image. They establish failure to recover the original trajectory under this specific law. A deliberate instruction change can be a legitimate new native dynamics; it is a failure only relative to a requirement to preserve or restore the old correction interpretation.

## Resources and current boundary

The realization uses five symbols, physical radius9, scale9 and one physical tick per source tick. Per horizontal source site it stores64 program symbols and4 data symbols, for68 occupied sites. The four complete macrocells span36 transverse coordinates, from-9 through26, with blank exterior. Their full allocated footprint is324 physical positions per source site, including padding. Preparation radius is bounded by2 in source coordinates.

This is finite transverse preparation, not finite total support for an infinite source. Roles, occupancy, axes and table-stage topology remain prepared architecture. The original source baseline still uses one bit per site and radius-one dynamics; no storage advantage, optimality, novelty or universal-program claim follows.

The immediate construction goal is met: an exact finite-height, locally prepared, physically programmed correction system with a nonconstant cap. The next substantive question is semantic program revision: which intended changes should preserve the old interpretation, which should establish a new one, and what local re-preparation or maintained structure must be supplied? Any proposed repair or alternate architecture needs its own frozen contract. The expanding-error witness remains evidence against this hold-mode attempt, not against that larger rule space. Class IV remains background intuition only.
