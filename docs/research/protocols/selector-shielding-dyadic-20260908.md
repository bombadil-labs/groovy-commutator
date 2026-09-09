# Selector-shielding dyadic prediction — 2026-09-08

## Status

Post-discovery confirmatory protocol, frozen after inspecting the shielding witness through tick 128 and the row-2 support through tick 128, but **before inspecting the complete row-0/1/2 interface state at tick 256**.

The original 1024-tick dual-kernel validation remains frozen separately. Its monolithic execution exceeded the local Python ceiling; this follow-up does not replace that protocol and does not turn a finite check into an all-time proof.

## Discovery pattern

For the fixed witness

\[
A=\{-5,0\},\qquad B=\{0,1,3,4,6\},
\]

let `C_t` be the coupled physical state and `L_t` the isolated lower-strip reference. Let

\[
\Gamma_t=C_t\triangle L_t
\]

be their difference set.

At dyadic fine ticks `t=32,64,128`, shift horizontal coordinates by

\[
u=x+t.
\]

The complete supports of `Gamma_t` on rows 0, 1 and 2 were found to obey the same finite/periodic template.

## Frozen tick-256 prediction

At `t=256`, predict **exactly**:

### Row 2

\[
\Gamma_{256}^{(2)}=
\{x:u=x+256\in\{2,4,6,\ldots,512\}\setminus\{8\}\}
\cup\{x:u=13\}.
\]

Equivalently the normalized support is every even `u` from 2 through 512 except 8, plus the single odd site 13.

### Row 1

The normalized support is

\[
\{-10,0,1,4,6,11\}
\cup
\{u:12\le u\le508,\;u\bmod8\in\{0,4,6\}\}.
\]

### Row 0

The normalized support is

\[
\{-9,1,6,9,12,14,16,18\}
\cup
\{u:24\le u\le506,\;u\bmod8\in\{0,2\}\}
\cup
\{508,510,513\}.
\]

### Shielding and polarity

Also predict at every directly checked tick through 256:

- the dense and independent sparse implementations agree on the complete coupled field;
- they agree on the complete isolated reference field;
- rows `y>=3` of coupled and reference remain identical;
- every row-2 coupled/reference difference is `0 -> 1`, never `1 -> 0`.

The last condition is the discovered dominance reduction for selector shielding; the exact local proof of that reduction is separate from this finite prediction.

## Acceptance

The prediction passes only if the complete normalized row-0/1/2 supports at tick 256 equal the sets above with no extra or missing coordinates, and all finite-prefix shielding/polarity checks pass.

Any mismatch is retained verbatim. Do not repair the template after evaluation.

## Nonclaims

A pass establishes a fresh dyadic continuation from 128 to 256. It does not prove the template for all powers of two and does not prove all-time shielding. The intended next step after a pass is an exact dyadic induction or finite causal-template proof.
