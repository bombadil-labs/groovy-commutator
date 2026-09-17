#!/usr/bin/env python3
"""Fast integrity tier for the 2026-09-16/17 handoff records (added 2026-09-17).

Three record sets entered the repository from Myk's GPT-session handoff rather
than from a run in this tree, so they carry their own manifests instead of a
`source_hashes` block. This check recomputes every hash those manifests
record. It establishes that the committed bytes are the bytes that were handed
over; it does not inspect result content, and it does not (cannot) recover the
2026-09-16 discriminator's lost protocol/runner bytes, whose absence the
reconstruction bundle declares explicitly.

  experiments/cross_dimensional_class4_20260917/MANIFEST.sha256   (GPT's overlay)
  experiments/jev_class4_20260916/manifest.json                   (Myk's Jev workspace, as packaged)
  experiments/jev_class4_20260916/manifest_integration.json       (raw responses + Run-3 materials)
  experiments/class4_selective_persistence_20260916/HASH_MANIFEST.json (GPT's reconstruction bundle)

Usage: python scripts/verify_handoff_manifests.py
"""
from __future__ import annotations
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]

def sha(p: pathlib.Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def check_sha256sum(manifest: pathlib.Path) -> list[str]:
    base = manifest.parent
    # The overlay manifest was written at the overlay root with repo-relative
    # paths; docs/ and results/ entries resolve against the repository root,
    # experiments/ entries against the repository root as well.
    problems = []
    for line in manifest.read_text().splitlines():
        if not line.strip(): continue
        digest, _, name = line.partition('  ')
        name = name.strip().lstrip('./')
        p = ROOT / name
        if not p.exists():
            # root-level records were moved into the experiment directory
            alt = base / pathlib.Path(name).name
            if alt.exists(): p = alt
        if not p.exists(): problems.append(f'{manifest.name}: {name} missing'); continue
        if sha(p) != digest: problems.append(f'{manifest.name}: {name} hash mismatch')
    return problems

def check_json_manifest(manifest: pathlib.Path) -> list[str]:
    base = manifest.parent
    problems = []
    for name, rec in json.loads(manifest.read_text()).items():
        p = base / name
        if not p.exists(): problems.append(f'{manifest.name}: {name} missing'); continue
        if sha(p) != rec['sha256']: problems.append(f'{manifest.name}: {name} hash mismatch')
        if 'bytes' in rec and p.stat().st_size != rec['bytes']: problems.append(f'{manifest.name}: {name} size mismatch')
    return problems

def main() -> int:
    problems = []
    problems += check_sha256sum(ROOT / 'experiments/cross_dimensional_class4_20260917/MANIFEST.sha256')
    problems += check_json_manifest(ROOT / 'experiments/jev_class4_20260916/manifest.json')
    problems += check_json_manifest(ROOT / 'experiments/jev_class4_20260916/manifest_integration.json')
    problems += check_json_manifest(ROOT / 'experiments/class4_selective_persistence_20260916/HASH_MANIFEST.json')
    for p in problems: print('FAIL', p)
    print('OK   handoff manifests' if not problems else f'{len(problems)} problem(s)')
    return 1 if problems else 0

if __name__ == '__main__':
    sys.exit(main())
