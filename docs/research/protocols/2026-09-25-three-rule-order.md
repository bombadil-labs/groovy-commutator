# Frozen check: order beyond cyclic phase

**Frozen before evaluation.** Inspected main `95570ba142edebb7db466ceb88f6d600da8db868`.
The two-rule phase theorem proves that `B∘A` and `A∘B` have identical
periodic-cycle counts on each finite ring. It does not compare permutations
of three rules that are not cyclic rotations. We test whether the distinction
can be witnessed without an all-rule census.

- **Fixed rules:** ECA 30, 54 and 110, selected because each has appeared as
  a project example. Let `A=E_30`, `B=E_54`, `C=E_110`.
- **Fixed comparison:** `C∘B∘A` versus `B∘C∘A`, i.e. swap the second and third
  slots with the first fixed. These are not cyclic rotations.
- **Domain:** every binary state on periodic rings of widths 4, 6 and 8.
- **Primary endpoint:** complete number of cycles of each least period for
  each stroboscopic map and width, computed by exact functional graph
  enumeration. Stop at width eight; no widening to force a positive.
- **Secondary endpoint:** whether the two maps agree at every source state,
  and one explicit differing source witness if not.
- **Prediction:** no sign prediction; both agreement and disagreement are
  informative. An unequal cycle count would show that the two-rule
  order-invariance does not extend to arbitrary three-rule permutations
  for these rules. Equal counts would only be a selected finite negative.
- **Verification:** independent scalar LUT enumeration of each transition
  and cycle count against the vectorized implementation; no asynchronous
  job, randomness, parameter fitting or cross-rule search.
- **Action:** regardless of result, do not launch an unrestricted three-rule
  search on its own. Ask what independently chosen task benefits from the
  difference; if none, park this line. Keep a known cyclic rotation as a
  positive check of the exact theorem.
