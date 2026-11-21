# Pre-evaluation appendix: transfer to existing Groovy rule transport

Companion to issue #333. Separate from the oscillator test, with its own
frozen design and no reuse of oscillator outcomes. Use the existing
`step_gated_diffusion` model in `src/groovy/nonuniform.py`, base revision
`b7dae73753ae4910f5373422d4dd76635c24e6bc`: update each visible bit from
its local ECA rule; each old live bit copies its left neighbor's rule
and each old dead bit keeps its own rule. Six cells, periodic boundary,
anchored bit coordinates, same initial mask (18,126,18,126,18,126), all 64
binary initial visible rows. No external drive. Evolve two steps and group
histories with identical visible rows and identical counts of Rule 126
at time 2. Use all unordered pairs of distinct initial rows within each
group, including pairs with identical attained full state. No rotation
quotient or parameter sweep.

Read out the entire visible row one update later. Count how many pairs
actually split naturally and retain the lexicographically first split
witness (starting rows, both attained rule masks, and both futures).
A natural split in a same-count group certifies that current visible row
and rule counts do not determine even the next visible row in this finite
family. If zero split, report zero (or no eligible pairs) and stop.

For the naturally splitting pairs compare full attained masks (exact by
construction), a uniformly random independently shuffled mask for each
history keeping its count (enumerate all distinct arrangements), and a
shared reset to the original alternating mask. Count the fraction of
cases in which both **specific labeled natural future rows** are replayed
correctly, not merely whether the ablation generates a new difference.
For the shuffle report the exact mean of the per-pair product of replay
probabilities; the shared reset produces the same next row in each
history and cannot replay both where they differ. This comparison uses
off-trajectory interventions for ablations, not for the original witness.
It is the causal-retention comparison only, not an endogenous Groovy jet,
a Class-IV test, or a new CA model.

Check scalar lookup plus transport against repository implementation on
the exact time-0 to time-3 domain, including shuffled one-step states.
Separate oscillator study and transfer conclusions. Do not infer new
follow-on scope.
