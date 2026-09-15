#!/usr/bin/env python3
"""Archive saved study inputs, raw arrays, scores, code, and independent review."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
UNIT=ROOT/'experiments/factor_balanced_interactions_20260915'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 paths={p for p in UNIT.rglob('*') if p.is_file() and p.name not in ('raw-archive.json','raw-manifest.json') and not p.name.endswith('.tmp.npz')}
 paths.update(p for p in (ROOT/'review/factor_balanced').glob('*') if p.is_file())
 paths.update(ROOT/p for p in ['scripts/factor_balanced_interactions.py','scripts/rule_ring_structure.py','scripts/rule_ring_selectors.py','scripts/summarize_factor_balanced.py','scripts/package_factor_balanced.py','scripts/plot_factor_balanced.py','results/factor_balanced_interactions_20260915.svg','results/factor_balanced_interactions_20260915.png','src/groovy/ca.py','experiments/rule_ring_structure_20260915/compact-relations.json','experiments/rule_ring_structure_20260915/raw-manifest.json','experiments/rule_ring_structure_20260915/raw-archive.json','docs/research/protocols/factor-balanced-interactions-20260915.md','docs/research/2026-09-15-factor-balanced-interactions.md'])
 files={str(p.relative_to(ROOT)):digest(p) for p in sorted(paths)}
 manifest={'schema':'factor-balanced-archive/v1','files':files,'excluded':'Canonical summary and external archive hash record avoid circular hashes.'}
 (UNIT/'raw-manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
 target=ROOT.parent/'factor-balanced-interactions-20260915.zip'
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(paths):z.write(p,str(p.relative_to(ROOT)))
  z.write(UNIT/'raw-manifest.json',str((UNIT/'raw-manifest.json').relative_to(ROOT)))
 with zipfile.ZipFile(target) as z:
  assert len(z.namelist())==len(files)+1==len(set(z.namelist()))
  for p,h in files.items():assert hashlib.sha256(z.read(p)).hexdigest()==h
 record={'file':target.name,'sha256':digest(target),'bytes':target.stat().st_size,'members':len(files)+1,'manifest_sha256':digest(UNIT/'raw-manifest.json')}
 (UNIT/'raw-archive.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
 print(json.dumps(record))
if __name__=='__main__':main()
