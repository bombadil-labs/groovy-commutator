#!/usr/bin/env python3
"""Author's separate vectorized check of the reviewer's post-hoc period result."""
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
UNIT=ROOT/'experiments/observation_catalog_20260915'
expected=json.loads((ROOT/'review/catalog-replay/period-witnesses.json').read_text())
rows=[]
for item in expected:
    key=f'w8_r{item["rule"]:03d}_d{item["dimension"]}'
    with np.load(UNIT/'inputs/relations'/f'{key}.npz') as q,np.load(UNIT/'lift'/f'{key}.npz') as g:
        representatives=q['orbit_representatives']
        symbols=q['finite_symbol'].ravel()[representatives]
        labels,counts=np.unique(symbols[symbols>0],return_counts=True)
        repeated=labels[counts>1]
        endpoints=np.isin(symbols,repeated)
        sources=g['event_source'][endpoints]
        roots=g['root'][sources]
        assert np.all(np.all(roots==np.roll(roots,4,axis=1),axis=1))
        assert not np.any(np.all(roots==np.roll(roots,2,axis=1),axis=1))
        assert not np.any(np.all(roots==np.roll(roots,1,axis=1),axis=1))
        pairs=int(np.sum(counts.astype(np.int64)*(counts-1)//2))
        assert pairs==item['total_pairs']==item['pair_period_counts'][0]['pairs']
        assert item['pair_period_counts'][0]['periods']==[4,4]
        rows.append({'rule':item['rule'],'dimension':item['dimension'],'pairs':pairs,
                     'all_repeated_block_endpoints_have_minimal_period_four':True})
out={'author':'Codex (OpenAI), /root','scope':'Independent vectorized check of post-hoc endpoint claim; source review of oracle and comparison code completed separately.',
     'cases':rows,'agree':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'independent_period_output_sha256':hashlib.sha256((ROOT/'review/catalog-replay/period-witnesses.json').read_bytes()).hexdigest()}
(ROOT/'review/catalog-author-crossreview.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
