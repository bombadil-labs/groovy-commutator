#!/usr/bin/env python3
"""Preserve every symbolic cell, physical key and exact original input."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/commutator_completion_20260915'
INPUT = ROOT.parent / 'gc-pilot/experiments/uniform_jet6_cache_20260914/run'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    files = [INPUT / 'uniform_jet6_rules.tar.gz', INPUT / 'archive_manifest.json',
             ROOT / 'experiments/beam_discriminator_loop_20260915/round01/tables.npz',
             UNIT / 'result.json'] + sorted(p for p in (UNIT / 'records').iterdir() if p.suffix in ('.npz', '.json'))
    files += [ROOT.parent / 'gc-pilot/scripts' / name for name in
              ('uniform_jet6_cache.py', 'on_beam_256_4d.py', 'on_beam_rule_analysis.py', 'sequential_lift_6d_pilot.py')]
    assert len(list((UNIT / 'records').glob('*.npz'))) == 1536
    assert len(list((UNIT / 'records').glob('*.json'))) == 1536
    members, archives, parts = [], [], [[]]
    part_bytes = 0
    for path in files:
        assert path.is_file()
        if part_bytes + path.stat().st_size > 240 * 1024 * 1024 and parts[-1]:
            parts.append([]); part_bytes = 0
        parts[-1].append(path)
        part_bytes += path.stat().st_size
    for i, part in enumerate(parts):
        archive_path = ROOT.parent / f'commutator-completion-raw-20260915-part{i + 1:02d}.zip'
        with zipfile.ZipFile(archive_path, 'w') as archive:
          for path in part:
            name = str(path.relative_to(ROOT.parent))
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED if path.suffix == '.json' else zipfile.ZIP_STORED
            with path.open('rb') as source, archive.open(info, 'w', force_zip64=True) as target:
                for block in iter(lambda: source.read(1 << 20), b''):
                    target.write(block)
            members.append({'archive': archive_path.name, 'path': name, 'bytes': path.stat().st_size, 'sha256': digest(path)})
        archives.append({'archive': archive_path.name, 'bytes': archive_path.stat().st_size,
                         'sha256': digest(archive_path), 'members': len(part)})
    result = {'archives': archives, 'bytes': sum(a['bytes'] for a in archives), 'members': members,
              'reproduction': 'Extract beside a gc-discriminator repository source directory. '
              'The exact cache and original keyer/import dependencies go into sibling gc-pilot, while D2 tables and all per-record symbolic outputs '
              'go into gc-discriminator. Replay review/commutator_completion_independent.py there. '
              'For a fresh primary run preserve protocols but move existing records/, result.json, and freeze.json '
              'out of experiments/commutator_completion_20260915 before running scripts/commutator_completion.py. '
              'Pass --archive and --manifest to override the two original-cache locations. '
              'Record task timings on the new machine; bitwise scientific outputs and counts are the audit targets.'}
    manifest = UNIT / 'raw-archive.json'
    if manifest.exists():
        prior = json.loads(manifest.read_text())
        old = {a['sha256']: a for a in prior.get('archives', [])}
        for entry in result['archives']:
            for key in ('library_file_id', 'file_id', 'version'):
                if key in old.get(entry['sha256'], {}):
                    entry[key] = old[entry['sha256']][key]
    manifest.write_text(json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({'archives': archives, 'bytes': result['bytes'], 'members': len(members)}))


if __name__ == '__main__':
    main()
