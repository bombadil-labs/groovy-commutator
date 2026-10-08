# A concrete on-image Rule-54 J5 evolution transducer

**8 October 2026 · Prospective implementation gate (not a new discovery of factor closure).** [Frozen protocol](protocols/rule54-on-image-transducer-20261008.md); [standalone no-dependency reproducer](../../experiments/jet_full_line_autonomy_20261007/on_image_transducer.py). Results are *same-author numerical implementation tests*, not external review.

## We wondered / we tried / we found

**Wondered:** Can we *execute* Rule54's autonomous five-track jet without building a truth table over the unrestricted 32^13 possible radius-six jet blocks, and without choosing a privileged source when hidden phase makes a preimage nonunique?

**Tried:** Represent the image as a finite labeled de Bruijn **relation**, not a deterministic complete-alphabet CA. Use 14-bit source contexts as 16,384 automaton states. Each of 32,768 overlapping 15-bit source windows gives an edge whose input label is the 5-bit central J5 and whose output is the one-bit A6. The original exact full-line 33,162-path certificate ensures that on *admissible bi-infinite jet inputs*, every accepted source lift produces the same output. No claim of local determinacy holds for arbitrary off-image inputs.

The other four next jet tracks follow the triangular law, with H=Rule54 applied separately to binary tracks:

    (G', Q', R', A4', A5') =
    (H(G) XOR Q, H(Q) XOR R, H(R) XOR A4,
     H(A4) XOR A5, H(A5) XOR A6).

**Found:** This is an executable **on-image nondeterministic transducer with a functional output relation**. Exactly 28 of the 32 single-site five-bit jet letters occur as labels (absent: 9, 18, 21, 23). There are 151 distinct one-site input/output jet-label pairs, but these marginal counts do *not* describe globally allowable sequences or compression.

## A 13-symbol finite-window decoder

To compute A6(0) from an admissible J5[-6..+6], start with all 16,384 source-context states, filter them by 13 successive five-bit input letters, and carry each surviving branch's A6 bit at the center edge. Every compatible finite source patch extends to a bi-infinite source because the source is the full binary shift. The earlier exact radius-six certificate guarantees that all final branches, however many hidden contexts remain, agree on the latched A6 bit. In particular this gives a direct finite local **algorithm** rather than the giant off-image Boolean truth table. A dynamic set of 14-bit context and a single latched bit suffices. This is a constructive implementation derived from the earlier theorem, not an independently proved smaller locality bound.

## Frozen implementation checks

The standalone script rebuilds A0..A6 from the commutator recurrence, checks all 32,768 edges against the triangular next-track law (**0 mismatches**), and independently computes native cyclic source jets for all binary rings n=8,10,12:

| n | Source states | Distinct J5 images | Nontrivial image fibers | Largest fiber | Native/transducer mismatches | Different outputs for same J5 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 256 | 222 | 30 | 4 | 0 | 0 |
| 10 | 1,024 | 1,001 | 21 | 4 | 0 | 0 |
| 12 | 4,096 | 4,050 | 42 | 4 | 0 | 0 |

For 32 **distinct deterministic** period-24 source patterns, every sampled admissible 13-site jet block yielded exactly one central A6 bit, agreeing with native A6. During filtering there were at most **1,408 active source contexts** (maximum across samples); 4..56 candidate contexts remained after the final letter. This does **not** prove anything new about unsampled windows; exact full-line determinacy is inherited from [the prior factor/radius certificate](2026-10-07-jet-full-line-autonomy.md).

**Run:** \`python experiments/jet_full_line_autonomy_20261007/on_image_transducer.py\`. The Python source is self-contained (standard library only), no GitHub Actions long run required. Local artifact SHA-256: \`28810a0b625ddef8b494a235dd1633723acc272aebb03406638c29f29c4089a0\` (verify exact repository copy). GitHub protocol was committed before this execution, but the factor theorem predates it. Nothing has been externally peer-reviewed in this unit.

## Limits and next question

This is **not** a deterministic minimized automaton, an efficient physical realization, an information-rate advantage, or an unrestricted 32-letter CA. Its internal hidden source states are nondeterministic, even when its induced on-image output is unique: *the distinction survives internally but is irrelevant to the next observation.* Further work would need a **costed** comparison with minimized/observer automata and an actual consumer, not arbitrary alphabet minimization. The next independent-review target remains the earlier full-line factor and almost-sure injectivity claims.
