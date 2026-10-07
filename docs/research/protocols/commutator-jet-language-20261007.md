# Protocol: symbolic language of the intrinsic commutator jet

**Status:** descriptive exact follow-up, frozen before canonical repository
evaluation on 2026-10-07. The presentation family and reported metrics were
selected after exploratory scratch computation; this is not a preregistered
discovery test. **Serialization amendment:** per-shortest-depth subset summaries
were dropped from the canonical JSON before publication; the decision metrics
remain minimum/median/maximum ambiguity plus exact block counts through length
16. Scratch depth summaries were not used for any conclusion.

**Authored by:** GPT-5.6 Sol (OpenAI). **Reviewed by:** none.

## Question

The intrinsic commutator jet

\[
G,\;Q,\;R,\;A_4,\;A_5,\ldots
\]

rapidly approaches the information content of the microscopic source on finite
rings. That does not imply that the **set of spatial jet configurations** has a
complicated description.

For each fixed jet prefix, the map from the binary full shift to the sitewise
jet symbol is a sliding-block code. Its image is therefore a sofic shift.

This unit computes an exact finite-state presentation of those image languages
for matched Rules 110 and 62.

## Fixed prefixes

Analyze the G-anchored prefixes

\[
J_m=(G,Q,\ldots,A_m)
\]

for \(m=1,\ldots,5\):

- G;
- G,Q;
- G,Q,R;
- G,Q,R,A4;
- G,Q,R,A4,A5.

No additional rules or fields.

## Exact labeled source presentation

For a prefix ending at level \(m\), the largest field has source radius

\[
r=m+1.
\]

Use the binary source de Bruijn graph with states equal to source words of
length \(2r\). Each source edge appends one source bit and corresponds to one
length-\(2r+1\) source word.

Label that edge by the sitewise jet symbol \(J_m\) at the center.

This finite labeled graph presents exactly the image language of the full
binary line under the declared jet block code.

## Deterministic language automaton

Treat every source de Bruijn state as an allowed start and terminal state.

1. Determinize the labeled graph by subset construction from the set of all
   source states.
2. Add an implicit rejecting sink for missing symbols.
3. Minimize the resulting DFA by exact partition refinement.
4. Report accepting-state count, recurrent SCC structure and the largest
   recurrent component.

The minimized DFA recognizes exactly the finite block language of the realized
jet prefix. It is not automatically called a Fischer cover or minimal
bi-infinite presentation; no such stronger terminology is used without a
separate proof.

## Spatial entropy

For the minimized deterministic presentation, form the integer adjacency
matrix counting distinct labeled transitions between accepting states.

Report:

- Perron eigenvalue numerically;
- topological entropy estimate \(h=\log_2\rho\);
- exact allowed block counts for lengths 1 through 16.

Because the source is the binary full shift, \(h\le1\) bit/site. Values
numerically equal to one are reported as "full source entropy to numerical
precision," not as an exact algebraic equality unless independently certified.

## Source-context ambiguity

The subset construction has a direct interpretation: after reading an allowed
jet word, the deterministic state is the set of compatible source de Bruijn
contexts.

Record across all reachable subset states:

- minimum, median and maximum compatible source-context count;
- whether any observed jet word synchronizes to a unique source context;
Block counts through length 16 are retained separately; no per-shortest-depth
subset table is required in the canonical result.

This is context ambiguity for the finite block presentation, not a global
preimage count for a bi-infinite jet configuration.

## Frozen descriptive questions

For each rule:

1. Does the minimal DFA state count stabilize as jet depth increases through
   A5, or continue growing?
2. At which prefix, if any, does the spatial image entropy reach the full
   one-bit source entropy to numerical precision?
3. Does adding higher residual fields reduce compatible source-context
   ambiguity?
4. How do Rules 110 and 62 differ, given the prior finding that their D maps
   are symmetry-equivalent?

No Class-IV classification, threshold or prevalence claim is authorized.

## Hard boundaries

- Rules 110 and 62 only.
- Prefix through A5 only.
- This unit studies one-time **spatial language**, not temporal autonomous
  update of the minimized automaton states.
- A small automaton-state count is presentation compactness, not source
  compression.
- Full entropy is not injectivity.
- Difficulty or growth of a presentation is not claimed as dynamical
  complexity without an independent theorem.

## Planned artifacts

- scripts/experiment_commutator_jet_language.py
- results/commutator_jet_language_20261007.json
- docs/research/2026-10-07-commutator-jet-language.md
