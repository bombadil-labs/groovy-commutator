#!/usr/bin/env python3
"""Lossless bundle of exact inputs, symbolic outputs and independent replay."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/commutator_relations_20260915'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    fixed = ['scripts/commutator_completion.py', 'scripts/commutator_relations.py',
             'scripts/package_commutator_relations.py', 'results/commutator_completion_20260915.json',
             'experiments/beam_discriminator_loop_20260915/round01/tables.npz',
             'experiments/beam_discriminator_loop_20260915/round01/result.json',
             'experiments/commutator_relations_20260915/protocol.md',
             'experiments/commutator_relations_20260915/protocol-freeze.json',
             'experiments/commutator_relations_20260915/recovery.md',
             'experiments/commutator_relations_20260915/execution-freeze.json',
             'experiments/commutator_relations_20260915/result.json',
             'experiments/commutator_relations_20260915/census.json',
             'experiments/commutator_relations_20260915/run.log',
             'experiments/commutator_relations_20260915/REPRODUCE.md',
             'review/gate1-review.md', 'review/replay_relations.py',
             'review/replay_portable.py', 'review/compare_relations.py',
             'review/comparison.json', 'review/replay.log', 'review/physical-replay-review.md']
    paths = [(ROOT / s, s) for s in fixed]
    paths += [(f, str(f.relative_to(ROOT))) for folder in (UNIT / 'records', ROOT / 'review/replay')
              for f in sorted(folder.iterdir()) if f.suffix in ('.npz', '.json')]
    paths += [(a.archive, 'inputs/uniform_jet6_rules.tar.gz'), (a.manifest, 'inputs/archive_manifest.json')]
    assert len(list((UNIT / 'records').glob('*.npz'))) == 78
    assert len(list((ROOT / 'review/replay').glob('*.npz'))) == 78
    members = []
    with zipfile.ZipFile(a.output, 'w') as z:
        for source, name in paths:
            assert source.is_file()
            info = zipfile.ZipInfo('gc-relations/' + name, date_time=(2026, 9, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED if source.suffix in ('.gz', '.npz') else zipfile.ZIP_DEFLATED
            with source.open('rb') as src, z.open(info, 'w', force_zip64=True) as dst:
                for block in iter(lambda: src.read(1 << 20), b''):
                    dst.write(block)
            members.append({'path': info.filename, 'bytes': source.stat().st_size, 'sha256': digest(source)})
    manifest = {'archive': a.output.name, 'bytes': a.output.stat().st_size, 'sha256': digest(a.output),
                'members': members, 'member_count': len(members),
                'complete_original_input_archive_included': True,
                'reproduction': 'Extract then read gc-relations/experiments/commutator_relations_20260915/REPRODUCE.md.'}
    (UNIT / 'raw-archive.json').write_text(json.dumps(manifest, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in manifest.items() if k != 'members'}))


if __name__ == '__main__':
    main()
