#!/usr/bin/env python3
"""Preserve all raw arrays and the immutable input in bounded-size ZIP volumes."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];UNIT=ROOT/'experiments/beam_discriminator_loop_20260915'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 files=[(p,str(p.relative_to(ROOT.parent))) for p in sorted(UNIT.glob('round*/*.npz'))]
 p=ROOT.parent/'gc-pilot/experiments/uniform_jet6_cache_20260914/run/uniform_jet6_rules.tar.gz';files.append((p,str(p.relative_to(ROOT.parent))))
 groups=[[]];sizes=[0]
 for p,name in files:
  if groups[-1] and sizes[-1]+p.stat().st_size>300*1024**2:groups.append([]);sizes.append(0)
  groups[-1].append((p,name));sizes[-1]+=p.stat().st_size
 manifest={'format':'ZIP_STORED; individual NPZ and input TAR.GZ members already compressed','extraction':'Extract every volume into one parent directory; gc-discriminator and gc-pilot paths match the frozen runners. The repository supplies scripts and text records.','volumes':[]}
 for i,group in enumerate(groups,1):
  path=ROOT.parent/f'beam-loop-raw-20260915-part{i}.zip';members=[]
  with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_STORED) as z:
   for p,name in group:
    z.write(p,name);members.append({'path':name,'sha256':sha(p),'bytes':p.stat().st_size})
  manifest['volumes'].append({'filename':path.name,'bytes':path.stat().st_size,'sha256':sha(path),'members':members});print(path.name,path.stat().st_size,len(members),flush=True)
 (UNIT/'raw-archive.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
