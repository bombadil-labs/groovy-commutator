# Is the higher-dimensional commutator fixed by the beam?

Frozen before experimental implementation and evaluation, 2026-09-15.
Authored by: Codex (OpenAI), /root. Protocol review: none at freeze; run authorized by Myk 2026-09-15 through standing Gate 1 approval and the immediate instruction "Let's do it" after the completion-independence audit proposal. Independent result review precedes publication. Local protocol/source hashes preserve chronology; no prospective remote-review chronology is claimed.

## Question and exact symbolic contract

For a fixed finite local binary neighborhood, let P be a partial **flip** rule with forced domain K. A completion chooses one bit u[q] for each unforced physical neighborhood q. It uses the same bit at every occurrence of q; source index, position, phase and time do not enter the local law.

For an invariant beam family B, H(Y) is fixed for every Y in B. Set D(Y)=Y XOR H(Y) and T(Y)=Y XOR H^2(Y). Then

G_H(Y) = D(H(Y)) XOR H(D(Y)) = T(Y) XOR delta_H(D(Y)).

At a cell whose neighborhood q in D(Y) is forced, G=T XOR P(q). At an unforced q, G=T XOR u[q]. Thus each distinct queried unforced key supplies one independent binary coordinate of the joint G field over the entire source family. If there are U such keys, exactly 2^U different joint G fields occur over unrestricted local Boolean completions. Repeated keys create exact equality or complement relations among ambiguous cells. A symbolic constant with u=0 is only a coordinate origin; no completion is selected as preferred.

The test asks whether U=0, and if not preserves the exact symbolic incidence. It does not fit a Class-IV discriminator, claim a causal feedback mechanism or assume G is invariant under recoding. Higher-dimensional G can depend on completion even while the ancestral six-field lift and T are completion-independent.

## Fixed domain and sources

Primary census: every one of the 1,536 archived records: all 256 ECA roots, source rings of widths 7 and 8, dimensions 2,3,4; every source word, longitudinal position and transverse phase. Reuse the immutable six-field archive with SHA-256 766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1. Each record retains its own finite-family partial rule and native neighborhood (radius two on the original line, three on each lifted axis). No lift or source trajectory is resynthesized. Verify original member hashes and archive representatives.

At D2, additionally evaluate the same archived difference configurations against the independently verified full-input D2 partial tables in experiments/beam_discriminator_loop_20260915/round01/tables.npz. Assert inclusion and agreement of each finite table in its full-input table. Report how many formerly free queries become forced. Ambiguity remaining under that full-input table is genuine relative to the declared first-lift full-line contract, witnessed even on a finite periodic source. D3/D4 statements remain relative to their finite source families; unforced there does not mean proven unforced on every infinite-input beam. Do not compare the widths as nested domains or pool them implicitly.

## Computation and retained evidence

Reconstruct exact physical keys for the archived family, obtain its native successors from the pinned flip table, match those successors back into the family, and obtain the second successors by the matched native index. Cross-check the resulting successor indices against independently recovered root words and the elementary truth table. For every difference configuration, reconstruct its physical neighborhoods and compare them with K.

Period-six repetition allows the repeated +3 transverse offset to be omitted in a key without changing equality. If using that compression or interned tuple nodes, preserve enough exact node/physical-key data to reconstruct every queried neighborhood. One keyer must retain its identity pool across the family and its difference configurations; never compare rule-local interned IDs across independent pools. The source batch is not a spatial dimension.

Preserve, per record, the archive member identity/hash, exact pinned keys and outputs, native successor indices, symbolic constants and variable labels for every G cell, exact definitions of every free key, per-state and per-phase summaries, and direct witnesses. Arrays may be losslessly compressed. Atomic per-record writes and hashes permit a documented resume without overwriting completed scientific evidence.

Report fixed-zero/fixed-one/free cell counts, U and the number of distinct free keys per source state; ambiguous-cell occurrences per variable; numbers of variables shared by multiple source states; and counts of cell pairs constrained to equal or opposite G values because they share a free key. Also report whether D(Y) itself belongs to the stored family: global off-image status must not be equated with encountering an unforced local key. Report aggregate results and all per-root values, including 54/110 and the established simple/chaotic controls. No thresholds, class ranking search, completion prior, completion sampling or preferred fill is introduced.

For each record with ambiguity, preserve the first free-key witness and the two completions differing only at that key. Their G fields differ exactly at that key's occurrences; their evolution and six-field encoding agree on the invariant family. For D2 full-input ambiguity preserve the full physical key and its absence from the complete table. For every record, selected deterministic events are also checked with literal scalar 7-by-...-by-5 neighborhoods against the compressed key construction.

## Controls, budget and interpretation

Before scientific evaluation, run small synthetic partial-table controls: enumerate all assignments to a handful of free keys, verify 2^U distinct fields, repeated-key covariance, forced-zero versus unspecified, and the G=T XOR delta(D) identity. These controls are algebraic checks, not new CA findings. For roots 0 and 204, assert fully determined zero G at every audited floor, since the difference family remains in the invariant family. Do not extend that assertion to other constant or affine roots without measurement.

Native family consistency, scalar keys, successor/root recovery and the full-input D2 inclusion checks are mandatory. No choice on a free entry may change H(Y), H^2(Y), T(Y), or the six-field lift for Y in B. Independent review must reconstruct membership and symbolic outputs by a separately implemented key method and verify the counts and explicit differing-completion witnesses; full replay runs outside Actions.

Local primary budget: 20 minutes and 2 GiB process memory, with atomic checkpoints and progress at least once per minute. If the budget is reached, retain completed records and label the rest censored; do not alter the domain or score after viewing results. Author/reviewer verification is separately timed. Automatic CI is compilation and pinned-source integrity only. Preserve all failures and deviations. Archive-wide counts are finite-domain exact; this unit does not prove all-dimensional G transport, arbitrary-parent liftability, preferred ambient dynamics or Class IV specificity.
