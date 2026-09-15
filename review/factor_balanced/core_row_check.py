"""Direct core convention control on saved fresh arrays; no model fitting."""
import hashlib
import importlib.util
import json
from pathlib import Path
import time
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
UNIT=ROOT/'experiments/factor_balanced_interactions_20260915'
spec=importlib.util.spec_from_file_location('independent_core_ca',ROOT/'src/groovy/ca.py')
ca=importlib.util.module_from_spec(spec);spec.loader.exec_module(ca)
start=time.monotonic();cases=[]
for n in [17,18,20,21]:
 for rule in [0,18,30,54,90,110,126,204]:
  path=UNIT/'partitions'/f'n{n:02d}_r{rule:03d}.npz'
  with np.load(path,allow_pickle=False) as data:nxt=data['successor']
  states=sorted({0,1,2,3,(1<<n)//3,(1<<n)//5,(1<<n)//7,(1<<n)-1})
  for state in states:
   row=np.array([(state>>i)&1 for i in range(n)],dtype=np.uint8)
   output=ca.apply_rule(row,rule)
   code=sum(int(bit)<<i for i,bit in enumerate(output))
   assert code==int(nxt[state]),(n,rule,state)
  cases.append({'ring':n,'rule':rule,'source_states':states})
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
result={'status':'verified','cases':cases,'rows':sum(len(c['source_states']) for c in cases),'core_sha256':sha(ROOT/'src/groovy/ca.py'),'verifier_sha256':sha(Path(__file__)),'wall_seconds':time.monotonic()-start}
(Path(__file__).parent/'core-row-verification.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
