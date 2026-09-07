# Rule 90 vs Rule 110: A Wet-Math Comparison
## Exact closure, structured noncommutation, and history-repairable coarse dynamics

**Status:** exploratory comparison notebook  
**Purpose:** compare the wet-math analyses previously developed around Rule 90 with Rule 110, using Rule 30 as an additional Class-III control where useful.

**Important caveat:** Rule 90 is an unusually algebraic/linear Class-III rule. Therefore Rule 90 vs Rule 110 is not by itself a clean “Class III vs Class IV” experiment. Rule 30 is included at key points to separate linearity from Wolfram class.

---

# 1. The three rules

- **Rule 90:** conventionally Class III; additive/linear over GF(2); generates the Sierpiński gasket.
- **Rule 30:** conventionally Class III; nonlinear, chaotic-looking; used here as a generic chaotic control.
- **Rule 110:** canonical Class IV; nonlinear; supports periodic ether plus localized structures and is computationally universal.

The central question is:

> **What survives when the exact Rule-90 constructions are repeated on Rule 110?**

---

# 2. First temporal derivative

For any ECA rule \(\phi\),

\[
D_\phi(S)=S\oplus\phi(S).
\]

Because the center-bit identity is Rule 204,

\[
D_\phi
\]

is itself an ECA with Wolfram number

\[
\phi\oplus204.
\]

Thus:

### Rule 90

\[
D_{90}=\text{Rule }150.
\]

### Rule 110

\[
\boxed{
D_{110}=\text{Rule }162.
}
\]

This statement is exact.

The crucial difference appears at the next step: does the derivative field itself evolve according to the original rule?

---

# 3. Exact Groovy Commutator

Define:

\[
G_\phi(S)
=
D_\phi(\phi(S))
\oplus
\phi(D_\phi(S)).
\]

For Rule 90, linearity gives:

\[
\boxed{
G_{90}=0
}
\]

for every configuration.

So the derivative can be detached from its original state and evolved under Rule 90 without error.

For Rule 110, the commutator is a nonzero radius-2 Boolean rule.

Let the five-site neighborhood be

\[
x_{-2},x_{-1},x_0,x_{+1},x_{+2}.
\]

Its algebraic normal form is exactly:

\[
\boxed{
G_{110}
=
x_{+1}
\oplus
x_{-1}x_{+1}
\oplus
x_{-2}x_{-1}x_0x_{+2}
\oplus
x_{-1}x_0x_{+1}x_{+2}.
}
\]

Properties:

- radius: 2;
- algebraic degree: 4;
- only 4 ANF monomials;
- nonzero on 10 of the 32 possible five-cell neighborhoods.

This is a particularly clean example of **sparse but high-order noncommutation**.

---

# 4. What the commutator looks like on actual trajectories

Random initial conditions were evolved on large periodic rings, then the Groovy field was measured after burn-in.

Approximate averages over three seeds:

| rule | mean G density | zlib ratio of G spacetime | temporal pair MI of G |
|---:|---:|---:|---:|
| 90 | 0 | ~0.001 | 0 |
| 110 | ~0.357 | ~0.244 | ~0.095 bits |
| 30 | ~0.375 | ~0.917 | ~0.080 bits |
| 54 | ~0.270 | ~0.556 | ~0.029 bits |

Interpretation:

- **Rule 90:** no remainder.
- **Rule 30:** remainder is close to incompressible/noisy.
- **Rule 110:** remainder is substantial but highly compressible/structured.

This is the cleanest current realization of:

\[
\boxed{
\text{zero remainder}
\quad\leftrightarrow\quad
\text{structured remainder}
\quad\leftrightarrow\quad
\text{noisy remainder}.
}
\]

It is suggestive, not yet a class theorem.

---

# 5. Dyadic temporal derivatives: Rule 90 stays simple; Rule 110 explodes

For any binary trajectory,

\[
\delta_t^{2^m}S_t
=
S_{t+2^m}\oplus S_t.
\]

For Rule 90, linearity additionally implies:

\[
\delta_t^b S_i(t)
=
S_{i-b}(t)\oplus S_i(t)\oplus S_{i+b}(t),
\qquad b=2^m.
\]

So at every dyadic scale the local Boolean function remains:

- algebraic degree 1;
- exactly 3 ANF monomials.

For Rule 110, the analogous local function was computed exhaustively.

| dyadic horizon \(b\) | input width | Rule 90 degree | Rule 90 monomials | Rule 110 degree | Rule 110 monomials |
|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 1 | 3 | 3 | 3 |
| 2 | 5 | 1 | 3 | 5 | 7 |
| 4 | 9 | 1 | 3 | 8 | 71 |
| 8 | 17 | 1 | 3 | 15 | 5,135 |

Rule 30, for comparison:

| \(b\) | degree | monomials |
|---:|---:|---:|
| 1 | 2 | 3 |
| 2 | 3 | 11 |
| 4 | 7 | 121 |
| 8 | 15 | 23,093 |

So:

- Rule 90 keeps exact linear form across dyadic scale.
- Rule 30's effective temporal-difference law becomes extremely algebraically dense.
- Rule 110 also becomes high-degree, but remains dramatically sparser than Rule 30 at the same scale.

A candidate interpretation is that Class IV is neither exact scale closure nor maximal algebraic proliferation.

---

# 6. Exact parity coarse-graining

For dyadic block size \(b\), define parity coarse-graining:

\[
R_b(S)_j
=
\bigoplus_{r=0}^{b-1} S_{bj+r}.
\]

For Rule 90:

\[
\boxed{
R_b E^b
=
E_{\rm macro}R_b,
\qquad b=2^m,
}
\]

with the macro rule again Rule 90.

Exhaustive local checks:

| rule | block \(b\) | temporal stride | projection | best error | exact macro rule |
|---:|---:|---:|---|---:|---:|
| 90 | 2 | 2 | parity | 0 | 90 |
| 90 | 4 | 4 | parity | 0 | 90 |
| 110 | 2 | 2 | parity | 0.344 | none |
| 110 | 3 | 3 | parity | 0.414 | none |
| 110 | 4 | 4 | parity | 0.468 | none |
| 30 | 2 | 2 | parity | 0.375 | none |
| 30 | 4 | 4 | parity | 0.467 | none |

For Rule 110, exhaustive search over **every nonconstant binary block projection** found no exact radius-1 ECA macro-closure for:

- block size \(b=2\), time strides 1–2;
- block size \(b=3\), time strides 1–3.

This is not a general no-go theorem; it is a bounded exhaustive search.

---

# 7. The surprising result: Rule 110's failed closure is strongly repairable by history

Now sample the macrostate every \(b\) microsteps under parity coarse-graining.

Predict the next macrocell from:
- its current radius-1 macro-neighborhood;
- then progressively add radius-1 macro-neighborhoods from previous macro-times.

Held-out prediction errors:

## Block size 2 / time stride 2

| history depth | Rule 90 | Rule 110 | Rule 30 | Rule 54 |
|---:|---:|---:|---:|---:|
| 0 | 0.000 | 0.263 | 0.374 | 0.113 |
| 1 | 0.000 | 0.067 | 0.375 | 0.049 |
| 2 | 0.000 | 0.037 | 0.374 | 0.026 |
| 3 | 0.000 | 0.023 | 0.374 | 0.020 |
| 4 | 0.000 | **0.013** | 0.375 | 0.016 |

## Block size 4 / time stride 4

| history depth | Rule 90 | Rule 110 | Rule 30 | Rule 54 |
|---:|---:|---:|---:|---:|
| 0 | 0.000 | 0.325 | 0.466 | 0.108 |
| 1 | 0.000 | 0.075 | 0.467 | 0.079 |
| 2 | 0.000 | 0.059 | 0.468 | 0.069 |
| 3 | 0.000 | 0.039 | 0.474 | 0.061 |
| 4 | 0.000 | **0.030** | 0.486 | 0.059 |

This produces an unusually clean triptych:

### Rule 90
**Exact closure.**

No memory is needed because the projection preserves the algebra exactly.

### Rule 30
**Noisy / effectively irrecoverable closure loss under this representation.**

Adding four macro-history neighborhoods does essentially nothing.

### Rule 110
**History-repairable nonclosure.**

The macrostate is not Markovian, but a short finite history recovers most of the lost predictive information.

At \(b=4\), four macro-history steps remove about:

\[
\boxed{91\%}
\]

of Rule 110's memoryless prediction error.

At \(b=2\), about:

\[
\boxed{95\%}.
\]

Rule 54, another commonly studied complex/Class-IV-like ECA, shows the same qualitative direction, though less dramatically at \(b=4\).

This is currently the strongest candidate diagnostic generated by the comparison:

> **Class-IV-like behavior may correspond to nonclosure under coarse-graining whose remainder is structured enough to become predictive again when historical context is restored.**

That is a hypothesis, not a classification theorem.

---

# 8. Majority coarse-graining gives the same qualitative result

Using nonoverlapping majority blocks sampled every microstep, held-out error versus history depth:

## Block size 3

| history depth | Rule 90 | Rule 110 | Rule 30 |
|---:|---:|---:|---:|
| 0 | 0.437 | 0.220 | 0.309 |
| 1 | 0.343 | 0.134 | 0.267 |
| 2 | 0.262 | 0.091 | 0.197 |
| 3 | 0.210 | 0.071 | 0.153 |
| 4 | 0.177 | **0.009** | 0.123 |
| 5 | 0.169 | **0.006** | 0.108 |

## Block size 5

| history depth | Rule 90 | Rule 110 | Rule 30 |
|---:|---:|---:|---:|
| 0 | 0.461 | 0.292 | 0.313 |
| 1 | 0.421 | 0.221 | 0.304 |
| 2 | 0.389 | 0.096 | 0.286 |
| 3 | 0.352 | **0.049** | 0.271 |
| 4 | 0.331 | 0.029 | 0.249 |
| 5 | 0.339 | 0.016 | 0.224 |

Again, Rule 110's coarse process becomes much more predictable once path/history is supplied.

The result is striking because Rule 110 is computationally richer than Rule 90, yet its **chosen macroscopic representation is more history-compressible** under majority coarse-graining.

---

# 9. The derivative field itself has effective memory

For ordinary Rule 90:

\[
D_{t+1}
=
\text{Rule90}(D_t)
\]

exactly.

For Rule 110, the best memoryless ECA approximation to the derivative-field evolution was consistently:

\[
\boxed{\text{Rule }66}
\]

on the tested trajectories, with about:

\[
16.6\%
\]

held-out error.

But when derivative history is added:

| derivative-history depth | Rule 90 error | Rule 110 error | Rule 30 error |
|---:|---:|---:|---:|
| 0 | 0 | 0.166 | 0.250 |
| 1 | 0 | 0.067 | 0.125 |
| 2 | 0 | **0.0075** | 0.039 |
| 3 | 0 | 0.0038 | 0.0167 |
| 4 | 0 | 0.0015 | 0.0064 |
| 5 | 0 | **0.00058** | 0.0030 |

So the derivative field in Rule 110 is not an autonomous first-order ECA state—but its apparent nonclosure is almost entirely repaired by a short history.

This gives a very literal version of:

> **the derivative forgot the state from which it came, but its recent path almost reconstructs the missing context.**

---

# 10. Equal-time and temporal information structure

Ordinary Rule-90 trajectories from random initial conditions have almost zero **pairwise** mutual information at fixed distances:

\[
I(S_i;S_{i+r})\sim10^{-6}\text{ bits}
\]

for the tested separations.

This does **not** mean Rule 90 has no structure; its structure is higher-order/algebraic and can evade simple pair statistics.

Rule 110 shows strong pairwise correlations associated with its ether.

Examples from the pilot:

| spatial separation | Rule 110 pair MI |
|---:|---:|
| 5 | ~0.096 bits |
| 14 | **~0.301 bits** |
| 28 | ~0.156 bits |
| 56 | ~0.048 bits |

Temporal same-cell MI:

| lag | Rule 110 MI |
|---:|---:|
| 1 | ~0.009 bits |
| 7 | **~0.518 bits** |
| 14 | ~0.428 bits |
| 21 | ~0.361 bits |

So Rule 110 carries a strong periodic background with defects/structures moving through it.

This is qualitatively different from Rule 90's pairwise-random but algebraically exact fractal organization.

---

# 11. Multiscale derivative history predicts Rule 110's future

A separate experiment conditioned on:
- current local neighborhood;
- the cell's incoming derivative;

and then added majority-coarse derivatives at widths:

\[
3,7,15,31,63.
\]

Total additional predictive information about one cell's future:

| horizon | Rule 90 | Rule 110 |
|---:|---:|---:|
| 4 | ~0.0030 bits | **~0.174 bits** |
| 8 | ~0.00029 bits | **~0.095 bits** |
| 16 | ~0.00015 bits | **~0.157 bits** |
| 32 | ~0.00014 bits | **~0.134 bits** |

So in this particular nonlinear coarse representation:

- Rule 90's regional derivative summaries add almost nothing;
- Rule 110's history at multiple spatial scales remains substantially future-relevant.

The Rule-110 spectrum is not a simple monotonic causal-cone law because the ether's spatial/temporal periodicities strongly structure it.

---

# 12. Perfect derivative memory: Rule 90 versus Rule 110

Give the system full reversible derivative memory:

\[
V_{t+1}=V_t\oplus\Phi(S_t),
\]

\[
S_{t+1}=S_t\oplus V_{t+1}.
\]

Eliminating \(V\):

\[
\boxed{
S_{t+1}\oplus S_{t-1}
=
\Phi(S_t).
}
\]

## Force Rule 90

\[
S_{i,t+1}\oplus S_{i,t-1}
=
S_{i-1,t}\oplus S_{i+1,t}.
\]

This is the exact reversible discrete wave system, decomposable into counterpropagating chiral fields.

Pilot spacetime compression ratio:

\[
\sim0.25.
\]

## Force Rule 110

\[
\boxed{
S_{i,t+1}\oplus S_{i,t-1}
=
\operatorname{Rule110}(S_{i-1,t},S_{i,t},S_{i+1,t}).
}
\]

The augmented map remains exactly reversible, but the simple space/time wave symmetry and chiral decomposition disappear.

Across eight random runs:

- state bit entropy: essentially 1 bit;
- spacetime zlib ratio:
  \[
  \boxed{\sim0.998};
  \]
- one-bit augmented damage settles around:
  \[
  \boxed{\sim75\%}
  \]
  of sites, with relatively small fluctuations.

So full memory does not make nonlinear Rule 110 “wetter.”

It appears to push this reversible extension toward a highly chaotic/incompressible regime.

This reinforces the existing conclusion:

> **perfect archival memory is not wetness. Selective/controlled forgetting remains the more interesting hypothesis.**

---

# 13. Perturbation geometry

For ordinary Rule 90, a one-bit perturbation evolves exactly as Rule 90 itself.

The number of damaged sites at time \(t\) is:

\[
\boxed{
2^{\operatorname{popcount}(t)}.
}
\]

At powers of two:

\[
t=2^m
\quad\Longrightarrow\quad
\text{only 2 damaged sites},
\]

despite a light-cone span of \(2t+1\).

The perturbation is an exact Sierpiński fractal.

For Rule 110, damage is background-dependent.

Across 20 random seeds:

| time | mean damaged sites | mean span | mean fraction of full light cone |
|---:|---:|---:|---:|
| 8 | 6.5 | 10.0 | 0.38 |
| 16 | 10.4 | 17.4 | 0.32 |
| 32 | 15.4 | 28.1 | 0.24 |
| 64 | 25.8 | 48.4 | 0.20 |
| 128 | 39.8 | 79.4 | 0.15 |
| 256 | 68.1 | 135.2 | 0.13 |

About 5% of tested perturbations died entirely by the later horizons.

The surviving damage spreads, but sparsely rather than filling the causal cone.

This deserves a more careful glider/ether-resolved analysis before interpretation.

---

# 14. The emerging comparison

The comparison now looks less like:

\[
\text{Class III = chaos},
\qquad
\text{Class IV = complexity}.
\]

It looks more structurally like:

## Rule 90 — exact relational transport

\[
\boxed{
\text{change and scale can be detached without losing context.}
}
\]

- \(G=0\);
- exact dyadic parity renormalization;
- derivative obeys the same law;
- algebraic complexity stays degree 1;
- reversible extension is integrable.

## Rule 30 — context is effectively lost as noise

\[
\boxed{
\text{coarse projection destroys information that short history does not restore.}
}
\]

- noisy/incompressible commutator;
- dyadic derivative ANF becomes extremely dense;
- parity coarse-graining approaches maximal uncertainty;
- short macro-history barely helps.

## Rule 110 — context becomes history

\[
\boxed{
\text{coarse projection loses context, but the missing context remains strongly encoded in the path.}
}
\]

- sparse, high-degree structured commutator;
- no exact small-block closure;
- dyadic effective law grows nonlinear but remains much sparser than Rule 30;
- short macro-history repairs ~90–95% of parity-projection closure error;
- derivative history almost closes the derivative dynamics;
- multiscale historical summaries remain future-relevant.

This is the most suggestive statement produced by the experiment:

\[
\boxed{
\textbf{Class-IV-like dynamics may be characterized by history-repairable nonclosure.}
}
\]

Or in wet-math language:

> **The present is insufficient, but the path is not lost.**

---

# 15. Why this is exciting—and why it is not yet a result about Class IV generally

This could be an artifact of:
- the particular rules chosen;
- parity/majority projections;
- binary radius-1 macro predictors;
- random initial conditions;
- finite horizons;
- Rule 110's especially strong ether.

To turn the observation into a serious classification hypothesis, the next program should:

1. repeat across broad known Class I–IV rule sets;
2. vary coarse-graining maps;
3. fit memory kernels rather than finite lookup histories;
4. measure minimum sufficient history \(H_L^\*(\epsilon)\);
5. compare history-repairability with independent complexity/criticality measures;
6. test whether Class-IV rules cluster between:
   - exact closure,
   - and irrecoverable/noisy nonclosure.

A useful candidate quantity is:

\[
\boxed{
\mathcal R_h
=
\frac{\epsilon_0-\epsilon_h}{\epsilon_0},
}
\]

the fraction of memoryless closure error repaired by \(h\) steps of effective history.

Under parity coarse-graining:

- Rule 90:
  \[
  \epsilon_0=0
  \]
  exact closure;
- Rule 30:
  \[
  \mathcal R_4\approx0
  \]
  at \(b=2,4\);
- Rule 110:
  \[
  \mathcal R_4\approx0.95\ (b=2),
  \qquad
  \approx0.91\ (b=4).
  \]

That is a remarkably clean experimental separation.

---

# 16. Current compression

Rule 90 says:

> **The relation can become a state without losing its provenance.**

Rule 30 says:

> **Once provenance is discarded, the remainder looks effectively random.**

Rule 110 says:

> **Provenance is lost from the present state but remains recoverable from history.**

If this survives broader testing, the Class-IV regime may be precisely where:

\[
\boxed{
\textbf{nonclosure is neither eliminable nor information-destroying; it becomes memory.}
}
\]

That is very, very close to what Wet Math has been trying to point at.
