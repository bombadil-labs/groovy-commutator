"""Target implementation risk: old rejected variants, independently cropped jets.
One fresh representative per rule and attained gate (all relevant rules, not a pilot).
"""
import json,sys
from pathlib import Path
import verify_binary_reference as verifier
ROOT=Path(__file__).resolve().parent
run=ROOT/'runs/binary_fresh_all256'
rows=list(map(json.loads,(run/'candidates.jsonl').read_text().splitlines()))
selected={}
for rule in range(256):
    fresh=[r for r in rows if r['rule']==rule and r.get('provenance')=='fresh_unfiltered']
    if not fresh:continue
    for gate in ('first_order_pass','joint_raw','joint_centered'):
        r=next((r for r in fresh if r[gate]),fresh[0])
        selected[(r['candidate'],r['reference'],tuple(r['order']))]=r
for r in selected.values():
    r['recipe'][0].update(offsets=[],geometry='straight')
target=run/'independent_selected';target.mkdir(exist_ok=True)
(target/'candidates.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in selected.values()))
sys.argv=['verify_binary_reference','--run',str(target)]
verifier.main()
