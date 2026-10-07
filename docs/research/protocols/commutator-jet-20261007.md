# Protocol: intrinsic commutator jet for Rules 110 and 62

**Status:** frozen before evaluation, 2026-10-07.  
**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Question

The latent-Q work found that, at cadence \(F=H^2\), retaining future Groovy
\(G(FX)\) supplies the missing future coordinate above current \((P,G)\) on
the tested Rule-110 rings.

There is a rule-intrinsic version of the same construction. For any
configuration-valued observable \(A\), define the characteristic-two
commutator with the source evolution \(H\)

\[
\mathcal C_H(A)=A\circ H\oplus H\circ A.
\]

Start with

\[
A_0=D_H=I\oplus H
\]

and iterate

\[
A_{k+1}=\mathcal C_H(A_k).
\]

Name

\[
A_0=D,\qquad A_1=G,\qquad A_2=Q,\qquad A_3=R.
\]

Along every source trajectory \(S_{t+1}=H(S_t)\),

\[
A_{k,t+1}=H(A_{k,t})\oplus A_{k+1,t}.
\]

Thus each new field is exactly the correction required to transport the
previous field under the source law.

This unit asks whether that tower has finite closure structure, and whether
Rules 110 and 62 differ in that structure despite their matched predictive-
history budget.

## Algebraic cadence bridge

For the parity experiment's cadence \(F=H^2\), define

\[
Q^{(2)}_G(X)
=
G(FX)\oplus F(G(X)).
\]

Given \(G(X)\), the two fields \(Q_G^{(2)}(X)\) and \(G(FX)\) are related by
the invertible coordinate change

\[
G(FX)=F(G(X))\oplus Q_G^{(2)}(X).
\]

Therefore \((P,G,G\circ F)\) and \((P,G,Q_G^{(2)})\) induce identical source
partitions on every domain. Verify this explicitly against the existing
Rule-110 latent-Q certificates at frozen widths where practical; the identity
itself is algebraic and does not depend on the finite test.

## Rules and domains

Primary matched pair:

- Rule 110;
- Rule 62.

One-step source cadence \(H\) for the intrinsic jet.

Exact finite periodic rings:

- \(n=8,10,12,14\) for all tower/fiber quantities;
- \(n=16\) only for summaries that remain under the resource budget.

No Class-IV census.

## Jet depth

Construct through

\[
A_5
\]

so that \(D,G,Q,R,A_4,A_5\) are available.

For each \(A_k\):

- exact local truth table on the full source window;
- minimal source radius;
- algebraic normal-form degree;
- truth-table activity fraction;
- equality / complement / shift-equivalence checks against earlier tower
  fields where meaningful.

## Prefix autonomy

For prefix

\[
J_k(X)=(A_0(X),\ldots,A_k(X)),
\]

the lower fields can be advanced from \(J_k\) if and only if
\(A_{k+1}(X)\) is determined by \(J_k(X)\), because

\[
A_{j}(HX)=H(A_j(X))\oplus A_{j+1}(X).
\]

For each rule, width and \(k=0,\ldots,4\), exhaustively compute:

- number of distinct \(J_k\) states;
- \(H(S\mid J_k)\) under the uniform finite-ring prior;
- \(H(A_{k+1}\mid J_k)\);
- exact global factor decision \(J_k\to A_{k+1}\);
- first exact witness when the factor fails.

Define **jet closure depth** on a finite ring as the first \(k\) for which
\(J_k\to A_{k+1}\) holds. If none through \(k=4\), record ">4"; do not extend
the tower in this unit.

This is a present-state factor question, not a suffix-memory statistic.

## Locality of any finite closure

If a prefix globally closes at some \(k\le4\), search source-independent local
laws for \(A_{k+1,i}\) from neighborhoods of the current jet fields at radii
0,1,2,3. Save the first closed radius or witnesses through radius three.

A global factor with no small-radius law remains a finite-ring autonomous
factor, not a full-line CA theorem.

## Matched-rule comparison

No scalar Class-IV decision is frozen.

The descriptive comparison is structural:

- Does either rule close at lower jet depth?
- How quickly does \(H(S\mid J_k)\) collapse toward zero?
- How much genuinely new information
  \(H(A_{k+1}\mid J_k)\) is introduced at each level?
- Do \(Q\) and \(R\) expose qualitatively different spatial organization
  despite similar earlier history budgets?

Any class interpretation is post-hoc and explicitly secondary.

## Figures

Generate scientific figures only from the exact simulation code.

For both Rule 110 and Rule 62, use the same declared single-seed initial
condition, finite width, boundary convention and time horizon. Render five
panels:

\[
S,\quad D,\quad G,\quad Q,\quad R.
\]

Definitions in the renderer must call the same jet implementation used by the
experiment. No generative-image tools.

Save:

- results/commutator_jet_20261007/rule110_SD GQR.png
- results/commutator_jet_20261007/rule62_SD GQR.png

(with filesystem-safe names in implementation).

## Hard boundaries

- No additional rules.
- No observer/threshold search.
- No claim that a finite-ring factor is a full-line factor.
- No claim of compression advantage merely because an individual latent field
  has low marginal entropy.
- Preserve negative results if the tower simply reconstructs the source.
- Distinguish the one-step intrinsic \(Q=\mathcal C_H(G)\) from the cadence-two
  \(Q_G^{(2)}=\mathcal C_{H^2}(G)\).

## Planned artifacts

- scripts/experiment_commutator_jet.py
- results/commutator_jet_20261007.json
- results/commutator_jet_20261007/*.png
- docs/research/2026-10-07-commutator-jet.md
