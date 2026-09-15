"""Independent archive integrity audit; intentionally external to archive."""
import hashlib
import json
from pathlib import Path
import time
import zipfile
ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT.parent/'factor-balanced-interactions-20260915.zip'
UNIT='experiments/factor_balanced_interactions_20260915/'
sha=lambda b:hashlib.sha256(b).hexdigest()
start=time.monotonic()
with zipfile.ZipFile(ARCHIVE) as z:
 names=z.namelist();assert len(names)==len(set(names))
 assert not any('.tmp.' in n or '__pycache__' in n for n in names)
 manifest_name=UNIT+'raw-manifest.json';manifest_bytes=z.read(manifest_name);manifest=json.loads(manifest_bytes)
 assert set(names)==set(manifest['files'])|{manifest_name}
 for name,digest in manifest['files'].items():
  data=z.read(name);assert sha(data)==digest,name
  assert sha((ROOT/name).read_bytes())==digest,(name,'local mismatch')
  if name.endswith('.npz'):
   with z.open(name) as handle:
    with zipfile.ZipFile(handle) as nested:assert nested.testzip() is None,name
 result=json.loads(z.read(UNIT+'confirmation-result.json'))
 arrays=[n for n in names if n.startswith(UNIT+'partitions/')]
 assert len(arrays)==32 and set(arrays)=={r['path'] for r in result['case_info']}
 for row in result['case_info']:assert manifest['files'][row['path']]==row['sha256']
 for name,digest in result['source_hashes'].items():assert manifest['files'][name]==digest,name
 review=[n for n in names if n.startswith('review/factor_balanced/')]
 required=['oracle.py','verify.py','fit-verification.json','cases-verification.json','fresh-independent-relations.json','score-verification.json','independent-review.md','author-crossreview.json','core_row_check.py','core-row-verification.json']
 assert all('review/factor_balanced/'+n in names for n in required)
 for stage in ['fit','score']:
  r=json.loads(z.read('review/factor_balanced/'+stage+'-verification.json'));assert r['status']=='verified'
  assert r['oracle_sha256']==manifest['files']['review/factor_balanced/oracle.py']
  assert r['verifier_sha256']==manifest['files']['review/factor_balanced/verify.py']
 output={'status':'verified','archive':str(ARCHIVE),'sha256':sha(ARCHIVE.read_bytes()),'bytes':ARCHIVE.stat().st_size,'members':len(names),'manifest_entries':len(manifest['files']),'manifest_sha256':sha(manifest_bytes),'canonical_fresh_arrays':32,'review_members':len(review),'all_member_hashes_match':True,'all_local_bytes_match':True,'all_nested_archives_valid':True,'temporary_members':0,'wall_seconds':time.monotonic()-start,'verifier_sha256':sha(Path(__file__).read_bytes())}
(ROOT/'review/factor-balanced-archive-check.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
print(json.dumps(output))
