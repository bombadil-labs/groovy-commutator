# Protocol: role-stack closure for the derivative-completed lift

Date: 2026-09-09
Status: preregistered before evaluation

## Question

The derivative-completed lift stores three equal-size lower-dimensional roles in one next-dimensional totalistic rule table:

\[
R' = [r\mid s\mid\delta].
\]

Can a simple, rule-independent higher-dimensional **state encoding** evolve under this lifted rule so that it remains an encoding of the lower state evolution?

This protocol tests the smallest exact recursive control family before attempting the much larger 2D -> 3D case.

## Lower family

Use binary center-independent totalistic radius-one rules in one dimension. Such a rule has three bits

\[
r=(r_0,r_1,r_2),
\]

indexed by the number of live left/right neighbors. There are exactly eight rules.

Use a periodic lower ring of width three. Its three-cell state `p` evolves to

\[
s=F_r(p),
\]

with incoming derivative

\[
\delta=p\oplus s,
\]

and then

\[
s^+=F_r(s).
\]

The lifted two-dimensional totalistic rule is the nine-bit table

\[
L(r,s,\delta)=[r\mid s\mid\delta].
\]

No class labels enter this test.

## Higher state encoding family

For each transverse period

\[
m\in\{3,4,5,6,7,8\},
\]

fix row zero as a three-cell **data row** equal to the current lower state `s`. Every other row is uniform zero or uniform one according to a binary guard word

\[
g\in\{0,1\}^{m-1}.
\]

Translation lets us fix the data row at phase zero without loss. Enumerate every guard word exactly.

The higher field is therefore an `m x 3` periodic torus with one variable data row and `m-1` uniform guard rows.

## Allowed moving frame

For each guard template, test every fixed transverse drift

\[
j\in\{0,\ldots,m-1\}.
\]

After one higher-dimensional update under `L(r,s,delta)`, success means the full field equals the same guard template with the next lower state `s+` in the data row, translated by `j` rows.

The drift is part of the operator template and must be the same for every source rule and every lower transition tested under that template.

No horizontal drift, rescaling, hidden channels, fitted decoder, or trajectory-specific phase is allowed.

## Structural tests

For every `(m, guard_word, drift)` template, evaluate all:

- 8 lower rules;
- 8 predecessor states `p`;
- corresponding exact `s=F_r(p)`, `delta=p xor s`, and `s+=F_r(s)`.

Record the rules for which the template succeeds on **all eight predecessor states**.

A template is a **universal role-stack operator** if it succeeds for all eight rules. A rule is **role-stack liftable within this budget** if at least one frozen template succeeds for it.

## Primary outputs

Save:

- total templates tested;
- universal templates, if any;
- for every rule, number and fraction of successful templates;
- minimal successful transverse period and associated symmetry-reduced templates;
- failure witnesses for templates/rules that do not close;
- whether successful templates use zero drift or a moving frame.

## Anti-overfitting

- This is a complete finite template family declared before evaluation.
- Every template is applied to every lower rule; templates are not selected by rule identity.
- No Wolfram class labels are loaded.
- This eight-rule totalistic control family is a mechanism test, not a Class-IV test.
- A negative result rules out only this one-data-row/uniform-guard architecture within periods 3 through 8.

## Decision boundary

If at least one nontrivial rule has a successful template, freeze the minimal successful template family and scale it to the 512-rule 2D totalistic family before adding more spatial freedoms.

If only constant/trivial rules succeed, characterize why the guards or data row fail and do not immediately enlarge the template budget.

If no rule succeeds, derive an obstruction for this architecture before exploring multi-data-row encodings.