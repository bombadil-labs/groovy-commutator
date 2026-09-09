# Research CI

Long-running research validation is separated from fast merge checks.

## Fast checks

`.github/workflows/research-checks.yml` runs on research-relevant pull requests and pushes to `main`. It is intended for invariants that finish quickly: imports/compilation, small exact regressions, and smoke executions of newly introduced instruments.

Fast checks may block a merge. Do not put exploratory sweeps or large exhaustive censuses here.

## Frozen research validation

`.github/workflows/research-run.yml` is the CI execution layer for preregistered or otherwise frozen workloads. The intended sequence is:

1. explore locally;
2. freeze and commit the protocol;
3. commit a shardable instrument;
4. let CI evaluate the frozen domain;
5. aggregate and audit exact coverage;
6. retain run artifacts and publish compact summaries.

Research027 representation design was the first CI-native workload. It partitions the 256 ECA rules into eight disjoint 32-rule shards. Every shard records the experiment schema, rule interval, ring width, and source/protocol hashes. The aggregate step rejects gaps, overlaps, mixed schemas, or mixed source hashes before evaluating scientific controls.

Research028 escalates the same pattern to the exact block-3 local repair lattice. Its implementation gate first evaluates Rules `30,54,90,106,110,184` across all 127 canonical binary targets, then fans the complete 256-rule census into sixteen disjoint 16-rule shards. The final aggregate must reproduce the Research026 block-3 closure controls before evaluating the new greedy/global-optimality and diminishing-returns summaries.

## Manual runs

Once a workload is present on the default branch, `research-run.yml` can also be launched through `workflow_dispatch`. Manual confirmatory runs should cite the workflow run and retained artifact in the corresponding research note when that provenance materially supports a published result.

## Design rule

CI is an execution environment, not part of an experiment's scientific definition. Shard boundaries, runner count, and artifact transport must not change the state space, observer family, protocol horizon, or acceptance criteria. Instruments should remain runnable locally with the same command-line arguments used by CI.
