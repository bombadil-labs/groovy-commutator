"""Finish the existential parent-zero check for unresolved centered paths."""
import argparse,json,time
from pathlib import Path
import numpy as np
from audit_recursive_binary import build,child_keys,groups,solve_g
root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=root/'runs/recursive_binary_3d_v2');ap.add_argument('--output',type=Path,default=root/'runs/recursive_binary_centering_alternatives');args=ap.parse_args()
prior=args.input;out=args.output;out.mkdir(exist_ok=False,parents=True)
rows=list(map(json.loads,(prior/'candidates.jsonl').read_text().splitlines()));tested=[];start=time.perf_counter()
for record in rows:
    if not record['first_order_pass'] or record['recursive_G']['passes'] or record['recursive_G']['mode']!='centered':continue
    rec=record['first_floor'];used=record['recursive_G']['parent_zero']
    for z,b in enumerate(rec['centered_branches']):
        if z==used or not b['passes']:continue
        s,states,pa,kids,mid=build(rec);bk=child_keys(kids[0],mid)
        targets={'native':(kids[0]^kids[1])[...,mid],'source':np.broadcast_to(s[:,mid,None,None],(len(s),4,4)),'parent':np.broadcast_to(pa[0][:,None,:,mid],(len(s),4,4))}
        unique,first,inv,vals,gates=groups(bk,targets)
        r=record.copy();r['recursive_G']=solve_g(rec,s,states,pa,kids,mid,bk,unique,vals,parent_zero_override=z);tested.append(r)
        print(json.dumps({'rule':rec['rule'],'parent_zero':z,'passes':r['recursive_G']['passes']}),flush=True)
(out/'candidates.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in tested));(out/'manifest.json').write_text(json.dumps({'seconds':time.perf_counter()-start,'rules':len(tested)},indent=2)+'\n')
