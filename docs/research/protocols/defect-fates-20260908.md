# Protocol: longer defect trajectories and certified recurrence

Freeze before evaluation. Continue the fixed 2D interpreter and six-cell
Rule-90 code of Research 015/016. Keep dimension changes, fitted decoders,
Class-IV labels, and remainder-feedback interventions out of this unit.

## Inputs, horizon, and outputs

All 64 block XOR masks, in both vertically periodic and single-block isolated
modes, fine horizon 32. Sample times 0,2,...,32. Logical backgrounds are:

- Every binary word of minimal period p for p=1..4, with each spatial phase
  retained as a different aligned background. Word bit i gives s_i. This is
  22 backgrounds (2+2+6+12), not 22 independent statistical samples.
- Two random cohorts of 16 nine-to-sixty-five-bit extensions each: generate
  the entire 65-bit word s[-32..32] independently with NumPy default_rng seeds
  2026090801 and 2026090802, Bernoulli probability 1/2. Save the actual words.
  These are sampled backgrounds, not an exhaustive longer-horizon statement.

For isolated mode, assess aligned blocks in rows -33..35, columns -32..33.
The required initial causal rectangle is rows -65..67, columns -64..65.
Shrink each dimension by one cell per side per tick. In periodic mode use
three vertical rows with wraparound (exactly the declared repeated system),
the same horizontal input range, and shrink only horizontally. These windows
contain the full possible response support through tick 32. No horizontal
torus or imposed exterior value enters the observation.

Save complete indexed int32 metrics for every mode/background/mask/sample:
response mass, bounding box coordinates, local code validity, and global
status (same, valid changed, outside). Empty boxes use a documented sentinel.
Periodic mass counts one vertical period. Also save per-trajectory response
hashes covering all samples, raw input words, aggregate tables, and witnesses.
Keep isolated and periodic masses separate. The complete geometric response
support, not a fixed-origin crop alone, determines disappearance and recovery.

## Recurrence screen and proof criterion

For each nonempty difference field delta_t, remove its bounding-box translation
and compare exact remaining binary arrays. Periodic mode may translate only
horizontally (vertical displacement fixed zero); isolated mode may translate
both coordinates. Test fine periods p=2,4,6,8 at even sample times, requiring
three successive equal normalized shapes at t-2p,t-p,t, with the same
displacement per period and each component of displacement bounded by p.
Retain the earliest screen match per trajectory, ordered by end time then p.

For periodic logical backgrounds, separately check the full undamaged
background: B_(a+p)=T_v B_a on its complete 3-by-2p_background spatial period,
where a=t-2p. If this identity holds and the complete finite (or vertically
periodic) response obeys delta_(a+p)=T_v delta_a, then the FULL perturbed
configuration obeys X_(a+p)=T_v X_a. Translation equivariance proves recurrence
for every subsequent period. This is a certificate, not extrapolation from
a shape alone. Save the earliest certified match, even if a prior shape match
was uncertified. Random backgrounds get shape screens only; no global
periodicity or all-future certificate is inferred from their finite word.

The search permits only these periods, translations and horizons. Report
no recovery, no screen, and no certificate as distinct bounded outcomes.
Also report first return to the original even-phase encoding when present,
including whether the returning state has changed content.

## Predeclared follow-up on any certified structures

If certificates exist, sort them by background ID, mode, mask and certificate
start time. Keep the first eight distinct signatures, where a signature is
mode, period, displacement, normalized response, and the complete periodic
background tile at the start. No dynamical class or appealing picture enters
selection. Otherwise this stage has no eligible cases.

From each selected certified state, compare no action, toggling its first
active response cell in row-major order, toggling the cell immediately right
of its bounding box at its top row, and both toggles. Periodic mode repeats
actions every three rows; isolated mode changes single cells. Evolve four
certified periods with sufficient causal padding. Measure difference from
the unperturbed certified trajectory, background response, and the pair's
failure of XOR superposition at the final time. A zero difference demonstrates
recovery to that trajectory, not merely recognition by a fitted decoder.

## Independent checks and interpretation

An independent implementation must pack the 64 masks into uint64 Boolean
truth sets and update by an explicit multiplexer, without importing the
primary encoder, evolution function, metric decoder, or recurrence decisions.
Compare every sampled response hash and metric, and independently verify all
reported recurrence screens/certificates. Follow-up trajectories must also
agree with the bitset update, including the unchanged certified-orbit control.
Check the primary undamaged and matched-flip samples against package Rule 90.

Any recovery discovered here is qualified by background, mask and mode. A
certificate proves periodic motion of a complete configuration on its stated
periodic background; it does not establish autonomy across other backgrounds,
logical computation, or a general fan-out/fold-in mechanism. A temporary spread
followed by contraction is measured geometrically before being interpreted.
