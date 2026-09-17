# Selective predictive persistence × disturbance spreading

## Status

**Prospective finite ECA result, not a universal Class-IV theorem.**

The candidate was frozen before the fresh primary simulation:

\[
S=\max(0,R_{w=7})\max(0,M_{h=8}),
\qquad
\text{select} \iff S>0.20 \land \alpha_{512}>0.50.
\]

Here:

- `R` is standardized selective retention: whether the visited trajectory preferentially occupies locally less-ambiguous same-window transitions relative to a boundary-conditioned uniform reference.
- `M` is held-out predictive gain from an eight-step local history relative to the current bit alone.
- `alpha_512` is the logarithmic doubling exponent of mean single-bit disturbance-support diameter from t=256 to t=512.

The same burned states feed both axes.

## Fresh conditions

| Condition | Ring width | Initial density | Outcome |
|---|---:|---:|---|
| P | 2053 | 0.5 | 54/110 only |
| V1 | 2063 | 0.3 | 54/110 only |
| V2 | 2081 | 0.7 | 54/110 only |
| S1 | 2069 | 0.1 | 54/110 only |
| S2 | 2099 | 0.9 | 54/110 only |

Across the five independently seeded conditions:

- **10/10** core-positive decisions (54 and 110) pass.
- **0/420** undisputed Class-I–III representative decisions pass.
- **0/10** disputed 41/106 decisions pass.
- **0/5** radius-two rare-correction mechanism challenges pass.
- **0/5** radius-two pure-shift controls pass.

This is a finite dependent panel, not an estimate of generalization accuracy.

## Separation margins

- Minimum positive `S`: **0.204989562**.
- Minimum positive `alpha_512`: **0.683126863**.
- Maximum `S` among undisputed negatives with `alpha_512 > 0.5`: **0.000000000**.
- Maximum `alpha_512` among undisputed negatives with `S > 0.2`: **0.498938757**.

Thus, in these five conditions, the negative cloud is more strongly separated than the declared thresholds imply: every fast-spreading undisputed negative has `S=0`, while the strongest-spreading high-`S` negative is Rule 62 at `alpha=0.4989387569`.

## Mechanism controls

The two Jev-derived Class-II confounders behave as intended:

- Rule 5 can have high `S` but its disturbance does not spread.
- Rule 62 has consistently high `S`, but remains below the spreading threshold in all five conditions.

Conversely, the chaotic controls 122 and 126 have `S=0` while spreading at roughly `alpha≈1`.

The radius-two rare-correction family is especially important: it exceeds the spreading threshold in four of five conditions but has `S=0` in every condition because its predictive-history gain is nonpositive. This directly distinguishes the new candidate from the earlier recurrence-plus-spreading proxy that this family could fool.

## Disputed conventional Class-IV rules

Under a common published Wolfram-class table, Rules 41 and 106 are Class IV alongside 54 and 110. The project has always reported 41/106 separately because their assignment is contested.

The present candidate **rejects both**:

- Rule 41 maps to the low-spread / low-selective-persistence region.
- Rule 106 maps extremely cleanly to the high-spread / zero-selective-persistence region.

Therefore this result must currently be described as a discriminator for the **54/110 core phenotype under the project convention**, not as a classifier reproducing every conventional Class-IV label.

This disagreement is scientifically useful: it says the candidate is not merely imitating the textbook label table. It operationally splits the four commonly listed representatives into distinct mechanisms.

## Prior-art boundary

The broad conceptual form is **not novel**.

Relevant prior art includes:

- Langton (1990), *Computation at the edge of chaos*: storage, transmission, and modification of information near a phase transition.
- Bagnoli, Rechtman & Ruffo (1992; later arXiv version), *Damage spreading and Lyapunov exponents in cellular automata*: perturbation spreading / Boolean-derivative Lyapunov analysis.
- Wuensche (1999), *Classifying cellular automata automatically*: automatic order/complexity/chaos discrimination using input-entropy variance, including glider-rich rules.
- Feldman, McTague & Crutchfield (2008), *The organization of intrinsic computation*: complexity–entropy diagrams and edge-of-chaos information processing.
- Borriello & Walker (2017), *An Information-Based Classification of Elementary Cellular Automata*: transfer-entropy-based ECA classification and explicit discussion of Rule 106's input sensitivity.
- Mediano et al. (2022), *Integrated information as a common signature of dynamical and information-processing complexity*: information storage/transfer in Rules 54 and 110 and a connection to edge-of-chaos complexity.
- Mirza (2026), *Microcanonical and Canonical Motif Ensembles for Cellular Automata*: the closest current prior art found; its abstract explicitly claims a phase plane combining block-entropy rate with damage-spreading velocity and a white-box threshold classifier of Wolfram classes.

So we must **not** claim novelty for “an information/organization axis plus damage spreading identifies Class IV.”

The candidate-specific possible contribution is narrower: `S` is not block entropy or generic complexity. It multiplies a selective-visitation retention statistic by held-out predictive value of temporal history, and it rejects the known radius-two rare-correction spreading mechanism while separating the 54/110 core phenotype in five fresh conditions. Whether that constitutes a useful novel diagnostic remains to be established against the full prior literature and broader CA families.

## Current interpretation

The cleanest working interpretation is a two-axis mechanistic map:

| | Low spreading | Sustained spreading |
|---|---|---|
| Low selective predictive persistence | Class I / simple II | Class III-like |
| High selective predictive persistence | Class II-like | **54/110 core complex phenotype** |

This is a hypothesis about mechanism, not a redefinition of Wolfram's classes.

## Next falsification targets

1. Test broader-radius rules and known complex rules outside ECA.
2. Generalize the measurement to 2D Class-IV systems such as Life, without tuning thresholds to those systems.
3. Apply it to natural ambient completions of lifted 54/110 and ask whether the core phenotype regenerates off-beam.
4. Compare quantitatively with Mirza's block-entropy × damage-spreading phase plane on the same trajectories.
5. Test alternative published ECA class conventions explicitly, especially Rule 106.

## Provenance

Primary protocol SHA-256:
`3e5c7efee950261c7e243aa1600951bd57ac163173051a97e7994ab2a3b20325`

Validation protocol SHA-256:
`71fc7979c03ac93661c803496e9d53fdd02296cbed712120bf13bfe1c26d74ae`

Stress protocol SHA-256:
`bd3b231e541f15ac8afac21cff0fac52845a74f01ddf06b749579293ea2c8cd2`