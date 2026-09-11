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
With no arguments every registered result is checked.
"""
from __future__ import annotations
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]

# result file -> {hash key recorded in its source_hashes: path the hash was taken of}
REGISTRY = {
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
    'results/second_lift_completion_20260911.json': {
        'script': 'scripts/verify_second_lift_completion.py',
        'protocol': 'docs/research/protocols/second-lift-completion-comparison-20260910.md'},
    'results/transverse_freedom_20260911.json': {
        'script': 'scripts/verify_transverse_freedom.py',
        'protocol': 'docs/research/protocols/transverse-freedom-20260911.md'},
    'results/intervention_axis_20260911.json': {
        'script': 'scripts/verify_intervention_axis.py',
        'protocol': 'docs/research/protocols/intervention-axis-20260911.md'},
}

def sha(p: pathlib.Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def check(result: str) -> list[str]:
    problems = []
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
        summary = json.loads((ROOT / t).read_text()).get('summary')
        print(('OK  ' if not p else 'FAIL') + f' {t}  summary={json.dumps(summary)}')
        for line in p: print('   ', line)
        bad += p
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
