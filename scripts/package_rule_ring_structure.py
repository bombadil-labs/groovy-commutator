#!/usr/bin/env python3
"""Preserve this study's raw data and code; no scientific recomputation."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT/'experiments/rule_ring_structure_20260915'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    # The archive excludes its own external hash record and the canonical
    # summary (which pins that hash). This avoids a self-referential checksum.
    paths = {p for p in UNIT.rglob('*') if p.is_file() and p.name not in ('raw-archive.json','raw-manifest.json')}
    paths.update(p for p in (ROOT/'review/rule_ring_structure').glob('*') if p.is_file())
    paths.update(ROOT/p for p in [
        'scripts/rule_ring_structure.py','scripts/rule_ring_selectors.py',
        'scripts/summarize_rule_ring_structure.py','scripts/package_rule_ring_structure.py',
        'scripts/import_observation_catalog.py','scripts/test_rule_ring_selectors.py','src/groovy/ca.py',
        'docs/tools/rule-ring-selectors.md','docs/research/2026-09-15-rule-ring-structure.md',
        'docs/research/protocols/rule-ring-structure-20260915.md',
        'results/rule_ring_structure_20260915.svg','results/rule_ring_structure_20260915.png'])
    files = {str(p.relative_to(ROOT)):digest(p) for p in sorted(paths)}
    manifest = {'schema':'rule-ring-structure-archive/v1','files':files,
                'excluded':'Archive hash record and canonical summary are external to avoid circular checksums.'}
    (UNIT/'raw-manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    archive = ROOT.parent/'rule-ring-structure-20260915.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as output:
        for p in sorted(paths):output.write(p,str(p.relative_to(ROOT)))
        output.write(UNIT/'raw-manifest.json',str((UNIT/'raw-manifest.json').relative_to(ROOT)))
    with zipfile.ZipFile(archive) as saved:
        assert len(saved.namelist()) == len(set(saved.namelist())) == len(files)+1
        for name, expected in files.items():
            assert hashlib.sha256(saved.read(name)).hexdigest() == expected
    record = {'file':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,
              'members':len(files)+1,'manifest_sha256':digest(UNIT/'raw-manifest.json')}
    (UNIT/'raw-archive.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps(record))


if __name__ == '__main__':main()
