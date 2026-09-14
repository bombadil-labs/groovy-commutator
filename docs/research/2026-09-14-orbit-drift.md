# Long temporal cycles separate into shape recurrence and spatial drift

Status: exact finite enumeration for Rules 110 and 54 on the periodic binary ring of size 14; no claim about other ring sizes.

Authored by: Codex (OpenAI), Myk's dimensional-lift session, 2026-09-14. Reviewed by: independent Codex agent `orbit_drift_review`, prospective Gate 1 and independent scientific reproduction; final exact-head Gate 2 and integration are tracked in [gathering #245](https://github.com/bombadil-labs/groovy-commutator/pull/245).

The reported long cycles are real. After identifying rotated copies of a pattern, Rule 110's period 91 reduces to a shape period of 13, and Rule 54's period 112 reduces to 16. In each case seven shape repetitions restore the original position. Six temporal cycles represent three families under translation and time advance.

This separates two sources of a long period. The factor 13 in Rule 110 survives the removal of spatial drift; the factor 7 counts the positional return. That is a useful distinction for a future arithmetic census, but this one ring does not establish a prime-distribution law.

## Fixed question, provenance and reconstruction

Myk approved a narrow annotation of the two reported Rule 110 period-91 cycles and four Rule 54 period-112 cycles in the supplied Fable brief. The brief `Pasted markdown(4).md` has SHA-256 `d954a378b92a280c8978a3e43c2c80839d30f67770dbdf2386701adfd99d7e22`. It supplied period counts but no raw cycle states; workspace and main-repository searches did not locate the raw data. We therefore reconstructed only the two 16,384-state graphs, preserving every recovered cycle while restricting drift annotations to the six specified targets.

The [frozen protocol](protocols/orbit-drift-20260914.md) received [independent prospective Gate 1](https://github.com/bombadil-labs/groovy-commutator/pull/245#issuecomment-5672111663) at `bffe131ff1ef3cbb59f07cc00aa738fa1bd29271`. Its review record was committed at `90ad79eeb09384fa15cf30e48cc3819e129afe0e`. The [implementation](../../scripts/orbit_drift_14.py) was pinned at `3d8a5eae255ef8da1a1f1a679889d5891244d037` before evaluation. No protocol deviation, outcome-driven retuning, additional rule/ring census, halo test or lift construction occurred. Implementation and evaluation remain separate commits in [sub-PR #246](https://github.com/bombadil-labs/groovy-commutator/pull/246).

Bit i of an integer is cell i; the ECA output is bit `4*left+2*center+right` of its rule number. The vectorized repository engine uses a flattened roll, so each source word receives its own two periodic padding cells before batching; the updated padding is discarded. Every successor is compared with an independent literal scalar neighborhood computation. Indegree pruning removes transients; the remaining cycles are saved in forward temporal order, beginning at their smallest integer state.

Both complete reported spectra match exactly:

| Rule | Period → number of temporal cycles | All cycles | Periodic states |
| --- | --- | ---: | ---: |
| 110 | 1→1, 7→2, 12→7, 14→1, 21→2, 91→2 | 15 | 337 |
| 54 | 1→1, 4→49, 112→4 | 54 | 645 |

## What the annotations measure

Let p be the least ordinary temporal period, and d the least positive spatial shift fixing the state. Define translation by $(\tau_a S)_i=S_{i+a\bmod14}$: positive a moves the visible pattern toward decreasing cell indices. Let q be the first positive time when the state becomes any translation of itself, and choose the unique a in $0\leq a<d$ with $E^qS=\tau_aS$.

For these periodic states,

$$p=q\,\frac{d}{\gcd(d,a)}.$$

The exact annotations are:

| Rule | Canonical state integer | p | d | q | a modulo d | Signed a | Positional repetitions | Translation family |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 110 | 125 | 91 | 14 | 13 | 12 | −2 | 7 | 125 |
| 110 | 143 | 91 | 14 | 13 | 12 | −2 | 7 | 125 |
| 54 | 39 | 112 | 14 | 16 | 10 | −4 | 7 | 39 |
| 54 | 57 | 112 | 14 | 16 | 4 | +4 | 7 | 57 |
| 54 | 78 | 112 | 14 | 16 | 10 | −4 | 7 | 39 |
| 54 | 114 | 112 | 14 | 16 | 4 | +4 | 7 | 57 |

The two Rule 110 cycles are translations of one another, allowing a temporal offset. Rule 54 has two such pairs with opposite signed shifts. Each target has full spatial period 14; these are not repetitions of smaller spatial words. All p, d, q and a values were checked at every temporal phase: 630 phases in total. Full cycles and each first-q-step witness are in the [raw cycle record](../../experiments/orbit_drift_14_20260914/run/cycles.json); the [CSV](../../experiments/orbit_drift_14_20260914/run/annotations.csv) gives the compact table.

Signed a is a sampling offset. Physical displacement toward increasing indices has the opposite sign. On a periodic ring, a is known only modulo d; these measurements do not identify a unique unwrapped particle velocity.

## Why the factorization holds

Translation commutes with E. On a periodic orbit, the spatial stabilizer is constant: any symmetry of S also fixes its successors, and advancing back to S proves the reverse inclusion. Thus every temporal phase has the same d.

The orbit under the map on translation classes has least period q. Consequently every ordinary return time is a multiple of q. Equivariance gives $E^{jq}S=\tau_{ja}S$. This equals S precisely when d divides ja. Its least positive solution is $j=d/\gcd(d,a)$, giving the formula. This argument applies to periodic orbits of any translation-equivariant deterministic map on a finite ring; it is not specific to these two ECAs.

It also explains the pairing. The distinct translations of a single temporal orbit split into $\gcd(d,a)$ temporal cycles. The intersection of its temporal orbit with the translations of a fixed phase has $d/\gcd(d,a)$ states. All three target families therefore have exactly two temporal cycles. Counting their members as six unrelated examples would overstate the evidence.

## Relation to lifting and arithmetic

For an injective one-step lift L satisfying $HL=LE$, induction gives $H^tL=LE^t$. Hence $H^t(L(S))=L(S)$ if and only if $E^t(S)=S$. Primitive temporal periods are preserved on the image. Computing these source periods therefore answers their temporal-period question for any faithful lift whose domain contains them. This run does not establish such a native local lift at ring size 14, and off-image states may have additional cycles.

Preservation of q and a needs a further condition: the lift must respect the spatial translation action being quotiented, without additional identifications arising from lifted-axis shifts. Injectivity and temporal commutation alone preserve p; they do not justify treating every higher-dimensional translation quotient as identical.

The natural next statistic for the proposed prime-orbit investigation is the joint record $(q,d,a)$, with rotation-related cycles grouped. At N=14 the Rule 110 family retains q=13 after drift removal, whereas Rule 54 retains q=16. Both remain dependent on the selected ring size. Whether 13 persists as N changes, or instead reflects an interaction constrained by the ring, is untested. The wider census, additive baselines and Witt-ring investigation remain future work.

## Verification, runtime and preserved account

Three known-answer controls ran before the targets: Rule 170 moving a single 1, Rule 204 fixing a single 1, and Rule 170 moving an alternating word. They check drift sign, zero drift and a smaller spatial period. The author checked all 32,768 successors. A separate [review implementation](../../review/orbit_drift_independent_review.py), importing neither author science code nor the CA library, used explicit bit lists and path visitation to independently reconstruct both complete graphs and every saved cycle. Its [signed execution record](../../review/orbit_drift_independent_review.json) confirms both spectra, all six annotations, every target temporal phase, every spacetime return and the three controls.

The primary driver's measured run took **0.133651 seconds** with **25.969 MiB peak process RSS**, against the fixed 60-second/512-MiB budget. Independent scientific checking took **0.230961 seconds**. These are distinct single-run measurements, not a comparative benchmark. Primary timing covers controls, reconstruction, scalar checking, annotations and intermediate saves; interpreter/import startup and final serialization lie outside that interval. The [execution metadata](../../experiments/orbit_drift_14_20260914/run/execution.json) records Python 3.12.14, NumPy 2.3.5, UTC times, source hashes and the implementation pin.

The [canonical account](../../results/orbit_drift_14_20260914.json) hashes the sources, raw evidence, reviewer record and [saved-data verifier](../../scripts/verify_orbit_drift_14.py). Automatic CI checks only those hashes and accounting of saved sequences/rotations; it performs no CA update or graph enumeration. Those checks do not independently establish that the supplied sequences are complete CA cycles: the local author and reviewer enumerations supply that evidence. The unchanged original scientific implementation and prior lift caches are preserved.

To check the saved record without running science:

```bash
python scripts/check_result_integrity.py results/orbit_drift_14_20260914.json
python scripts/verify_orbit_drift_14.py
```

For an explicitly requested local reconstruction, use the pinned implementation and a fresh output directory. Compare cycles and annotations semantically because timings vary. The independent reviewer script also runs locally; it writes its review record, so preserve the committed record before any new review run.
