# Is there a bounded adaptive source recoder for the erased-distinction frontier?

Open, and open in a specific, bounded way. For the declared block-3 / cadence-3
one-defect frontier, a deterministic adaptive rail-selector carrying at most
`m <= 4` hidden proof states and asked for exact equality through macro-horizon
`t <= 6` is the terminal proof grammar this program authorizes. The question is
whether any of the 22 frontier seed languages admits such a recoder.

Current classification, unchanged since 2026-09-10 and reconfirmed 2026-09-14:

| status | seed languages |
| --- | ---: |
| exact bounded negative (no recoder through four proof states) | 14 |
| exactly classified in total | **14 / 22** |
| bounded-recoder certificates found | **0** |
| still undecided (scheduling `pending`, not censored) | 8 |

The eight undecided seeds are rules 122, 154, 161, 164, 166, 180, 210 and 218 on
their frozen ordered pairs. Each stopped during *universal verification* of a
synthesized machine, not during synthesis, so the machine grammar does not need
enlarging to continue — only the verification backend.

## Scope and limits

`0` certificates is a statement about 14 exactly classified seeds plus 8
undecided ones. It is **not** evidence that the eight have no bounded recoder,
and it is not a negative result about them: an unfinished exact computation
carries no verdict in either direction. Four proof states is an authorized
budget, not a privileged bound, and failure through `t <= 6` does not imply
failure at later structural horizons. Nothing here transfers to other observers,
other cadences, or other source languages.

The recovery campaign's own difficulty is likewise not evidence of hard
dynamics: the eight remaining queries have 39 to 54 free source-background bits
and no fully assigned direct-evaluation leaf has yet been reached, which locates
a cost, not an obstruction.

What would change the account: any one of the eight decided either way. A
certificate would be the program's first positive permanence witness and would
need an independent Z3 or separately implemented Boolean audit before
publication; an exact negative on all eight would complete the bounded negative
for `m <= 4, t <= 6` and would let the Program be marked complete/dormant for
this frontier. Until then it stays open.
