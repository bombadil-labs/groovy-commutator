# One extra binary row makes the Groovy history spatial

**Exact constructive result, 2026-09-22.** Authored by: Codex (OpenAI).
Reviewed by: none. Separate implementations supply verification, not a second
reviewer. Follow-up within [PR #295](https://github.com/bombadil-labs/groovy-commutator/pull/295).

## What changed

The [raw three-row encoding](2026-09-22-groovy-three-row-geometry.md) cannot
advance under a uniform binary 2D rule. Myk asked to keep exploring the repair.
We tested appending exactly one constant row, with no source track or external
row labels. **Both constant values work.**

For either c=0 or c=1, repeat

```
L_c(S) = (G(S), G(ES), G(E^2 S), c)
```

vertically, with every row extending over the full horizontal integer line.
There is a binary 2D CA Phi_c such that Phi_c L_c=L_c E for every Rule-30
source S, and for every vertical translation of the encoding. One new update
equals one source update. A sufficient stencil is x=-6..6, y=-2..1: 13 columns
by four rows. These are ordinary binary cells with one uniform local rule;
temporal roles are not supplied by the caller. No isotropy is imposed.

Each result is a local proof on the complete source cone, so it holds on the
infinite line and, by invariance and induction, through every future step.
It does not depend on extrapolating finite-ring success.

## The ones row: phase becomes locally visible

An exact graph calculation proves that **Rule 30's G field never contains
four consecutive ones**. A run of three is possible. For the radius-two G
map, inspect all 32 five-bit source words. The edges labelled G=1 form an
acyclic graph on the sixteen four-bit overlap states, with maximum path
length three. The saved record includes every edge, a decreasing rank on
every edge, and a path attaining length three. An independent Boolean
calculation checks the complete truth table and graph certificate.

Consequently a constant ones row is recognizable from four adjacent bits.
In every valid four-row neighborhood there is exactly one such separator.
The executable rule in `src/groovy/separator_lift.py` does the following:

1. Inspect x=-1..2 in each row y=-2..1 to locate the separator.
2. For the oldest or middle history row, copy the next row's center bit.
3. For the newest history row, use the existing radius-six, memory-three
   Groovy law on the three correctly ordered data rows.
4. For the separator row, output one.

The declared ambient completion outputs zero if the marker is ambiguous or
absent, or a newest-row history lookup is outside the certified table. That makes a total
binary 2D rule. It preserves the valid encoded family; this completion is
chosen for definiteness, without a claim about its other dynamics.

The marked history table has 164,477 forced keys. Its digest exactly matches
the independently certified table from PR #294. An unpacked Boolean replay
checks the actual constructed local rule on all 2,097,152 source words of
length 21, in each of the four temporal roles: **8,388,608 cases**.

## The zeros row: unique labels are not necessary

G can be uniformly zero, so the zero separator has no analogous forbidden-run
decoder. The frozen search found no phase collision for source periods 1..12.
That finite absence was not treated as a proof. We then exhausted the complete
21-bit source cone for the same 13-by-4 stencil, across all four phases.

Every repeated neighborhood requested the same output. This gives **657,893
forced local keys**, and default zero on every unforced key makes Phi_0 total.
The primary packed and independent unpacked computations produce the same
ordered table digest:

```
1cb4e0c97e4f708af70e7f6538f08930b5b4589c6a92e0367a9f86b5f45a3149
```

The zero-table generator is `zero_table()` in
`scripts/verify_groovy_separator_lift.py`; the original-source cone and row
ordering regenerate its forced assignments. The ones construction additionally
has the directly executable plane update `groovy.separator_lift.step`.

The all-zero encoded plane makes the distinction clear. Its four temporal
phases are indistinguishable, yet all require output zero. **A correct local
update need not recover labels whose ambiguity does not change its output.**
Thus unique phase recovery is a sufficient repair strategy, not a necessary
condition for geometric evolution. Both positive laws answer the same exact
source/cadence question as the preceding three-row negative.

## The stronger criterion

This is a proof deduction after the evaluations, not a preregistered prediction.
Let q(S,p) be any continuous, horizontally equivariant, finite-period vertical
encoding of source state S and phase p; the source E is a CA. A uniform local
update on its encoded image exists exactly when

```
q(S,p) = q(T,r)  implies  q(ES,p) = q(ET,r).
```

Necessity is determinism. For sufficiency, the encoded image is compact and
shift-invariant. The implication lets the continuous successor map factor
through q; the induced map is continuous because a continuous surjection from
a compact space to a Hausdorff space is a quotient map. It commutes with both
spatial translations. Compactness then supplies a finite neighborhood for the
center output. Defining arbitrary outputs on unrealized neighborhoods extends
it to a full binary CA. This criterion is for finite-alphabet encodings with
the stated shift actions; it supplies no minimal radius or free speedup.

The relevant question is therefore whether forgotten distinctions alter the
required successor, rather than whether every temporal role can be named.
The three-row certificate violates this criterion; both four-row laws meet it.

## Representation and computation costs

| Representation | Stored bits per source column | What is established |
| --- | ---: | --- |
| Three named G-history tracks | 3 | Known radius-six history law; temporal slots supplied |
| Three raw vertically repeated G rows | 3 | Uniform one-step binary evolution impossible |
| Three G rows plus a constant row | 4 | Uniform binary 2D evolution certified here, either constant |
| Three G rows plus a marker channel | 6 | Earlier four-state-cell construction |

The four-row construction adds one stored bit per source column, keeps the
binary alphabet and represents phase in the plane. This is not an optimum
over arbitrary encodings, a speedup or a gain in independent degrees of freedom.
For a finite n-column representation:

- **Initialization:** generate the same three G rows as the marked-history
  baseline, then write n separator bits. One straightforward shared computation
  uses E(S)..E^4(S), three evaluations of E on change masks, and nine n-bit XORs:
  7n elementary local-rule evaluations and 9n bit XORs, plus storage writes and
  temporary buffers. This is an explicit upper bound, not a minimum.
- **Rule preparation:** the ones implementation generates its history table
  from 2^21 source words once. The sparse table stores 164,477 39-bit keys and
  one output bit each; the implementation uses uint64 keys and uint8 values,
  about 1.48 MB excluding array overhead. The zero law's 657,893 52-bit keys
  plus output bits use about 5.92 MB in the same array representation.
- **Maintenance/computation:** per source update the ones construction copies
  two n-bit rows, computes one n-bit row with n history lookups, and retains
  the separator. Literal synchronous plane output writes 4n bits, even though
  the separator is unchanged. Marker detection and lookup work must be charged.
- **Local access:** phase detection reads sixteen bit positions (four per
  row). Only the newest role needs the full 39-bit history window; its union
  with marker detection uses at most 43 distinct lattice positions. The simple
  implementation gathers the whole 52-position rectangle at every output cell:
  208n input-bit accesses per plane tick before reuse. No timing advantage over
  named tracks is claimed. The zero law uses one table lookup per output cell
  from that rectangle.

These are stored-state, table and operation accounts. They are not measured
wall-clock performance or a claim that the extra spatial axis is unconstrained.

## Evidence and publication

[Frozen protocol](protocols/groovy-four-row-separator-20260922.md):
[`28475d0`](https://github.com/bombadil-labs/groovy-commutator/commit/28475d0de55491f86299cbcd704c9538d5805db2).
Graph/search implementation before evaluation:
[`628c1ac`](https://github.com/bombadil-labs/groovy-commutator/commit/628c1acffce1fe932125d3fe1252e4038418fa81).
Construction/table verifier before evaluation:
[`19b011f`](https://github.com/bombadil-labs/groovy-commutator/commit/19b011fc7017e428af6bfb502a7be5cbf5b2c562).

The [image and bounded-search record](../../results/groovy_four_row_separator_20260922.json)
preserves the first stage, including its then-pending construction and zero-table
checks. The [completion record](../../results/groovy_separator_lift_20260922.json)
resolves both. These records pin the protocol, implementation and inputs by
SHA-256. All previous canonical bytes remain unchanged. The same narrow CI
workflow runs the sub-minute replays; the central legacy registry is untouched.

Execution-order deviation: the first-stage runner completed the fixed zero-row
periodic screen before implementing/replaying the ones construction. The final
verifier combines the two independent cone checks in one pass. Both separator
values, domains, stencils, caps and decision criteria stayed frozen; no outcome
was used to change a candidate or threshold.

```
OPENBLAS_NUM_THREADS=1 python scripts/groovy_four_row_separator.py --check
OPENBLAS_NUM_THREADS=1 python scripts/verify_groovy_separator_lift.py --check
python -m pytest tests/test_groovy_separator_lift.py -q
```

The frozen two-candidate question is complete. Larger encodings, other source
rules, a native-G tower and ambient pattern searches are not part of this
result. The next decision is what operation on the spatial history would
justify studying a particular geometry or off-image completion.
