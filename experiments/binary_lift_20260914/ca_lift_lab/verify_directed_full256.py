"""Targeted independent verification spanning every rule and gate outcome."""
import json
from pathlib import Path
import verify_directed_reference_23_232 as verify
ROOT=Path(__file__).resolve().parent;RUN=ROOT/'runs/directed_full256';SEL=RUN/'independent_selected';SEL.mkdir(exist_ok=True)
rows=list(map(json.loads,(RUN/'candidates.jsonl').read_text().splitlines()));chosen={}
def sig(r):
    c=r['recipe'][0];return (r['rule'],c['mask'],c['shift'],r['reference'],tuple(r['order']))
for rule in range(256):
    rr=[r for r in rows if r['rule']==rule]
    for gate in ('first_order_pass','joint_raw','joint_centered'):
        r=next((x for x in rr if x[gate]),rr[0]);chosen[sig(r)]=r
(SEL/'candidates.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in chosen.values()))
verify.RUN=SEL;verify.main()
result=json.loads((SEL/'verification.json').read_text());result.update(selection='one success or failure representative per rule and gate',selected_records=len(chosen),full_census_records=len(rows))
(RUN/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
