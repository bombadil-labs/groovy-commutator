# Protocol: retain the interface and test repeated closure

Freeze before evaluation. Keep the Research018 binary 2D interpreter F,
horizontal alignment, alternating background B(y,2i)=0, B(y,2i+1)=1,
and two-fine-tick cadence. No fitted decoder, new law, class labels, or 3D test.

## Six-bit enlargement W

In each two-column block retain the physical cells (y,x mod 2), in this order:
(0,1), (1,0), (1,1), (2,0), (2,1), (3,0). These six freely variable bits
form a 64-symbol logical alphabet. Keep (0,0)=0, (3,1)=1, and all exterior
rows in B. The decoder reads these six cells; W is injective. This contains
every original adjacent pair V_0(a,b): its six bits are
(1 XOR a, a, 1, 0, 1 XOR b, b). It also contains all F^2 V_0 outputs found
in Research018, including their four interface residual cells.

Exhaust all 64^3 = 262,144 left/center/right symbol triples. The input index
has bits 6*j+v for block j=0,1,2 (left to right) and retained cell v=0..5.
Evolve input rows -4..7 and columns -2..3 twice, shrinking the causal window,
to output rows -2..5 and columns 0..1. Check the ENTIRE output against W's
fixed cells and exterior background, not just its decoded six-bit symbol.
Save valid-input count, every fixed-cell violation count, first failed input
and first witness for each violated coordinate. Save all output words as hex
in input-index order (uint64 little-endian), plus their SHA256 digest.
If W is invariant, this gives its total radius-one update. If it fails,
do not promote the partial readout to an exact coupled logical rule.

## Reachable states from the original pair

Freely variable interface cells might admit states the actual interaction
never produces. Separately exhaust the original V_0 causal inputs through
t=2,4,6,8 fine ticks. Let k=t/2. Enumerate all bits of a_i,b_i for
i=-k..k: input index bits 2*j and 2*j+1 hold a and b at i=j-k.
There are 2^(4*k+2) assignments, respectively 64,1024,16384,262144.
Input columns -t..1+t shrink to 0..1. Input rows -2*t..3+2*t shrink to
-t..3+t, covering every row that can differ from B. No torus is used.

At each declared horizon record the W-valid count, the count with any
change outside the original four rows, every changed exterior/fixed-cell
count, first deterministic witnesses, and the union of affected row bounds.
Save SHA256 of every output packed as uint64 little-endian in input order.
Counts are exhaustive LOCAL causal patterns, not whole-trajectory survival
probabilities. A violation excludes W for actual reachable dynamics; an
absence through eight ticks proves only this bounded statement.

## Independent audit

Commit primary and audit instruments before evaluation. Primary evolution
uses the existing NumPy array-gather update. Audit uses its own encoder and
an explicit Boolean multiplexer with 64 inputs packed into each uint64,
without importing the primary encoder, updater, or validity summarizer.
Compare all output words, counts, and deterministic witnesses for W and
every reachable horizon. Record instrument hashes and total audited fields.

The two tests distinguish unrestricted symbol closure from the actual
reachable subset. Failure is scoped to this six-cell representation; it
does not prove unbounded vertical spreading or exclude other constrained
encodings. Any new representation, all-time argument, or follow-up witness
analysis after the census must be labeled as a subsequent deduction/test.
