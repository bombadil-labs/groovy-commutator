# RECONSTRUCTED protocol — selective predictive persistence × spreading / stress

**Status:** reconstructed 2026-09-17.  
**Historical protocol SHA-256 cited by report:** `bd3b231e541f15ac8afac21cff0fac52845a74f01ddf06b749579293ea2c8cd2`  
**This file does not claim to match that hash.**

## Shared frozen candidate

The surviving report states that the candidate was frozen before the fresh primary simulation:

\[
S=\max(0,R_{w=7})\max(0,M_{h=8}),
\qquad
\mathrm{select}\iff S>0.20\land\alpha_{512}>0.50.
\]

`R` is the exact selective-retention statistic inherited from the 2026-09-15
independent Class-IV program:

- take a seven-bit core block `b` and its two immediate external bits `e`;
- evolve the same seven sites one ECA step under the fixed external bits;
- let `p_e(b)=log2(number of seven-bit predecessors producing that same seven-bit output)`;
- condition the uniform reference mean only on the first two and last two core bits;
- residual = boundary-conditioned reference ambiguity minus `p_e(b)`;
- standardize visited mean residual by the uniform standard deviation over all `(e,b)`;
- zero-variance rules receive `R=0`.

`M` is the exact held-out local-history predictive gain inherited from that program:

- at one spatial site, `C` is the current bit;
- `H` is `C` plus eight older bits;
- `Y` is the next bit;
- split the six independent trajectory seeds into folds 1–3 and 4–6;
- in each direction, estimate `P(Y|C)` and `P(Y|H)` on the training fold with
  Jeffreys 0.5 smoothing per output;
- evaluate cross entropy on the held-out fold;
- predictive gain is `CE(C)-CE(H)`;
- `M` is the mean gain over the two train/test directions.

The disturbance coordinate is

\[
\alpha_{512}=\log_2\frac{\bar d(512)}{\bar d(256)},
\]

where `d(t)` is single-bit perturbation support diameter and the report states
96 trials per condition/rule = 16 origins × 6 burned seed states. The same
burned states feed `R`, `M`, and disturbance spreading.

The 88 minimum ECA representatives under reflection/complement conjugation are
the finite rule domain. Conventional 54 and 110 are the primary positive
families; disputed 41 and 106 are reported separately. Two radius-2 mechanism
controls were also present: `radius2-correction` and `radius2-pure-shift`.

## Important reconstruction limit

The exact six fresh RNG seed values used for each 2026-09-16 condition have not
been recovered. The exact local definition of the radius-2 rare-correction
challenge has also not been recovered. The surviving numerical rows for both
radius-2 controls are preserved in the evidence and reconstructed canonical
JSON.

Therefore this file is a reconstruction of the frozen scientific contract, not
the original protocol bytes. It MUST NOT be represented as matching the
historical SHA-256 cited by the report.

## Stress conditions

Run the already-frozen candidate without retuning at extreme densities:

| id | width | density | burn | scored transitions |
|---|---:|---:|---:|---:|
| S1 | 2069 | 0.1 | 2048 | 512 |
| S2 | 2099 | 0.9 | 2048 | 512 |

Each condition uses six independent fresh seeds (exact historical seed values
unrecovered) and 16 perturbation origins per seed.

These are robustness/stress checks, not additional independent positive rule
families.
