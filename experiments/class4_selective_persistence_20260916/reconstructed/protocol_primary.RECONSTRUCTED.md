# RECONSTRUCTED protocol — selective predictive persistence × spreading / primary

**Status:** reconstructed 2026-09-17 from surviving report and derived tables.  
**Historical protocol SHA-256 cited by report:** `3e5c7efee950261c7e243aa1600951bd57ac163173051a97e7994ab2a3b20325`  
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

## Primary fresh condition

- condition id: `P`
- ring width: **2053**
- initial Bernoulli density: **0.5**
- burn-in: **2048**
- scored transitions for retention/history: **512**
- trajectory seeds: **six independent fresh PCG64 seeds; exact values unrecovered**
- spreading trials: **16 origins × 6 burned seeds = 96**
- spreading readout times: **256 and 512**
- thresholds: `S > 0.20` and `alpha_512 > 0.50`
- no threshold, feature, width, history depth, or positive family may be retuned after seeing P.

## Domain and controls

Score all 88 symmetry-representative ECAs plus:
- radius-2 rare-correction mechanism challenge (definition unrecovered; output rows survive),
- radius-2 pure shift (historical orientation/implementation unrecovered; output rows survive).

Primary label policy:
- primary positives: 54, 110;
- primary negatives: inherited undisputed Class I–III representatives;
- 41 and 106: disputed, descriptive only.

## Declared interpretation boundary

Passing is evidence only for the finite 54/110 core phenotype under this
protocol. It is not a universal definition of Wolfram Class IV and is not a
generalization-accuracy estimate.
