# Same visible present, different futures: what the bond layout kept

**Bounded sampled oscillator result and exact finite transfer null.**
We trained two copies of a 16×16 oscillator grid on stripes pointing the
same way, one with one cycle across the grid and one with three. We turned
off the drive and set their visible phases to the **same exact array**.
The later phases distinguished the two training histories on the frozen
local-alignment score in **31 of 32 paired seeds** when the learned bonds
stayed in place. Shuffling bonds within each axis without changing either
distribution, or retaining only the two directional means, removed that
contrast on this score. This does not mean the ablations erased every
trace of history.

[Issue #333](https://github.com/bombadil-labs/groovy-commutator/issues/333) ·
[Frozen oscillator protocol](protocols/2026-11-21-phase-scramble-333.md) ·
[Frozen CA transfer protocol](protocols/2026-11-21-phase-scramble-333-transfer.md) ·
[Runner](../../experiments/phase_scramble_333/run.py) ·
[Raw per-pair scores and canonical provenance](../../results/phase_scramble_333_20261121.json)

## The oscillator experiment

This is a headless reproduction of the dynamics in [the upstream square-grid
memory tour](https://github.com/project-89/coherence-lattice-alpha/blob/20e50e08fda5b50181cb8c565a41a1e8d950a436/explorable/alpha/sections/06-plm-npd.html#L539-L667),
not a browser/rendering replay. We kept the torus, synchronous Float32
phase state, phase-then-bond update, and live bond learning; a Taylor
ratio for the Bessel functions replaces the upstream approximation.
The two drive fields match their multiset of natural frequencies. Their
nearest-neighbor differences do not match: RMS drive gradient is
sqrt(2) times 0.9 times sin(pi k/16). Different local training stress is
a possible mechanism of encoding, not a remaining drive cue.

Train for 3000 steps. In every continuation set the actually consumed
natural frequency to the same constant everywhere. There is no per-step
noise or other integrator state. Use the same seed-specific fresh phase
array across both histories and all ablations. Verify that the common
untrained bond field yields byte-identical raw phase trajectories on
every tick to 2500. Both resets and shuffle-invariance assertions passed.

The readout takes the cosine of the horizontal phase difference at each
edge, averages down columns, and contrasts Fourier powers at the doubled
training frequencies (6 minus 2). It sees only phases, not bonds or drive
labels; it detects the spacing of local alignment, not restoration of the
literal driven phase field. `Δ` is the score of the three-cycle history
minus that of the one-cycle history within a seed. At the primary horizon
of 1000 steps:

| Retained bonds | Mean Δ | Paired bootstrap 95% interval | Pair concordance |
|---|---:|---:|---:|
| Intact | +0.10796 | [0.08680, 0.12855] | 31/32 |
| Shuffled within each axis | −0.00117 | [−0.00646, 0.00419] | 13/32 |
| Two axis means | +0.00004 | [−0.00770, 0.00681] | 18/32 |
| Shared untrained | 0 | [0, 0] | 16/32 (all ties) |

Intact-minus-shuffle was +0.10913 [0.08708, 0.13050] and
intact-minus-means was +0.10792 [0.08701, 0.12799]. The prespecified
placement gate passed; descriptive horizons 250 and 2500 were consistent
with it. Concordance is paired ordering, not single-trial classifier
accuracy. The intervals are descriptive percentile intervals, not
simultaneous intervals. On the orientation control at 1000 steps,
balanced accuracy was 100% for intact, within-axis shuffle and means;
50% for global shuffle and untrained.

**The secondary readout prevented an overclaim.** Direct unit-complex
phase power told a different story at 1000 steps: contrast +0.04101
intact and −0.08826 with just the two axis means (descriptive, no gate).
The compressed field still carries history for at least a different
phase readout. Placement is needed to reproduce the strong *specified*
alignment contrast under these ablations, not shown necessary for
decoding all spacing information. We did not prove indefinite memory,
optimality of a decoder, natural attainability of the imposed resets,
or anything about the upstream physics.

## The transfer to Groovy

We checked the existing left-copy gated rule transport on a six-cell
ring: fixed alternating 18/126 rule field, all 64 starting visible rows,
two training updates. Four pairs had the same attained visible present
and the same number of 126s. **Zero of four split on the next visible row**.
Shuffle/reset recovery rates are not applicable. The full scalar update
and repo implementation agreed across the enumerated domain. These are
naturally reached matched states; the lack of a split at this fixed
horizon is not a theorem about other initial fields, rings or times.
No adjustment or continuation is indicated by this unit.

## Replay and review

From repository root with Python and NumPy 2.3.5 (the replay environment):

```sh
python experiments/phase_scramble_333/run.py --fixtures
python experiments/phase_scramble_333/run.py --evaluate /tmp/phase333-osc.json
PYTHONPATH=src python experiments/phase_scramble_333/transfer.py > /tmp/phase333-ca.json
python experiments/phase_scramble_333/package.py /tmp/phase333-osc.json /tmp/phase333-ca.json > /tmp/phase333-packed.json
cmp /tmp/phase333-packed.json results/phase_scramble_333_20261121.json
python scripts/check_result_integrity.py results/phase_scramble_333_20261121.json
```

The independent reviewer checked frozen oscillator implementation
`6a883dea2dfb53ea9ee487158534e22bbae766b2`, reran seed 11 alone and the
batch of seeds 9–12 (all raw-derived scores and the batch's raw baseline
hash exact), and recomputed all summary fields from the full raw score
arrays (maximum discrepancy 1.11e-16). For transfer implementation
`1e0dcd764652045d0a59aea962ab56a669190d8f`, replay was byte-identical and
a separate scalar enumeration confirmed the four pairs and zero splits.
