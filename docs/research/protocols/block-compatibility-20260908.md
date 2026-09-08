# Protocol: rectangular block encodings in fixed moving frames

Status at writing: design fixed before evaluation. Extend Research 014 while
keeping its 2D ternary interpreter unchanged. No Wolfram class labels enter
the search, scoring, witness selection, or controls.

## Encoding, budget, and frames

For every positive rectangle height m and width w with m*w<=6, choose every
ordered pair of distinct binary blocks A,B. Bit y*w+j encodes row y and
within-block column j. Encode logical bit s_i by placing A or B at columns
w*i through w*i+w-1, with period m in the vertical direction. This is an
injective full-field encoding E; adjacent blocks share their physical edge
neighborhoods. One logical bit costs m*w cells per vertical period.

The fixed fine update is

F(X)(y,x)=X(y+2X(y,x)-1, x+X(y,x-1)+X(y,x+1)-1).

For cadence k=1,2,3, consider fixed horizontal and vertical displacements
u,v in [-k,k] per coarse update. Vertically equivalent displacements modulo
m are identical on this family: retain the representative minimizing
(abs(v),v). Keep all horizontal displacements as physically distinct frames.
Let T_(v,u) shift the field by v rows and u columns. Seek an elementary rule r
such that, for every logical configuration,

F^k E = T_(v,u) E phi_r.

Equivalently Q=T_(-v,-u) F^k obeys Q E=E phi_r. The translation is a change
of observation frame, not a physical repair operation. The laboratory-frame
trajectory is F^(kt) E(s)=T_(tv,tu) E(phi_r^t(s)). Frame speed, block origin,
codewords, cadence and target rule stay fixed throughout each candidate.

## Exact local criterion

For a target block at logical position zero, the moving-frame output reads
the physical interval [u-k, u+w-1+k] at time zero. Its logical dependencies
are floor((u-k)/w) through floor((u+w-1+k)/w). Include the entire central
logical triple [-1,1] as well. Exhaust every assignment to the union interval.
This supplies all relevant causal inputs without imposing a small logical
ring. Local agreement establishes the identity at every logical ring width
and on the infinite line.

For each candidate, distinguish (1) at least one output block outside {A,B},
(2) all output blocks valid but decoded output depends on context beyond the
central triple, and (3) a unique elementary target. Save the complete outcome
matrix in a documented compressed textual form, with deterministic indexing
and a decoder. Keep aggregate counts by rectangle/cadence/frame and sparse
records of every successful candidate. Include deterministic rejection
witnesses for each parameter group and category when present.

## Structural description and controls

Compute each admitted elementary rule's essential inputs and exact Boolean
algebraic normal form. Distinguish constant, single-input, multi-input affine,
and multi-input nonlinear updates. This is a structural description, not a
claim about gliders, sustained computation, universality or Class IV.
Report rules absent from the previous no-frame column result {23,232}, both
literally and modulo spatial reflection and state-complement conjugacy.

Report stationary-frame versus moving-frame results and equal-area shapes.
Width-one, zero-frame results must reproduce Research 014 at heights 1..6.
Check codeword swap, vertical code translation, and combined complement plus
full spatial reflection (which reverses frame velocities and reflects the
lower rule). Do not quotient a within-block horizontal rotation: it generally
changes which logical bits meet at physical block edges. Record raw code
counts separately from symmetry/vertical-period equivalence classes.

## Independent audit and action responses

Recompute every outcome using Boolean truth sets and a horizontally shrinking
causal window, with periodic vertical coordinates. This implementation must
not call the primary array update or reuse its output decoding decisions.
Agreement includes failed candidates, not just selected positive witnesses.

Select, for each distinct admitted rule, the smallest successful encoding
ordered by (area,m,w,A,B,k,abs(u)+abs(v),u,v). Also select the smallest
stationary-frame encoding and the smallest width>1 encoding when present.
Deduplicate candidates; this choice does not depend on trajectory results.

At widths 5 and 7, check four coarse updates for every logical initial state
and compare decoded trajectories with the independent package CA engine.
On width 5, check every length-three word over no-op and logical cell-zero
flip. In the laboratory frame at coarse time t, the physical flip is A XOR B
at the translated block footprint (tv,tu), once per vertical period. Charge
popcount(A XOR B) physical cell flips. Check every intermediate coarse step,
without physically translating the fine state between steps.

The intertwining and matched-action identities then imply preservation of
all finite action words, at the declared frame/cadence, by induction. They do
not imply resilience to an isolated fine-cell defect or automatic recovery
of unknown code phase; Research 014 already separates these questions.

## Records and interpretation

Save parameters, full indexed outcomes, census, successful encodings, rule
signatures, witnesses, source/protocol hashes, independent audit totals,
finite trajectory checks, and a reproducible summary/figure. Existing fixed
interpreter functions are imported with their source hashes. No engine
change is part of this experiment.

Any success is bounded to this code family, cell budget, time budget and
frame search. Any exclusion is likewise bounded; there is no all-height
claim for width>1 in this unit. General CA simulation through encoding and
rescaling is established background (see Research 014's references), not a
new concept claimed here. Label deductions or additional tests devised
after the census as follow-ups. Keep the boundary question parked and the
remainder-feedback law open unless explicitly tackled in a later unit.
