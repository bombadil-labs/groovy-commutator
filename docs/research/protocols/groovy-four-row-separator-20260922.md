# One constant separator for three Groovy history rows

Frozen before implementation and evaluation, 2026-09-22.
Authored by: Codex (OpenAI). Reviewed by: none.
Inspected main: `a8dee2d0510f22e7f992a65346e3167cd64ac2dd`.
Preceding result: `1a594b33ccba81958ce70977c0a2cc6ad0328ad4`, PR #295.
Myk requested continued bounded exploration of the temporal-to-spatial move.

## Decision and scope

The raw period-three encoding fails because identical planes can demand
different successors at different temporal phases. Does one additional
constant binary row preserve the needed role information? A positive would
give a binary spatial construction with four rows instead of the earlier
four-state marker-channel construction. A negative closes these two simple
separators; it does not justify a wider encoding census. Existing ordered
memory-three closure and generic lifts are baselines, not new discoveries.

For Rule 30 on every binary source S on Z, let G_j=G(E^j S). Test precisely
L_c(S)=(G_0,G_1,G_2,c^Z), repeated vertically, for c=0 and c=1. Include every
vertical translate. A single binary translation-equivariant 2D CA must send
each translated L_c(S) to the equally translated L_c(ES), at one source
step per update. There is no source track, external label, clock or boundary.
The two separator values define separate candidate rules.

Primary local stencil if needed: x=-6..6, y=-2..1 (52 positions). On the
four-periodic encoding it sees each row once; the same radius-six ordered
G-history law is the computation baseline. A declared default-zero output
on unforced neighborhoods completes any successful partial table. A direct
phase construction may use a larger horizontal marker-detection window if
an exact finite bound requires it; report that cost separately and do not
call it a positive 13-by-4 result without checking that stencil.

## Evaluation order and stop

1. Compute G's radius-two local truth table on all 32 source words. Its
   de Bruijn graph has 16 four-bit nodes and 32 edges. For each output c,
   determine whether the edges labelled c have a cycle. A cycle supplies a
   periodic source with uniform G=c. If acyclic, retain a topological ranking
   and the exact maximum path length: this bounds every run of c in any G
   row, making a constant c separator locally recognizable. Verify all edge
   labels independently with Rule 30's scalar Boolean expression.
2. If a separator is recognizable by that bound, derive its phase decoder and
   combine it with the previously certified ordered memory-three law. Verify
   the decoder's four phases and the known law's complete source cone with an
   independent implementation. Preserve table digests / complete certificates.
   This is a constructive all-source result, not a finite-ring extrapolation.
3. For each candidate not settled by that argument, exhaust source periods
   n=1..12, words in binary integer order, phases 0..3. Stop that candidate at
   the first equal complete input plane with different required outputs. Keep
   full source words, G rows, phases and differing coordinate; verify using
   independent scalar periodic indexing. Such a certificate excludes every
   neighborhood, regardless of the chosen local stencil.
4. Only for candidates still unsettled, exhaust all 2^21 source words and all
   four phases for the 13-by-4 stencil. The oldest three G fields have source
   radii 2,3,4, so 21 bits cover all 13-column neighborhoods and the center
   of G_3. Record an explicit conflicting pair or the entire forced table's
   ordered digest plus a regenerable implementation. A negative only excludes
   this stencil; a consistent table proves closure on the full source family.
   Independently replay a positive with unpacked source-cone arithmetic.

Budget: 120 seconds of scientific evaluation and 2 GiB per invocation. Stop
at the first decisive result for each of the two candidates. Label every
skipped stage with its reason and every cap as unresolved. No other rules,
separator formulas, depths, radii or timing models are queued. Replays follow
the same bounded contract. Preserve the preceding raw-three-row evidence.

## Costs and interpretation

Report four stored binary cells per source column versus three for the raw
history and six for the two-channel marker baseline. Charge initialization
of the three G rows, static separator storage, reads, successor computation,
and maintained writes explicitly. Finite horizontal period is a certificate
construction tool, not the target domain. Do not claim speedup, optimum over
all binary encodings, ambient behavior, isotropy, native-G closure or physics.

No directional prediction is registered. The possible forbidden-run argument
is a proposed sufficient criterion, not a presumed property of Rule-30 G.
Record a general quotient/phase-compatibility criterion if it follows by
proof, marking deductions made after evaluation as such. Extend gathering
PR #295 with separate protocol, implementation and evaluation commits.
