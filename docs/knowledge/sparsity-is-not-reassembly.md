# Fewer active cells need not mean spatial reassembly

For a single logical pulse in the exact Rule-90 strip, at fine time t=2n,

$$
\text{changed cells}=2^{1+\operatorname{popcount}(n)},\qquad
\text{horizontal span}=4n+2.
$$

The count follows from the binary factorization of Rule 90's shift polynomial;
each logical one changes two strip cells. The extremes of the pulse move apart
at every coarse update. At fine ticks 30 and 32, the changed-cell count falls
from 32 to 4 while the horizontal span grows from 62 to 66 columns.

Thus cancellation creates recurrent sparsity across an expanding spatial
extent. It does not establish a bounded returning object or spatial fold-in.
This exact example motivates measuring support geometry alongside activity
counts. See [the longer experiment](../research/2026-09-08-defect-fates.md).
