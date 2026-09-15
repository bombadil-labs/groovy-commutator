# Round 10: rare corrections to transport as a mechanism adversary

Protocol review: none at freeze; run authorized by Myk2026-09-15. Evaluation precedes independent review. This is a targeted generalization/mechanism test, not a new labeled Class IV validation set.

For radius r=1,2,3 define F_r(X)_i=X_{i+r} XOR product_{j=-r}^{r-1}X_{i+j}. Radius1 is ECA106. Include pure shift X_{i+r} controls. Every F_r is right-permutive and preserves the iidBernoulli(1/2) measure on the infinite line: every n-bit output word has exactly2^(2r) preimages of length n+2r. Thus spatial slices stay iid, although time slices need not be independent. The p1,v=-r recurrence error is2^(-2r), giving q=2^(1-2r). This is an exact value for that candidate, not a theorem about the minimum over candidates.

Use seeds6041541/6041542, observed width4093, burn2048,1024 usable frames,32 equally spaced perturbation sites,horizon512. Implement open-window shrinking evolution with adequate iid padding for all trajectories and disturbance cones; do not use periodic rings. Generalize comparison velocities to |v|<=r*p, p1..8, as required by the declared radius. Keep q and alpha cutoffs at0.5, and report their decisions, all selected recurrences, empirical8-bit spatial entropy and one-step matched-shift errors. Pure shifts must have zero mismatch and bounded disturbance diameter. A selected r2/r3 rule would refute the inference from low q plus spread to an ordered spatial background, NOT establish a mislabeled Wolfram-class counterexample. Do not assign new class labels.

Also verify the ECA local reflection/complement conjugacy identities exhaustively for all256 tables and all8 neighborhoods. These transformations preserve q (velocity set reflected as needed), support diameter, and the finite decision under matched inputs/perturbations; this algebraic control does not test arbitrary nonlinear recodings.

Five-minute local budget, no cutoff changes. Stop at ten unless a specific extra test can resolve a nearly settled question.
