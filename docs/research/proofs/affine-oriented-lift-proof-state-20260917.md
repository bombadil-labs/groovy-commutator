# Affine-Oriented Lift — Formal Proof State

**Updated:** 2026-09-16  
**Purpose:** concise handoff sufficient to resume the proof/research in a fresh chat.  
**Status:** native dimensional induction is established for every binary finite-memory CA on \(\mathbb Z^d\): a rule-independent finite-memory entry proof followed by a dimension-free algebraic recursion theorem. The independently replayed all-256 ECA census is retained as a finite verification of the special radius-1 case. A locally equivalent affine gauge exposes a completion-free typed Groovy/tangent structure. Native single-track lifted \(G\) remains a distinct, generally completion-dependent object.

---


# 0. Theorem status

**Current verdict:** the affine-oriented six-field operator below is the project's generalized native lift operator for the binary setting, and its existence/recursion theorem is proved in the current formal development.

Precisely:

- **Domain:** every binary finite-memory cellular automaton on \(\mathbb Z^d\), \(d\ge 1\).
- **First lift:** proved by a rule-independent locality/translation-equivariance argument with inherited memory enlarged from \(M\) to \(M+\{-e,0,e\}\) and new-axis radius \(3\).
- **Recursive lifts:** proved by a dimension-free algebraic phase-synchronization theorem; after entry, each new dimension appends only a radius-\(3\) axis.
- **Exactness:** on the prepared marked beam,
  \[
  H_{n+1}\circ L_n^\dagger=L_n^\dagger\circ H_n,
  \]
  with finite local parent recovery at every floor.
- **Not claimed:** uniqueness/minimality of the operator, \(k\)-ary generalization, arbitrary non-\(\mathbb Z^d\) groups, unique off-beam completion, or preservation of the descendant rule's native single-track Groovy commutator.

The preferred affine gauge is

\[
\boxed{
L_H^\dagger(X)=
\left(
X\oplus\tau_{v_+}X,\;
1\oplus X\oplus\tau_{v_-}X,\;
X\oplus H(X),\;
X\oplus H^2(X),\;
0,\;
X
\right).
}
\]

This is locally equivalent on the valid beam to the earlier nonlinear recovery gauge, but is the cleanest final theorem statement.


# 0A. Referee clarifications to the final theorem statement

The publication statement must preserve five distinctions.

## A. The displacement schedule is recursive, not literally constant

The six-field **grammar** is fixed:

\[
L_{H;v_+,v_-}^\dagger(X)=
\left(
X\oplus\tau_{v_+}X,\;
1\oplus X\oplus\tau_{v_-}X,\;
X\oplus H(X),\;
X\oplus H^2(X),\;
0,\;
X
\right).
\]

But the displacement pair changes with the floor.

For the first lift of an arbitrary source CA, choose a primitive source direction \(e\) and use

\[
\boxed{
v_+^{(0)}=e,\qquad v_-^{(0)}=-e.
}
\]

After the first lift, let \(a_n\) denote the newest spatial axis created by the \(n\)-th lift. At every later step use

\[
\boxed{
v_+^{(n)}=a_n+e,\qquad
v_-^{(n)}=a_n-e.
}
\]

Thus the same six-field operator grammar is reused recursively, with the rails chosen diagonally through the newest axis and the original distinguished source direction.

The theorem should say “the same affine-oriented six-field grammar with this recursive displacement schedule,” not “literally the same pair of translations.”

## B. Exactness is on the marked beam and its phase translates

For each floor \(n\), let \(B_n\) be the aligned prepared marked beam and let

\[
\widehat B_n
\]

be its saturation under the period-six phase translations on all lifted axes.

The descendant CA \(H_n\) is required to satisfy

\[
\boxed{
H_{n+1}\circ L_n^\dagger
=
L_n^\dagger\circ H_n
}
\]

on \(B_n\), equivalently on the phase-saturated invariant family \(\widehat B_{n+1}\).

A total ambient binary CA exists by completing the forced local table arbitrarily away from that family, but the theorem does **not** claim:

- a unique off-beam completion;
- a global conjugacy of the full shifts;
- that unrelated ambient states have any specified interpretation.

The correct phrase is:

> “evolves the marked beam and all of its phase translates exactly.”

## C. Why memory widens only at entry

For the source CA with finite memory \(M\), the raw source representation does not yet contain separate projection rows.

Therefore the first lift must directly inspect the translated parent neighborhoods needed by both rails, giving the sufficient inherited memory

\[
\boxed{
W=M+\{-e,0,e\}.
}
\]

After the first lift, the marked parent already carries

\[
X\oplus\tau_{v_+}X
\quad\text{and}\quad
1\oplus X\oplus\tau_{v_-}X
\]

as physical rows.

Once \(X\) is locally recovered, those rows expose the shifted values

\[
\tau_{v_+}X,\qquad \tau_{v_-}X
\]

inside the same child neighborhood.

Therefore later lifts do **not** need another Minkowski widening along inherited axes. They only append the seven-site new-axis window:

\[
\boxed{
M_{n+1}=\{-3,-2,-1,0,1,2,3\}\times M_n.
}
\]

This is the structural reason entry costs one widening while recursion does not.

## D. “Arbitrarily deep” means every finite depth

The theorem proves:

\[
\boxed{
\forall N<\infty,\quad
\text{the construction can be iterated through }N\text{ added dimensions.}
}
\]

It does **not** construct or claim an infinite-dimensional limit CA.

Use “every finite lift depth” rather than an unqualified “arbitrarily deep” when precision matters.

## E. The entry lemma is not pure row algebra

The affine six-row syntax alone has false phase interpretations for rotations \(2,3,4\).

The entry theorem instead uses only the defining properties of a binary CA:

- one deterministic local rule;
- finite memory;
- translation equivariance.

These rule-independent axioms exclude every false cyclic interpretation.

So the logical structure is

\[
\boxed{
\text{general binary finite-memory entry lemma}
+
\text{rule-free marked recursive lemma}.
}
\]

The all-256 ECA computation and the Game-of-Life checks are verifications, not logical premises.

---

# 0B. Publication-form theorem statement

## Affine-Oriented Binary Dimensional Lift Theorem

Let

\[
H:\mathbb F_2^{\mathbb Z^d}\to\mathbb F_2^{\mathbb Z^d}
\]

be any binary cellular automaton with finite memory set \(M\), and choose a primitive source-lattice direction \(e\).

For a parent state \(X\), define the affine-oriented six-field grammar

\[
\boxed{
L_{H;v_+,v_-}^\dagger(X)=
\left(
X\oplus\tau_{v_+}X,\;
1\oplus X\oplus\tau_{v_-}X,\;
X\oplus H(X),\;
X\oplus H^2(X),\;
0,\;
X
\right).
}
\]

### Entry

For the first lift choose

\[
v_+=e,\qquad v_-=-e.
\]

There exists a binary CA one dimension higher whose local rule, on the marked beam and all six phase translates, evolves this encoding exactly and locally recovers \(X\).

A sufficient inherited memory set is

\[
\boxed{
W=M+\{-e,0,e\},
}
\]

with radius \(3\) on the new period-six axis.

### Recursion

After the first lift, let \(a_n\) be the newest existing lifted axis. For the next lift choose

\[
\boxed{
v_+=a_n+e,\qquad v_-=a_n-e.
}
\]

The marked six-field grammar then phase-synchronizes algebraically without using the parent truth table. If \(M_n\) is a sufficient parent memory set, a sufficient child memory is

\[
\boxed{
M_{n+1}=\{-3,\ldots,3\}\times M_n.
}
\]

Thus, for every finite lift depth \(N\), there are binary descendant CAs and locally recoverable marked beams satisfying

\[
\boxed{
H_{n+1}\circ L_n^\dagger
=
L_n^\dagger\circ H_n
\qquad
(0\le n<N)
}
\]

on the corresponding marked beam and its phase translates.

Therefore:

\[
\boxed{
\text{every binary finite-memory CA on }\mathbb Z^d
\text{ admits a finite-locality dimensional tower through every finite depth.}
}
\]

The theorem does not assert uniqueness/minimality, a nonbinary generalization, an infinite-dimensional limit, unique off-beam completion, or preservation of the descendant rule's native single-track Groovy commutator.

# 1. Core dynamics

For a binary CA \(H\), define

\[
D_H(X)=X\oplus H(X),
\qquad
T_{2,H}(X)=X\oplus H^2(X).
\]

The affine-oriented six-field lift uses directional vectors \(v_+,v_-\):

\[
\begin{aligned}
F_0 &= X\oplus\tau_{v_+}X,\\
F_1 &= 1\oplus X\oplus\tau_{v_-}X,\\
F_2 &= D_H(X),\\
F_3 &= T_{2,H}(X).
\end{aligned}
\]

The single new ingredient is

\[
\boxed{F_1=1\oplus X\oplus\tau_{v_-}X.}
\]

The constant is time-independent, so it cancels from temporal differences.

Two recovery gauges are useful.

### Historical nonlinear gauge

\[
F_4=XD,\qquad F_5=X(1\oplus D).
\]

Then \(F_4\oplus F_5=X\).

### Affine gauge

\[
\boxed{F_4=0,\qquad F_5=X.}
\]

The two gauges carry exactly the same aligned source information. On valid historical codewords,

\[
(XD,\;X(1\oplus D))
\mapsto
(0,\;F_4\oplus F_5)=(0,X),
\]

and from the affine gauge,

\[
(0,X)
\mapsto
(XD,\;X(1\oplus D))
\]

using \(D=F_2\).

Thus the affine gauge is a local recoding of the six-field beam information. It is the preferred chart for the tangent/Groovy analysis below.

---

# 2. Geometry and axis bookkeeping

For the ECA base, the first lift uses

\[
v_+=+e_1,\qquad v_-=-e_1.
\]

At every recursive lift \(D_d\to D_{d+1}\), with \(e_d\) the **newest existing lifted axis** and \(e_1\) the **original longitudinal/source axis**,

\[
\boxed{
v_+=e_d+e_1,
\qquad
v_-=e_d-e_1.
}
\]

In the recursive proof notation:

- \(k\): the newly created six-phase axis;
- \(p\): the parent newest lifted axis \(e_d\);
- \(x\): always the original longitudinal axis \(e_1\).

Therefore every checksum offset \(x\pm1\) remains on the original source axis at every dimension. Older lifted axes \(e_2,\ldots,e_{d-1}\) are spectators in the synchronization lemma.

At D3 specifically, \(p=e_2\), \(x=e_1\).  
At D4, \(p=e_3\), \(x=e_1\), while \(e_2\) is a spectator.  
And so on.

---

# 3. ECA entry theorem

The marked first lift was independently reconstructed with a scalar, shrinking-window implementation:

- all 256 ECAs;
- all \(2^9=512\) complete source dependency words;
- all six new-axis phases;
- no source wraparound;
- direct 35-bit physical neighborhoods.

For the historical marked gauge:

\[
\boxed{256/256}
\]

pass native consistency, source recovery, and unique physical phase identification.

A second scalar phase decoder explicitly tries all six candidate row rotations and checks:

1. six-field algebra;
2. both directional projection equations;
3. \(Y=H(X)\);
4. \(Z=H(Y)\);

under the same ECA rule.

Again:

\[
\boxed{256/256}
\]

have exactly one valid phase on every complete source case.

The affine gauge \((F_4,F_5)=(0,X)\) was independently checked on the same complete domain:

\[
\boxed{
256/256\text{ native},
\quad
256/256\text{ recovery},
\quad
256/256\text{ unique phase}.
}
\]

Thus every ECA enters the marked recursively closed class.

---

# 4. Recursive self-synchronization: historical gauge

For the historical nonlinear gauge, the recursive phase language admits explicit Boolean separators \(I_s\) for every nonzero rotation \(s\in\mathbb Z_6\).

An independent ANF implementation reconstructs the generic temporal-jet grammar from fresh variables and verifies exactly:

\[
\begin{array}{c|cc}
s & I_s(R) & I_s(\rho_sR)\\
\hline
1&1&0\\
2&0&1\\
3&0&1\\
4&1&0\\
5&0&1.
\end{array}
\]

No ECA truth table or finite dimension appears in this verification.

### Separator-degree lemma

A symbolic linear-algebra search over the full six-phase, three-column recursive cylinder gives:

- \(s=1,5\): linear separators exist;
- \(s=2,3,4\): **no affine-linear separator exists**.

Explicit quadratic separators exist for \(s=2,3,4\).

Therefore the minimum ANF separator degree is exactly

\[
\boxed{
\deg_{\min}(s)=
\begin{cases}
1,& s\in(\mathbb Z/6)^\times=\{1,5\},\\[2mm]
2,& s\in\{2,3,4\}.
\end{cases}
}
\]

So the “units mod 6” pattern is an exact lemma for the historical recursive chart, not a visual coincidence.

---

# 5. Recursive self-synchronization: affine gauge

The affine gauge makes the recursive grammar affine-linear.

Let the parent six-phase temporal code at time \(t\) have arbitrary first two phases and

\[
\begin{aligned}
W_t^2 &= a_t\oplus a_{t+1},\\
W_t^3 &= a_t\oplus a_{t+2},\\
W_t^4 &= 0,\\
W_t^5 &= a_t.
\end{aligned}
\]

Build the next marked lift using the diagonal vectors \(v_\pm\).

Every wrong child phase now has a **linear** separator, and in fact only three two-bit checks are needed.

### Rotation \(s=1\)

\[
\boxed{
J_1=
R_{1,3,-1}\oplus R_{2,2,-1}=1
}
\]

on every genuine marked patch, while

\[
J_1(\rho_1R)=0.
\]

### Rotations \(s=2,3,4\)

The single checksum

\[
\boxed{
J_{234}
=
R_{0,4,-1}\oplus R_{1,4,1}=1
}
\]

on every genuine patch, while

\[
J_{234}(\rho_sR)=0,
\qquad s=2,3,4.
\]

### Rotation \(s=5\)

\[
\boxed{
J_5=
R_{0,3,-1}\oplus R_{1,3,-1}=1
}
\]

on every genuine patch, while

\[
J_5(\rho_5R)=0.
\]

These identities follow by direct substitution from \(W^4=0\), \(W^5=a_t\), and the marked minus rail.

Hence the affine recursive phase theorem is completely algebraic and linear:

\[
\boxed{
\mathcal L_{\rm aff}\cap\rho_s\mathcal L_{\rm aff}=\varnothing
\quad
(s=1,\ldots,5).
}
\]

This is the preferred human proof of recursive synchronization.

---

# 6. Finite-memory induction theorem

Let \(H\) be a parent CA on \(\mathbb Z^d\) with finite memory set \(M\).

Once the new-axis phase is synchronized, a child neighborhood over

\[
\boxed{
M'=\{-3,-2,-1,0,1,2,3\}\times M
}
\]

recovers the five complete parent keys

\[
\begin{aligned}
A &= X|_{g+M},\\
B &= X|_{g+v_++M},\\
C &= X|_{g+v_-+M},\\
D &= H(X)|_{g+M},\\
E &= H^2(X)|_{g+M}.
\end{aligned}
\]

If \(h\) is the parent local rule, put

\[
a=h(A),\quad b=h(B),\quad c=h(C),\quad d=h(D),\quad e=h(E).
\]

Then the affine-gauge child successor is

\[
\boxed{
(a\oplus b,\;
1\oplus a\oplus c,\;
a\oplus d,\;
a\oplus e,\;
0,\;
a).
}
\]

The historical gauge replaces the final pair by

\[
(a(a\oplus d),\;a(1\oplus a\oplus d)).
\]

Thus the lift is closed on its own image.

For every ECA root and every finite dimension,

\[
\boxed{
H_{d+1}\circ L_d^\dagger
=
L_d^\dagger\circ H_d
}
\]

on the marked beam, with local parent recovery.

The compact rectangular radii are

\[
\boxed{
(3,2),
(3,3,2),
(3,3,3,2),
\ldots
}
\]

for ECA roots.

For the pure D0-descended tower they are

\[
\boxed{
(3),
(3,3),
(3,3,3),
\ldots.
}
\]

No inherited-radius growth is required.

---

# 7. Phase-saturated beam

At floor \(d\), phase translations form

\[
P_d=(\mathbb Z_6)^{d-1}
\]

for an ECA-root tower, or \((\mathbb Z_6)^d\) for a D0-root tower.

Phase separation implies the action is free.

Thus the phase-saturated marked beam is a principal finite frame cover:

\[
\boxed{
P_d\curvearrowright\widehat B_d
\quad\text{freely}.
}
\]

With the aligned section,

\[
\widehat B_d\cong B_{\rm source}\times P_d.
\]

The important statement is local: the phase coordinate is recoverable from a bounded binary neighborhood without an external label.

The unmarked zero background can have a full phase stabilizer. The affine marker removes this isotropy.

---

# 8. Signed translations and the D0 bit

Define the split extension

\[
\boxed{
0\to\mathbb Z_2
\to
\widetilde G
\to
G
\to0,
\qquad
\widetilde G=G\times\mathbb Z_2.
}
\]

Let

\[
T_{(v,\epsilon)}X
=
\epsilon\oplus\tau_vX.
\]

The grading character is

\[
\chi(v,\epsilon)=\epsilon.
\]

The two marked rails are ordinary change masks of signed transports:

\[
P_+=X\oplus T_{(v_+,0)}X,
\]

\[
P_-^\dagger=X\oplus T_{(v_-,1)}X.
\]

For every such affine transport,

\[
\boxed{
G_{T_{(v,\epsilon)}}\equiv\epsilon=\chi(v,\epsilon).
}
\]

Thus Groovy restricted to the signed-translation subgroup is exactly its \(\mathbb Z_2\) grading character.

At D0, the spatial group is trivial and only

\[
\widetilde G_0\cong\mathbb Z_2
\]

remains.

The two rails reduce literally to

\[
\boxed{(0,1).}
\]

---

# 9. Groovy as restricted polarization

For any Boolean dynamics \(H\), define the finite-difference/tangent action

\[
\partial H_X(U)
=
H(X)\oplus H(X\oplus U).
\]

Define centered polarization

\[
B_H(X,U)
=
H(X\oplus U)\oplus H(X)\oplus H(U)\oplus H(0).
\]

Then

\[
\boxed{
G_H(X)
=
\partial H_X(D_HX)\oplus H(D_HX)
}
\]

and

\[
\boxed{
G_H^\circ(X)
=
\partial H_X(D_HX)\oplus\partial H_0(D_HX).
}
\]

Equivalently,

\[
\boxed{
G_H^\circ(X)
=
B_H(X,D_HX).
}
\]

Therefore centered Groovy is polarization restricted to the **trajectory-displacement graph**

\[
\Gamma_H=\{(X,D_HX)\}.
\]

This explains the corrected affine converse:

- \(B_H(X,U)\equiv0\) for **all** pairs iff \(H\) is affine;
- \(G_H^\circ\equiv0\) only requires \(B_H\) to vanish on \(\Gamma_H\).

Rules 4 and 200 are nonlinear but satisfy the restricted condition.

Exact seven-cell-ring control:

- Rules 4 and 200: \(B_H(X,D_HX)=0\) for every \(X\);
- yet \(B_H(1,2)\ne0\), so all-pairs polarization is nonzero;
- affine Rule 90 has \(B_H\equiv0\) on all pairs.

This also explains why an all-pairs polarization-covariance no-go does not imply a no-go for \(G\)-transport.

---

# 10. Groovy bundle / diagonal-defect formulation

Define the bundle dynamics

\[
\boxed{
\mathbb H(X,U,V)
=
\left(
H(X),\;
\partial H_X(U),\;
H(V)
\right).
}
\]

If the two fiber coordinates initially agree,

\[
U=V,
\]

then after one step their discrepancy is

\[
\partial H_X(U)\oplus H(U).
\]

On the trajectory section

\[
U=V=D_HX,
\]

that discrepancy is exactly

\[
\boxed{G_H(X).}
\]

Thus noncentered Groovy is the failure of the diagonal fiber \(U=V\) to remain invariant when one copy is transported tangentially and the other is treated as an ordinary point.

For centered Groovy, use the reference tangent transport

\[
\mathbb H^\circ(X,U,V)
=
\left(
H(X),\;
\partial H_X(U),\;
\partial H_0(V)
\right).
\]

Then on the diagonal,

\[
U=V=D_HX,
\]

the fiber discrepancy after one step is

\[
\boxed{G_H^\circ(X)=B_H(X,D_HX).}
\]

Moreover,

\[
H\text{ affine}
\iff
\partial H_X=\partial H_0\text{ for all }X
\iff
\text{the centered diagonal is invariant for all }(X,U).
\]

Rules 4 and 200 preserve it only on the selected trajectory section, explaining their nonlinear zero-G behavior.

---

# 11. Exact chain rule under a lift

If an encoding \(L\) intertwines

\[
F\circ L=L\circ H,
\]

define

\[
\partial L_X(U)
=
L(X)\oplus L(X\oplus U).
\]

Then, whenever the two source points are in domain,

\[
\boxed{
\partial F_{L(X)}(\partial L_XU)
=
\partial L_{H(X)}(\partial H_XU).
}
\]

Thus true tangent transport is fixed by the beam intertwining theorem.

For \(U=D_HX\),

\[
\partial L_X(D_HX)=D_F(LX).
\]

The previously observed completion freedom of native lifted \(G\) therefore has an exact type-theoretic source:

\[
G_F(LX)
=
\underbrace{\partial F_{LX}(D_F(LX))}_{\text{true tangent transport, beam-fixed}}
\oplus
\underbrace{F(D_F(LX))}_{\text{point evolution applied to a tangent vector}}.
\]

The second input need not be a beam point.

Hence:

\[
\boxed{
\text{beam evolution fixes tangent transport but not point evolution on tangent vectors.}
}
\]

This is the precise reason native single-track lifted \(G\) is generally completion-dependent.

---

# 12. Affine-jet residual theorem

In the affine six-field gauge define

\[
\Lambda_m^H(X)
=
\left(
P_+(X),\;
m\oplus P_-(X),\;
X\oplus HX,\;
X\oplus H^2X,\;
0,\;
X
\right).
\]

For arbitrary \(U\), compare:

1. the **secant/tangent encoding**
   \[
   \Lambda_1^H(X)\oplus\Lambda_1^H(X\oplus U);
   \]
2. the **independent point-vector encoding**
   \[
   \Lambda_0^H(U).
   \]

Their XOR is exactly

\[
\boxed{
\left(
0,\;
0,\;
C_H(X,U),\;
C_{H^2}(X,U),\;
0,\;
0
\right),
}
\]

where

\[
C_F(X,U)
=
F(X)\oplus F(X\oplus U)\oplus F(U)
=
B_F(X,U)\oplus F(0).
\]

For the trajectory displacement \(U=D_HX\),

\[
\boxed{
\Lambda_1(X)\oplus\Lambda_1(HX)\oplus\Lambda_0(D_HX)
=
\left(
0,\;
0,\;
G_H(X),\;
[D_H,H^2](X),\;
0,\;
0
\right).
}
\]

Thus, in the affine chart:

- the ordinary Groovy commutator is literally the \(F_2\) residual row;
- the \(F_3\) residual row is the second-lag commutator
  \[
  D_H(H^2X)\oplus H^2(D_HX).
  \]

The centered version adds the fixed vector

\[
(0,0,H(0),H^2(0),0,0)
\]

and yields

\[
(0,0,B_H(X,U),B_{H^2}(X,U),0,0).
\]

This is an exact, completion-free **typed Groovy carrier** at the source level.

A direct exhaustive check over all 256 ECAs and all seven-cell-ring states agrees identically with the algebra.

---

# 13. Why the affine gauge is useful

For the historical gauge, the minimum recursive separator degree is

\[
1,2,2,2,1
\]

for rotations \(1,\ldots,5\).

For the affine gauge, **every** wrong rotation has a two-bit linear separator.

So the affine chart simultaneously:

1. preserves the same six-field beam information;
2. linearizes the recursive phase proof;
3. separates affine point (\(m=1\)) and vector (\(m=0\)) sectors;
4. concentrates Groovy/polarization residuals into the temporal rows.

It is therefore the preferred gauge for further tangent/Groovy work, while the historical gauge remains the connection to the existing repository results.

---

# 14. What is proved versus open

## Proved / exact

- **general binary finite-memory first lift:** every binary CA on \(\mathbb Z^d\) with finite memory \(M\) and chosen primitive direction \(e\) admits the affine-oriented first lift with inherited memory \(M+\{-e,0,e\}\);
- independently replayed marked ECA first lift: all 256, complete local domain;
- recursive phase synchronization: dimension-free algebraic theorem;
- finite-memory recursive lift at compact radii;
- D0 signed-translation interpretation;
- Groovy grading character on \(G\times\mathbb Z_2\);
- \(G^\circ=B_H(X,D_HX)\);
- finite-difference chain rule under intertwining;
- tangent-vs-point explanation of native lifted-G completion freedom;
- affine-jet residual carrier formula;
- all-dimensional two-beam ancestral Groovy transport.

## Still open / next

1. **Typed all-dimensional Groovy bundle transport.**  
   Construct the recursive multi-track lift carrying:
   - the marked point frame;
   - the true tangent vector;
   - the independent point-vector/reference tangent track.
   The point frame supplies phase, so the \(m=0\) vector tracks need not self-synchronize independently.

2. Decide whether the typed bundle yields a useful all-dimensional ancestral \(G\) carrier without adding redundant information.

3. Keep this distinct from **native single-track \(G\)** of a chosen ambient completion; the latter remains completion-dependent in general.

4. After the typed bundle is settled, revisit old \(G\)-carrier / DT2 results through the identity
   \[
   G^\circ=B_H(X,D_HX).
   \]

---

# 15. Headline

The native dimensional lift is now understood as a self-synchronizing affine frame tower.

The same affine grading that fixes orientation also exposes the correct typing of Groovy:

\[
\boxed{
\text{points live in the }m=1\text{ affine sector,}
\qquad
\text{differences live in the }m=0\text{ vector sector.}
}
\]

Groovy is the defect between two ways of transporting the same displacement:

\[
\boxed{
\text{true tangent transport}
\quad\text{vs.}\quad
\text{treating the displacement as an ordinary point.}
}
\]

Centered Groovy is exactly polarization on the trajectory-displacement graph:

\[
\boxed{
G_H^\circ(X)=B_H(X,D_HX).
}
\]



# 16. Tangent functor and all-dimensional typed transport

For any Boolean map \(f:V\to W\), define its finite-difference tangent prolongation

\[
\boxed{
Tf(X,U)
=
\left(
f(X),\;
\partial f_X(U)
\right),
}
\]

where

\[
\partial f_X(U)=f(X)\oplus f(X\oplus U).
\]

This construction is exactly functorial.

For composable maps \(f,g\),

\[
\begin{aligned}
\partial(g\circ f)_X(U)
&=
g(fX)\oplus g(f(X\oplus U))\\
&=
\partial g_{fX}\!\left(
fX\oplus f(X\oplus U)
\right),
\end{aligned}
\]

therefore

\[
\boxed{
T(g\circ f)=Tg\circ Tf.
}
\]

Hence every intertwining lift

\[
F\circ L=L\circ H
\]

automatically induces an intertwining tangent lift

\[
\boxed{
TF\circ TL
=
TL\circ TH.
}
\]

This is completion-independent.

Although the tangent vector

\[
\partial L_X(U)=L(X)\oplus L(X\oplus U)
\]

need not itself be a point-beam configuration, the tangent map \(TF\) evaluates \(F\) at the two beam endpoints

\[
L(X),\qquad L(X\oplus U),
\]

not at their XOR as an absolute point.

Thus the proved all-dimensional point lift immediately yields an all-dimensional **typed tangent lift**.

If the point lift has a local decoder, its tangent prolongation is also locally recoverable: decode \(X\) from \(L(X)\), decode \(X\oplus U\) from

\[
L(X)\oplus\partial L_X(U)=L(X\oplus U),
\]

then XOR them to recover \(U\).

So tangent transport needs no new completion policy and no new dimensional census.

---

# 17. Polarization and the centered-G diagonal defect

Define the centered polarization

\[
B_H(X,U)
=
H(X)\oplus H(U)\oplus H(X\oplus U)\oplus H(0).
\]

Since

\[
B_H(X,U)
=
\partial H_X(U)\oplus\partial H_0(U),
\]

it is the difference between tangent transport at basepoint \(X\) and tangent transport at the origin.

Thus

\[
\boxed{
G_H^\circ(X)
=
B_H(X,D_HX).
}
\]

The centered Groovy commutator is exactly the restriction of polarization to the trajectory-displacement graph

\[
\Gamma_H=\{(X,D_HX)\}.
\]

This cleanly separates two statements:

\[
H\text{ affine}
\iff
B_H(X,U)=0\quad\forall X,U,
\]

whereas

\[
G_H^\circ\equiv0
\iff
B_H(X,D_HX)=0\quad\forall X.
\]

The second is strictly weaker.

On a seven-cell ring:

- affine Rule 90 has \(B_H=0\) on every pair;
- nonlinear Rules 4 and 200 have
  \[
  B_H(X,D_HX)=0
  \]
  for every \(X\), but for example
  \[
  B_H(1,2)\ne0.
  \]

This gives a direct geometric explanation of the known nonlinear zero-\(G\) exceptions.

It also explains why the earlier all-pairs polarization-covariance no-go is compatible with nontrivial \(G\)-carrier results: \(G\) probes only the dynamically selected slice \(\Gamma_H\).

---

# 18. Groovy bundle

Define the three-track bundle dynamics

\[
\boxed{
\mathbb H(X,U,V)
=
\left(
H(X),\;
\partial H_X(U),\;
H(V)
\right).
}
\]

On the fiber diagonal \(U=V\), the difference between the two updated fiber coordinates is

\[
\partial H_X(U)\oplus H(U).
\]

On the trajectory section

\[
U=V=D_HX,
\]

this is exactly

\[
\boxed{G_H(X).}
\]

So noncentered Groovy is the defect of invariance of the diagonal when one copy of a displacement is transported as a tangent vector and the other is evolved as an ordinary point.

For centered Groovy, define

\[
\boxed{
\mathbb H^\circ(X,U,V)
=
\left(
H(X),\;
\partial H_X(U),\;
\partial H_0(V)
\right).
}
\]

Then the diagonal defect is \(B_H(X,U)\), and on \(U=D_HX\) it is \(G_H^\circ(X)\).

The centered diagonal is invariant for **all** \(X,U\) iff \(H\) is affine.

The nonlinear Rules 4 and 200 preserve it only on the trajectory-displacement section.

---

# 19. Affine-jet carrier and horizon commutators

In the affine six-field gauge,

\[
\Lambda_m^H(X)
=
\left(
P_+(X),\;
m\oplus P_-(X),\;
X\oplus HX,\;
X\oplus H^2X,\;
0,\;
X
\right).
\]

For any \(U\), define the secant encoding

\[
\delta\Lambda_X(U)
=
\Lambda_1(X)\oplus\Lambda_1(X\oplus U).
\]

Then

\[
\boxed{
\delta\Lambda_X(U)
\oplus
\Lambda_0(U)
=
\left(
0,\;
0,\;
C_H(X,U),\;
C_{H^2}(X,U),\;
0,\;
0
\right),
}
\]

where

\[
C_F(X,U)
=
\partial F_X(U)\oplus F(U)
=
B_F(X,U)\oplus F(0).
\]

For the trajectory displacement \(U=D_HX\), define the horizon commutators

\[
\boxed{
K_t(X)
=
D_H(H^tX)
\oplus
H^t(D_HX)
=
[D_H,H^t](X).
}
\]

Then

\[
K_0=0,
\qquad
K_1=G_H,
\]

and the affine-jet residual is

\[
\boxed{
\delta\Lambda_X(D_HX)
\oplus
\Lambda_0(D_HX)
=
(0,\;0,\;K_1(X),\;K_2(X),\;0,\;0).
}
\]

Thus the \(D\) and \(T_2\) rows expose the first two members of the **power-commutator hierarchy**.

This is distinct from the previously measured trajectory history

\[
G_H(H^tX).
\]

---

# 20. Nonlinear cocycle law for the horizon commutators

The horizon commutators satisfy an exact composition law.

Let

\[
A_t=D_H(H^tX),
\qquad
B_t=H^t(D_HX),
\qquad
K_t=A_t\oplus B_t.
\]

Then for \(s,t\ge0\),

\[
\begin{aligned}
K_{s+t}(X)
&=
D_H(H^{s+t}X)
\oplus
H^{s+t}(D_HX)\\
&=
K_s(H^tX)
\oplus
\left(
H^s(A_t)\oplus H^s(B_t)
\right).
\end{aligned}
\]

Since \(A_t=B_t\oplus K_t\),

\[
\boxed{
K_{s+t}(X)
=
K_s(H^tX)
\oplus
\partial H^s_{H^t(D_HX)}
\!\left(K_t(X)\right).
}
\]

In particular,

\[
\boxed{
K_{t+1}(X)
=
G_H(H^tX)
\oplus
\partial H_{H^t(D_HX)}
\!\left(K_t(X)\right).
}
\]

So the horizon commutator is an accumulated discrepancy:

- inject the current trajectory Groovy value \(G_H(H^tX)\);
- transport the previous discrepancy through the finite-difference tangent action along the differentiate-first path.

For \(t=1\),

\[
K_2(X)
=
G_H(HX)
\oplus
\partial H_{H(D_HX)}
\!\left(G_H(X)\right).
\]

This gives a principled interpretation of why a two-step temporal coordinate is useful: it contains the first transported accumulation of commutator error, not merely another copy of \(G\).

---

# 21. Original versus affine recovery gauges

The historical nonlinear gauge and affine gauge are exactly equivalent on aligned valid six-field states.

Historical:

\[
(F_4,F_5)=(XD,\;X(1\oplus D)).
\]

Affine:

\[
(F_4,F_5)=(0,X).
\]

The aligned recodings are

\[
\boxed{
\Phi:
(XD,\;X(1\oplus D))
\mapsto
(0,\;XD\oplus X(1\oplus D))
=
(0,X),
}
\]

and

\[
\boxed{
\Psi:
(0,X)
\mapsto
(XD,\;X(1\oplus D)).
}
\]

They are inverse on the valid code image.

Because the marked beam is locally phase-synchronizing, this aligned change of gauge extends to a bounded local recoding on the phase-saturated beam.

Thus the affine gauge does not discard beam information. It chooses coordinates in which:

- the recursive phase proof becomes linear;
- point/vector grading is explicit;
- the Groovy residual is concentrated in the temporal rows.

---

# 22. Current next question

Native lift induction is no longer the open problem.

The next target is the **typed Groovy bundle**, not native single-track lifted \(G\).

The point lift gives the tangent lift automatically by functoriality.

The source Groovy bundle gives a completion-independent distinction between:

1. tangent transport;
2. point evolution of the same displacement.

The remaining task is to find the smallest useful recursively lifted representation of that bundle:

- marked point/frame track;
- tangent track;
- point-vector or reference-tangent track;

with the point frame supplying phase to the \(m=0\) vector sectors.

A successful construction would give an all-dimensional ancestral \(G\) carrier while keeping it formally distinct from the completion-dependent native \(G\) of an arbitrary ambient child completion.



# 23. Two-beam ancestral Groovy transport theorem

The smallest completion-free ancestral Groovy carrier does not require a three-track tangent bundle.

For a source state \(X\), form the derivative graph embedding

\[
\boxed{
J_D(X)=\left(X,\;D_HX\right).
}
\]

Evolve both coordinates under the ordinary product dynamics

\[
H\times H.
\]

After \(t\) steps,

\[
(H\times H)^tJ_D(X)
=
\left(
H^tX,\;
H^t(D_HX)
\right).
\]

Define the local observation

\[
\mathcal K(A,B)=D_H(A)\oplus B.
\]

Then

\[
\boxed{
\mathcal K\!\left((H\times H)^tJ_D(X)\right)
=
K_t(X)
=
D_H(H^tX)\oplus H^t(D_HX).
}
\]

Thus

\[
K_0=0,
\qquad
K_1=G_H(X).
\]

So the ordinary Groovy commutator is the first failure of the derivative graph \(J_D\) to be invariant under the product evolution \(H\times H\).

The second coordinate carries **no independent source information**: it is the deterministic derived state \(D_HX\). It materializes the alternate operator ordering.

### Dimensional transport

Let

\[
L_d
\]

be any of the proved locally recoverable dimensional lifts of \(H\), with native descendant law \(F_d\):

\[
F_d\circ L_d=L_d\circ H.
\]

Then the product lift

\[
\boxed{
L_d\times L_d
}
\]

intertwines the product dynamics:

\[
\boxed{
(F_d\times F_d)\circ(L_d\times L_d)
=
(L_d\times L_d)\circ(H\times H).
}
\]

Therefore both initial configurations

\[
L_d(X),
\qquad
L_d(D_HX)
\]

are ordinary states on the **same descendant beam under the same native rule**.

At every time \(t\), local source recovery gives

\[
H^tX
\quad\text{and}\quad
H^t(D_HX),
\]

so \(K_t(X)\), and in particular

\[
\boxed{G_H(X)=K_1(X),}
\]

is locally recoverable at every lifted dimension without querying any off-beam completion.

This is an all-dimensional **ancestral Groovy transport theorem**.

It is deliberately distinct from the descendant rule's own native commutator \(G_{F_d}\), which remains completion-dependent when its cellwise difference field leaves the beam.

### Relation to the six-field coordinates

The ordinary point beam internally stores the evolve-then-differentiate branch through its temporal-difference field.

The companion beam seeded by \(D_HX\) supplies the differentiate-then-evolve branch as an ordinary beam trajectory.

Thus the Groovy double beam makes the two operator orderings literal:

\[
\boxed{
\text{beam A: }X\to H^tX\to D_H(H^tX),
}
\]

\[
\boxed{
\text{beam B: }X\to D_HX\to H^t(D_HX).
}
\]

Their discrepancy is \(K_t\).

Because the first-lift theorem covers **every** source configuration, the companion derivative beam automatically cohabits with the source beam; no separate cohabitation compatibility search is required.

---

# 24. Centered two-beam carrier

The centered horizon commutator is

\[
\boxed{
K_t^\circ(X)
=
K_t(X)\oplus H^t(0).
}
\]

Using \(X\oplus D_HX=HX\),

\[
\boxed{
K_t^\circ(X)
=
B_{H^t}(X,D_HX).
}
\]

At \(t=1\),

\[
K_1^\circ=G_H^\circ.
\]

The reference background \(H^t(0)\) is determined by the source law and does not require an additional independent beam.

So the same two-beam construction transports centered Groovy after adding the known reference orbit.

---

# 25. Relation to the existing “commutator history” experiment

Do not conflate two distinct histories.

The prior repository experiment records

\[
\boxed{
G_H(H^tX),
}
\]

the ordinary one-step Groovy commutator evaluated successively along the native trajectory. That is the object called commutator history in the existing research record. 

The new horizon sequence is

\[
\boxed{
K_t(X)
=
[D_H,H^t](X).
}
\]

They are related by the nonlinear cocycle

\[
\boxed{
K_{t+1}(X)
=
G_H(H^tX)
\oplus
\partial H_{H^t(D_HX)}
\!\left(K_t(X)\right).
}
\]

Thus \(K_t\) is an accumulated, tangent-transported history of the ordinary trajectory commutators, not the same time series.

The affine three-jet residual exposes \(K_1\) and \(K_2\) directly in its two temporal rows.

---

# 26. Updated next target

The native lift proof and an all-dimensional ancestral Groovy carrier are now both available.

The next nontrivial question is narrower:

> Can the two-beam carrier be compressed back into **one physical marked beam plus a locally defined companion/vector sector**, while retaining completion independence?

Equivalently:

- two marked beams are sufficient;
- native one-beam cellwise \(G\) is generally not sufficient;
- determine the minimal typed intermediate object between them.

The affine gauge is the preferred chart for this compression problem because its secant-versus-point residual places

\[
K_1,\;K_2
\]

directly into the two temporal rows.



# 27. General binary finite-memory entry theorem

The ECA census is no longer the logical entry theorem.

Let

\[
H:\mathbb F_2^{\mathbb Z^d}\to\mathbb F_2^{\mathbb Z^d}
\]

be **any** binary CA with finite memory set

\[
M\subset\mathbb Z^d,
\]

and enlarge \(M\) harmlessly so \(0\in M\).

Choose a primitive lattice direction \(e\in\mathbb Z^d\).

Define the affine-gauge first lift

\[
\begin{aligned}
F_0 &= X\oplus\tau_eX,\\
F_1 &= 1\oplus X\oplus\tau_{-e}X,\\
F_2 &= X\oplus Y,\\
F_3 &= X\oplus Z,\\
F_4 &= 0,\\
F_5 &= X,
\end{aligned}
\]

where

\[
Y=H(X),\qquad Z=H^2(X).
\]

Let

\[
\boxed{
W=M+\{-e,0,e\}.
}
\]

A child neighborhood with new-axis radius three and inherited memory \(W\) is sufficient both to synchronize phase and to compute the child successor.

## Pure row algebra is not sufficient

The affine six-row syntax alone admits exactly the kind of false phases that the historical ECA base decoder had to remove dynamically.

### Rotations 2 and 4

The constant codeword

\[
(0,1,0,1,0,0)
\]

is the affine encoding of

\[
X=0,\qquad Y=0,\qquad Z=1.
\]

Its two-row rotation is

\[
(0,1,0,0,0,1),
\]

the affine encoding of

\[
X=1,\qquad Y=1,\qquad Z=1.
\]

So rotations \(2\) and \(4\) are algebraically admissible.

### Rotation 3

Let \(X\) alternate along \(e\),

\[
\tau_eX=1\oplus X,
\]

and choose

\[
Y=0,\qquad Z=1\oplus X.
\]

Then the six rows are

\[
(1,0,X,1,0,X),
\]

which are invariant under a three-row rotation.

Therefore no rule-free first-lift phase theorem is possible from the six-row algebra alone.

The distinction is exactly:

- rotations \(1,5\), the units of \(\mathbb Z_6\), are excluded by the marked projection algebra itself;
- rotations \(2,3,4\), the nonzero nonunits, require dynamical consistency.

This mirrors the recursive separator-degree lemma.

---

## Dynamical exclusion of every wrong rotation

Suppose a physical first-lift neighborhood from a genuine trajectory

\[
X,\;Y=H(X),\;Z=H(Y)
\]

also admits a wrong cyclic interpretation as another valid first-lift trajectory under the **same** CA \(H\).

Write

\[
P_+=X\oplus\tau_eX,
\qquad
P_-^\dagger=1\oplus X\oplus\tau_{-e}X.
\]

Only the local functionality and translation equivariance of \(H\) are used.

### Rotation \(s=1\)

The candidate zero row is the true \(X\)-row, forcing \(X=0\).

Then its candidate state row is \(P_+=0\), while its candidate plus projection is \(P_-^\dagger=1\).

But the plus projection of the zero candidate state is 0.

Contradiction.

### Rotation \(s=5\)

The candidate state row is the true zero row, so \(X'=0\).

Candidate validity forces the true \(X\)-row to be zero, hence the true plus projection is also zero.

But the candidate minus projection of \(X'=0\) must be 1.

Contradiction.

### Rotation \(s=2\)

Candidate validity forces

\[
P_+=0,
\]

so \(X\) is locally invariant under \(e\), and therefore

\[
P_-^\dagger=1.
\]

The rotated projection equations then force

\[
D=X\oplus Y=0
\]

on the parent memory set and

\[
T=X\oplus Z=1
\]

at the center.

Hence \(X\) and \(Y\) agree on \(M\). Since \(H\) uses the same local rule at both points,

\[
Y(0)=H(X)(0)=H(Y)(0)=Z(0).
\]

But \(D(0)=0\) and \(T(0)=1\) give

\[
Y(0)=X(0),
\qquad
Z(0)=1\oplus X(0),
\]

a contradiction.

### Rotation \(s=4\)

Candidate validity forces

\[
D=0
\]

and makes the candidate state

\[
X'=T.
\]

Its candidate plus projection is zero, so \(T\) is locally \(e\)-invariant. Its candidate marked minus projection is the true \(X\)-row, hence

\[
X=1
\]

on the required local region.

Therefore the true projections satisfy

\[
P_+=0,\qquad P_-^\dagger=1.
\]

In the wrong interpretation this means

\[
D'=0,\qquad T'=1.
\]

Thus candidate \(X'\) and \(Y'\) agree on \(M\), while candidate \(Z'\) differs from them at the center.

Functionality of the same local rule \(H\) demands

\[
Y'(0)=H(X')(0)=H(Y')(0)=Z'(0),
\]

contradiction.

### Rotation \(s=3\)

Candidate validity forces

\[
P_-^\dagger=0,
\]

so \(X\) alternates along \(e\):

\[
\tau_eX=1\oplus X.
\]

The candidate state is

\[
X'=D.
\]

Its candidate marked minus projection is also zero, so \(D\) alternates along \(e\).

Therefore

\[
Y=X\oplus D
\]

is locally invariant under \(e\).

The candidate plus projection of \(D\) is 1, forcing the candidate two-step row to make

\[
Z'
\]

alternate along \(e\).

But candidate validity also requires

\[
Z'=H(Y').
\]

The \(M\)-neighborhoods of the locally \(e\)-invariant \(Y'\) at 0 and \(e\) are identical, so translation-equivariance and locality imply

\[
Z'(0)=Z'(e).
\]

The alternating relation gives

\[
Z'(e)=1\oplus Z'(0).
\]

Contradiction.

Thus no nontrivial cyclic phase can occur.

\[
\boxed{
\text{Every binary finite-memory CA has a phase-synchronized affine-oriented first lift.}
}
\]

---

## First-lift memory cost

The sufficient inherited memory set is

\[
\boxed{
W=M+\{-e,0,e\}.
}
\]

This set contains:

- \(M\), for the center parent key;
- \(M+e\), for the \(+e\) shifted parent key;
- \(M-e\), for the \(-e\) shifted parent key;
- enough overlap to perform the local dynamical contradictions above.

The full child memory is

\[
\boxed{
N_1=\{-3,-2,-1,0,1,2,3\}\times W.
}
\]

For a 1D symmetric radius-\(r\) parent,

\[
M=[-r,r],
\]

so

\[
W=[-(r+1),r+1].
\]

Hence the first affine-oriented lift needs inherited radius only

\[
\boxed{r+1,}
\]

not \(2r\).

After entry into the marked six-field class, recursion appends new radius-3 axes with **no further inherited-radius growth**.

A fresh independent finite-domain control over 512 randomly chosen radius-2 binary CAs exhaustively enumerated every required \(2^{15}\) source word at inherited radius 3. All 512 pass both native consistency and parent recovery.

This control is not the proof; the argument above is rule-independent.

---

# 28. Fully general binary lift theorem

Combine the general entry theorem with self-bootstrap closure.

Let \(H\) be any binary finite-memory CA on \(\mathbb Z^d\), \(d\ge1\), with finite memory \(M\), and choose a primitive direction \(e\).

Then the affine-oriented six-field construction produces a binary CA \(H_1\) one dimension higher with:

1. finite local native evolution;
2. local recovery of the entire parent state;
3. exact intertwining
   \[
   H_1\circ L_0=L_0\circ H;
   \]
4. a free locally readable six-phase coordinate on the new axis.

The first child uses inherited memory

\[
W=M+\{-e,0,e\}
\]

and new-axis radius 3.

Every later descendant is obtained by the rule-free affine recursion theorem. If \(M_1\) is the first child memory, then

\[
\boxed{
M_{n+1}=\{-3,\ldots,3\}\times M_n.
}
\]

Therefore **every binary finite-memory CA admits an affine-oriented dimensional tower through every finite lift depth**.

The ECA theorem is the special case

\[
M=\{-1,0,1\},
\]

giving first inherited radius 2 and the compact sequence

\[
(3,2),
(3,3,2),
(3,3,3,2),
\ldots
\]

already measured in the project.

The pure D0 case remains the separate unary base

\[
(3),(3,3),(3,3,3),\ldots.
\]

Thus “general” no longer means “all 256 ECAs.”

It means:

\[
\boxed{
\text{all binary cellular automata with finite memory on }\mathbb Z^d.
}
\]

---


## Independent non-ECA referee control: Conway's Game of Life

As a sanity check independent of the proof, the general first-lift construction was instantiated for Conway's Game of Life, a binary 2D Moore-neighborhood CA.

Choose \(e\) along one lattice axis. Its Moore memory \(M=[-1,1]^2\) gives first-lift inherited memory

\[
W=M+\{-e,0,e\},
\]

a \(5\times3\) inherited stencil, together with radius \(3\) on the new period-six axis.

Two finite controls were run:

1. **Exhaustive \(3\times3\) torus:** all \(512\) source states, every spatial position, every one of the six phases.
   - no native-output collision;
   - no parent-recovery collision;
   - no within-event phase collision.

2. **10,000 random \(5\times5\) torus states:**  
   \(1{,}364{,}226\) distinct marked local keys observed.
   - no native-output collision;
   - no parent-recovery collision;
   - no within-event phase collision.

These are referee sanity checks only. The general entry theorem is rule-independent and does not rely on Game of Life or any finite census.

# 29. Binary scope

Every theorem above is over

\[
\boxed{\mathbb F_2.}
\]

The construction relies essentially on:

- XOR as addition;
- the unique nontrivial binary complement;
- the \(\mathbb Z_2\) affine grading;
- Boolean AND in the historical chart;
- ANF / characteristic-two identities.

A \(k\)-ary generalization would require a new grading/cover and is **not** established here.

Accordingly the theorem should be titled and stated as a theorem about **binary** cellular automata, not arbitrary finite alphabets.

---

# 30. Discrete Duhamel / Lady Windermere interpretation

Recall the horizon commutator

\[
K_t(X)
=
D_H(H^tX)\oplus H^t(D_HX)
\]

and the exact recurrence

\[
\boxed{
K_{t+1}(X)
=
G_H(H^tX)
\oplus
\partial H_{H^t(D_HX)}
\!\left(K_t(X)\right).
}
\]

This has the exact form of a discrete Duhamel or Lady-Windermere error recursion:

- \(G_H(H^tX)\) is the **fresh local ordering defect** injected at step \(t\);
- the second term transports the previously accumulated discrepancy through the finite-difference tangent action.

For nonlinear \(H\),

\[
U\mapsto\partial H_X(U)
\]

need not be linear. Therefore the recursion does **not** generally unroll into a GF(2) sum of independently transported local defects. It remains nested:

\[
K_t
=
G_{t-1}
\oplus
\partial H_{\beta_{t-1}}
\left(
G_{t-2}
\oplus
\partial H_{\beta_{t-2}}
(\cdots)
\right),
\]

with basepoints

\[
\beta_j=H^j(D_HX).
\]

This nesting is precisely where nonlinear dynamics differs from affine dynamics.

### Affine case

If

\[
H(X)=MX\oplus c,
\]

then

\[
\partial H_X(U)=MU
\]

is basepoint-independent and linear, while

\[
G_H\equiv c.
\]

The recurrence becomes

\[
K_{t+1}=c\oplus MK_t,
\]

so it unrolls exactly to

\[
\boxed{
K_t
=
\bigoplus_{j=0}^{t-1}M^{\,j}c
}
\]

(up to equivalent reversal of the summation index).

Thus the usual linear Duhamel/Lady-Windermere fan is recovered exactly in the affine case; nonlinear rules retain the nested tangent transport.




# 31. Rule beam versus state/trajectory beam

The theorem is **uniform over source states**.

Fix:

- one binary finite-memory CA rule \(H\);
- one chosen source direction \(e\);
- the affine-oriented lift grammar.

Then the encoder

\[
L_H^\dagger
\]

is defined for **every** source configuration

\[
X\in\mathbb F_2^{\mathbb Z^d}.
\]

The descendant local rule \(H^\uparrow\) is compiled once from \(H\) and the representation contract. It does **not** depend on a selected source state, initial condition, orbit, or trajectory.

Define the aligned **rule beam**

\[
\boxed{
B_H
=
L_H^\dagger\!\left(\mathbb F_2^{\mathbb Z^d}\right).
}
\]

Its phase saturation is

\[
\boxed{
\widehat B_H
=
\bigcup_{\phi\in P}
\tau_\phi B_H,
}
\]

where \(P\) is the finite product of six-phase groups on the lifted axes.

The theorem proves:

\[
\boxed{
H^\uparrow(B_H)\subseteq B_H
}
\]

and, more strongly,

\[
\boxed{
H^\uparrow\circ L_H^\dagger
=
L_H^\dagger\circ H
\qquad
\text{for every source state }X.
}
\]

Because \(L_H^\dagger\) has a local inverse on its image, the aligned rule beam is an injective local recoding of the **entire state space and dynamics of the rule \(H\)**, not of one orbit.

Thus the quantifiers are

\[
\boxed{
\forall H\;
\forall X\;
\forall n<\infty:
\quad
\text{the marked lift exists and intertwines at lift depth }n.
}
\]

not

\[
\exists X\text{ or one observed trajectory}.
\]

### Recommended terminology

- **rule beam \(B_H\):** the invariant encoded image of every valid state of one fixed source rule \(H\);
- **phase-saturated rule beam \(\widehat B_H\):** all locally equivalent phase translates of that rule beam;
- **state fiber:** the encoded copy \(L_H^\dagger(X)\) of one source configuration \(X\);
- **trajectory inside the rule beam:** the orbit
  \[
  L_H^\dagger(X),\;
  L_H^\dagger(HX),\;
  L_H^\dagger(H^2X),\ldots
  \]

So a trajectory is a path **through** the rule beam; it is not the beam itself.

### Conjugacy statement

On the aligned beam, local recovery gives

\[
R_H\circ L_H^\dagger=\mathrm{id}.
\]

Therefore

\[
\boxed{
H
\;\cong\;
H^\uparrow|_{B_H}
}
\]

by the local encoding \(L_H^\dagger\) and decoder \(R_H\).

On the phase-saturated beam the phase coordinate is preserved, giving the finite-cover form

\[
\boxed{
H^\uparrow|_{\widehat B_H}
\cong
H\times\mathrm{id}_{P}.
}
\]

Hence the lift does not merely reproduce selected behaviors. It embeds the whole rule dynamics as an invariant, locally decodable beam.

This terminology also clarifies cohabitation:

> two different source rules \(H_1,H_2\) **cohabit** when their two rule beams can be supported by one common ambient higher-dimensional completion without conflicting forced local outputs.




# 32. Prior-art comparison: Toffoli 1977 and Smith 1971

## Toffoli 1977 — reversible embedding by spatializing history

Tommaso Toffoli's 1977 paper, *Computation and Construction Universality of Reversible Cellular Automata*, proves that an arbitrary \(d\)-dimensional CA can be constructively embedded/simulated in a reversible CA of dimension \(d+1\).

The construction's objective is **reversibilization**. Because an arbitrary irreversible CA destroys information, a reversible simulator must retain the information that the source dynamics would erase. The added spatial dimension is used as a space-time/history bookkeeping resource: successive \(d\)-dimensional slices/registers represent successive stages of the irreversible computation, with old information retained so the global higher-dimensional evolution can be inverted.

A local reversible primitive has the familiar form

\[
(s_{\rm inputs},t)
\mapsto
(s_{\rm inputs},\,t\oplus f(s_{\rm inputs})),
\]

so the source bits are kept while a fresh target/register acquires the irreversible output. The higher-dimensional reversible medium thereby contains enough history/garbage to reconstruct the past.

This is categorically different from the present theorem:

- our descendant CA is **not required to be reversible**;
- the extra dimension is a bounded period-six frame, not an ever-growing history tape;
- the rule beam stores only functions of the **current source state**
  \[
  X,\;H(X),\;H^2(X)
  \]
  plus frame information;
- no past state or discarded information is accumulated to restore reversibility;
- the beam is a forward-invariant locally decodable image satisfying
  \[
  H^\uparrow L=LH
  \]
  for every source configuration.

Indeed, if a reversible ambient CA \(F\) admitted an injective forward-invariant encoding \(J\) with

\[
FJ=JH
\]

in this strong conjugacy sense, then \(H\) itself would have to be injective. Toffoli can simulate arbitrary irreversible \(H\) precisely because his notion of embedding carries additional history degrees of freedom rather than making the current-state image alone a reversible invariant copy.

**Positioning:** Toffoli establishes that dimension can buy reversibility. The affine-oriented rule beam uses dimension for a different resource: a finite local frame in which the original (possibly irreversible) dynamics is reproduced without changing its information-loss semantics.

---

## Smith 1971 — simulation tradeoffs and self-addressing binary macrocells

Alvy Ray Smith's 1971 paper, *Cellular Automata Complexity Trade-Offs*, studies simulation as a way to trade among:

- neighborhood size;
- state-set cardinality;
- time scale;
- spatial structural complexity.

Smith already uses an injective simulation relation of essentially the same broad form as an intertwining encoding: configurations of one CA are encoded into another so iterates of the target reproduce iterates of the source, possibly with time rescaling.

His major conclusions include:

- \(d+1\) cells suffice as a minimum neighborhood template for the class of \(d\)-dimensional CAs;
- binary is the minimum universal state-set cardinality;
- state-set and neighborhood complexity can be exchanged;
- linear time overhead can be removed, and arbitrary integer speedup can be obtained at additional structural cost.

### The especially relevant binary state-reduction construction

To simulate an \(r\)-state CA with binary cells, Smith replaces each source cell by a fixed binary **macrocell**.

The macrocell contains both:

1. payload bits encoding the simulated source state; and
2. **position/address information** telling a uniform binary local rule where it sits inside the macrocell.

The position pattern is supplied by a cyclic shift-register code; Smith explicitly draws on zero-free shift-register sequences so that local neighborhoods can identify position without a globally distinguished marker.

This is the closest conceptual ancestor found so far to the phase-synchronization problem in the affine-oriented lift.

Broadly:

\[
\text{Smith: payload + binary position code}
\]

versus

\[
\text{our lift: derived dynamical jet + affine orientation bit}.
\]

Both solve the same uniformity problem:

> identical binary cells must locally infer their role inside a structured encoding without being handed an absolute coordinate label.

But the constructions differ substantially.

### Smith versus the affine-oriented lift

**Smith**

- remains in the **same spatial dimension**;
- replaces one source cell by a spatial block/macrocell;
- introduces explicit periodic/address bits from a shift-register sequence;
- uses the block code to reduce a larger alphabet to binary;
- simulator complexity depends on source alphabet / chosen tradeoff;
- spatial scale changes under the simulation;
- the main objective is structural complexity tradeoff.

**Affine-oriented lift**

- adds **one spatial dimension**;
- source and target are already binary;
- does not use a conventional standalone address track;
- uses six derived fields
  \[
  (P_+,P_-^\dagger,D,T_2,0,X)
  \]
  whose local relations make phase self-synchronizing;
- the only explicit affine asymmetry is one fixed XOR bit on a directional rail;
- the encoding is locally invertible on an invariant **rule beam** containing every state of the source rule;
- time remains one-for-one:
  \[
  H^\uparrow L=LH;
  \]
- after the entry lift, the same grammar recursively lifts its own image with no further inherited-memory widening.

Smith therefore makes “binary” and “self-addressing simulation” unavailable as novelty claims in the broad sense. The candidate novelty is the very specific **dimension-raising, fixed-six-field, one-bit affine, recursively closed rule-beam construction**.

---

## The useful genealogy

A useful conceptual genealogy is:

\[
\boxed{
\text{Toffoli: extra dimension as history/reversibility}
}
\]

\[
\boxed{
\text{Smith: binary local self-addressing for uniform simulation}
}
\]

\[
\boxed{
\text{Affine-oriented lift: extra dimension as a finite self-synchronizing rule frame}
}
\]

The present theorem combines features that these classical constructions treat separately:

- Toffoli's cross-dimensional move;
- Smith's binary, locally self-addressing simulation problem;
- an injective invariant encoding of the full source dynamics;
- a fixed period-six affine frame;
- recursive closure of the encoding grammar itself.

Broad dimensional simulation and binary simulation are firmly prior art. Any novelty claim must be made at the level of this specific combination and construction, not at those broader levels.



# 33. Prior-art deep search: intrinsic simulation, induction, and presentations

The strongest relevant prior-art result found after the Toffoli/Smith pass is not bulking itself but **induction of cellular automata from a subgroup to a larger group**.

## A. Curtis–Hedlund–Lyndon / block-code background

For subshifts, every continuous shift-commuting map is a sliding block code. Thus any injective local recoding of an invariant subsystem is standard symbolic-dynamical structure.

Consequently, once an encoding \(L\) is known to be continuous, shift-compatible on the declared source action, injective, and to satisfy

\[
FL=LH
\]

on a closed invariant image, the existence of a local presentation on that image is unsurprising from the classical theory. The nontrivial content of the affine-oriented construction is therefore the **explicit binary code, phase synchronization, memory bounds, and recursive closure**, not the abstract existence of some local subsystem presentation.

---

## B. Bulking / intrinsic simulation

Delorme–Mazoyer–Ollinger–Theyssier formalize injective CA simulation via:

- subautomaton embeddings;
- spatial block packing;
- time rescaling;
- shifts.

Their injective bulking relation is defined for two CA of the **same dimension** \(d\). A source CA is simulated when some rescaling of it is a subautomaton of some rescaling of the target.

Therefore bulking gives the right vocabulary for:

- injective simulation;
- local decoding;
- block rescaling;
- subsystem comparison;

but the standard definition does not itself supply the cross-dimensional \(\mathbb Z^d\to\mathbb Z^{d+1}\) move.

Our rule beam is stronger than a trajectory simulation but, as a dynamical subsystem, fits the general “injective local simulation / conjugate subsystem” worldview.

---

## C. Induction from a subgroup to a larger group

Capobianco (2008/2009) and Ceccherini-Silberstein–Coornaert (2009) study **induced cellular automata**.

Let \(G\le\Gamma\). If

\[
A=\langle S,N,f\rangle
\]

is a CA on \(G\), its induced CA \(A^\Gamma\) on \(\Gamma\) uses:

- the same alphabet \(S\);
- the same neighborhood \(N\subseteq G\subseteq\Gamma\);
- the same local rule \(f\).

The larger system decomposes over the left cosets of \(G\) in \(\Gamma\). Each coset evolves as an independent copy of the original \(G\)-CA.

For

\[
G=\mathbb Z^d,\qquad
\Gamma=\mathbb Z^{d+1},
\]

the cosets are precisely the layers indexed by the new coordinate.

Thus the induced CA is the rigorous literature version of the **repeated-layer control**:

\[
\boxed{
\text{one copy of the source CA per transverse layer, with no coupling between layers.}
}
\]

This gives, long before the present work:

- same alphabet;
- one time step per source time step;
- arbitrary finite-memory source CA;
- immediate iteration to still larger groups/dimensions.

Therefore the broad theorem

> “every finite-memory CA can be represented one dimension higher, recursively”

is decisively prior art / trivial under induction.

The new theorem must not be sold at that level.

### Exact delta

The induced/repeated-layer CA has **rank-deficient geometry**: the added direction is dynamically ignored.

The affine-oriented rule beam instead constructs a nonconstant period-six transverse frame whose local fields are

\[
(P_+,P_-^\dagger,D,T_2,0,X),
\]

and whose native local rule reads the added axis in order to synchronize row role and recover the five parent queries.

The candidate contribution is therefore a **specific nontrivial presentation of the induced source dynamics** in which:

- the physical alphabet remains binary;
- the added direction carries derived source/rule information rather than duplicate copies;
- the phase coordinate is locally self-synchronizing with no external row label;
- the same six-field grammar is closed on its own image;
- the added direction participates essentially in the known local decoding/evolution construction.

Whether the resulting ambient child rule is irreducibly higher-dimensional off the beam is a separate question; the theorem concerns the rule beam.

---

## D. Capobianco's “CA as presentations” viewpoint

Capobianco explicitly studies what happens when a local description for a CA/subshift on a group is reused on a larger group and frames CA as **presentations of dynamical systems**.

This is very close to the correct conceptual category for the affine-oriented lift.

The present construction should be positioned as:

\[
\boxed{
\text{a special binary self-synchronizing presentation of an induced CA subsystem,}
}
\]

not as the discovery that induction/dimensional presentation is possible.

This prior art also sharpens the scientific question:

> What representation advantage does the affine-oriented presentation have over the canonical coset-wise induced presentation?

Known answers include:

- it makes \(D_HX\) and \(T_{2,H}X\) literal spatial coordinates;
- it materializes the Groovy/tangent residual structure;
- it locally exposes a \(\mathbb Z_2\)-graded directional frame;
- it provides the rule-beam / tangent-bundle geometry motivating the research program.

These are representational/dynamical-structure claims, not simulation-existence claims.

---

## E. Róka: simulations between Cayley-graph architectures

Róka (1999) gives sufficient conditions for uniform simulation between CA architectures on Cayley graphs. In particular, if a group homomorphism has finite kernel and finite-index image, the architectures can uniformly simulate one another.

This does **not** identify \(\mathbb Z^d\) and \(\mathbb Z^{d+1}\) as equivalent architectures:

\[
[\mathbb Z^{d+1}:\mathbb Z^d]=\infty.
\]

Our rule-beam construction evades that issue by living on a highly constrained invariant subsystem; it is not an equivalence of the two ambient full-shift architectures.

---

## F. Finite factors can be folded into the alphabet

Capobianco's work on CA over semidirect products shows that when one group factor is finite, it can be absorbed into the alphabet while preserving the dynamics.

This is directly relevant to the period-six phase axis.

On the phase-saturated rule beam, the finite phase group is

\[
P_d=(\mathbb Z_6)^k.
\]

Abstractly, the rule-beam dynamics is

\[
H\times\mathrm{id}_{P_d}.
\]

So a finite period-six axis is not intrinsically a new dynamical dimension: it can be folded into an enlarged alphabet.

The affine-oriented construction's point is precisely to realize that finite phase/frame information **spatially while keeping the physical alphabet binary**, and to make the phase locally recoverable.

This links the result directly back to Smith's state-set reduction/self-addressing problem.

---

## G. Projective subactions / one-more-dimension SFT simulation

Hochman, Aubrun–Sablik, and Durand–Romashchenko–Shen establish that lower-dimensional effective subshifts can be represented using local constraints one dimension higher, using factors/projective subactions or fixed-point tilings.

These results are much more general on the **static constraint** side.

They do not by themselves provide the particular one-step deterministic binary CA evolution

\[
H^\uparrow L=LH
\]

with the affine six-field self-synchronizing code.

So the affine lift is not novel because “local constraints can represent lower-dimensional structure one dimension up”; that is well established.

---

## H. Embedding dynamical systems into CA

Müller–Spandl (2009) prove that very general topological dynamical systems on metric Cantor spaces can be embedded into cellular automata on Cayley graphs, even preserving topological entropy.

Thus the existence of invariant CA subsystems conjugate to complicated source dynamics is itself very broad prior art.

Again, the specificity of the present result is the explicit binary representation and its algebraic interpretation.

---

## I. Current novelty boundary after the deep search

### Firmly prior art / not novelty

Do **not** claim novelty for:

- embedding/simulating a CA inside another CA;
- cross-dimensional CA simulation;
- same-alphabet lift to a larger group/dimension;
- recursive dimension raising in the trivial induced/layered sense;
- invariant conjugate subsystems;
- binary simulation;
- locally self-addressing block simulations in the broad sense;
- using one extra dimension to realize lower-dimensional symbolic structure.

### Candidate-specific contribution

The construction still appears unusual in the searched literature as the following exact package:

1. a fixed **six-field binary jet**
   \[
   (P_+,P_-^\dagger,D,T_2,0,X);
   \]
2. one affine \(\mathbb Z_2\) directional marker;
3. phase-free local synchronization of a period-six physical axis;
4. exact local parent recovery;
5. one-step intertwining on the full rule beam;
6. recursive closure of that same jet grammar;
7. explicit compact memory bounds;
8. direct Groovy/polarization/tangent interpretation of the encoded temporal rows.

The safe framing is therefore:

> **an explicit affine-oriented, self-synchronizing binary presentation of the induced source dynamics, designed so that temporal derivatives and Groovy/tangent structure become spatial coordinates.**

This is a much narrower claim than “a universal dimensional lift theorem,” and is the claim for which no equivalent construction has yet been found in the searched literature.

### Important unresolved novelty check

A stronger literature search should still target:

- self-synchronizing / comma-free block codes used specifically as CA subsystem presentations;
- binary recodings of finite group extensions with locally inferred phase;
- CA “jet” or spacetime-derivative encodings;
- phase-free spatialization of \(X,HX,H^2X\);
- recursively closed block-code presentations.

Those are now the most plausible places for a genuinely equivalent construction to hide.

# 34. Canonicity audit: “the lift” versus “a lift”

The broad dimensional-lift conditions do **not** characterize the affine-oriented jet lift uniquely.

There are classical self-synchronizing macrocell/“freezing” constructions, and there is even a very small explicit alternative in the present binary cross-dimensional setting.

## A. Period-3 necklace lift

Choose the two binary words

\[
c_0=001,
\qquad
c_1=011.
\]

Their cyclic orbits are disjoint:

\[
\operatorname{Orb}(c_0)
=
\{001,010,100\},
\]

\[
\operatorname{Orb}(c_1)
=
\{011,110,101\}.
\]

Thus every nonconstant binary triple uniquely identifies:

1. the encoded source bit \(b\in\{0,1\}\); and
2. its phase \(j\in\mathbb Z_3\).

Let \(H\) be any binary CA on \(\mathbb Z^d\) with finite memory \(M\).

Define

\[
\boxed{
N(X)(g,y)
=
c_{X(g)}(y\bmod3).
}
\]

This gives a period-three extra spatial axis.

A child cell at \((g,y)\) reads the three vertical cells

\[
(y-1,y,y+1)
\]

at every inherited position \(g+m,\;m\in M\).

Each triple locally decodes \(X(g+m)\); the center triple also identifies the common phase \(j\).

Apply the parent local rule \(h\) to the decoded \(M\)-pattern to obtain

\[
b=H(X)(g),
\]

then output

\[
c_b(j).
\]

Therefore there is a phase-free binary child CA \(F\) with memory

\[
\boxed{
M\times\{-1,0,1\}
}
\]

such that

\[
\boxed{
F\circ N=N\circ H.
}
\]

The source bit is locally recoverable from the same three-cell vertical code.

Because the target is again binary, the **same necklace grammar** can be applied recursively at every later finite dimension.

Hence this is another universal binary finite-memory dimensional lift satisfying:

- one-step exact intertwining;
- local parent recovery;
- phase-free local evolution;
- binary physical alphabet;
- nonconstant finite-period added axis;
- recursive closure through every finite depth.

It is simpler than the affine-oriented jet lift if these are the only criteria.

### Minimality inside the necklace ansatz

For a nontrivial globally phased code with one primitive cyclic word per source bit:

- period \(2\) has only one primitive binary necklace, so it cannot assign disjoint full-period phase orbits to both payload values;
- period \(3\) has at least two.

Thus period \(3\) is minimal in this narrow “one repeated codeword per binary payload” class.

This is **not** a global lower bound over all CA encodings.

## B. Relation to freezing / ungrouping prior art

Cervelle–Formenti–Guillon formalize essentially the general phase-synchronization principle.

For a macrocell alphabet \(B\subset A^h\), impose a sufficiently strong **freezing** condition preventing ambiguous overlaps. Then the phase-saturated union

\[
\Lambda
=
\bigcup_{0\le i<h}
\sigma^i(B^{\mathbb Z})
\]

is a disjoint union, so a local rule can infer the unique macrocell phase \(i\) without an externally supplied coordinate label.

They then define an “ungrouped” partial CA whose local rule simulates the grouped CA on this phase-saturated subshift.

Guillon–Richard likewise use **strongly freezing** binary languages to encode additional alphabet information inside binary configurations.

Therefore:

\[
\boxed{
\text{phase-free self-synchronizing CA encoding is established prior art.}
}
\]

There are many such encodings.

The affine-oriented construction must not claim uniqueness at that level.

## C. What is actually special about the affine-oriented jet lift

The necklace/freezing lift solves the synchronization problem by adding a conventional positional code.

The affine-oriented jet lift instead requires the added six phases themselves to be **specific dynamical observables**:

\[
\boxed{
(P_+,P_-^\dagger,D_HX,T_{2,H}X,\text{recovery pair}).
}
\]

Its extra coordinate therefore literalizes:

- two oriented spatial finite differences;
- the one-step trajectory displacement;
- the two-step temporal displacement;
- the source state.

This is why Groovy/polarization/tangent quantities become visible as spatial residuals.

The necklace lift does none of that; its transverse axis is only an address/payload code.

Thus the affine-oriented lift is not canonical among all valid dimensional lifts. Its possible canonicity is conditional on a much narrower **jet representation contract**.

## D. Narrow uniqueness evidence inside the jet ansatz

Even inside the six-field project there is gauge freedom.

Known equivalent or admissible choices include:

- historical nonlinear recovery
  \[
  (XD,\;X(1\oplus D));
  \]
- affine recovery
  \[
  (0,X);
  \]
- global row complement;
- cyclic phase choice;
- spatial reflection / opposite chirality.

A previous complete census of all \(64\) constant six-row XOR masks found several masks satisfying universal base closure and recursive synchronization; after quotienting obvious complement symmetries, more than one representative remains.

However, among all **single-row** XOR markers in the frozen six-field row convention, only the marker on the minus-direction projection satisfies both:

1. universal base lift; and
2. rule-free recursive synchronization.

After spatial reflection, the opposite chirality gives the mirrored equivalent construction.

So the strongest current canonicity statement is:

\[
\boxed{
\text{the affine orientation bit is unique among one-row markers in the frozen jet grammar, up to chirality.}
}
\]

This is far weaker than uniqueness of the lift itself.

## E. Correct current terminology

Use:

> **the affine-oriented jet lift**

as the name of the chosen construction.

Do **not** use “the unique dimensional lift.”

The mathematically honest status is:

\[
\boxed{
\text{a universal lift, with a plausibly canonical normal form inside a specified jet ansatz.}
}
\]

The true uniqueness problem is now:

> Fix an explicit representation contract—binary alphabet, one-step exactness, local recovery, no independent phase/address tape, designated spatial- and temporal-difference coordinates, recursive closure, and a complexity/minimality budget. Classify all lifts satisfying it up to local conjugacy, reflection, phase rotation, complement, and recovery-gauge change.

Only such a classification could justify calling an equivalence class **the** lift for those conditions.

# 35. Class-IV inheritance under lift: beam versus ambient rule

Known higher-dimensional Class-IV-like cellular automata exist (canonical example: Conway Life in 2D; higher-dimensional Life variants also exhibit localized propagating structures). For the affine-oriented lift, however, distinguish two notions.

On the rule beam,
\[
H^\uparrow|_{B_H}\cong H.
\]
Therefore every property that is genuinely invariant under this conjugacy is inherited by the encoded subsystem. A 1D Class-IV root therefore gives a Class-IV-like invariant subsystem at every finite lift depth in the strong sense of exact encoded dynamics.

This does **not** imply that the full ambient descendant CA is Wolfram Class IV from generic ambient initial conditions. The rule beam is a highly constrained finite-phase subshift and the lift theorem leaves off-beam completion nonunique. Different ambient completions can agree exactly on the beam while behaving very differently elsewhere.

A 1D localized particle also becomes periodic in each newly added transverse direction under the prepared beam, so it is a stripe/sheet (codimension structure), not automatically a genuinely localized n-dimensional glider.

Natural future experiment: choose fixed, natural completion policies for lifted 54/110 and ask whether generic ambient 2D/3D initial conditions regenerate Class-IV-like localized structures. Controls must include roots from Classes I–III and multiple completion policies.

# 36. Jev-guided selective-persistence × spreading discriminator

## A. Jev scout

A frozen Jev probe withheld the already-known recurrence/spreading channels and exposed anonymous primitive measurements. Jev's strongest stable semantic judgments were persistence across conditions and selective memory. Both ranked the core 54/110 families highly and achieved finite-panel AUC 1.0 against the inherited Class-III representatives, while several Class-II rules remained confounders. An opaque generic-profile control did not reproduce the signal. Jev therefore served as a semantic feature scout, not a final classifier.

The transparent post-hoc distillation was
\[
S=\max(0,R_{w=7})\max(0,M_{h=8}),
\]
where R is standardized selective retention and M is held-out predictive gain from eight-step local history relative to the current bit.

This suggested the mechanistic conjunction
\[
\text{selective predictive persistence}\ \land\ \text{sustained disturbance spreading}.
\]

## B. Frozen fresh candidate

Before fresh simulation, freeze
\[
\boxed{\text{select iff }S>0.20\ \land\ \alpha_{512}>0.50,}
\]
with
\[
\alpha_{512}=\log_2\frac{\bar d(512)}{\bar d(256)},
\]
where \(\bar d(t)\) is mean support diameter over 96 single-bit perturbation trials (16 origins × 6 independent seeds). The same burned states feed both S and alpha.

Primary condition: width 2053, density 0.5, burn 2048, 512 scored transitions. Validation/stress conditions change width and density without retuning:

- N=2063, density 0.3;
- N=2081, density 0.7;
- N=2069, density 0.1;
- N=2099, density 0.9.

Each condition uses six fresh seeds.

## C. Exact finite result

Across all five fresh conditions:

- 54/110: 10/10 condition decisions selected;
- 84 undisputed inherited Class-I–III representatives: 0/420 selected;
- disputed 41/106: 0/10 selected;
- radius-2 rare-correction mechanism challenge: 0/5 selected;
- radius-2 pure shift: 0/5 selected.

Margins over all five conditions:

\[
\min S_{54/110}=0.2049895616,
\qquad
\min \alpha_{54/110}=0.6831268635.
\]

Every undisputed negative with \(\alpha>0.5\) has exactly \(S=0\) under the clipped definition. Among negatives with \(S>0.2\), the largest spreading exponent is Rule 62 at
\[
\alpha=0.4989387569.
\]

Thus the observed negative cloud forms a clean cross-like phase-plane separation: high-persistence Class-II-like rules fail spreading, while strongly spreading Class-III-like rules fail selective persistence.

Key mechanism controls:

- Rule 5: often high S, alpha=0.
- Rule 62: high S, alpha below 0.5 in all five conditions (closest 0.49894).
- Rules 122/126: S=0, alpha≈1.
- radius-2 correction family: S=0 in all five conditions; alpha>0.5 in four of five. This directly rejects the rare-correction mechanism that could pass the earlier recurrence+spreading proxy.

## D. Label-convention limitation

A common published Wolfram table lists representatives 41,54,106,110 as Class IV. The project's inherited protocol treats 41/106 as disputed and defines 54/110 as the core positives. The new candidate rejects 41 and 106 robustly:

- 41 lies in low-spread / low-selective-persistence territory;
- 106 lies in high-spread / zero-selective-persistence territory.

Therefore this is presently a finite discriminator for the **54/110 core phenotype under the project convention**, not a classifier reproducing every conventional Class-IV label. This disagreement is itself mechanistically informative and must remain explicit.

## E. Prior-art boundary

The broad two-axis idea is not novel. Relevant prior art includes Langton (1990) on information storage/transmission/modification at the edge of chaos; Bagnoli/Rechtman/Ruffo on CA damage spreading and Lyapunov exponents; Wuensche (1999) on input-entropy-variance automatic CA classification; Feldman/McTague/Crutchfield (2008) on complexity-entropy diagrams; Borriello/Walker (2017) on transfer-entropy ECA classification; and Mediano et al. (2022) on information storage/transfer in Rules 54/110.

Most importantly, Fuat Kaan Mirza (2026 preprint) explicitly reports a phase plane combining block-entropy rate and damage-spreading velocity, with a white-box threshold classifier reproducing Wolfram classes. Thus **do not claim novelty for “information/organization metric + damage spreading identifies Class IV.”**

Potentially distinctive delta: S is specifically selective predictive persistence (selective visitation relative to predecessor ambiguity × held-out predictive value of history), not block entropy/general randomness; and it rejects the known radius-2 rare-correction spreading mechanism while splitting conventional 41/106 away from the 54/110 core phenotype. Novelty remains unverified until a fuller literature comparison.

## F. Current mechanistic hypothesis

Working map:

\[
\begin{array}{c|cc}
& \text{low spreading} & \text{sustained spreading}\\
\hline
\text{low selective persistence} & \text{I/simple II-like} & \text{III-like}\\
\text{high selective persistence} & \text{II-like} & \text{54/110 core complex phenotype}
\end{array}
\]

This is a falsifiable mechanism hypothesis, not a redefinition of Wolfram classes.

Next falsification targets: broader-radius rules; higher-dimensional complex CAs (especially Life); natural ambient completions of lifted 54/110; direct comparison with Mirza's entropy×damage phase plane on identical trajectories; and explicit alternative ECA class conventions, especially Rule 106.


# 37. Completion-independent first-floor 2D beam invariants

The final affine-oriented first lift was exhaustively enumerated for all 256 ECAs over the complete 9-bit source window and all six transverse phases. The child physical neighborhood is 5×7 = 35 bits. The lift forces only a partial 2D local rule \(D_H\to\mathbb F_2\); every total completion agreeing on that domain carries the same prepared rule beam.

If \(F_H=|D_H|\), there are \(2^{2^{35}-F_H}\) total binary completions. Thus ambient 2D Wolfram class is not determined by the root beam.

Exact first-floor findings:

- native child-output consistency: 256/256;
- local phase recovery: 256/256;
- local parent-bit recovery: 256/256;
- for every root, all six phase sheets have equal cardinality:
  \[
  |D_{H,0}|=\cdots=|D_{H,5}|,\qquad |D_H|=6|D_{H,p}|;
  \]
- for every root, the full phase-saturated forced domain has affine hull dimension 30 in \(\mathbb F_2^{35}\), codimension 5. The five universal affine relations are the five longitudinal equalities between transverse offsets -3 and +3 in a period-six axis;
- on each fixed phase sheet, the tuple
  \[
  (\dim_{m aff}D_{H,p},h_2(H,p),h_3(H,p))
  \]
  is independent of phase, where \(h_k\) is the evaluation rank of Boolean monomials of degree at most \(k\);
- these phase-conditioned quantities, forced-domain size, and root-level cohabitation partner counts are exactly invariant under ECA reflection/complement symmetry orbits.

Native polynomial extension degree on the forced domain is at most cubic for every ECA: child output has degree distribution 4 affine / 51 quadratic / 201 cubic; parent recovery 95 quadratic / 161 cubic; phase decoder 55 quadratic / 201 cubic. The four conventional Class-IV representative orbits require cubic output/recovery/phase decoding, but many other roots do too.

For conventional Class-IV representatives, phase-sheet `(h2,h3)` is:
- 41: (111,265)
- 54: (105,184)
- 106: (94,218)
- 110: (98,202)

These values are descriptively high but do not define a clean Class-IV boundary.

Exact final-affine 2D cohabitation over all 32640 unordered ECA pairs gives 30320 compatible pairs and 17926 compatible nonvacuous pairs. Within the conventional Class-IV representatives, 54/110 are compatible with 36 shared keys; 106/110 are incompatible with 564 shared keys; 41/54 and 41/110 are compatible but vacuous; 41/106 and 54/106 are compatible and nonvacuous.

A notable exhaustive finite fingerprint is
\[
I(H)=(h_2(H),h_3(H),N_{m nv}(H)),
\]
where \(N_{m nv}\) is the number of nonvacuously compatible partners among the other 255 ECAs. This triple takes 88 distinct values on the 88 reflection/complement ECA symmetry orbits. Thus, within the finite ECA universe, the completion-independent geometry of the first lifted 2D beam suffices to fingerprint the source symmetry orbit without directly reading the source truth table.

This is an empirical exhaustive finite-family fact, not yet a theorem for arbitrary CA families/radii, and not yet a novelty claim. A dedicated prior-art search is required before promotion.

Interpretive consequence: Class-IV dynamics is inherited exactly *on the beam* by conjugacy, but generic ambient 2D class is not forced because almost all 35-bit truth-table entries remain free. The scientifically interesting next questions are invariance/renormalization of these local-language quantities across 2D→3D→…, and whether fixed natural completions of 54/110 regenerate the selective-persistence × spreading phenotype off-beam.
