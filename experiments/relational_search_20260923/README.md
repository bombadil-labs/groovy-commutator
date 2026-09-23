# Relational witness-search pilot

The [decision](../../docs/research/2026-09-23-relational-search-decision.md)
and [frozen protocol](../../docs/research/protocols/relational-search-pilot-20260923.md)
define the scope. This is a method benchmark on a known finite answer.
No unrestricted Prolog program search or new CA census is involved.

## Reproduce

Use Python with NumPy and Node 22 or later. From the repository root:

```sh
npm ci --prefix experiments/relational_search_20260923 --no-audit --no-fund
python -m unittest discover -s tests -p test_relational_search.py
python experiments/relational_search_20260923/run.py \
  --implementation-commit COMMIT_CONTAINING_THESE_SOURCES \
  --output /tmp/relational-search-new.json
```

Output paths are exclusive-create. Do not reuse the canonical result path.
The runner records source hashes, runtime versions, all six local trials,
candidate lists, oracle witnesses, every pruning reason and phase/total times.
Each local worker has its own fresh domain and Prolog process; its entire
process group is killed after 120 seconds. OS filesystem caches are not
flushed. Three trials do not establish a portable performance advantage.
RSS fields are Linux `ru_maxrss` in KiB: the Python worker and its terminated
Node child are measured separately, not added into a simultaneous peak.

`--setup-seconds` can record a separately measured package-install duration.
Installation is not part of search time. A null value means it was not
measured, not that installation was free. This environment could not install
native SWI through apt because OS identity switching was restricted; the
pilot uses the official, lockfile-pinned `swipl-wasm` package.

## Optional Jev acquisition

When `TYPESAFE_API_KEY` is available in the process environment, the same
runner performs one additional `jev_ranked` trial. Otherwise it records
`not_evaluated / missing_credential`; no substitute score is generated.
Keep credentials out of files and arguments. No external API runs in tests.

The implementation pins requested model `jev-1.13.0` and records the actual
response model and token usage. It uses TypeSafe's typed Choice endpoint.
The heuristic selects only among at most eight surviving equal-cost candidates.
The exact oracle remains authoritative. Requests omit the historical answer
and rule number; a known encoder can still appear as an ordinary candidate.
At most six requests, 8,000 bytes per request, 20 seconds per request and
180 seconds for the entire arm are permitted. No retries. Any API/choice
error falls back to canonical order and makes the Jev comparison incomplete.
Fallbacks after the request budget are part of the bounded strategy and
recorded separately. Preserve a fresh acquisition as a new artifact; do not
replace a missing-access record with retrospectively acquired evidence.

## What is verified

Python independently checks that Prolog generated all 406 target refinements.
Every witness is validated before insertion. A final audit replays every
witness and rejection, covers every cheaper candidate, checks the successful
encoder with the pre-existing independent metric routine, and reconstructs
the known greedy regret across the full finite interval.

The semantic unit tests use toy data: missing candidates, false future
disagreements, noncolliding witnesses, joint repairs and out-of-tier Jev
choices. They do not rerun the timed benchmark. A canonical result can be
audited without Prolog or an API using
`python experiments/relational_search_20260923/verify.py RESULT.json`;
this takes the existing NumPy audit route. The bounded CI job runs the toy
tests and this saved-certificate audit, never a paid API or timed search.

The objective is uniform-source observation entropy. A five-label encoder
still takes twelve fixed-width bits per four-block row, plus a 24-bit lookup
table. Source-based refreshing retains twelve source bits, performs three
fine updates and four lookups. No autonomous update law is synthesized here.
Both baseline arms use Prolog so their difference isolates witness filtering;
this does not compare Prolog against a native Python grammar or SAT solver.
