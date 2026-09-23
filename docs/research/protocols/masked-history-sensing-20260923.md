# When can visible history reveal a hidden cell?

Frozen 2026-09-23 against main `69c9121c627b15952d57b179a1bc6b0c95ccb29a`.
Authored by Codex (OpenAI). Reviewed by: none.

## Decision

Test a rigorous fragment of the proposed sensing/inpainting idea: a known
observational gap can hide a distinction needed for a fixed task, while later
visible CA history may reveal it. If the fixed task is already decidable at
time zero, stop; if it becomes decidable after a short history, report exact
conflict witnesses and observational cost; if not, preserve that bounded
negative without widening the horizon or source domain. This is a sensing
experiment, not an intervention, a HAVOK/SLAM implementation, an auditory
model, or a performance claim. The simple baseline reads all 12 bits once.

## Fixed contract

- Hidden clean source `s` is one of the 52 distinct states in the integrated
  prediction/repair domain: the four rotations `V` of `(0011)^3` plus each
  one-bit injury. These are possible *physical* source states. The physical
  system evolves unperturbed under synchronous Rule 54 on a periodic 12-cell
  ring. Bit `i` is cell `i`.
- Independently, one addressed cell `m` is erased from the *observation*, not
  from the physical state. The address is known. The same address is erased
  at each snapshot; all other 11 cells are read without error. Each of the
  12 choices of `m` is checked on every source, with equal source-mask weight.
- For `h` in `{0,1,2}`, the observation `O_{m,h}(s)` consists of `m` and the
  ordered visible words of `s,E(s),...,E^h(s)`. No image-generation prior or
  stochastic corruption is assumed. An observation fiber contains all
  permitted sources giving the same `O`.
- The task output is `T(s)=1[E^4(s) in V]`. The first measurement precedes
  that endpoint, and even `h=2` leaves two unobserved CA steps. The other
  task is full source reconstruction `R(s)=s`; these costs must not be
  conflated. On this ring the prior result has `T(s)=1[s in V]`, but verify
  it again before evaluation.
- A task is exactly answerable for an observation if its label is constant
  across the observation fiber. Reconstructing the source requires a singleton
  fiber. Count distinct conflicting fibers and source-mask cases in them for
  each `h`; also give the first lexicographic witness `(m,s,s')` for each
  conflict type, its source values and labels, and whether a later visible
  snapshot splits the pair. Report per-mask first successful `h`, or `>2`.

The fiber criterion is an exact finite identifiability result: a deterministic
decoder cannot give two different labels for the same observation, whereas a
constant label on each fiber defines a decoder. Test both `T` and identity,
including ambiguity that persists at the two-step cutoff. This theorem does
not establish recovery of an arbitrary clean sound from unknown noise.

## Costs and procedure

Charge 11 observed bits per snapshot, `(h+1)*11` physical bit reads per
source-mask case, plus the known mask address if it is transmitted (four
bits, or free only when the fixed sensor location is shared in advance).
Retaining all words needs `(h+1)*11` bits; recording a single Boolean task
answer needs one bit after inference. Model use requires `h` full 12-cell CA
updates and a Rule-54 specification, versus a direct 12-bit source read at
time zero. No online-memory, circuit-minimality, runtime or energy advantage
is claimed. Count 52*12 source-mask cases; run no all-rule sweep, new target
selection, noisy-channel optimizer, or horizon beyond two.

Implement enumeration and a separate scalar audit using
`groovy.ca.apply_rule_int`; cap each at 30 seconds. Pin protocol and code
before evaluation. Preserve source hashes and all frozen predictions. A
resource cap means `not_evaluated`, never a scientific negative.

## Predictions before evaluation

- P1: at `h=0`, at least one fiber contains an intact stripe and a damaged
  state requiring different `T` outputs; full state is not reconstructable.
- P2: `h=1` removes some but not all `T`-conflicting source-mask cases.
- P3: `h=2` makes `T` answerable for every source-mask case.
- P4: there is some `(m,h)` at which `T` is answerable for all sources but
  full source reconstruction is not; this would show a strict task/identity
  difference in the frozen sensor family and may fail.

Any positive result depends on this narrow source domain, known erasure
address, synchronous evolution and chosen task. Inpainting the missing bit,
task prediction and acting on the physical CA remain distinct operations.
