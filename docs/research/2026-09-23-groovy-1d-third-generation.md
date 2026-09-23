# A third recursive G exists for two explicit 1D chains

**Exact bounded follow-up, 2026-09-23.** Authored by Codex (OpenAI).
Reviewed by: none. [PR #296](https://github.com/bombadil-labs/groovy-commutator/pull/296).

Myk asked whether either of the nonconstant second-generation positives,
Rules 2 and 16, extends another generation. **Both do, for one of the four
fixed rule-choice combinations tested per source.** The successful third
field is nonconstant and has a present-only radius-four update: nine cells
on the same one-dimensional line. The all-zero completion branch fails.

## The exact chain

Retain the definitions and two first-rule choices from the
[second-generation unit](2026-09-23-groovy-1d-second-generation.md):

```
O1 = G_r
O2 = G_F composed with O1
O3 = G_H composed with O2
```

Here F advances O1 and H advances O2 on the fields inherited from original
source rule r. We test whether a local J satisfies
`J(O3(S)) = O3(E_r(S))` for every binary source on the infinite integer line.
Cadence is one synchronous source update, with no burn-in and no temporal
memory. Only this inherited domain is tested in the follow-up.

The earlier result already fixed two first-level choices F: fill unused
local-table entries with zero or with one. For each, this follow-up fixes
the published second-level H (unused entries zero), plus a one-fill
sensitivity alternative. All eight cases were declared before evaluation.

## Results for both mirror rules

The following verdicts hold separately for each source, 2 and 16:

| First update F: unused entries | Second update H: unused entries | Third-generation outcome |
| --- | --- | --- |
| 0 | 0 | No present-only law at any spatial radius; period-7 witness |
| 0 | 1 | No present-only law at any spatial radius; period-10 witness |
| **1** | **0** | **Nonconstant positive; minimum symmetric radius four** |
| 1 | 1 | Unresolved beyond radius four; no periodic witness through period twelve |

The unresolved cases have explicit local conflicts at every tested radius
0..4. This excludes those radii only. It does not establish failure at all
spatial radii, and periodic absence is not a positive result. No bound was
raised after seeing these outcomes.

The successful rules use precisely the previously published pair:

| Source r | First update F | Second update H |
| --- | --- | --- |
| 2 | `0xfcf4ccc4` | `0x010c0c0c` |
| 16 | `0xfca0ffa0` | `0x07000708` |

These are five-input truth-table integers: bit j gives the output for the
five-cell binary neighborhood j, with the leftmost input most significant.
J's 512-position partial truth table is preserved in the canonical result;
filling its unused entries with zero supplies an explicit total 1D rule.
No native G of J, or fourth generation, was evaluated.

For each positive, O3 has minimum symmetric source radius six, with 2,114
one-entries among its 8,192 local source patterns. It is nonconstant and
differs from O2. The radius-four J identity exhausts every **21-bit original
source cone: 2,097,152 words per source**, with separate unpacked replay.
Conflicts at radii 0..3 establish the stated minimum symmetric update radius.
Complete causal support makes the local identity exact on the infinite
line and at every future source step, rather than only on tested rings.

## How the primary zero-fill chain breaks

For source Rule 2 with both missing-entry fills zero, repeat either source
below periodically:

| Original source S | Complete third G field O3(S) | O3 after one source step |
| --- | --- | --- |
| `0011111` | `0000001` | `0000010` |
| `0100110` | `0000001` | `0000000` |

Identical complete observations demand different successors. This is an
all-radius obstruction to present-only evolution, not a failure to find a
small enough neighborhood. The saved record also includes the other three
negative witnesses. Every witness was replayed by applying the three native
commutators directly with scalar periodic arithmetic.

## Verification and boundaries

### Interpretation: one transient, then rigid transport

The following is an algebraic deduction after the evaluations, prompted by
Myk's question about "evaporation". It requires no new experiment and is an
important limit on the significance of the surviving chains.

Rule 2 outputs one exactly on input neighborhood 001. Consequently, two
ones in any updated source row cannot be one or two cells apart: the
corresponding 001 neighborhoods would contradict each other. They are
separated by at least two zeros. On such a row Y, Rule 2 simply copies the
right neighbor, because every one already has two zeros immediately to its
left. Define the left shift by `sigma(Y)[i] = Y[i+1]`. Then, for every S,

```
E_2^2(S) = sigma(E_2(S)).
E_2^t(S) = sigma^(t-1)(E_2(S)) for t >= 1.
```

Rule 16 is the reflected statement with right shift. Every fixed local G
observation, including every composed O_k here, commutes with spatial
translation. Therefore

```
O_k(E_2^t(S)) = sigma^(t-1)(O_k(E_2(S))) for t >= 1.
```

All these inherited traces are rigidly translating after the first source
update. A nonconstant higher G is not evidence of richer long-term dynamics
in this family. Closure on all original sources asks whether the observation
also predicts the initial transient; on the one-step source image, **every
fixed local observation already has the simple shift law**, whether or not
it closes on the full starting domain. The growing all-source update radius
does not contradict this post-transient simplicity. This deduction concerns
inherited fields, not arbitrary states of F, H or J, and not other source rules.

"Evaporation of distinctions" has a precise limited interpretation. Since
`O_(k+1) = G_Fk composed with O_k`, any two sources identified by O_k remain
identified at later generations, once the rule choices are fixed. A later
layer cannot recover lost original-source distinctions. This does not prove
strict information loss at every stage or an entropy-decrease rate.

Nor is it necessarily thinning of one-bits. Under an independent fair-bit
original source at the initial time, the successful branch has expected
one-fraction `280/2048` (13.7%) at generation two and `2114/8192` (25.8%) at
generation three. These expectations follow directly from the saved truth
tables, not a new trajectory experiment. Density can increase while source
information cannot. The useful result here concerns retained distinctions
and transient predictability; additional recursion depth alone would not
establish emergent dynamical complexity.

### Provenance and checks

- [Frozen follow-up protocol](protocols/groovy-1d-third-generation-20260923.md),
  commit [`4c93804`](https://github.com/bombadil-labs/groovy-commutator/commit/4c93804f9dc70031c07a3b4704eac4aca56e1505).
- [Implementation before evaluation](../../scripts/groovy_1d_third_generation.py),
  commit [`8c7559c`](https://github.com/bombadil-labs/groovy-commutator/commit/8c7559cf5b6d34bae2cb662f1f5271eac35eb627).
- [Canonical third-generation result](../../results/groovy_1d_third_generation_20260923.json):
  hashes of both units' inputs and implementations, all F/H tables, observation
  radii and digests, positive J tables, negative witnesses and unresolved cases.

For each of eight cases, direct unpacked evaluation of three nested G maps
on all 2,097,152 words of the unreduced 21-bit source cone independently
checked the composed observation table. Positive closure uses an additional
complete-cone unpacked replay. These are independent arithmetic implementations
within one agent session, not independent scientific review. The fixed caps
were 120 seconds and 2 GiB per invocation, periods 1..12, J radii 0..4 and
a 23-bit maximum source cone for local closure.

```
OPENBLAS_NUM_THREADS=1 python scripts/groovy_1d_third_generation.py --check
python -m pytest tests/test_groovy_1d_third_generation.py -q
```

This answers the requested existence question for explicit 1D chains.
It is not independent of rule completion: a tested choice changes closure
from failure to success at this generation. The two positive sources are
mirror partners, not independent dynamical families. All eight third fields
are nonconstant and differ from their respective second fields; no fixed
point or indefinitely closed hierarchy has been demonstrated. Stop here
unless a further question is requested. Rule 30, memory repairs and spatial
encodings remain outside this follow-up.
