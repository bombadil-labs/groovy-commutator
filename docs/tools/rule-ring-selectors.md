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

## Using the instrument

Run software checks with `python scripts/test_rule_ring_selectors.py` (NumPy is
needed only by the catalog adapter and its synthetic-array test). The generic
comparison engine uses the Python standard library. It does not change CA
update rules or their JavaScript mirror.

The saved archive must be extracted first; raw NPZ files are not downloaded
automatically. Import an explicit subset, for example:

```bash
python scripts/import_observation_catalog.py \
  --catalog /path/to/extracted/observation-catalog \
  --rules 18 30 54 90 110 126 --candidates 3 27 --metrics 2 6 \
  --widths 7 8 9 --output /tmp/catalog-cases.jsonl
python scripts/rule_ring_selectors.py \
  --cases /tmp/catalog-cases.jsonl \
  --query experiments/rule_ring_selectors/example-query.json \
  --output /tmp/rule-ring-comparison.json --correlations
```

The first command only copies saved measurements. The second is a new
descriptive analysis: it has not been run on those scientific measurements as
part of this infrastructure unit. Its example panel is a usage illustration,
not a frozen scientific selection. Candidate 3 is one-step change; candidate
27 pairs state with two-step change. Metrics 2 and 6 are refinement and
complementary gain; complementary gain is undefined for a single observation,
so those imported values remain null.

A JSONL input row has this shape (values below are synthetic):

```json
{"rule":"54","ring":12,"observation":"my-observation/my-measure","payload":0.25,"context":{"ensemble":"synthetic","floor":1,"cadence":1,"completion":"full-rule","replicate":0},"source":"fixture:54:12"}
```

Only exactly matching observations and context objects form a rectangle. Add
all material experimental distinctions to `context`, including a definition or
version for the observation. The field `source` identifies the original case;
the CLI additionally hashes its case file, query, engine, and plugin files.
Library callers of `compare()` must separately preserve their input files and
implementation identity. Hashing a plugin file does not hash all of its imports.

The query accepts `rules`, `rings`, `observations`, and exact `contexts` lists
for selecting cases. Its four function lists are `ring`, `rule`, `relation`,
and `comparison`; each entry specifies `name`, optional unique `id`, `params`,
and optional required `version`. Defaults are arithmetic ring descriptors,
ECA rule descriptors, signed scalar difference, and change across rings.
Use an empty `rule` list for non-ECA identifiers unless supplying a custom
rule descriptor. Missing requested rings contribute to missing-rectangle
coverage when that observation/context has any selected cases. A wholly absent
observation/context cannot produce a coverage row; selected-case count can be
zero and never means a measured zero response.

For the built-in signed relation, with a<b in the recorded deterministic rule
order and n<m, the change is

```math
[x(b,m)-x(a,m)]-[x(b,n)-x(a,n)].
```

The output also retains both signed differences and the absolute change.
`at_n` and `at_m` are the input relation values; they are not differences
between the raw rule numbers. This is one available relation, not the
definition of every future structural comparison.

## Adding selectors and structural relations

A trusted plugin exports `register(registry)`. For example:

```python
def register(registry):
    registry.add("ring", "same_residue",
                 lambda n, m, modulus: {"equal": int(n % modulus == m % modulus)},
                 version="1")
    registry.add("relation", "shared_labels",
                 lambda a, b: sorted(set(a) & set(b)), version="1")
    registry.add("comparison", "label_turnover",
                 lambda a, b: {"symmetric_difference": len(set(a) ^ set(b))},
                 version="1")
```

Load it with `--plugin /path/to/plugin.py`, then select those names in the query.
`shared_labels` requires list payloads whose label identities are comparable
across cases; it is an API illustration, not a partition-isomorphism algorithm.
A partition or graph relation needs its own justified alignment or invariant.

Ring functions receive `(n,m,**params)`, rule functions receive the recorded
string identifiers `(a,b,**params)`, relation functions receive two payloads,
and comparison functions receive the two resulting relations. Relations may
return any JSON value. Descriptor and comparison functions return dictionaries
of finite numeric values or null. Functions must be deterministic and must not
mutate their arguments. Versions are author-supplied identities, not verification
that the callable implements its advertised semantics.

There is no fixed registry size or observation catalog. Each invocation lists
finitely many functions and parameter sets, with explicit resource bounds.
All relation/comparison combinations in that query are applied to all selected
observations; use separate queries for incompatible payload schemas. Arithmetic
uses exact trial division intended for practical experimental ring sizes, not
cryptographic integer factorization. Whole query results are held in memory;
the comparison budget bounds expansion, not arbitrary input payload size.

## What has been validated

The software tests cover prime support versus prime exponents, n=1, ECA
symmetry descriptors, deterministic rectangle orientation, distinct replicate
contexts, missing/null cases, duplicate rejection, 150 parameterized custom
selectors, a structural payload/relation/comparison, pre-evaluation budgets,
plugin provenance, atomic output failure, and exact synthetic catalog indices.
No scientific signature is selected or confirmed by these tests. New empirical
searches retain the repository's independent protocol and result review gates.
