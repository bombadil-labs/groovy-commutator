# Groovy is a basepoint defect, not the lift's section defect

**Evidence:** exact algebra plus exhaustive finite verification on the declared local ECA domains.  
**Authored by:** GPT-5.6 Sol (OpenAI), 2026-10-06. **Reviewed by:** none.

We wondered whether the affine-oriented dimensional lift could be understood as an extension of dynamical systems, with Groovy's `G` acting as the cocycle or obstruction measuring failure of a section to commute with evolution. The question was prompted by the 2026-10-06 OpenAI math release and, more generally, by the idea that otherwise-lost information may become explicit state in a larger representation.

We tried the literal formulation first. It dies immediately for a good reason: the existing lift theorem already proves that the marked-beam encoding `L` intertwines the source and lifted evolutions,

\[
H^\uparrow(L(X)) = L(H(X)).
\]

Therefore the canonical section/evolution defect is exactly zero. `G` is not that defect.

What survives is sharper. `G` measures the error made when a **change** is evolved as though it were an ordinary **state**, instead of being transported at the state where the change lives. The affine-oriented lift's two temporal residual rows are precisely second cross-effects of its centered encoding. For nonlinear rules the induced change transport depends on the basepoint; for the 16 affine ECAs it does not.

This note derives that statement, verifies it across all 256 ECAs, records a bounded negative third-order probe, and gives a structural explanation for the old nonlinear zero-`G` exceptions Rules 4 and 200.

Protocol: [typed lift defect](protocols/typed-lift-defect-20261006.md) and [frozen Gate-E probes](protocols/typed-lift-defect-gate-e-probes-20261006.md). Canonical result: [`results/typed_lift_defect_20261006.json`](../../results/typed_lift_defect_20261006.json). Runner: [`scripts/experiment_typed_lift_defect.py`](../../scripts/experiment_typed_lift_defect.py).

## 1. The section defect is zero

The affine-oriented lift theorem already establishes

\[
H^\uparrow\circ L = L\circ H.
\]

Thus the proposed Boolean defect

\[
H^\uparrow(L(X))\oplus L(H(X))
\]

vanishes identically on the beam. This prevents a seductive relabeling: the lift really does commute with the base evolution on its encoded family, so nonzero Groovy must be comparing different objects.

## 2. States and changes have different transport laws

Let the configuration space be a Boolean group under XOR. Define the finite difference of `H` at basepoint `X` in displacement `U` by

\[
\partial H_X(U)=H(X\oplus U)\oplus H(X).
\]

Define the dynamical displacement

\[
d_H(X)=X\oplus H(X).
\]

Because \(X\oplus d_H(X)=H(X)\),

\[
\partial H_X(d_H(X))
 =H(H(X))\oplus H(X)
 =d_H(H(X)).
\]

So the dynamical displacement is transported exactly by the finite-difference action. If

\[
T H(X,U)=(H(X),\partial H_X(U)),
\qquad
v_H(X)=(X,d_H(X)),
\]

then

\[
\boxed{T H\circ v_H=v_H\circ H.}
\]

This is the commuting square the initial extension hypothesis was looking for, but it lives in the **state/change bundle**, not in a defect of the dimensional beam section.

The distinction is established mathematical territory rather than new vocabulary. Change-action and Cartesian-difference work treats discrete derivatives as transport of changes and explicitly includes finite-difference and Boolean differential calculi. See Alvarez-Picallo and Pacaud Lemay, [Cartesian Difference Categories](https://arxiv.org/abs/2011.12600).

## 3. Centered Groovy is basepoint dependence of change transport

The repository's raw Groovy field is

\[
G_H(X)=d_H(H(X))\oplus H(d_H(X)).
\]

The correctly typed first term is

\[
d_H(H(X))=\partial H_X(d_H(X)).
\]

At the origin,

\[
\partial H_0(U)=H(U)\oplus H(0).
\]

Therefore

\[
\boxed{
G_H(X)\oplus H(0)
=\partial H_X(d_H(X))\oplus\partial H_0(d_H(X))
=B_H(X,d_H(X)).
}
\]

So the old polarization identity has a direct typed reading:

> **Centered Groovy is the failure of finite-difference transport to be basepoint-independent, sampled along the rule's own dynamical displacement.**

For an affine map \(H(X)=AX\oplus c\), \(\partial H_X(U)=AU\) is independent of `X`. The local ECA truth-table audit makes that boundary exact: change transport is basepoint-independent for exactly the 16 affine ECAs

\[
0,15,51,60,85,90,102,105,150,153,165,170,195,204,240,255,
\]

and basepoint-dependent for the other 240. Rule 110 already has a three-bit local witness: for displacement word `001`, base words `000` and `010` produce different finite differences.


### The exact noncommuting square

The original cocycle intuition was therefore close, but attached to the wrong
projection.

On the trivialized change bundle write

\[
p(X,U)=X,\qquad q(X,U)=U.
\]

The legitimate bundle projection \(p\) always intertwines the change transport
with point evolution:

\[
\boxed{p\circ TH=H\circ p.}
\]

The second-coordinate map \(q\), however, forgets the basepoint of a change.
For a nonlinear map there is no reason for

\[
q\circ TH
\quad\text{and}\quad
H\circ q
\]

to agree. Evaluated on the dynamical-change section \(v_H\),

\[
\boxed{
G_H
=
q\circ TH\circ v_H
\;\oplus\;
H\circ q\circ v_H.
}
\]

Indeed the first path is \(d_H\circ H\) and the second is \(H\circ d_H\).
So raw Groovy is exactly the commutation defect produced by **flattening a
based change into an ordinary point before evolving it**.

The centered version replaces point evolution on the flattened change by
\(H^\circ(U)=H(U)\oplus H(0)\):

\[
G_H^\circ
=
q\circ TH\circ v_H
\;\oplus\;
H^\circ\circ q\circ v_H.
\]

For affine \(H\), this square commutes for every \((X,U)\), not merely along
\(v_H\). Rules 4 and 200 are subtler: the square does not commute globally,
but its defect vanishes on the particular dynamical-change section selected
by the rule itself.

The entire horizon family has the same form. Since
\(TH^t\circ v_H=v_H\circ H^t\),

\[
\boxed{
K_t(X)
=
q\!\left((TH)^t(v_H(X))\right)
\oplus
H^t\!\left(q(v_H(X))\right).
}
\]

Thus \(K_t\) compares two ways of evolving the initial change for \(t\) steps:
keep its basepoint and use typed change transport, or erase its basepoint at
time zero and repeatedly apply the point dynamics to the resulting bitstring.
\(K_1=G\) is simply the first member of this projection-defect family.

This is a more precise home for the old "missing column" intuition: the missing
column is not an extra term in the source evolution. It is the **basepoint
coordinate that the second projection discards**.

## 4. The affine-oriented lift stores a two-step change jet

Its temporal fields are

\[
F_2=X\oplus H(X),\qquad
F_3=X\oplus H^2(X),\qquad
F_5=X.
\]

Let

\[
U_0=d_H(X),\qquad U_1=d_H(H(X)).
\]

Then

\[
F_2=U_0,\qquad F_3=U_0\oplus U_1,
\]

so \(U_1=F_2\oplus F_3\). The temporal core `(F5,F2,F3)` is therefore algebraically equivalent to `(X,U0,U1)`: a basepoint, its current dynamical change, and that change after one correctly typed transport step. The remaining rows provide the oriented spatial rails and zero marker needed for the self-synchronizing binary presentation.

This does **not** prove that the entire six-row construction is a canonical categorical tangent object. It does explain why tangent/change structure was already visible in its temporal residuals.

## 5. The lift residual is a cross-effect of the encoding

Center the six-field encoding:

\[
J_H(X)=L_H(X)\oplus L_H(0).
\]

The two spatial rails and source row are linear after centering. The second cross-effect is therefore

\[
\boxed{
\operatorname{cr}_2(J_H)(X,Y)
=(0,0,B_H(X,Y),B_{H^2}(X,Y),0,0).
}
\]

For a reduced map `f`, the second cross-effect `f(x+y)-f(x)-f(y)` is the standard measure of failure of additivity; over \(\mathbb F_2\), subtraction and addition coincide. This is Eilenberg-Mac Lane vocabulary, not terminology invented for this project.

Along the trajectory graph \(Y=H(X)\), define

\[
K_t(X)=d_H(H^tX)\oplus H^t(d_HX).
\]

Then

\[
B_{H^t}(X,HX)=K_t(X)\oplus H^t(0),
\]

so

\[
\operatorname{cr}_2(J_H)(X,HX)
=(0,0,K_1\oplus H(0),K_2\oplus H^2(0),0,0).
\]

This is the centered form of the residual that the 2026-09-17 verifier had already found as `(0,0,K1,K2,0,0)`, with `K1 = G`. The new result is the interpretation: the residual is not a failure of the beam section to intertwine. It is the nonlinear cross-effect of the **encoding itself**, concentrated in its two temporal rows.


### Polarization is an exact 2-cocycle — and therefore not a nontrivial obstruction class

There is one precise sense in which the cocycle intuition *does* become
literal.

Let the additive configuration group be \(V\), let \(V\) also be the
coefficient module with trivial action, and center the rule:

\[
\bar H(X)=H(X)\oplus H(0).
\]

Then the polarization is

\[
B_H(X,Y)
=
\bar H(X\oplus Y)\oplus\bar H(X)\oplus\bar H(Y).
\]

For ordinary group cohomology with trivial coefficients, this is exactly the
2-coboundary of the 1-cochain \(\bar H\):

\[
\boxed{B_H=\delta\bar H.}
\]

Consequently it obeys the 2-cocycle identity identically,

\[
B_H(X,Y)\oplus B_H(X\oplus Y,Z)
=
B_H(Y,Z)\oplus B_H(X,Y\oplus Z),
\]

but its cohomology class is always zero:

\[
[B_H]=0\in H^2(V,V).
\]

This is an important negative result for the original extension-obstruction
hypothesis. The nonlinearity measured by \(B_H\) is real at the level of the
**cocycle representative**, but ordinary group cohomology quotients it away
because the representative is already exact. The distinction between an
affine and nonlinear rule is therefore \(B_H=0\) versus \(B_H\ne0\), not a
nonzero cohomology class.

Centered Groovy is the restriction of this exact 2-coboundary to the rule's
own dynamical graph,

\[
G_H^\circ(X)=B_H(X,d_H(X)).
\]

Rules 4 and 200 show why the restriction matters: \(B_H\) is globally nonzero
for both rules, while it vanishes on every pair \((X,d_H(X))\) selected by
their own dynamics.

This statement uses the ordinary trivial coefficient action. A different
module action or a different cohomology theory could encode other structure;
nothing here rules that out. It does rule out interpreting the present
polarization itself as a nontrivial ordinary \(H^2\) obstruction.

## 6. The horizon law is nonlinear change transport, not generally a linear cocycle

Let

\[
X_t=H^tX,\qquad
U_t=d_H(X_t),\qquad
R_t=H^t(U_0),\qquad
K_t=U_t\oplus R_t.
\]

The exact recurrence is

\[
\boxed{
K_{t+1}=G(X_t)\oplus\partial H_{R_t}(K_t).
}
\]

Indeed,

\[
G(X_t)=U_{t+1}\oplus H(U_t),
\]

while

\[
\partial H_{R_t}(K_t)
=H(R_t\oplus K_t)\oplus H(R_t)
=H(U_t)\oplus R_{t+1}.
\]

The two `H(U_t)` terms cancel.

The previous verifier checked this through short horizons. The new runner independently checks horizons 0 through 6 for every state of rings 5, 6 and 7 under all 256 ECAs, with zero failures.

Calling this simply a "cocycle" would hide an important distinction. A standard linear cocycle/skew product has a fibre action linear in the fibre variable, typically `F(x,v)=(Tx,A(x)v)`. Our finite-difference transport need not be additive in `u`, and the recurrence above uses the moving basepoint `R_t`. For affine ECAs it collapses to a fixed linear fibre action. For nonlinear ECAs the safer description is **basepoint-dependent change transport** or a nonlinear skew/change-action law unless a stronger categorical formulation is supplied.

## 7. Exact verification

The canonical runner is independent of NumPy and uses integer-encoded periodic ECAs. Its own SHA-256 is

`66253f440ad565280e215c6b4631af256bef29a878c39ab18c1a55167e7ba5eb`.

| Gate | Domain | Result |
| --- | --- | --- |
| B: typed transport | all 256 rules, every state on rings 5, 6, 7 | 0 failures |
| B: \(G^\circ=B(X,d_HX)\) | same | 0 failures |
| C: lift cross-effect | all 256 rules, all \(32^2\) source pairs on ring 5 | 0 failures |
| C: trajectory specialization | all 256 rules, every state on rings 5, 6, 7 | 0 failures |
| D: horizon recurrence | all 256 rules, every state on rings 5, 6, 7, horizons 0..6 | 0 failures |
| D: basepoint-independent local fibre action | all ECA local tables | exactly 16 affine rules |

Ring 5 contains the complete radius-two source-pair dependency for Gate C, so that check is an exact local ECA identity rather than evidence from one arbitrary finite size.

## 8. Third cross-effects do not rescue graph-restricted blindness

A tempting next hypothesis was that Rules 4 and 200 evade centered `G` because `G` only samples the second cross-effect, while a third cross-effect would expose their cubic nonlinearity.

The algebraic control works: among ECAs the ANF-degree census is degree 0: 2 rules; degree 1: 14; degree 2: 112; degree 3: 128. The unrestricted third cross-effect is nonzero for exactly those 128 cubic rules.

But all three frozen trajectory-derived probes fail to expose Rules 4 and 200. On the complete radius-three ring-7 domain, each probe is nonzero for 119 rules and zero for 137. The orbit and correctly typed probes miss the same nine cubic rules:

\[
1,4,8,64,76,200,205,223,236.
\]

The raw-displacement probe misses a different nine:

\[
1,4,19,32,128,140,196,200,205.
\]

Rules 4 and 200 are zero under all three. Gate E ends here; there is no fourth formula search.

Post hoc, the equality of the orbit and typed third-order probes is itself explained. For an ECA the third cross-effect is the alternating trilinear polarization of the cubic ANF part. Since

\[
d_HX=X\oplus HX,\qquad d_H(HX)=HX\oplus H^2X,
\]

trilinearity and vanishing on repeated arguments give

\[
\operatorname{cr}_3(H)(X,d_HX,d_H(HX))
=\operatorname{cr}_3(H)(X,HX,H^2X).
\]

So those two probes were algebraically the same question.

## 9. Rules 4 and 200 are projection-like complements

The failed third-order rescue led to a cleaner explanation of the old counterexamples.

Their truth tables satisfy

\[
4\oplus200=204,
\]

and Rule 204 is identity. Hence as global maps

\[
H_{200}=I\oplus H_4,\qquad H_4=I\oplus H_{200}.
\]

The exhaustive radius-two audit also finds

\[
H_4^2=H_4,\qquad H_{200}^2=H_{200},
\]

and

\[
H_4\circ H_{200}=0,\qquad H_{200}\circ H_4=0.
\]

Thus they form a nonlinear projection-like complementary pair: each is idempotent, their XOR is identity, and each annihilates the other's image.

Consequently

\[
D_{H_4}=H_{200},\qquad D_{H_{200}}=H_4.
\]

For `P=H4`, `Q=H200`,

\[
G_P(X)=D_P(PX)\oplus P(D_PX)=Q(PX)\oplus P(QX)=0.
\]

The same argument holds with the pair reversed.

Rules 4 and 200 therefore do not have zero `G` because they secretly lack nonlinearity; both are cubic. Their own dynamics choose a displacement sector on which the two projection-like components annihilate one another.

The local Boolean forms make the complement visible. With left, center, right bits \(l,c,r\),

\[
H_4=c\oplus lc\oplus cr\oplus lcr,
\]

while

\[
H_{200}=lc\oplus cr\oplus lcr.
\]

Their XOR is exactly `c`, Rule 204.


### There are no other nonlinear flat cases

The projection-like pair is not just an explanation for two known
counterexamples. For ECAs it completes the classification of identically flat
**centered** Groovy.

Write the local rule in algebraic normal form

\[
f(l,c,r)=a_0+a_Ll+a_Cc+a_Rr
+a_{LC}lc+a_{LR}lr+a_{CR}cr+a_{LCR}lcr.
\]

The center of \(G^\circ\) has radius two, so its value on all 32 five-bit
source words is the complete full-line local condition. Eliminating those
finite Boolean equations gives the equivalent coefficient constraints

\[
\begin{aligned}
a_{LR}&=0,\\
a_{CR}&=a_{LCR},\\
a_{LC}&=a_{LCR},\\
a_0a_{LCR}&=a_Ra_{LCR}=a_La_{LCR}=0.
\end{aligned}
\]

This has exactly two branches.

If \(a_{LCR}=0\), then \(a_{LC}=a_{LR}=a_{CR}=0\), while the constant and
linear coefficients are free. These are exactly the 16 affine ECAs.

If \(a_{LCR}=1\), then

\[
a_0=a_L=a_R=a_{LR}=0,\qquad
a_{LC}=a_{CR}=a_{LCR}=1,
\]

with only \(a_C\) free. \(a_C=0\) is Rule 200 and \(a_C=1\) is Rule 4.

Therefore

\[
\boxed{
G^\circ_H\equiv0
\quad\Longleftrightarrow\quad
H\text{ is affine, or }H\in\{4,200\}
}
\]

for elementary cellular automata.

This is an exact finite-universe classification, not a claim about arbitrary
Boolean cellular automata. The standalone verifier
[\`verify_centered_g_zero_classification.py\`](../../scripts/verify_centered_g_zero_classification.py)
checks all \(2^8\) ECA coefficient assignments and all 32 complete radius-two
source words with zero mismatches; the canonical result is
[\`centered_g_zero_classification_20261006.json\`](../../results/centered_g_zero_classification_20261006.json).
It was discovered post hoc from the mechanism audit and is recorded as such,
rather than retroactively presented as a preregistered prediction.

## 10. Prior-art boundary

Three pieces of vocabulary already exist and should be used rather than reinvented:

1. **Finite differences / change actions.** Cartesian difference categories explicitly encompass finite differences and Boolean differential calculus and carry tangent-bundle structure: https://arxiv.org/abs/2011.12600
2. **Cross-effects.** The second cross-effect as failure of additivity and higher cross-effects as polynomial-degree tests go back to Eilenberg-Mac Lane; a modern concise statement appears in https://math.jhu.edu/~eriehl/BJORT.pdf
3. **Linear cocycles.** Standard dynamical-systems usage takes a skew product with linear fibre action `A(x)v`; our nonlinear finite-difference action should not be silently identified with that narrower object.

The candidate project-specific contribution is therefore not the existence of finite differences, cross-effects, tangent bundles, or cocycles. It is the specific identification of the Groovy objects:

- \(G^\circ\) as **basepoint dependence of finite-difference transport along the dynamical displacement**;
- the old `(K1,K2)` lift residual as the temporal part of \(\operatorname{cr}_2(J_H)\);
- the six-row lift's temporal core as a self-synchronizing binary presentation of `(X,U0,U1)`;
- Rules 4/200 as an exact nonlinear projection-like mechanism explaining the failure of the old affine converse.

A broader novelty claim would require a dedicated literature search.

## 11. What this changes

The original cocycle-lift hypothesis was wrong in its literal form and useful because it failed quickly.

The cleaner picture is

\[
\boxed{
\text{state }X
\quad+\quad
\text{change }U
\quad+\quad
\text{basepoint-dependent transport }\partial H_X(U).
}
\]

Groovy asks what happens when the last two types are flattened:

\[
\boxed{
G^\circ_H(X)
=
\text{typed transport at }X
\;\oplus\;
\text{the same displacement transported at }0.
}
\]

That makes the earlier "missing column" intuition more precise. For a nonlinear rule, a displacement alone does not determine how it evolves. The **basepoint** is part of the information required to transport the change.

This unit does not establish a resource advantage, Class-IV discriminator, ambient property of the dimensional lift, or universal canonicity of the six-field encoding. It does give a concrete mathematical type error underlying the original commutator and an exact way the lift stores the information needed to avoid it.

## Reproduction

```bash
python scripts/experiment_typed_lift_defect.py
```

The canonical result intentionally excludes wall-clock timing so byte-for-byte replay is deterministic. A local run on 2026-10-06 completed in about 20 seconds; runtime is not part of the evidence contract.