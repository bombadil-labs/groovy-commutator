# Independent census: the asymptotic-closure gate is broad, not discriminative

**Evidence:** independent all-representative census supplied by Fable/Claude and
imported verbatim from the user-provided result JSON.  
**Recorded by:** GPT-5.6 Sol (OpenAI), 2026-10-07. **Independent implementation:** Fable/Claude.

The bounded scaling unit in
[asymptotic closure scaling](2026-10-07-asymptotic-closure-scaling.md)
reported that Rules 54 and 110 passed a frozen finite-panel gate under the
nonoverlapping block-2 parity observer. The gate required:

1. at widths 16 and 18, the safe-forgetting reserve \(R=n-H_\infty\) to lie
   strictly between Rule 30 and Rule 184; and
2. \(h_*(18)>h_*(14)\).

Fable independently reimplemented the same measure and reproduced the
published 54/110 values exactly. Fable then ran the broader census that the
original protocol deliberately stopped short of.

The raw supplied result is preserved as
[the imported census](../../results/asymptotic_closure_fable_census_20261007.json),
with a compact derived summary in
[the census summary](../../results/asymptotic_closure_fable_census_summary_20261007.json).

## Specificity result

The census contains 88 canonical ECA representatives at widths 12, 14, 16 and
18.

The reserve corridor alone passes for

\[
55/88
\]

representatives at both widths 16 and 18.

Adding the repair-depth growth condition leaves

\[
\boxed{41/88}
\]

representatives, a base rate of about 47%.

The 41 passers break down as:

| repository class | passers |
| --- | ---: |
| I | 2 |
| II | 30 |
| III | 5 |
| IV | 4 |

All four Class-IV representatives in this canonical census pass, but so do 37
non-IV representatives. The condition is therefore not a useful Class-IV
discriminator in its present form.

## Rule 62 is the critical matched control

Rule 62 (Class II) nearly shadows Rule 110 on the two primary coordinates:

| Rule | \(h_*(14\to18)\) | \(R(16)\) | \(R(18)\) |
| ---: | ---: | ---: | ---: |
| 62 | \(4\to5\) | 0.5290 | 0.5954 |
| 110 | \(4\to6\) | 0.5385 | 0.6059 |

The safe-forgetting reserve sequences are nearly indistinguishable over the
available widths. Thus the amount and scaling of required history do not by
themselves explain the dynamical distinction between these rules.

This makes 62 versus 110 a better next comparison than the extreme 30/184
anchors: hold predictive-compression geometry approximately fixed and ask what
the newly necessary distinctions **do**.

## Correction to the theorem target

The earlier note proposed as a possible theoretical target a nonvanishing but
subextensive reserve \(R(n)=o(n)\).

The supplied census makes that target poorly motivated for Rule 110 on the
available widths. Its reserve increases by roughly 0.067 bits per added two
cells over \(n=12,14,16,18\), consistent on this short sequence with an
approximately positive reserve density rather than an obviously subextensive
quantity.

No asymptotic law is inferred from four points. The correction is narrower:
**subextensivity is no longer the preferred theorem target.**

## Disposition

The original frozen gate remains a valid, reproducible bounded observation.
Its interpretation is downgraded:

> **The corridor is a broad necessary-condition-like geometry under this
> observer, not a discriminator.**

The next experiment should control for that geometry rather than threshold it
again. In particular, compare matched Rules 62 and 110 using the algebra of
situated change / Groovy transport inside the exact predictive refinement
tower.
