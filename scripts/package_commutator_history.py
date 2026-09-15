#!/usr/bin/env python3
"""Preserve exact input trajectories and the output histories/count tables."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT/'experiments/commutator_history_20260915'


def main():
    paths = [ROOT/'experiments/beam_discriminator_loop_20260915'/f'round{n:02d}/trajectories.npz'
             for n in (6, 10)] + [UNIT/'histories-and-counts.npz', UNIT/'response-arrays.npz']
    target = ROOT.parent/'commutator-history-raw-20260915.zip'
    members = []
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_STORED) as archive:
        for path in paths:
            data = path.read_bytes()
            name = 'gc-discriminator/'+str(path.relative_to(ROOT))
            entry = zipfile.ZipInfo(name, date_time=(2026, 9, 15, 0, 0, 0))
            archive.writestr(entry, data)
            members.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    manifest = {'archive': target.name, 'bytes': target.stat().st_size,
                'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'members': members,
                'reproduction': 'Extract beside a gc-discriminator directory containing the repository sources. '
                'For a fresh run, move completed generated outputs out of experiments/commutator_history_20260915, '
                'preserving protocol.md, protocol-freeze.json, response-protocol.md and response-protocol-freeze.json. '
                'Run scripts/commutator_history.py first, then scripts/commutator_response.py after result.json exists. '
                'Keep the archived original input arrays in their recorded paths.'}
    manifest_path = UNIT/'raw-archive.json'
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text())
        if previous.get('sha256') == manifest['sha256']:
            for key in ('library_file_id', 'file_id', 'version'):
                if key in previous:
                    manifest[key] = previous[key]
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'archive': str(target), 'bytes': manifest['bytes'], 'members': len(members)}))


if __name__ == '__main__':
    main()
