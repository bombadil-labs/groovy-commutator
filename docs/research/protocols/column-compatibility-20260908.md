# Protocol: invariant column encodings under the fixed 2D interpreter

Status at writing: construction and tests defined before enumeration. This is
a restricted compatibility search, not a Class-IV scoring study. Keep the
2D ternary interpreter from Research 012 fixed. Do not fit the higher law,
decoder, or action dictionary to individual trajectories.

## Objects and target

For binary fields X(y,x), define the synchronous radius-one update

F(X)(y,x) = X(y + 2X(y,x) - 1, x + X(y,x-1) + X(y,x+1) - 1).

Choose two different binary columns a,b of height m. Define E(s)(y,x) to
be a[y mod m] when s[x]=0 and b[y mod m] when s[x]=1. This defines a full
infinite 2D field (or a vertically periodic cylinder) for every 1D state.
Overlapping neighborhoods share actual cells; no independent table is forced
into each neighborhood. The decoder P recognizes a or b in each full period.
The representation budget is m physical cells per logical bit per vertical
period, with no auxiliary channel or external clock state.

For cadence k in {1,2,3}, require

F^k E(s) = E(phi_r(s)) for every binary 1D state s,

where r is one fixed elementary rule. Enumerate all possible r; a successful
encoding uniquely determines r because a differs from b and every input
triple is tested. Constant-output rules remain controls. Intermediate fine
ticks may leave the encoding; validity is required at each sampled k-th tick.
No horizontal drift or additional blocking is allowed in this first test.

This is a family of 1D organizations inside a fixed 2D CA, with one logical
degree of freedom per column. It is not a fully free 2D state space or a
recursively closed dimensional ladder. Storage of a whole lower rule table
in every neighborhood is not required by this encoding.

## Finite-height census

Enumerate every ordered distinct pair (a,b) at heights 1 through 6 and each
cadence. Test all 2^(2k+1) horizontal causal windows. Distinguish:

1. an evolved column outside {a,b};
2. evolved columns in {a,b}, but different decoded outputs for the same
   central triple under different outer context;
3. exact compatibility with an elementary rule.

Save one row per pair/cadence, including failure counts, induced rule when
present, and a deterministic first local witness. Count raw encodings and
primitive vertical periods separately. Swapping codewords conjugates the
lower rule by bit complement. Vertical translation preserves the rule;
complement plus vertical reflection is accompanied by horizontal reflection
of the lower rule. Check these transformations rather than treating symmetry
copies as independent evidence. Report lower-rule reflection/complement
orbits; load no Wolfram class labels.

## All-height graph test

Each vertical position has one of four row types: the pair (a_y,b_y),
encoded as a_y + 2b_y. Thus type 0 is constant zero, type 1 complements
the logical bit, type 2 copies it, and type 3 is constant one.

At cadence k, an output cell depends on 2k+1 neighboring row types and
2k+1 neighboring logical bits. Exhaust all 4^(2k+1) vertical words and
all 2^(2k+1) horizontal windows. For a proposed lower rule r, a vertical
word is allowed exactly when the output equals its central row type
applied to r's output, for every horizontal window.

Make a directed graph whose vertices are words of length 2k over four
row types and whose edges are allowed overlapping length-(2k+1) words.
A periodic encoding exists iff a directed cycle contains a variable row
type (1 or 2); a cycle containing only constants would have a=b and is
excluded. Test this by strongly connected components and a variable-center
edge whose endpoints belong to the same component. Extract a deterministic
cycle witness for every admitted rule/cadence and directly verify its code.

This decision is exact for every finite vertical height under the specified
columnwise encoding and cadence bound. It does not exclude horizontally
blocked encodings, nonperiodic vertical organization, larger cadences, other
2D update laws, or larger alphabets.

## Action preservation and physical damage

Logical actions are no-op and flipping cell zero before each coarse update.
Their physical representatives are no-op and XORing column zero with a XOR b.
These act within the encoded family. Charge popcount(a XOR b) physical flips
per vertical period. Once the intertwining identity is established, induction
gives preservation of every finite word of these matched actions and updates.

For direct finite checks and damage measurements, select all successful
primitive codes with height <=3, plus the lexicographically first successful
code for each (rule,cadence) in the finite-height census. For any rule/cadence
admitted only by the all-height graph, add its extracted cycle witness.
Deduplicate literal (m,a,b,k,r) tuples. Selection does not use damage results.

On rings of widths 5 and 7, enumerate all initial states. Verify four coarse
updates after no-op and after the matched flip. On width 5, also verify every
length-three word of the two actions, including every intermediate coarse
state. Separately flip one physical cell at (y,0), for each row y. At times
0 through 4 coarse ticks, count whether the full field is in the code family,
equals the undamaged evolution, or equals the matched-flip evolution. Preserve
cases that reenter the family as well as persistent damage. These are finite
damage-response measurements; matched action preservation is not automatic
error correction or resilience to arbitrary physical perturbations.

## Independent checks and records

- Compare the vectorized 2D update against the previous scalar patch
  interpreter on all 512 local patches and deterministic complete small grids.
- Compare induced 1D evolution against src/groovy/ca.py.
- Check graph decisions against every finite-height successful code and
  against independent shrinking-window evaluation of extracted cycles.
- Check direct finite trajectories, action words, and declared symmetries.
- Retain rejected-window witnesses, graph cycle witnesses, exact parameters,
  script/protocol hashes, aggregate damage records, and a reproducible figure.
- Include constant and vertically repeated identity-column controls. Do not
  equate passing with complexity, universality, or a dimensional fixed point.

The method is motivated by the established use of block encodings and time
rescaling in CA simulation; our particular fixed interpreter and periodic
column restriction define the experiment. Background: Delorme, Mazoyer,
Ollinger, and Theyssier, [Bulking II](https://arxiv.org/abs/1001.5471).
Any interpretation or extra analysis chosen after results must be labeled
as a follow-up rather than part of this frozen search.
