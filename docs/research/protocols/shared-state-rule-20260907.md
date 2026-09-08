# Shared states and rules: frozen protocol

Frozen before evaluation, 2026-09-07. Motivated by the user's eight-bit state/rule identification and eight-neighbor 2D extension. No novelty, irreducibility, or agency claim is a primary outcome.

## Encodings

An eight-bit pattern x has bit i at ring cell i. A permutation p decodes rule bit k as pattern bit p[k]. Identity, all eight cyclic shifts, all eight reflected shifts (identity counted once), and eight additional unique permutations from NumPy default_rng(20260907), in draw order, give 24 encodings. These are encoding interventions, not independent physical samples. Spatial relabeling with the dynamics conjugated is a separate exact control.

## Coupled ring

All 65,536 pairs z=256*r+s, r,s in 0..255. E_p(r,s) applies the elementary rule decoded from r to s on an eight-cell periodic ring. Update simultaneously: s'=E_p(r,s). Three modes: frozen r'=r; mutual r'=E_p(s,r); derivative r'=s XOR s'. Derivative is an eight-bit pattern subsequently decoded using p. No sequential updates. Build full functional graphs for all 24 encodings and three modes. Report image size, fixed points, cycle count, recurrent states, maximum period, maximum transient, largest basin, recurrent rule-change fraction, and nonzero joint commutator fraction. Joint D(z)=z XOR F(z), G(z)=D(F(z)) XOR F(D(z)); this is a 16-bit fixed-map diagnostic, distinct from applying a time-varying rule while silently keeping D fixed. Save graph hashes and cycle-length histograms. Validate base stepping against groovy.ca, mutual swap symmetry, frozen-encoding conjugacy, independent orbit traversals, and graph accounting.

## Eight-neighbor 2D selector

Eight bits ordered N, NE, E, SE, S, SW, W, NW; center is bit 8. Rule bit k = neighbor p[k]. Input address q=4*W+2*C+E (horizontal) or 4*N+2*C+S (vertical). Next center = neighbor p[q]. This is a fixed nine-input Boolean rule; derive and save its 512-output table. All 40,320 permutations, both axes: enumerate exact local tables; report number of distinct tables, output-one counts, essential input counts and algebraic degree. These are not arbitrary nine-input rules. Every output copies a surrounding bit, hence uniform zero and one are fixed; copying is not conservation of total population.

For the same 24 selected encodings and both axes, enumerate global graphs on 3x3 and 4x4 periodic grids (512 and 65,536 configurations). Report the same graph statistics except rule-change fraction. These are finite-size results only. Independently check all 512 local inputs for selected encodings with scalar evaluation and validate a 90-degree conjugacy by rotating both the address axis and the rule-position mapping. This distinguishes a coordinate change from changing just the encoding. Inspect paired seed traces only for illustration; graph results are exhaustive. No unbounded scaling or Class-IV classification.

## Interpretation and reproducibility

The shared finite space ensures closure by construction, not discovery. A fixed deterministic finite graph has one successor per complete state and eventually cycles: any branching must be explicitly introduced or refer to inverse images/partial observations. Compare encoding sensitivity before assigning physical meaning. Same-time rule extraction is an exact local-rule factorization, not proof that the representation is useless or that memory is the only route to interesting dynamics. Save scripts, parameters, hashes, complete aggregate tables, checks, and a Research note; update knowledge records. Any unplanned extension must be labeled post hoc.
