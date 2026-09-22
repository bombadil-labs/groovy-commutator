# Groovy readout: the useful cache does not require the six-field lift

2026-09-22. Authored by Codex. Evidence: algebraic construction and explicit
cost accounting, not a timing experiment or a minimal-circuit theorem.
Independent review is recorded on the gathering PR before integration.

## Question and decision

Does the affine six-field lift earn further work by making the original
Rule-110 Groovy field cheaper to read? It exposes a useful cached expression,
but an ordinary three-track recoding of stored time slices exposes exactly
the same expression. Under a marked-track interface, the six fields are not
needed for this readout benefit. **No-go for a new numerical campaign on this
candidate.** This is not a claim that three named tracks replace the lift's
phase-free binary geometry or recursive synchronization theorem.

The [portfolio survey](2026-09-22-program-survey.md) requested this bounded
design comparison. We use the existing definitions and lift theorem, without
generating trajectories, enumerating rules, or fitting a cost model. There
is no new empirical protocol or measured performance result.

## Common contract

Let H be Rule 110 on arbitrary binary configurations of the integer line.
Write Y=H(X), Z=H²(X), D=X XOR Y, and T=X XOR Z. The target is the original
source field G(X)=D(H(X)) XOR H(D(X)), at source site i and source time t.
It is not the native commutator of a descendant rule.

All representations are initialized from the same X and must advance one
source tick per maintenance step. Stored future slices Y and Z require
preprocessing; they are not free past history. Cost is a vector: stored bits
per source site, bits read per query, physical access geometry, primitive
Rule-110 evaluations, XORs, initialization and ongoing maintenance. We do not
collapse these into a scalar without a workload and architecture.

For the marked-track comparison, an array component/row address is known.
Separate tracks may be packed in a multibit alphabet or laid out as named
binary rows; this is stated access, not a phase-free binary CA implementation.
For periodic-axis encodings, storage means one transverse fundamental period
per source site, not the infinite repetition of that period.

## Exact readout identity

Direct substitution gives, on the entire integer line,

```
G(X) = Y XOR Z XOR H(D)
     = D XOR T XOR H(D).
```

Thus the six-field lift's rows F2=D and F3=T suffice for

```
G_i = D_i XOR T_i XOR f(D_{i-1}, D_i, D_{i+1}),
```

where f is the eight-entry Rule-110 local table. This reads four stored bits,
uses one f evaluation and two binary XORs. With the query anchored at F2,
the four addressed positions have horizontal radius one and vertical offsets
zero and one. The surrounding 3-by-2 rectangle has six cells, but only four
are read. A marked query does not pay to rediscover its row address.

Now store only (X,D,T). This is an invertible pointwise recoding of (X,Y,Z):
Y=X XOR D and Z=X XOR T. It supplies exactly the same four query inputs,
with the same expression, in three tracks instead of six. Its validity is an
algebraic identity for every source configuration, not a finite-ring inference.

## A maintained cache, not a free precomputed answer

The three-track cache remains valid after a source step using

```
X' = X XOR D
D' = D XOR T
T' = (X XOR D) XOR H(X XOR T).
```

Indeed X'=Y, D'=Y XOR Z, and T'=Y XOR H(Z). These are precisely the same
cache definitions for the next source state. A radius-one multitrack update
suffices. One explicit circuit per site forms three neighboring Z bits,
forms Y_i, evaluates f on the three Z bits, and forms D'_i and T'_i:
one f call and six XORs, with Y_i reused as X'_i. These are construction
counts, not optimized lower bounds; copies, writes and communication still
cost resources on a real machine.

Initialization computes H(X) and H²(X), then the two differences: two full
source-rule passes and two XORs per site. It has source dependency radius two.
The two passes impose startup work/latency even though subsequent updates
advance at one source tick per step.

## Constructive comparison, not a universal Pareto frontier

Each row is one explicit implementation; numbers are upper bounds, not minima.
All f calls refer to the same three-input table. Constant table descriptions
are separate from per-site mutable storage.

| Representation | Stored bits/site | One G query: reads; f calls; XORs | Initialization | One maintenance tick |
| --- | ---: | --- | --- | --- |
| Source X | 1 | 5; 5; 5, horizontal radius 2 | None beyond loading X | One f/site, radius 1 |
| Named slices (X,Y,Z) | 3 | 7; 1; 5, horizontal radius 1 | Two source-rule passes | (Y,Z,H(Z)): one f/site plus copies |
| Named cache (X,D,T) | 3 | 4; 1; 2, horizontal radius 1 | Two passes + two XOR/site | One f + six XOR/site, radius 1 |
| Marked period-three necklace | 3 | 5; 5; 5, on the known payload row | Write (0,X,1) | Keep marker rows; one f on payload/site |
| Marked six-field jet | 6 | 4; 1; 2, across D and T rows | Two passes, differences and spatial rails | Maintain the three-track cache plus the two spatial rails and zero row |

For direct source readout, compute Y at i-1,i,i+1 (three f calls), Z_i
(one), and H(D)_i (one). Three XORs form the local D inputs and two combine
Y_i,Z_i,H(D)_i. For named slices, read X and Y at three sites and Z_i.
The jet maintenance row describes a marked-track algorithm: after computing
the new cache, form X'_i XOR X'_{i+1} and 1 XOR X'_i XOR X'_{i-1} for its
rails. It is not the operation count of an optimized native lifted table.

Alternatively, direct G is one Boolean function of five source bits, so a
32-entry table can evaluate it with five reads and one lookup. That lookup is
not a three-input f call: the table grows from eight to 32 bits and its input
wiring changes. This further prevents interpreting primitive f counts alone
as a speedup. No minimal circuit or minimal read neighborhood is claimed.

## The phase-free comparison is a different interface

The [existing theorem](2026-09-17-affine-oriented-lift-theorem.md) gives the
necklace a phase-free binary update with horizontal/vertical radii (1,1),
and the first-floor six-field lift sufficient radii (2,3). The latter's
ambient full-shift stencil has 35 positions. On a valid period-six beam its
first and seventh transverse rows coincide, so an on-beam physical key has 30
distinct mutable cells. These are sufficient neighborhoods, not mandatory
dense-table storage or proven minimal radii.

At an unknown necklace phase, the vertical triple has one or two ones;
majority recovers X regardless of its rotation. Decoding five neighboring
columns therefore gives a constructive G query with 15 binary reads in a
5-by-3 rectangle, five three-input majority operations, and the direct-source
calculation above. It pays decoding rather than receiving a free phase label.

For the jet, the four-read expression presupposes the D/T addresses. The
theorem supplies a local phase decoder, but its work and any additional access
must be charged before comparing an arbitrary-phase query. We have not
minimized that composite decoder/readout. Nor have we turned (X,D,T) into a
phase-free binary code with the same physical stencil. Consequently the table
does **not** prove that the three-track cache dominates every binary phase-free
implementation of the jet, or that the necklace is best for every workload.

## What changed, and what remains open

The operation proposed as a reason to reopen the lift is already available
in a smaller marked cache. Under that interface, the extra rails and marker
do not contribute to G readout; their job is synchronization and geometry.
This separates a real caching benefit from an unestablished dimensional
advantage. None of it supplies a Class-IV discriminator or an asynchronous
implementation.

Do not fund a broad benchmark to re-establish these identities. Reopening
requires an actual consumer whose requirements exclude named tracks or place
a concrete value on phase-free binary locality, plus a matched baseline and
accounting for decoding and upkeep. A strict-geometry decoder optimization
could then be a different justified question; it is not automatically next.
Ordinary source access remains the low-storage baseline. Caching can be useful,
but we have not specified a workload that makes its extra maintenance pay.
The subsequent [repository consumer
audit](2026-09-22-phase-free-consumer-audit.md) found no current downstream
operation requiring the stricter interface, so the application question is
dormant rather than queued for a decoder benchmark.
