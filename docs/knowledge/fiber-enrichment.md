# A base rule's height-one fiber is enriched or depleted in the persistence × spreading phenotype

Sampling 512 of the 4096 Life-like rules that restrict on a height-one strip
to each of ECAs 54, 22, 0, 90 and 204, and measuring the starred observables
at height two (width 521, density 0.5, the cross-dimensional unit's contract),
the fraction of rules with `S* > 0` and `alpha_x > 0.5` is 0.47, 0.37, 0.25,
0.22 and 0.07 respectively; a tie-corrected Kruskal–Wallis test on `S*`
gives p ≈ 10⁻⁴⁰ as a descriptive statistic. HighLife (`S*` 0.125) and Life
(0.010) lie inside their fibers' 10th–90th percentile bands, so the named
complex rules are typical members, not outliers. The frozen bet that
fiber(22) would split into Life-like and explosive halves failed: 72% of it
spreads ballistically. A height-four subsample preserves the ordering except
that 54 and 22 tie.

Status: exploratory. One strip height, one density, one contract, finite
samples; the ordering may be explained by the activity the six fixed bits
impose (fibers with fixed births spread, the identity fiber freezes), which
a census over all 64 fibers or fixed-live-bit-matched fibers would separate.
Rule 110 has no fiber in this family.

Source: [fiber census](../research/2026-09-17-fiber-census.md); protocol `docs/research/protocols/2026-09-17-fiber-census.md`.

## Update, 2026-09-17: all 64 fibers

The [64-fiber census](../research/2026-09-17-fiber-census-64.md) (128 rules
per fiber) finds both-positive fractions from 0.05 (fiber of 76) to 0.51
(fiber of 54), median 0.22. A logistic model with pairwise interactions
between the six exposed bits beats main effects out of sample for
both-positive and spreading (birth-survival pairs strongest), not for
persistence. The eight affine bases sit inside the others' interquartile
range. The first census's 0-versus-90 ordering swapped on fresh samples; the
ends held.


## Update, 2026-09-17: rule 110 acquires a fiber

The Life-like family reaches only the 64 reflection-symmetric ECAs, so rule
110 had no fiber in any census above. The
[handed census](../research/2026-09-17-handed-fiber-census.md) replaces the
Moore count by `(centre, west neighbour, count of the other seven)`, 32 table
entries. Its height-one restriction is a coordinate projection **onto all 256
ECAs, every fiber exactly 2²⁴ rules**, and it contains the Life-like family.

Nine fibers at 256 rules and all 256 at twelve: fiber(110) is both-positive at
0.543, in a statistical tie at the top with its mirror 124 (0.555) and with 54
(0.531), and far above 30 (0.273), 90 (0.223), 0 (0.164) and 204 (0.105). The
enrichment sits on the **persistence** axis: fibers 22 and 30 spread more
(0.922, 0.906 against 0.844) and still fall far below on the conjunction,
because they persist at 0.469 and 0.312 against 0.629.

Two findings generalize beyond the panel. A base's own one-dimensional
phenotype predicts its fiber's on **both** axes across all 256 bases
(spreading p ≈ 2 × 10⁻¹⁶, persistence p ≈ 3 × 10⁻⁹, descriptive since fibers
are not independent); in the Life-like family persistence had looked like a
purely two-dimensional activity effect. And the non-additivity of the exposed
bits replicates in eight bits with the same shape: interactions win out of
sample for spreading only.

Chirality is **not** detectable. The family marks a direction, so fiber(124)
is a genuinely different set of rules from fiber(110), and the two are
indistinguishable (spread 0.852 against 0.844, p = 0.81, the point estimate
leaning opposite to the frozen prediction).

A methodological correction belongs with this entry. The protocol's null-pair
calibration compared two *independently seeded* samples of the deduced-identical
fibers 110 and 137, which rejects at the nominal rate by construction; it
rejected at p = 0.027 and was mistaken for a possible implementation fault. A
matched-seed control (same seed stream, complemented initial states) shows the
implementation is exactly complement-covariant to 1.6 × 10⁻¹⁵. Null-pair
calibrations in this Program must pair the draws, not only the distributions.

Status: still exploratory. One strip height, one density, one contract, and the
observer is reflection-symmetric while the family is not.

## Update, 2026-09-18: persistence decomposes into base and completion

The [matched-completion unit](../research/2026-09-18-matched-completion-persistence.md)
splits the persistence axis. Persistence is `R* > 0 ∧ M* > 0`: retention and
history gain. Because the height-one restriction is a coordinate projection, a
24-bit completion is one object shared by every fiber, so the same completion can
be embedded under every base and every seed held fixed across them.

Eight bases × 512 completions at height two: **history gain is base-dominated**
(degrees-of-freedom-adjusted variance component 0.0396 against the completion's
0.0116) and **retention is completion-dominated** (0.0217 against 0.0348).
Spreading is base-dominated as well, so retention is the one observable the
refinement chooses for itself. Holding a completion fixed, rule 110 beats rule 30
on history gain for 87.1% of completions while their retention difference is null.

Two structural facts beyond the decomposition. History gain **anticorrelates**
between distant bases rather than merely failing to transfer (Spearman −0.414 for
110 against 30, −0.254 against 90, while 54, 5 and 22 run positive), so the same
completion pushes different bases' history gain in opposite directions; this is
unexplained. And history gain is **not bit-additive at all**: a cross-validated
ridge fit on the 24 completion bits has negative `R²` in every base, while
retention is partly additive, up to 0.271.

A correction to the Class-IV reading. At height four the persistence-only control
rule 5, whose one-dimensional history gain is 0.976 against 110's 0.903, overtakes
110 on mean history gain (0.290 against 0.277); height two cannot separate them
because both sit at the ceiling. **History-gain inheritance tracks the base's
one-dimensional history gain, not its informal class.** The enrichment reported in
the handed census is real, but Class-IV-ness is not its explanation.

Status: exploratory. Eight bases, one contract, one density, height two for the
main grid.
