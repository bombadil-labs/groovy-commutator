# Recovery protocol: censored horizon-6 causal witnesses — 2026-09-09

**Status:** frozen after the Research032 phase-2 aggregate and before any alternate-solver evaluation.  
**Branch:** `research/causal-witness-automaton-20260909`  
**Dependency:** Research032 frozen symbolic-MDD protocol and phase-1/2 CI runs.

## Why this recovery exists

The fresh horizon-6 MDD pass produced no new witness births among rules that completed, but six rules hit the preregistered 5,000,000-node ceiling:

`{122,126,129,146,161,182}`.

Therefore the horizon-6 result is **censored**, not a global null.

The ceiling remains unchanged. This follow-up uses a different exact method only on the censored remainder.

## Congruence certificate

Let `g:A^3->A` be an induced eight-symbol macro rule and let `T:A->{0,1}` be a target.

Start from the target kernel

`K_T = {(a,b): T(a)=T(b)}`.

For a relation `R`, define `Phi(R)` to contain `(a,b) in K_T` iff for every `x,y in A`, substituting `a` for `b` in any one argument of `g` produces outputs still related by `R`:

- `g(a,x,y) R g(b,x,y)`;
- `g(x,a,y) R g(x,b,y)`;
- `g(x,y,a) R g(x,y,b)`.

Starting from `R_0=K_T`, iterate

`R_{n+1}=Phi(R_n)`

until stable. On a finite alphabet this terminates. Reflexivity, symmetry, and transitivity are preserved, so the fixed point is a target-respecting congruence.

### All-time safety theorem

If `a R_infinity b`, then two configurations identical except for `a` versus `b` are componentwise `R_infinity`-equivalent initially. Congruence compatibility preserves componentwise equivalence after every macrostep, and `R_infinity` refines the target kernel. Hence the target spacetime fields are identical forever.

Therefore

`a R_infinity b  =>  w_T(a,b)=infinity`.

This is a **sufficient** permanent-equivalence certificate, not a necessary one: arbitrary future contexts used by algebraic congruence may be dynamically unreachable.

## Frozen congruence census observation

The congruence calculation is performed only after the fresh h=6 MDD run was launched, so it cannot affect the phase-2 outcome.

Across the 52,712 pair/target distinctions still unresolved after horizon 5:

- 47,352 are certified permanently invisible by the target-respecting congruence;
- 5,360 are not certified by this simple condition.

For four of the six h=6-censored rules, **all** unresolved distinctions are congruence-certified:

- Rule 126: 21/21;
- Rule 129: 21/21;
- Rule 146: 21/21;
- Rule 182: 21/21.

These rules cannot contain a horizon-6 birth.

Only Rules 122 and 161 retain non-congruence unresolved cases. The exact h<=5 relation freezes the following 12 pair/target cases for recovery:

### Rule 122, target `00100000`

- `1-4`
- `1-5`
- `3-6`
- `3-7`
- `4-5`
- `6-7`

### Rule 161, target `00000100`

- `0-1`
- `0-4`
- `1-4`
- `2-3`
- `2-6`
- `3-6`

Do not add or remove cases after the alternate solver is run.

## Exact independent h=6 solver

Use the original fine ECA, not the symbolic MDD.

At macro-horizon 6:

- dependency word length is 13 macro symbols;
- this is 39 fine initial cells;
- six macrosteps equal 18 fine ECA ticks;
- after shrinking the exact radius-1 fine light cone for 18 ticks, three final fine cells remain, forming the tested output macro symbol.

For each frozen `(rule,target,pair)` and each of the 13 possible changed macro-symbol axes:

1. create two 39-bit initial rows;
2. constrain them equal everywhere except the selected three-bit block;
3. fix that block to the two frozen symbols `a` and `b` respectively;
4. encode 18 fine ECA updates on the shrinking causal cone for both rows;
5. require the final three-bit target values to differ.

Solve the resulting finite Boolean formula exactly with Z3.

- `SAT` means an explicit h=6 causal witness exists;
- `UNSAT` means no h=6 witness exists for that axis;
- a pair/target is h=6-invisible only if all 13 axes are UNSAT.

No periodic boundary condition is used.

## Witness replay

For every SAT result, save the complete 13-symbol macro word on both sides and replay it with a separately written scalar fine-ECA evaluator for 18 ticks. The final three-bit macro outputs and binary target values must match the solver model.

A SAT result that fails replay is invalid.

## Null-result audit

If all 12 frozen pair/target cases are UNSAT at h=6, perform a second independent CNF/SAT encoding using a different Boolean representation or solver backend before promoting the recovered global h=6 null.

The second audit need only cover the 12 frozen cases × 13 axes; it must not import the Z3 transition-builder implementation.

## Interpretation rules

- If any frozen case is SAT, horizon 6 contains a genuine new birth. Stop broad searching and characterize that witness/symmetry family.
- If all are independently UNSAT, then the Research032 family has **no new causal-witness births at horizons 4, 5, or 6**. This is still a finite-horizon statement; do not infer infinity for the remaining 5,360 non-congruence cases.
- Do not raise the MDD node budget after seeing the censored rules.
- Do not launch h=7 before interpreting the recovered h=6 result and the congruence/non-congruence split.
