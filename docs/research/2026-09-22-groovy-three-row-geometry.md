# Three Groovy rows need their temporal seam

**Exact obstruction, 2026-09-22.** Authored by: Codex (OpenAI).
Reviewed by: none. Self-verification uses two implementations, not two reviewers.
[PR #295](https://github.com/bombadil-labs/groovy-commutator/pull/295).

## What we asked

Rule 30's Groovy field has a certified local update when it retains three
ordered observations. Myk asked whether those three times could become spatial
rows of one binary 2D automaton. We tested the simplest unlabelled version:
repeat the three raw rows vertically, include all vertical translations, and
require one uniform rule to advance the history one source step.

We found a collision between entire encoded planes. **No binary 2D CA of any
finite neighborhood can implement this particular encoding and cadence.**
The obstruction is lost temporal phase. It does not rule out representing
history spatially with a marker, boundary, different encoding or alphabet.

## Contract and certificate

Let E be Rule 30 on the full binary integer line, with no burn-in, and
G_j(S)=G(E^j S). Define L(S)(x,y)=G_{y mod 3}(S)(x). Write R for the vertical
translation (RA)(x,y)=A(x,y+1). A candidate Phi must obey

```
Phi(R^p L(S)) = R^p L(ES), for every S and p=0,1,2.
```

There are no row labels, retained source bits or external time feeds. One
Phi update is one source update. This is a period-three plane, not a finite
strip with recognizable boundaries and not an initialized infinite history.

Take the periodically repeated source S=`00010011110`. Its next source row is
ES=`00111110001`. The saved certificate gives:

| Source time | Whole Groovy row, repeated horizontally | Name |
| --- | --- | --- |
| 0 | `00110110010` | A |
| 1 | `01100010011` | B |
| 2 | `00100010010` | C |
| 3 | `00110110010` | A |
| 4 | `01100010111` | B' |

B and B' differ at horizontal coordinate 8 (zero based). Thus

```
L(S)    = (A, B, C), repeated vertically
L(ES)   = (B, C, A) = R L(S)
L(E^2S) = (C, A, B') != R L(ES) = (C, A, B).
```

Translation equivariance and the required update would give

```
Phi(L(ES)) = Phi(R L(S)) = R Phi(L(S)) = R L(ES),
```

but correctness requires Phi(L(ES))=L(E^2S). These differ. Equivalently, the
two inputs R L(S) and L(ES) are exactly the same infinite plane, but their
specified outputs R L(ES) and L(E^2S) disagree at (8,2). Even a nonlocal
deterministic map cannot satisfy both requirements on the phase-saturated
encoded family. An arbitrary off-image completion cannot repair this conflict:
both obligations concern the encoded family itself.

The finite periodic calculation transfers exactly to Z^2: a local CA applied
to an n-periodic source is computed by modular indexing, and equality over
the complete 11-by-3 fundamental tile is equality everywhere. This uses a
periodic witness to refute a full-line claim, not absence on finite rings to
establish one.

## A general necessary condition

The certificate suggests an exact lemma, derived after evaluation. Let O be
any observable of a deterministic source E, and let L_k stack k consecutive
O rows with vertical period k. Suppose a translation-equivariant Phi satisfies
Phi L_k=L_k E. If O(E^k S)=O(S), then L_k(ES)=R L_k(S). Commuting Phi^m
with R shows, for every m>=0,

```
L_k(E^(m+1) S) = R L_k(E^m S).
```

Reading the last row gives O(E^(m+k) S)=O(E^m S) for every m>=0. Therefore:
**a return of one observed row after k steps must lock the entire future
observation sequence into period k.** A return followed by a different
continuation obstructs the raw period-k lift. This is a necessary condition,
not a sufficiency theorem or a classification of all observables.

Our A,B,C,A,B' sequence violates that condition for O=G and k=3. There is no
contradiction with the marked memory-three law: that law reads ordered tuples
and is allowed to distinguish (A,B,C) from (B,C,A). Removing the distinction
between temporal roles is a further quotient, and this quotient is not
compatible with evolution.

## What was evaluated and what was skipped

The [protocol](protocols/groovy-three-row-geometry-20260922.md) was frozen in
[`5fdd928`](https://github.com/bombadil-labs/groovy-commutator/commit/5fdd92803f74cecae8e429a61025506bd0197073).
The search and independent scalar verifier were pinned before evaluation in
[`a354d42`](https://github.com/bombadil-labs/groovy-commutator/commit/a354d42ff678c6528ee3c7840ef3c3bc57d2a6dd).
The [canonical record](../../results/groovy_three_row_geometry_20260922.json)
pins those files and the CA engine by SHA-256.

The search exhausted periods 1..10, then stopped after visiting 498 source
words and 1,492 phase cases at period 11. No pair of n-periodic sources
collides for n<=10 in this search; no minimality claim about nonperiodic
preimages or other representations follows. The whole run took under one second locally.
The planned 13-by-3 stencil evaluation, later periods and radius enlargement
were not run: the whole-plane certificate already rules them out.

The search uses the numpy CA engine. A separate scalar implementation uses
Rule 30's Boolean formula `left XOR (center OR right)` and explicit periodic
indexing to reproduce the saved fields, whole-plane equality and defect.
Targeted tests check the single-trajectory argument and reject corrupted
phase, field, output and defect metadata. No historical result bytes changed.

```
OPENBLAS_NUM_THREADS=1 python scripts/groovy_three_row_geometry.py --check
python -m pytest tests/test_groovy_three_row_geometry.py -q
```

The new result's integrity registration is the unit-specific `--integrity`
and `--check` entry point in the narrow geometry workflow. As in PR #294, the
central registry is left unchanged to avoid dispatching unrelated historical
workflows. The shared integrity check still verifies the previous artifacts;
it does not itself cover this new result. Automatic geometry checks take
seconds and have a three-minute job cap.

## What this leaves open

The strongest conclusion is about **raw, unlabelled, period-three encoding at
one-step cadence**, on every Rule-30 source. It is not a no-2D-lift theorem,
a failure of memory-three autonomy, or a claim about native descendant G.

A sufficient repair exists by construction if the alphabet may grow: pair
each data bit with a fixed marker bit whose rows repeat `100`. The three
vertical marker neighborhoods identify the three roles. The uniform rule
copies G_1 and G_2 into the first two roles and applies the known radius-six
history law in the newest role, while preserving the marker. Reordering the
three visible data rows by their marker roles uses vertical radius one.
To make the rule total, copy the marker bit everywhere and set the data output
to zero whenever the marker neighborhood is invalid or the history lookup is
undefined. This gives a four-state 2D CA preserving the valid marked histories.
This is a construction from the existing law, not another empirical run or a
minimality result; the chosen off-image behavior has no further claim attached.

The next useful design question, if pursued, is whether a specified binary
geometry can carry that temporal seam with a small explicit cost. The existing
six-field and generic encoding constructions are baselines. Another possibility
is to retain a finite strip boundary, which itself supplies positional context.
Neither repair nor an ambient-dynamics experiment is automatically queued.
