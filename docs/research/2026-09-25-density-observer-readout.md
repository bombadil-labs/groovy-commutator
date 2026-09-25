# Density classification: where does the answer reside?

**Status:** prior-art correction and exact interface comparison, 2026-09-25.
Inspected main `5823d46ef2512525b5de72c0afc16dc6c3000d76` after PR #314;
no open PRs/issues. No new empirical evaluation. Reviewed by: none.

## The missing earlier result

The [first calibration note](2026-09-25-density-classification-contract.md)
described Fukś's 1997 staged Rule-184→232 solution. It omitted an important
1996 result by Capcarrere, Sipper and Tomassini: **Rule 184 alone perfectly
classifies finite-ring density under an output specification that reads the
surviving same-symbol blocks instead of demanding homogeneous consensus**.
This changes how we interpret the role of the second rule. The first note's
staged theorem and resource accounting remain true; the suggestion that
composition is necessary to *make the answer exist* was too strong. Rule
232 changes the answer's physical output format and accessibility: majority
cases become homogeneous, while ties remain alternating.

Primary sources: [Capcarrere, Sipper and Tomassini, *Physical Review Letters*
77, 4969 (1996), author's PDF](https://www.moshesipper.com/pubs/density_ca.pdf)
([DOI](https://doi.org/10.1103/PhysRevLett.77.4969)); [Fukś, *Physical
Review E* 55, R2081 (1997), Proposition
4](https://arxiv.org/pdf/comp-gas/9703001); [Land and Belew, *Physical
Review Letters* 74, 5148 (1995)](https://doi.org/10.1103/PhysRevLett.74.5148).
The 1995 impossibility concerns convergence to the majority's **uniform
binary state** under one fixed two-state rule. The 1996 construction changes
the output language; the 1997 construction changes the rule in time. These
are different contracts, not contradictions. None proves that either design
has a resource advantage over counting with global access.

## Shared input and exact output languages

Input: every binary configuration on a synchronous periodic ring of known
length `L≥2`, with a fixed left/right orientation and no intervention after
initialization. Let `N1` be the initial count of ones. The classification
label is `+` if `N1>L/2`, `-` if `N1<L/2`, and `=` if tied (only even `L`).
For comparison, keep this three-way label fixed while varying the *physical
output* and *observer*.

Rule 184 conserves `N1`. Fukś's finite-ring bound says that at
`n=floor((L-2)/2)` no `00` remains for `+`, no `11` remains for `-`, and
neither remains for `=`. Conservation ensures at least one pair of the
majority kind in a strict-majority case. Thus the **whole-ring predicate**

| Label | At the Rule-184 deadline `n` |
| --- | --- |
| `+` | At least one `11`, no `00` |
| `-` | At least one `00`, no `11` |
| `=` | Neither pair; the ring alternates |

already decodes the initial label exactly. Capcarrere et al. independently
give the conservative deadline `T=ceil(L/2)` and prove the corresponding
block-language result. We use Fukś's shorter bound only for the whole-ring
scan and keep the 1996 paper's own deadline for its fixed-port proposal.
We do not equate its `T` with Fukś's `n`.

## Matched observer and resource contracts

| Interface | Dynamical work and control | Observer access and decision |
| --- | --- | --- |
| **Raw count, label only** | No CA updates. A central processor knows `L`, reads all `L` input bits, and keeps a `ceil(log2(L+1))`-bit count plus control. | Returns the three-way label directly. This is the baseline when sequential/global source access is permitted; it lacks radius-one distributed locality. To demand a consensus *configuration*, add `L` writes and a spatial parity origin for a tied alternating output. |
| **184, whole-ring scan** | One 8-entry rule, `n` synchronous radius-one rounds, `Ln` site updates; an observer needs the length-dependent deadline. | Read the `L` bits in the deadline snapshot (or all `L` adjacent pairs), retain two “seen 00/11” flags, and use the table above. A scan is not a one-site local read. Reading `L` bits suffices to form all pairs, including the wraparound pair. |
| **184, one fixed pair over time** | Same single rule, run until `T=ceil(L/2)` before interpreting pair sightings. The 1996 paper states a same-symbol pair of the majority kind cycles through any designated neighboring cells within at most `L-1` additional rounds; a worst-case deadline is `T+L-1`. Charge the corresponding `L(T+L-1)` site updates if all rounds are needed. | Read the same two neighboring cells each round from `T` through `T+L-1`; `11` means `+`, `00` means `-`, and no same-symbol pair by the deadline means `=`. An event detector can stop early on `+/-`; a guaranteed finite tie decision needs a known deadline. This is a local read port, with external knowledge of `L` and time. |
| **184→232, homogeneous-majority output** | Fukś uses `n` rounds of 184 and `m=floor((L-1)/2)` of 232: `L-2` rounds, `L(L-2)` site updates, two 8-entry rules, a length-dependent global switch and endpoint. | The final *whole configuration* is all ones for `+`, all zeros for `-`, alternating for `=`. Given the theorem and the deadline, two adjacent bits at any fixed port distinguish all three outputs (`11`, `00`, or a mixed pair). For odd `L` with ties excluded, one bit suffices. This improves spatial availability of the endpoint output at the price of additional dynamics and control. |

These counts are logical site updates and source-read incidences, not measured
runtime or energy. A distributed parallel CA can have smaller latency than a
serial scanner even with more total work; both access geometry and hardware
must be fixed before saying one is cheaper. If the output is only the label
and global reads are cheap, the raw-count baseline defeats any supposed
computational need for the staged CA. If every cell must *locally carry the
answer* on strict-majority inputs, the scan and the staged program do not
meet the same output contract. A final two-bit read after the staged
endpoint is an observer decoding a promised global output, not a claim
that the fixed port can certify that
promise without the theorem and deadline.

## An exact stopping boundary for clockless tie detection

**Elementary causal-cone deduction, not a result claimed from the papers.**
Suppose a fixed finite-radius CA starts from unmarked binary rings of
arbitrary even length. A designated observer sees only a fixed finite port
and its past, is not told the ring length, and must halt with a correct
three-way answer in finite time on every input. Consider a perfectly
alternating tie ring on which it halts at time `t`. Choose a much larger even
alternating ring and flip one zero to one farther than the CA's radius-`t`
causal cone from the port. The observed history through `t` is identical,
but the second input has a strict one-majority. The observer would halt
with the wrong tie answer. Therefore **absence of a pair, observed for a
finite time at an unmarked fixed port without a length bound, cannot certify
a tie on all rings**. A known `L`, a global scan, an extra length signal, or
a changed promise/task escapes this argument. This says nothing against
local decisions for strict-majority inputs that eventually exhibit a pair.

## Research decision

The answer can reside as a constrained *pattern language* before it exists
as homogeneous cell states. Here the second rule's role is output
amplification, not the initial extraction of the density distinction. The
observer pays for seeing a whole ring or waiting at a local port; consensus
pays for additional evolution and an externally timed switch. That is a
more useful, contract-specific instance of our representation question
than another ECA schedule search.

Close this correction and keep the composition application line parked.
A next empirical unit would need a named physical or biological consumer
that prefers one output contract, plus access, clock, memory and latency
prices. Do not treat the 1996 paper's statement about regular output
languages as a hardware cost comparison, or infer Class-IV behavior,
Groovy-specific utility, or universal problem-solving efficiency.
