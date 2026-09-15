# Comparing rule relations across ring relations

This is research infrastructure, not a new Class-IV experiment. It implements
Myk's request to make arithmetic and other selectors extensible rather than
choosing one favored ring-size condition. No new CA trajectories or scientific
shortlist are generated in this unit. Validation uses constructed fixtures and
checks that the previous observation catalog can be imported faithfully.

## Data and comparison contract

An input case has a rule identifier, positive integer ring length, observation
identifier, JSON payload, context object, and source reference. Context describes
the ensemble, floor, completion contract, cadence, sampling, and replicate as
applicable. Cases are only joined when their entire context and observation
match. Width is a separate coordinate. The caller must supply an honest context;
the tool cannot detect an omitted confounder.

The basic comparison uses four cases: rules a and b on rings n and m.
An observation-specific relation R compares the two rules' payloads at each
ring. A comparison C then compares R(a,b;n) and R(a,b;m). For scalar payloads,
the built-in relation is the signed difference b-a; the default comparison
retains the two differences, their change, and its absolute value. Numeric
ordering of rule identifiers has no scientific interpretation. Unordered rule
pairs have a deterministic orientation, which is recorded.

Relation and comparison functions are separately extensible: payloads can be
partitions, graphs, or references to retained arrays. Such payloads require an
explicit domain-appropriate relation; unequal ring sizes do not supply a
canonical alignment of their cells. The core does not invent one.

Rule-pair and ring-pair feature functions are independent extension points.
Initial ring features retain gcd/lcm, divisibility, common prime support,
prime-exponent differences, and configurable divisibility/valuation probes.
Initial rule features provide ECA truth-table Hamming distance and symmetry
orbit membership, explicitly as descriptors rather than dynamical distances.
Users can register more functions and parameter sets without changing the
engine. A query records the selected functions, parameters, and their version
identifiers. Plugins are trusted Python code, explicitly loaded by the caller.

All four case references, relation outputs, comparison scores, and descriptor
values remain in the output. Missing cases are counted, never zero-filled;
undefined numeric values remain null. Duplicate case keys and non-finite
numbers are errors. Different contexts are never silently pooled.

## Correlations and resource limits

Optional Pearson summaries compare numeric descriptors with comparison scores,
separately for each context, observation, relation, and comparison. They report
usable rows, distinct rule pairs and ring pairs, constant/insufficient-data
reasons, and the complete scan size. These are descriptive correlations, with
no IID p-values or classifier claim: pair rows share endpoints, selectors
overlap, and searching many selectors creates selection effects. Confirmation
must hold out appropriate rule families and ring families in a separately
reviewed experimental protocol.

There is no fixed selector count. Each invocation has an explicit finite
comparison budget, checked before relation evaluation, to prevent accidental
quadratic expansion. The engine accepts an iterable of input cases and explicit
rule/ring subsets. Output is written atomically only after a complete scan.

## Existing catalog adapter

The adapter imports saved finite metric arrays from the observation catalog
of 2026-09-15. It preserves each observation/metric identity, exact width,
source hash and array index. Widths 7, 8 and 9 share the exhaustive, pointed,
unburned source ensemble. The developed width-1021 runs are intentionally not
coerced into that context. Importing data does not rerun the original experiment
or supply new evidence for any arithmetic family.

Implementation and executable usage examples will accompany this contract.
