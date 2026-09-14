#!/usr/bin/env python3
"""Read-only provenance/accounting check and local replay for the binary lift unit.

--check recomputes the published account from the preserved evidence. It does
not rerun the scientific census. --replay reruns the existing targeted author
verifiers and complete G-collision diagnosis in a disposable extracted copy.
No scientific replay is wired into automatic CI. All original outputs remain
unchanged; wall-clock fields are not claimed to reproduce byte for byte.
"""
from __future__ import annotations
import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/binary_lift_20260914'
DATA = ROOT / 'results/binary_lift_20260914'
RESULT = 'results/binary_lift_20260914.json'
MANIFEST = DATA / 'bundle_manifest.json'
PROVENANCE = 'docs/research/protocols/binary-lift-retrospective-record-20260914.md'


def read_json(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_paths(manifest):
    paths = [str(Path(__file__).relative_to(ROOT)), str(MANIFEST.relative_to(ROOT)), PROVENANCE]
    paths += manifest['code_files']
    paths += [x['path'] for x in manifest['archive_parts']]
    return {f'input_{i:03d}': p for i, p in enumerate(sorted(paths))}


def integrity():
    # Unit-specific registration uses the canonical engine, without editing
    # its legacy global registry (which fans out to unrelated full replays).
    import check_result_integrity as shared
    shared.REGISTRY[RESULT] = source_paths(read_json(MANIFEST))
    problems = shared.check(RESULT)
    if problems:
        raise RuntimeError('\n'.join(problems))


def extract(destination):
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError('Extraction destination must be empty')
    manifest = read_json(MANIFEST)
    chunks = []
    for entry in manifest['archive_parts']:
        path = ROOT / entry['path']
        if sha(path) != entry['sha256']:
            raise ValueError(f'Archive part changed: {path}')
        chunks.append(path.read_bytes())
    archive = base64.b64decode(b''.join(chunks), validate=True)
    if hashlib.sha256(archive).hexdigest() != manifest['archive_sha256']:
        raise ValueError('Archive digest mismatch')
    expected = {e['path']: e for e in manifest['members']}
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:xz') as tar:
        members = tar.getmembers()
        if len(members) != len(expected) or {m.name for m in members} != set(expected):
            raise ValueError('Archive inventory mismatch')
        for member in members:
            p = Path(member.name)
            if not member.isfile() or p.is_absolute() or '..' in p.parts:
                raise ValueError(f'Unsafe archive member: {member.name}')
            content = tar.extractfile(member).read()
            entry = expected[member.name]
            if len(content) != entry['bytes'] or hashlib.sha256(content).hexdigest() != entry['sha256']:
                raise ValueError(f'Member digest mismatch: {member.name}')
            target = destination / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    shutil.copytree(UNIT / 'ca_lift_lab', destination / 'ca_lift_lab', dirs_exist_ok=True)
    return destination / 'ca_lift_lab'


def rows(lab, run, name='candidates.jsonl'):
    return [json.loads(line) for line in (lab/'runs'/run/name).read_text().splitlines()]


def recipe_key(r):
    c = r['recipe'][0]
    return r['rule'], c['mask'], c['shift'], r['reference'], tuple(r['order'])


def account(lab):
    floors = {}
    source_records = []
    for label, run in [('symmetric', 'binary_fresh_all256'), ('directed', 'directed_full256')]:
        rr = rows(lab, run)
        assert len(rr) == len({recipe_key(r) for r in rr}) == 24576
        assert all(sum(r['rule'] == rule for r in rr) == 96 for rule in range(256))
        floors[label] = {k: sorted({r['rule'] for r in rr if r[k]})
                         for k in ('first_order_pass', 'joint_raw', 'joint_centered')}
        source_records.extend(rr)
    floors['combined'] = {k: sorted({r['rule'] for r in source_records if r[k]})
                          for k in ('first_order_pass', 'joint_raw', 'joint_centered')}
    three = rows(lab, 'universal_3d')
    assert sorted(r['rule'] for r in three) == list(range(256))
    best = rows(lab, 'universal_3d', 'best_known_G_paths.jsonl')
    four = rows(lab, 'binary_4d')
    selected = {k: sorted(r['rule'] for r in three if r['gates'][k]['passes']) for k in ('native', 'source', 'parent')}
    selected['G_eligible'] = sorted(r['rule'] for r in three if r['G_eligible'])
    selected['original_G'] = sorted(r['rule'] for r in three if r['recursive_G']['passes'] and r['recursive_G']['mode'] == 'raw')
    selected['centered_only_G'] = sorted(r['rule'] for r in three if r['recursive_G']['passes'] and r['recursive_G']['mode'] == 'centered')
    selected['missing_first_floor_G'] = sorted(r['rule'] for r in three if not r['G_eligible'])
    best_account = {m: sorted(r['rule'] for r in best if r['recursive_G']['mode'] == m) for m in ('raw', 'centered')}
    assert all(r['first_order_pass'] and r['recursive_G']['passes'] for r in best)
    diagnostics = rows(lab, 'first_floor_g_obstructions', 'diagnoses.jsonl')
    phase = rows(lab, 'first_floor_g_obstructions', 'phase_oracle.jsonl')
    categories = {k: sum(r['category'] == k for r in diagnostics) for k in (
        'same_field_probe_ambiguity', 'cross_field_probe_ambiguity', 'native_probe_or_zero_incompatibility')}
    rescued = sorted({r['rule'] for r in phase if r['phase_aware_centered_passes']})
    holdouts = selected['missing_first_floor_G']
    assert len(diagnostics) == 3040 and len(phase) == 608
    assert {r['rule'] for r in diagnostics} == set(holdouts)
    result = {
        'first_floor': floors,
        'three_dimensional_selected': selected,
        'three_dimensional_best_known': best_account,
        'four_dimensional_historical': {
            'tested': sorted(r['rule'] for r in four),
            'faithful': sorted(r['rule'] for r in four if r['first_order_pass']),
            'recursive_G': sorted(r['rule'] for r in four if r['recursive_G']['passes'])},
        'obstructions': {'holdout_rules': holdouts, 'faithful_recipes': len(diagnostics),
                         'categories': categories, 'phase_aware_rescued_rules': rescued,
                         'phase_aware_rescued_recipes': sum(r['phase_aware_centered_passes'] for r in phase),
                         'phase_oracle_scope': 'Only recipes already faithful under the original uniform unlabeled native/recovery gates; initially unfaithful recipes were not retested under labels',
                         'phase_aware_still_blocked_rules': sorted(set(holdouts)-set(rescued))},
    }
    result['summary'] = {
        'first_floor_faithful': len(floors['combined']['first_order_pass']),
        'first_floor_original_G': len(floors['combined']['joint_raw']),
        'first_floor_centered_G': len(floors['combined']['joint_centered']),
        'three_dimensional_faithful': len(set(selected['native']) & set(selected['source']) & set(selected['parent'])),
        'three_dimensional_selected_G': len(selected['original_G'])+len(selected['centered_only_G']),
        'three_dimensional_best_known_G': len(best),
        'four_dimensional_historical_G': len(result['four_dimensional_historical']['recursive_G']),
        'first_floor_holdouts_blocked_with_phase_labels': len(result['obstructions']['phase_aware_still_blocked_rules'])}
    assert list(result['summary'].values()) == [256, 133, 220, 256, 200, 206, 105, 29]
    return result


def canonical(lab):
    result = account(lab)
    mapping = source_paths(read_json(MANIFEST))
    return {'schema_version': 1, 'date': '2026-09-14',
            'review_status_at_import': 'Gate 2 pending; Gate 1 exception approved by Myk',
            'evidence_status': 'Retrospective exhaustive finite-domain computation; author verification, no independent-agent review yet',
            'source_paths': mapping, 'source_hashes': {k: sha(ROOT/p) for k, p in mapping.items()}, **result}


def coverage_csv(lab):
    first = rows(lab, 'binary_fresh_all256') + rows(lab, 'directed_full256')
    memberships = {k: {r['rule'] for r in first if r[k]}
                   for k in ('first_order_pass', 'joint_raw', 'joint_centered')}
    best = {r['rule']: r for r in rows(lab, 'universal_3d', 'best_known_G_paths.jsonl')}
    four = {r['rule']: r for r in rows(lab, 'binary_4d')}
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(['rule', 'first_floor_faithful_exists', 'first_floor_original_G_exists',
                     'first_floor_centered_G_exists', 'selected_mask', 'selected_shift',
                     'selected_Q', 'selected_order', 'selected_3d_native', 'selected_3d_source_recovery',
                     'selected_3d_parent_recovery', 'selected_3d_G_eligible', 'selected_3d_G_mode',
                     'selected_3d_G_pass', 'best_known_3d_G_mode', 'historical_4d_faithful', 'historical_4d_G'])
    label = {'raw': 'original', 'centered': 'centered', None: 'none'}
    for rec in sorted(rows(lab, 'universal_3d'), key=lambda r: r['rule']):
        r, f = rec['rule'], rec['first_floor']
        b, old = best.get(r), four.get(r)
        writer.writerow([r, *[int(r in memberships[k]) for k in memberships],
                         f['recipe'][0]['mask'], f['recipe'][0]['shift'], f['reference'],
                         ''.join('PDMQ'[c] for c in f['order']),
                         *[int(rec['gates'][k]['passes']) for k in ('native', 'source', 'parent')],
                         int(rec['G_eligible']), label[rec['recursive_G']['mode']],
                         int(rec['recursive_G']['passes']), label[b['recursive_G']['mode']] if b else 'none',
                         int(old['first_order_pass']) if old else 'not_tested',
                         int(old['recursive_G']['passes']) if old else 'not_tested'])
    return stream.getvalue()


def replay(lab):
    for script in ('verify_binary_fresh.py', 'verify_directed_full256.py', 'verify_universal_3d.py', 'verify_decoder_obstruction.py'):
        if script == 'verify_universal_3d.py':
            shutil.rmtree(lab/'runs/universal_3d/targeted_verification')
        subprocess.run([sys.executable, str(lab/script)], cwd=lab, check=True)
    target = lab/'runs/replayed_g_obstructions'
    subprocess.run([sys.executable, str(lab/'diagnose_first_floor_g.py'), '--output', str(target)], cwd=lab, check=True)
    subprocess.run([sys.executable, str(lab/'diagnose_first_floor_g.py'), '--tagged-run', str(target)], cwd=lab, check=True)
    for name in ('diagnoses.jsonl', 'phase_oracle.jsonl'):
        assert (target/name).read_bytes() == (lab/'runs/first_floor_g_obstructions'/name).read_bytes(), name
    print('Targeted author checks passed; complete collision records replayed byte for byte.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--integrity', action='store_true')
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--extract', type=Path)
    mode.add_argument('--replay', action='store_true')
    mode.add_argument('--write-record', action='store_true')
    args = parser.parse_args()
    if not args.write_record:
        integrity()
    if args.integrity:
        print('Binary lift release: all registered source and evidence hashes match.')
        return
    if args.extract:
        print(extract(args.extract))
        return
    with tempfile.TemporaryDirectory(prefix='binary-lift-release-') as tmp:
        lab = extract(Path(tmp))
        record = canonical(lab)
        table = coverage_csv(lab)
        if args.write_record:
            (ROOT/RESULT).write_text(json.dumps(record, indent=2)+'\n')
            (DATA/'rule_coverage.csv').write_text(table)
        else:
            assert record == read_json(ROOT/RESULT), 'Canonical account differs from preserved evidence'
            assert table == (DATA/'rule_coverage.csv').read_text(), 'Per-rule CSV differs from preserved evidence'
        print(json.dumps(record['summary'], sort_keys=True))
        if args.replay:
            replay(lab)


if __name__ == '__main__':
    main()
