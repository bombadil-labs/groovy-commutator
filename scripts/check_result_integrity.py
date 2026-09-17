#!/usr/bin/env python3
"""Fast integrity tier for canonical result files (added 2026-09-11).

Each canonical JSON records the SHA-256 of the script that produced it and of
every input file it read. This check recomputes those hashes from the working
tree and fails if any differ. What it establishes is provenance coherence only:
a verifier or input edited without regenerating the result is caught in
seconds. It does NOT inspect result content: a result file edited by hand with
its source_hashes left intact passes this check. Result content is guarded by
the full byte-for-byte replay, which the workflows run on any pull request that
modifies the canonical result file, on pushes to main, weekly, and on manual
dispatch (Codex's review of PR #90 pinned this contract down).

Usage: python scripts/check_result_integrity.py [result.json ...]
With no arguments every registered result is checked, and a missing result
fails the sweep the same as naming it explicitly would. (2026-09-12: an
earlier version of this sweep reported a missing registered result as PEND,
for a unit's implementation-only commit registering a result before it was
generated. Codex's Gate-2 review on PR #206 noted that once a unit's
canonical result exists, keeping that allowance lets a future accidental
deletion or rename of an accepted result evade this tier silently. Every
currently registered result exists, so the allowance was removed outright
rather than narrowed; an implementation-only stage that needs to register a
result before generating it should register it only once the canonical run
has actually produced the file.)
"""
from __future__ import annotations
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]

# result file -> {hash key recorded in its source_hashes: path the hash was taken of}
REGISTRY = {
    'results/rule_ring_structure_20260915.json': {'docs/research/protocols/rule-ring-structure-20260915.md': 'docs/research/protocols/rule-ring-structure-20260915.md', 'experiments/rule_ring_structure_20260915/REPRODUCE.md': 'experiments/rule_ring_structure_20260915/REPRODUCE.md', 'experiments/rule_ring_structure_20260915/confirmation-execution.json': 'experiments/rule_ring_structure_20260915/confirmation-execution.json', 'experiments/rule_ring_structure_20260915/confirmation-result.json': 'experiments/rule_ring_structure_20260915/confirmation-result.json', 'experiments/rule_ring_structure_20260915/confirmation-seal.json': 'experiments/rule_ring_structure_20260915/confirmation-seal.json', 'experiments/rule_ring_structure_20260915/discovery-execution.json': 'experiments/rule_ring_structure_20260915/discovery-execution.json', 'experiments/rule_ring_structure_20260915/discovery-result.json': 'experiments/rule_ring_structure_20260915/discovery-result.json', 'experiments/rule_ring_structure_20260915/discovery-selection.json': 'experiments/rule_ring_structure_20260915/discovery-selection.json', 'experiments/rule_ring_structure_20260915/implementation-freeze.json': 'experiments/rule_ring_structure_20260915/implementation-freeze.json', 'experiments/rule_ring_structure_20260915/raw-archive.json': 'experiments/rule_ring_structure_20260915/raw-archive.json', 'experiments/rule_ring_structure_20260915/raw-manifest.json': 'experiments/rule_ring_structure_20260915/raw-manifest.json', 'review/rule_ring_structure/author-crossreview.json': 'review/rule_ring_structure/author-crossreview.json', 'review/rule_ring_structure/check_readouts.py': 'review/rule_ring_structure/check_readouts.py', 'review/rule_ring_structure/confirmation-independent-relations.json': 'review/rule_ring_structure/confirmation-independent-relations.json', 'review/rule_ring_structure/confirmation-verification.json': 'review/rule_ring_structure/confirmation-verification.json', 'review/rule_ring_structure/discovery-independent-relations.json': 'review/rule_ring_structure/discovery-independent-relations.json', 'review/rule_ring_structure/discovery-verification.json': 'review/rule_ring_structure/discovery-verification.json', 'review/rule_ring_structure/independent-review.md': 'review/rule_ring_structure/independent-review.md', 'review/rule_ring_structure/oracle.py': 'review/rule_ring_structure/oracle.py', 'review/rule_ring_structure/readout-verification.json': 'review/rule_ring_structure/readout-verification.json', 'review/rule_ring_structure/verify.py': 'review/rule_ring_structure/verify.py', 'scripts/package_rule_ring_structure.py': 'scripts/package_rule_ring_structure.py', 'scripts/rule_ring_selectors.py': 'scripts/rule_ring_selectors.py', 'scripts/rule_ring_structure.py': 'scripts/rule_ring_structure.py', 'scripts/summarize_rule_ring_structure.py': 'scripts/summarize_rule_ring_structure.py', 'src/groovy/ca.py': 'src/groovy/ca.py'},
    'results/observation_catalog_20260915.json': {'docs/research/protocols/observation-catalog-20260915.md': 'docs/research/protocols/observation-catalog-20260915.md', 'experiments/observation_catalog_20260915/REPRODUCE.md': 'experiments/observation_catalog_20260915/REPRODUCE.md', 'experiments/observation_catalog_20260915/confirmation-execution.json': 'experiments/observation_catalog_20260915/confirmation-execution.json', 'experiments/observation_catalog_20260915/confirmation-result.json': 'experiments/observation_catalog_20260915/confirmation-result.json', 'experiments/observation_catalog_20260915/confirmation-seal.json': 'experiments/observation_catalog_20260915/confirmation-seal.json', 'experiments/observation_catalog_20260915/discovery-execution.json': 'experiments/observation_catalog_20260915/discovery-execution.json', 'experiments/observation_catalog_20260915/discovery-result.json': 'experiments/observation_catalog_20260915/discovery-result.json', 'experiments/observation_catalog_20260915/implementation-freeze.json': 'experiments/observation_catalog_20260915/implementation-freeze.json', 'experiments/observation_catalog_20260915/lift-execution.json': 'experiments/observation_catalog_20260915/lift-execution.json', 'experiments/observation_catalog_20260915/lift-input-hashes.json': 'experiments/observation_catalog_20260915/lift-input-hashes.json', 'experiments/observation_catalog_20260915/protocol-freeze.json': 'experiments/observation_catalog_20260915/protocol-freeze.json', 'experiments/observation_catalog_20260915/raw-archive.json': 'experiments/observation_catalog_20260915/raw-archive.json', 'experiments/observation_catalog_20260915/selected-shortlist.json': 'experiments/observation_catalog_20260915/selected-shortlist.json', 'experiments/on_beam_256_4d_20260914/labels.json': 'experiments/on_beam_256_4d_20260914/labels.json', 'review/catalog-author-crossreview.json': 'review/catalog-author-crossreview.json', 'review/catalog-gate1.md': 'review/catalog-gate1.md', 'review/catalog-independent-review.md': 'review/catalog-independent-review.md', 'review/catalog-verification.json': 'review/catalog-verification.json', 'review/catalog_author_crossreview.py': 'review/catalog_author_crossreview.py', 'review/catalog_compare.py': 'review/catalog_compare.py', 'review/catalog_oracle.py': 'review/catalog_oracle.py', 'review/catalog_period_witnesses.py': 'review/catalog_period_witnesses.py', 'scripts/observation_catalog.py': 'scripts/observation_catalog.py', 'scripts/summarize_observation_catalog.py': 'scripts/summarize_observation_catalog.py'},
    'results/commutator_relations_20260915.json': {'experiments/commutator_relations_20260915/REPRODUCE.md': 'experiments/commutator_relations_20260915/REPRODUCE.md', 'experiments/commutator_relations_20260915/execution-freeze.json': 'experiments/commutator_relations_20260915/execution-freeze.json', 'experiments/commutator_relations_20260915/protocol-freeze.json': 'experiments/commutator_relations_20260915/protocol-freeze.json', 'experiments/commutator_relations_20260915/protocol.md': 'experiments/commutator_relations_20260915/protocol.md', 'experiments/commutator_relations_20260915/publication-normalization.json': 'experiments/commutator_relations_20260915/publication-normalization.json', 'experiments/commutator_relations_20260915/raw-archive.json': 'experiments/commutator_relations_20260915/raw-archive.json', 'experiments/commutator_relations_20260915/recovery.md': 'experiments/commutator_relations_20260915/recovery.md', 'results/commutator_completion_20260915.json': 'results/commutator_completion_20260915.json', 'review/compare_relations.py': 'review/compare_relations.py', 'review/comparison.json': 'review/comparison.json', 'review/gate1-review.md': 'review/gate1-review.md', 'review/physical-replay-review.md': 'review/physical-replay-review.md', 'review/replay_portable.py': 'review/replay_portable.py', 'review/replay_relations.py': 'review/replay_relations.py', 'scripts/commutator_completion.py': 'scripts/commutator_completion.py', 'scripts/commutator_relations.py': 'scripts/commutator_relations.py', 'scripts/package_commutator_relations.py': 'scripts/package_commutator_relations.py', 'scripts/summarize_commutator_relations.py': 'scripts/summarize_commutator_relations.py'},
    'results/commutator_completion_20260915.json': {'experiments/beam_discriminator_loop_20260915/round01/result.json': 'experiments/beam_discriminator_loop_20260915/round01/result.json', 'experiments/commutator_completion_20260915/freeze.json': 'experiments/commutator_completion_20260915/freeze.json', 'experiments/commutator_completion_20260915/protocol-freeze.json': 'experiments/commutator_completion_20260915/protocol-freeze.json', 'experiments/commutator_completion_20260915/protocol.md': 'experiments/commutator_completion_20260915/protocol.md', 'experiments/commutator_completion_20260915/raw-archive.json': 'experiments/commutator_completion_20260915/raw-archive.json', 'review/commutator_completion_independent.json': 'review/commutator_completion_independent.json', 'review/commutator_completion_independent.py': 'review/commutator_completion_independent.py', 'scripts/commutator_completion.py': 'scripts/commutator_completion.py', 'scripts/package_commutator_completion.py': 'scripts/package_commutator_completion.py', 'scripts/summarize_commutator_completion.py': 'scripts/summarize_commutator_completion.py'},
    'results/commutator_history_20260915.json': {'experiments/beam_discriminator_loop_20260915/round06/result.json': 'experiments/beam_discriminator_loop_20260915/round06/result.json', 'experiments/beam_discriminator_loop_20260915/round10/result.json': 'experiments/beam_discriminator_loop_20260915/round10/result.json', 'experiments/commutator_history_20260915/freeze.json': 'experiments/commutator_history_20260915/freeze.json', 'experiments/commutator_history_20260915/protocol-freeze.json': 'experiments/commutator_history_20260915/protocol-freeze.json', 'experiments/commutator_history_20260915/protocol.md': 'experiments/commutator_history_20260915/protocol.md', 'experiments/commutator_history_20260915/raw-archive.json': 'experiments/commutator_history_20260915/raw-archive.json', 'experiments/commutator_history_20260915/response-freeze.json': 'experiments/commutator_history_20260915/response-freeze.json', 'experiments/commutator_history_20260915/response-protocol-freeze.json': 'experiments/commutator_history_20260915/response-protocol-freeze.json', 'experiments/commutator_history_20260915/response-protocol.md': 'experiments/commutator_history_20260915/response-protocol.md', 'experiments/commutator_history_20260915/response-result.json': 'experiments/commutator_history_20260915/response-result.json', 'experiments/commutator_history_20260915/result.json': 'experiments/commutator_history_20260915/result.json', 'experiments/on_beam_256_4d_20260914/labels.json': 'experiments/on_beam_256_4d_20260914/labels.json', 'review/commutator_history_independent.json': 'review/commutator_history_independent.json', 'review/commutator_history_independent.py': 'review/commutator_history_independent.py', 'review/commutator_response_independent.json': 'review/commutator_response_independent.json', 'review/commutator_response_independent.py': 'review/commutator_response_independent.py', 'scripts/commutator_history.py': 'scripts/commutator_history.py', 'scripts/commutator_response.py': 'scripts/commutator_response.py', 'scripts/package_commutator_history.py': 'scripts/package_commutator_history.py', 'scripts/plot_commutator_history.py': 'scripts/plot_commutator_history.py', 'scripts/summarize_commutator_history.py': 'scripts/summarize_commutator_history.py'},
    'results/beam_discriminator_loop_20260915.json': {'experiments/beam_discriminator_loop_20260915/BRIEF.md': 'experiments/beam_discriminator_loop_20260915/BRIEF.md', 'experiments/beam_discriminator_loop_20260915/INDEX.md': 'experiments/beam_discriminator_loop_20260915/INDEX.md', 'experiments/beam_discriminator_loop_20260915/environment.json': 'experiments/beam_discriminator_loop_20260915/environment.json', 'experiments/beam_discriminator_loop_20260915/raw-archive.json': 'experiments/beam_discriminator_loop_20260915/raw-archive.json', 'experiments/beam_discriminator_loop_20260915/round01-protocol.md': 'experiments/beam_discriminator_loop_20260915/round01-protocol.md', 'experiments/beam_discriminator_loop_20260915/round01-summary.md': 'experiments/beam_discriminator_loop_20260915/round01-summary.md', 'experiments/beam_discriminator_loop_20260915/round01/freeze.json': 'experiments/beam_discriminator_loop_20260915/round01/freeze.json', 'experiments/beam_discriminator_loop_20260915/round01/result.json': 'experiments/beam_discriminator_loop_20260915/round01/result.json', 'experiments/beam_discriminator_loop_20260915/round02-protocol.md': 'experiments/beam_discriminator_loop_20260915/round02-protocol.md', 'experiments/beam_discriminator_loop_20260915/round02-summary.md': 'experiments/beam_discriminator_loop_20260915/round02-summary.md', 'experiments/beam_discriminator_loop_20260915/round02/freeze.json': 'experiments/beam_discriminator_loop_20260915/round02/freeze.json', 'experiments/beam_discriminator_loop_20260915/round02/result.json': 'experiments/beam_discriminator_loop_20260915/round02/result.json', 'experiments/beam_discriminator_loop_20260915/round03-protocol.md': 'experiments/beam_discriminator_loop_20260915/round03-protocol.md', 'experiments/beam_discriminator_loop_20260915/round03-summary.md': 'experiments/beam_discriminator_loop_20260915/round03-summary.md', 'experiments/beam_discriminator_loop_20260915/round03/freeze.json': 'experiments/beam_discriminator_loop_20260915/round03/freeze.json', 'experiments/beam_discriminator_loop_20260915/round03/recovery-freeze.json': 'experiments/beam_discriminator_loop_20260915/round03/recovery-freeze.json', 'experiments/beam_discriminator_loop_20260915/round03/result.json': 'experiments/beam_discriminator_loop_20260915/round03/result.json', 'experiments/beam_discriminator_loop_20260915/round04-protocol.md': 'experiments/beam_discriminator_loop_20260915/round04-protocol.md', 'experiments/beam_discriminator_loop_20260915/round04-summary.md': 'experiments/beam_discriminator_loop_20260915/round04-summary.md', 'experiments/beam_discriminator_loop_20260915/round04/freeze.json': 'experiments/beam_discriminator_loop_20260915/round04/freeze.json', 'experiments/beam_discriminator_loop_20260915/round04/result.json': 'experiments/beam_discriminator_loop_20260915/round04/result.json', 'experiments/beam_discriminator_loop_20260915/round05-protocol.md': 'experiments/beam_discriminator_loop_20260915/round05-protocol.md', 'experiments/beam_discriminator_loop_20260915/round05-summary.md': 'experiments/beam_discriminator_loop_20260915/round05-summary.md', 'experiments/beam_discriminator_loop_20260915/round05/freeze.json': 'experiments/beam_discriminator_loop_20260915/round05/freeze.json', 'experiments/beam_discriminator_loop_20260915/round05/result.json': 'experiments/beam_discriminator_loop_20260915/round05/result.json', 'experiments/beam_discriminator_loop_20260915/round06-protocol.md': 'experiments/beam_discriminator_loop_20260915/round06-protocol.md', 'experiments/beam_discriminator_loop_20260915/round06-summary.md': 'experiments/beam_discriminator_loop_20260915/round06-summary.md', 'experiments/beam_discriminator_loop_20260915/round06/freeze.json': 'experiments/beam_discriminator_loop_20260915/round06/freeze.json', 'experiments/beam_discriminator_loop_20260915/round06/result.json': 'experiments/beam_discriminator_loop_20260915/round06/result.json', 'experiments/beam_discriminator_loop_20260915/round07-protocol.md': 'experiments/beam_discriminator_loop_20260915/round07-protocol.md', 'experiments/beam_discriminator_loop_20260915/round07-summary.md': 'experiments/beam_discriminator_loop_20260915/round07-summary.md', 'experiments/beam_discriminator_loop_20260915/round07/freeze.json': 'experiments/beam_discriminator_loop_20260915/round07/freeze.json', 'experiments/beam_discriminator_loop_20260915/round07/result.json': 'experiments/beam_discriminator_loop_20260915/round07/result.json', 'experiments/beam_discriminator_loop_20260915/round08-protocol.md': 'experiments/beam_discriminator_loop_20260915/round08-protocol.md', 'experiments/beam_discriminator_loop_20260915/round08-summary.md': 'experiments/beam_discriminator_loop_20260915/round08-summary.md', 'experiments/beam_discriminator_loop_20260915/round08/freeze.json': 'experiments/beam_discriminator_loop_20260915/round08/freeze.json', 'experiments/beam_discriminator_loop_20260915/round08/result.json': 'experiments/beam_discriminator_loop_20260915/round08/result.json', 'experiments/beam_discriminator_loop_20260915/round09-inspection.json': 'experiments/beam_discriminator_loop_20260915/round09-inspection.json', 'experiments/beam_discriminator_loop_20260915/round09-protocol.md': 'experiments/beam_discriminator_loop_20260915/round09-protocol.md', 'experiments/beam_discriminator_loop_20260915/round09-summary.md': 'experiments/beam_discriminator_loop_20260915/round09-summary.md', 'experiments/beam_discriminator_loop_20260915/round09/freeze.json': 'experiments/beam_discriminator_loop_20260915/round09/freeze.json', 'experiments/beam_discriminator_loop_20260915/round09/result.json': 'experiments/beam_discriminator_loop_20260915/round09/result.json', 'experiments/beam_discriminator_loop_20260915/round10-protocol.md': 'experiments/beam_discriminator_loop_20260915/round10-protocol.md', 'experiments/beam_discriminator_loop_20260915/round10-summary.md': 'experiments/beam_discriminator_loop_20260915/round10-summary.md', 'experiments/beam_discriminator_loop_20260915/round10/freeze.json': 'experiments/beam_discriminator_loop_20260915/round10/freeze.json', 'experiments/beam_discriminator_loop_20260915/round10/result.json': 'experiments/beam_discriminator_loop_20260915/round10/result.json', 'experiments/beam_discriminator_loop_20260915/round11-protocol.md': 'experiments/beam_discriminator_loop_20260915/round11-protocol.md', 'experiments/beam_discriminator_loop_20260915/round11-summary.md': 'experiments/beam_discriminator_loop_20260915/round11-summary.md', 'experiments/beam_discriminator_loop_20260915/round11/freeze.json': 'experiments/beam_discriminator_loop_20260915/round11/freeze.json', 'experiments/beam_discriminator_loop_20260915/round11/result.json': 'experiments/beam_discriminator_loop_20260915/round11/result.json', 'experiments/on_beam_256_4d_20260914/labels.json': 'experiments/on_beam_256_4d_20260914/labels.json', 'review/beam_loop_independent.json': 'review/beam_loop_independent.json', 'review/beam_loop_independent.py': 'review/beam_loop_independent.py', 'scripts/beam_loop_round01.py': 'scripts/beam_loop_round01.py', 'scripts/beam_loop_round02.py': 'scripts/beam_loop_round02.py', 'scripts/beam_loop_round03.py': 'scripts/beam_loop_round03.py', 'scripts/beam_loop_round03_recover.py': 'scripts/beam_loop_round03_recover.py', 'scripts/beam_loop_round04.py': 'scripts/beam_loop_round04.py', 'scripts/beam_loop_round05.py': 'scripts/beam_loop_round05.py', 'scripts/beam_loop_round06.py': 'scripts/beam_loop_round06.py', 'scripts/beam_loop_round07.py': 'scripts/beam_loop_round07.py', 'scripts/beam_loop_round08.py': 'scripts/beam_loop_round08.py', 'scripts/beam_loop_round09.py': 'scripts/beam_loop_round09.py', 'scripts/beam_loop_round10.py': 'scripts/beam_loop_round10.py', 'scripts/beam_loop_round11.py': 'scripts/beam_loop_round11.py', 'scripts/package_beam_loop_raw.py': 'scripts/package_beam_loop_raw.py', 'scripts/plot_beam_discriminator_loop.py': 'scripts/plot_beam_discriminator_loop.py', 'scripts/summarize_beam_discriminator_loop.py': 'scripts/summarize_beam_discriminator_loop.py', 'src/groovy/ca.py': 'src/groovy/ca.py'},
    'results/partial_cohabitation_20260915.json': {p:p for p in ('scripts/partial_cohabitation_20260915.py', 'docs/research/protocols/partial-cohabitation-20260915.md', 'experiments/on_beam_256_4d_20260914/labels.json')},
    'results/response_quotient_20260915.json': {'docs/research/protocols/response-quotient-20260915.md': 'docs/research/protocols/response-quotient-20260915.md', 'experiments/on_beam_256_4d_20260914/labels.json': 'experiments/on_beam_256_4d_20260914/labels.json', 'experiments/response_quotient_20260915/frozen_runner.py': 'experiments/response_quotient_20260915/frozen_runner.py', 'scripts/response_quotient_20260915.py': 'scripts/response_quotient_20260915.py', 'scripts/summarize_response_quotient_20260915.py': 'scripts/summarize_response_quotient_20260915.py'},
    'results/class4_composite_20260915.json': {'docs/research/protocols/class4-composite-validation-20260915.md': 'docs/research/protocols/class4-composite-validation-20260915.md', 'docs/research/protocols/class4-independent-20260915-clarifications.md': 'docs/research/protocols/class4-independent-20260915-clarifications.md', 'docs/research/protocols/class4-independent-20260915.md': 'docs/research/protocols/class4-independent-20260915.md', 'experiments/on_beam_256_4d_20260914/labels.json': 'experiments/on_beam_256_4d_20260914/labels.json', 'results/class4_independent_20260915.json': 'results/class4_independent_20260915.json', 'scripts/class4_composite_20260915.py': 'scripts/class4_composite_20260915.py', 'scripts/class4_independent_20260915.py': 'scripts/class4_independent_20260915.py', 'src/groovy/ca.py': 'src/groovy/ca.py'},
    'results/class4_independent_20260915.json': {"scripts/class4_independent_20260915.py":"scripts/class4_independent_20260915.py","src/groovy/ca.py":"src/groovy/ca.py","docs/research/protocols/class4-independent-20260915.md":"docs/research/protocols/class4-independent-20260915.md","docs/research/protocols/class4-independent-20260915-clarifications.md":"docs/research/protocols/class4-independent-20260915-clarifications.md","experiments/on_beam_256_4d_20260914/labels.json":"experiments/on_beam_256_4d_20260914/labels.json"},
    'results/orbit_drift_14_20260914.json': {'docs/research/protocols/orbit-drift-20260914.md': 'docs/research/protocols/orbit-drift-20260914.md', 'experiments/orbit_drift_14_20260914/run/annotations.csv': 'experiments/orbit_drift_14_20260914/run/annotations.csv', 'experiments/orbit_drift_14_20260914/run/cycles.json': 'experiments/orbit_drift_14_20260914/run/cycles.json', 'experiments/orbit_drift_14_20260914/run/execution.json': 'experiments/orbit_drift_14_20260914/run/execution.json', 'review/orbit_drift_independent_review.json': 'review/orbit_drift_independent_review.json', 'review/orbit_drift_independent_review.py': 'review/orbit_drift_independent_review.py', 'scripts/orbit_drift_14.py': 'scripts/orbit_drift_14.py', 'scripts/verify_orbit_drift_14.py': 'scripts/verify_orbit_drift_14.py', 'src/groovy/ca.py': 'src/groovy/ca.py'},
    'results/uniform_jet6_cache_20260914.json': {'scripts/uniform_jet6_cache.py': 'scripts/uniform_jet6_cache.py', 'scripts/uniform_jet6_analysis.py': 'scripts/uniform_jet6_analysis.py', 'scripts/on_beam_256_4d.py': 'scripts/on_beam_256_4d.py', 'scripts/on_beam_rule_analysis.py': 'scripts/on_beam_rule_analysis.py', 'scripts/sequential_lift_6d_pilot.py': 'scripts/sequential_lift_6d_pilot.py', 'docs/research/protocols/uniform-jet6-cache-20260914.md': 'docs/research/protocols/uniform-jet6-cache-20260914.md', 'experiments/on_beam_256_4d_20260914/labels.json': 'experiments/on_beam_256_4d_20260914/labels.json', 'results/binary_lift_20260914/rule_coverage.csv': 'results/binary_lift_20260914/rule_coverage.csv', 'experiments/on_beam_256_4d_20260914/run/floors.jsonl': 'experiments/on_beam_256_4d_20260914/run/floors.jsonl', 'experiments/on_beam_256_4d_20260914/run/paths.jsonl': 'experiments/on_beam_256_4d_20260914/run/paths.jsonl', 'experiments/on_beam_256_4d_20260914/run/summary.json': 'experiments/on_beam_256_4d_20260914/run/summary.json', 'accounting': 'scripts/verify_uniform_jet6_cache.py', 'reader': 'scripts/read_uniform_jet6_cache.py', 'execution': 'experiments/uniform_jet6_cache_20260914/run/execution.json', 'summary': 'experiments/uniform_jet6_cache_20260914/run/summary.json', 'analysis': 'experiments/uniform_jet6_cache_20260914/run/analysis.json', 'archive_manifest': 'experiments/uniform_jet6_cache_20260914/run/archive_manifest.json', 'benchmark': 'experiments/uniform_jet6_cache_20260914/run/benchmark.json', 'floors': 'experiments/uniform_jet6_cache_20260914/run/floors.jsonl', 'paths': 'experiments/uniform_jet6_cache_20260914/run/paths.jsonl'},
    'results/on_beam_256_4d_20260914.json': {'script': 'scripts/on_beam_256_4d.py', 'analysis_script': 'scripts/on_beam_rule_analysis.py', 'native_core': 'scripts/sequential_lift_6d_pilot.py', 'accounting': 'scripts/verify_on_beam_256_4d.py', 'protocol': 'docs/research/protocols/on-beam-256-4d-classes-20260914.md', 'recipes': 'results/binary_lift_20260914/rule_coverage.csv', 'labels': 'experiments/on_beam_256_4d_20260914/labels.json', 'execution': 'experiments/on_beam_256_4d_20260914/run/execution.json', 'summary': 'experiments/on_beam_256_4d_20260914/run/summary.json', 'analysis': 'experiments/on_beam_256_4d_20260914/run/analysis.json', 'archive_manifest': 'experiments/on_beam_256_4d_20260914/run/archive_manifest.json', 'floors': 'experiments/on_beam_256_4d_20260914/run/floors.jsonl', 'paths': 'experiments/on_beam_256_4d_20260914/run/paths.jsonl'},
    'results/sequential_lift_6d_20260914.json': {'script': 'scripts/sequential_lift_6d_pilot.py', 'protocol': 'docs/research/protocols/sequential-lift-6d-pilot-20260914.md', 'accounting': 'scripts/verify_sequential_lift_pilot.py', 'raw_floors': 'experiments/sequential_lift_6d_20260914/run/floors.jsonl', 'raw_summary': 'experiments/sequential_lift_6d_20260914/run/summary.json', 'execution': 'experiments/sequential_lift_6d_20260914/run/execution.json'},
    'results/forced_tables_20260917/summary.json': {
        'script': 'scripts/forced_tables_20260917.py',
        'protocol': 'docs/research/protocols/2026-09-17-forced-tables.md',
        'sweep': 'results/sweep_full_classified.parquet',
        'labels': 'experiments/on_beam_256_4d_20260914/labels.json',
        'tables_d2': 'results/forced_tables_20260917/tables_d2.npz',
        'invariants': 'results/forced_tables_20260917/invariants.json',
        'pairs': 'results/forced_tables_20260917/pairs.npz',
        'families': 'results/forced_tables_20260917/families.json',
        'regime_join': 'results/forced_tables_20260917/regime_join.json',
        'd3_panel': 'results/forced_tables_20260917/d3_panel.json'},
    'results/handed_fiber_census_20260917/summary.json': {
        'protocol': 'docs/research/protocols/2026-09-17-handed-fiber-census.md',
        'run': 'experiments/handed_fiber_census_20260917/run.py',
        'evaluate': 'experiments/handed_fiber_census_20260917/evaluate.py',
        'control6': 'experiments/handed_fiber_census_20260917/control6_matched.py',
        'rows': 'results/handed_fiber_census_20260917/rows.json',
        'exactness': 'results/handed_fiber_census_20260917/exactness_control.json',
        'matched_control': 'results/handed_fiber_census_20260917/control6_matched.json'},
    'results/fiber_census_64_20260917/summary.json': {
        'protocol': 'docs/research/protocols/2026-09-17-fiber-census-64.md',
        'run': 'experiments/fiber_census_64_20260917/run.py',
        'evaluate': 'experiments/fiber_census_64_20260917/evaluate.py',
        'rows': 'results/fiber_census_64_20260917/rows.json',
        'exactness': 'results/fiber_census_64_20260917/exactness_control.json'},
    'results/fiber_census_20260917/summary.json': {
        'protocol': 'docs/research/protocols/2026-09-17-fiber-census.md',
        'run': 'experiments/fiber_census_20260917/run.py',
        'summarize': 'experiments/fiber_census_20260917/summarize.py',
        'census_k2': 'results/fiber_census_20260917/fiber_census_k2.json',
        'census_k4': 'results/fiber_census_20260917/fiber_census_k4.json',
        'exactness_k2': 'results/fiber_census_20260917/exactness_control_k2.json',
        'exactness_k4': 'results/fiber_census_20260917/exactness_control_k4.json'},
    'results/affine_lift_20260917.json': {
        'script': 'scripts/verify_affine_lift.py',
        'proof': 'docs/research/proofs/affine-oriented-lift-proof-state-20260917.md'},
    'results/representation_invariants_20260910.json': {
        'script': 'scripts/verify_representation_invariants.py',
        'local_correction_caps': 'results/local_correction_caps_20260910.json',
        'sweep_full_classified': 'results/sweep_full_classified.parquet'},
    'results/cap_census_complement_extension_20260911.json': {
        'script': 'scripts/verify_cap_census_complement_extension.py',
        'local_correction_caps': 'results/local_correction_caps_20260910.json',
        'representation_invariants_audit': 'results/representation_invariants_20260910.json'},
    'results/cap_shift_census_20260911.json': {
        'script': 'scripts/verify_cap_shift_census.py',
        'local_correction_caps': 'results/local_correction_caps_20260910.json'},
    'results/higher_block_recoding_20260911.json': {
        'script': 'scripts/verify_higher_block_recoding.py',
        'local_correction_caps': 'results/local_correction_caps_20260910.json',
        'cap_shift_census': 'results/cap_shift_census_20260911.json'},
    'results/parity_coarse_graining_20260911.json': {
        'script': 'scripts/verify_parity_coarse_graining.py',
        'representation_invariants_audit': 'results/representation_invariants_20260910.json'},
    'results/parity_history_bound_20260911.json': {
        'script': 'scripts/verify_parity_history_bound.py',
        'parity_coarse_graining_script': 'scripts/verify_parity_coarse_graining.py',
        'parity_coarse_graining_result': 'results/parity_coarse_graining_20260911.json'},
    'results/linear_observations_20260911.json': {
        'script': 'scripts/verify_linear_observations.py',
        'parity_coarse_graining_result': 'results/parity_coarse_graining_20260911.json',
        'parity_history_bound_result': 'results/parity_history_bound_20260911.json'},
    'results/block_majority_20260911.json': {
        'script': 'scripts/verify_block_majority.py',
        'parity_coarse_graining_result': 'results/parity_coarse_graining_20260911.json'},
    'results/isolated_cell_20260911.json': {
        'script': 'scripts/verify_isolated_cell.py',
        'parity_coarse_graining_result': 'results/parity_coarse_graining_20260911.json',
        'block_majority_result': 'results/block_majority_20260911.json'},
    'results/complement_observation_20260911.json': {
        'script': 'scripts/verify_complement_observation.py',
        'block_majority_result': 'results/block_majority_20260911.json',
        'isolated_cell_result': 'results/isolated_cell_20260911.json'},
    'results/wiring_dilation_20260911.json': {
        'script': 'scripts/verify_wiring_dilation.py',
        'block_majority_result': 'results/block_majority_20260911.json',
        'isolated_cell_result': 'results/isolated_cell_20260911.json'},
    'results/factor_radius_20260911.json': {
        'script': 'scripts/verify_factor_radius.py',
        'block_majority_result': 'results/block_majority_20260911.json',
        'isolated_cell_result': 'results/isolated_cell_20260911.json',
        'complement_observation_result': 'results/complement_observation_20260911.json'},
    'results/ring_closure_certificate_20260911.json': {
        'script': 'scripts/verify_ring_closure_certificate.py',
        'factor_radius_result': 'results/factor_radius_20260911.json',
        'linear_observations_result': 'results/linear_observations_20260911.json'},
    'results/depth_one_certificate_20260911.json': {
        'script': 'scripts/verify_depth_one_certificate.py',
        'block_majority_result': 'results/block_majority_20260911.json',
        'isolated_cell_result': 'results/isolated_cell_20260911.json',
        'complement_observation_result': 'results/complement_observation_20260911.json',
        'linear_observations_result': 'results/linear_observations_20260911.json'},
    'results/full_shift_depth_two_20260911.json': {
        'script': 'scripts/verify_full_shift_depth_two.py',
        'depth_one_certificate_result': 'results/depth_one_certificate_20260911.json'},
    'results/full_shift_depth_three_20260912.json': {
        'script': 'scripts/verify_full_shift_depth_three.py',
        'ring_closure_certificate_result': 'results/ring_closure_certificate_20260911.json',
        'depth_one_certificate_result': 'results/depth_one_certificate_20260911.json',
        'full_shift_depth_two_result': 'results/full_shift_depth_two_20260911.json'},
    'results/full_shift_depth_three_linear_20260912.json': {
        'script': 'scripts/verify_full_shift_depth_three_linear.py',
        'ring_closure_certificate_result': 'results/ring_closure_certificate_20260911.json',
        'depth_one_certificate_result': 'results/depth_one_certificate_20260911.json',
        'full_shift_depth_two_result': 'results/full_shift_depth_two_20260911.json',
        'linear_observations_result': 'results/linear_observations_20260911.json'},
    'results/second_lift_completion_20260911.json': {
        'script': 'scripts/verify_second_lift_completion.py',
        'protocol': 'docs/research/protocols/second-lift-completion-comparison-20260910.md'},
    'results/transverse_freedom_20260911.json': {
        'script': 'scripts/verify_transverse_freedom.py',
        'protocol': 'docs/research/protocols/transverse-freedom-20260911.md'},
    'results/intervention_axis_20260911.json': {
        'script': 'scripts/verify_intervention_axis.py',
        'protocol': 'docs/research/protocols/intervention-axis-20260911.md'},
    'results/interface_factor_20260911.json': {
        'script': 'scripts/verify_interface_factor.py',
        'protocol': 'docs/research/protocols/interface-factor-20260911.md'},
    'results/zero_dimensional_base_20260912.json': {
        'script': 'scripts/verify_zero_dimensional_base.py',
        'protocol': 'docs/research/protocols/zero-dimensional-base-20260912.md',
        'history_algebra_result': 'results/history_algebra_checks.json',
        'shared_state_audit': 'results/shared_state_rule_20260907_audit.json',
        'shared_state_local': 'results/shared_state_rule_20260907_local.json',
        'guard_free_axial_result': 'results/guard_free_axial_lift_20260910.json',
        'editable_routing_result': 'results/editable_routing_tables_20260909.json'},
    'results/relational_rank_20260912.json': {
        'script': 'scripts/verify_relational_rank.py',
        'protocol': 'docs/research/protocols/relational-rank-20260912.md',
        'guard_free_axial': 'results/guard_free_axial_lift_20260910.json',
        'transverse_freedom': 'results/transverse_freedom_20260911.json',
        'intervention_axis': 'results/intervention_axis_20260911.json'},
    'results/interface_history_20260911.json': {
        'script': 'scripts/verify_interface_history.py',
        'protocol': 'docs/research/protocols/interface-history-20260911.md',
        'interface_factor_result': 'results/interface_factor_20260911.json',
        'interface_factor_script': 'scripts/verify_interface_factor.py'},
    'results/interface_history_global_20260912.json': {
        'script': 'scripts/verify_interface_history_global.py',
        'protocol': 'docs/research/protocols/interface-history-global-20260912.md',
        'gate1_clarification': 'docs/research/protocols/interface-history-global-gate1-clarification-20260912.md',
        'predecessor_protocol': 'docs/research/protocols/interface-history-20260911.md',
        'predecessor_script': 'scripts/verify_interface_history.py',
        'predecessor_result': 'results/interface_history_20260911.json',
        'interface_factor_script': 'scripts/verify_interface_factor.py',
        'interface_factor_result': 'results/interface_factor_20260911.json'},
    'results/interface_history_cross_width_20260912.json': {
        'script': 'scripts/verify_interface_history_cross_width.py',
        'protocol': 'docs/research/protocols/interface-history-cross-width-20260912.md',
        'interface_history_protocol': 'docs/research/protocols/interface-history-20260911.md',
        'interface_history_script': 'scripts/verify_interface_history.py',
        'interface_history_result': 'results/interface_history_20260911.json',
        'interface_history_global_protocol': 'docs/research/protocols/interface-history-global-20260912.md',
        'interface_history_global_script': 'scripts/verify_interface_history_global.py',
        'interface_history_global_result': 'results/interface_history_global_20260912.json',
        'interface_factor_script': 'scripts/verify_interface_factor.py'},
    'results/dimensional_history_scaling_control_20260912.json': {
        'script': 'scripts/verify_dimensional_history_scaling_control.py',
        'parent_protocol': 'docs/research/protocols/dimensional-history-scaling-20260912.md',
        'gate1_refreeze': 'docs/research/protocols/dimensional-history-scaling-gate1-refreeze-20260912.md'},
    'results/depth_two_certificate_20260912.json': {
        'script': 'scripts/verify_depth_two_certificate.py',
        'full_shift_depth_two_script': 'scripts/verify_full_shift_depth_two.py',
        'full_shift_depth_two_result': 'results/full_shift_depth_two_20260911.json',
        'depth_one_certificate_result': 'results/depth_one_certificate_20260911.json'},

    'results/closed_violation_depth_three_20260913.json': {
        'script': 'scripts/verify_closed_violation_depth_three.py',
        'full_shift_depth_three_script': 'scripts/verify_full_shift_depth_three.py',
        'depth_one_certificate_script': 'scripts/verify_depth_one_certificate.py',
        'depth_one_certificate_result': 'results/depth_one_certificate_20260911.json',
        'depth_two_certificate_result': 'results/depth_two_certificate_20260912.json',
        'full_shift_depth_two_result': 'results/full_shift_depth_two_20260911.json',
        'full_shift_depth_three_result': 'results/full_shift_depth_three_20260912.json',
        'full_shift_depth_three_linear_result': 'results/full_shift_depth_three_linear_20260912.json'},

    'results/dimensional_resonance_response_20260912.json': {
        'script': 'scripts/verify_dimensional_resonance_response.py',
        'protocol': 'docs/research/protocols/dimensional-resonance-response-20260912.md',
        'gate1_refreeze': 'docs/research/protocols/dimensional-resonance-response-gate1-refreeze-20260912.md',
        'gate1_null_clarification': 'docs/research/protocols/dimensional-resonance-response-gate1-null-clarification-20260912.md',
        'gate1_approval': 'docs/research/protocols/dimensional-resonance-response-gate1-approval-20260912.md',
        'source_census_script': 'scripts/verify_dimensional_resonance_source_census.py',
        'physical_predecessor_script': 'scripts/verify_interface_factor.py'},

    'results/factor_balanced_interactions_20260915.json': {'docs/research/protocols/factor-balanced-interactions-20260915.md': 'docs/research/protocols/factor-balanced-interactions-20260915.md', 'experiments/factor_balanced_interactions_20260915/REPRODUCE.md': 'experiments/factor_balanced_interactions_20260915/REPRODUCE.md', 'experiments/factor_balanced_interactions_20260915/confirmation-execution.json': 'experiments/factor_balanced_interactions_20260915/confirmation-execution.json', 'experiments/factor_balanced_interactions_20260915/confirmation-result.json': 'experiments/factor_balanced_interactions_20260915/confirmation-result.json', 'experiments/factor_balanced_interactions_20260915/fit-execution.json': 'experiments/factor_balanced_interactions_20260915/fit-execution.json', 'experiments/factor_balanced_interactions_20260915/fit-result.json': 'experiments/factor_balanced_interactions_20260915/fit-result.json', 'experiments/factor_balanced_interactions_20260915/historical-provenance.json': 'experiments/factor_balanced_interactions_20260915/historical-provenance.json', 'experiments/factor_balanced_interactions_20260915/historical-relations.json': 'experiments/factor_balanced_interactions_20260915/historical-relations.json', 'experiments/factor_balanced_interactions_20260915/implementation-freeze.json': 'experiments/factor_balanced_interactions_20260915/implementation-freeze.json', 'experiments/factor_balanced_interactions_20260915/prediction-seal.json': 'experiments/factor_balanced_interactions_20260915/prediction-seal.json', 'experiments/factor_balanced_interactions_20260915/predictions.json': 'experiments/factor_balanced_interactions_20260915/predictions.json', 'experiments/factor_balanced_interactions_20260915/raw-archive.json': 'experiments/factor_balanced_interactions_20260915/raw-archive.json', 'experiments/factor_balanced_interactions_20260915/raw-manifest.json': 'experiments/factor_balanced_interactions_20260915/raw-manifest.json', 'experiments/factor_balanced_interactions_20260915/score-tables.md': 'experiments/factor_balanced_interactions_20260915/score-tables.md', 'review/factor_balanced/author-crossreview.json': 'review/factor_balanced/author-crossreview.json', 'review/factor_balanced/cases-verification.json': 'review/factor_balanced/cases-verification.json', 'review/factor_balanced/core-row-verification.json': 'review/factor_balanced/core-row-verification.json', 'review/factor_balanced/core_row_check.py': 'review/factor_balanced/core_row_check.py', 'review/factor_balanced/fit-verification.json': 'review/factor_balanced/fit-verification.json', 'review/factor_balanced/fresh-independent-relations.json': 'review/factor_balanced/fresh-independent-relations.json', 'review/factor_balanced/independent-review.md': 'review/factor_balanced/independent-review.md', 'review/factor_balanced/oracle.py': 'review/factor_balanced/oracle.py', 'review/factor_balanced/score-verification.json': 'review/factor_balanced/score-verification.json', 'review/factor_balanced/verify.py': 'review/factor_balanced/verify.py', 'scripts/factor_balanced_interactions.py': 'scripts/factor_balanced_interactions.py', 'scripts/package_factor_balanced.py': 'scripts/package_factor_balanced.py', 'scripts/plot_factor_balanced.py': 'scripts/plot_factor_balanced.py', 'scripts/rule_ring_selectors.py': 'scripts/rule_ring_selectors.py', 'scripts/rule_ring_structure.py': 'scripts/rule_ring_structure.py', 'scripts/summarize_factor_balanced.py': 'scripts/summarize_factor_balanced.py', 'src/groovy/ca.py': 'src/groovy/ca.py'},
}

def sha(p: pathlib.Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def check(result: str) -> list[str]:
    problems = []
    if not (ROOT / result).exists(): return [f'{result}: result file missing']
    data = json.loads((ROOT / result).read_text())
    recorded = data.get('source_hashes')
    if not isinstance(recorded, dict): return [f'{result}: no source_hashes block']
    mapping = REGISTRY[result]
    for key, expected in recorded.items():
        if key not in mapping: problems.append(f'{result}: hash key {key!r} not registered'); continue
        path = ROOT / mapping[key]
        if not path.exists(): problems.append(f'{result}: {mapping[key]} missing'); continue
        actual = sha(path)
        if actual != expected: problems.append(f'{result}: {key} -> {mapping[key]} hash {actual[:12]} != recorded {expected[:12]}')
    for key in mapping:
        if key not in recorded: problems.append(f'{result}: registered key {key!r} absent from source_hashes')
    return problems

def main(argv: list[str]) -> int:
    targets = argv or list(REGISTRY)
    bad = []
    for t in targets:
        t = str(pathlib.Path(t)); t = t if t in REGISTRY else str(pathlib.Path(t).relative_to(ROOT)) if pathlib.Path(t).is_absolute() else t
        if t not in REGISTRY: print(f'not registered: {t}'); bad.append(t); continue
        p = check(t)
        summary = json.loads((ROOT / t).read_text()).get('summary') if (ROOT / t).exists() else None
        print(('OK  ' if not p else 'FAIL') + f' {t}  summary={json.dumps(summary)}')
        for line in p: print('   ', line)
        bad += p
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
