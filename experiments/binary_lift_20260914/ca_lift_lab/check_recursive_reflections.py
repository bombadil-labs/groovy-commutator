"""Mirror successful fixed paths into failed source IDs; no parameter search."""
import argparse,json,time
from pathlib import Path
import numpy as np
from audit_recursive_binary import build,child_keys,groups,solve_g
root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=root/'runs/recursive_binary_3d_v2');ap.add_argument('--output',type=Path,default=root/'runs/recursive_binary_reflections');args=ap.parse_args()
prior=args.input;out=args.output;out.mkdir(exist_ok=False,parents=True)
rows=list(map(json.loads,(prior/'candidates.jsonl').read_text().splitlines()));old=list(map(json.loads,(root/'runs/binary_reference_4rows/candidates.jsonl').read_text().splitlines()))
def mirror(r):return sum(((r>>(((i&1)<<2)|(i&2)|((i>>2)&1)))&1)<<i for i in range(8))
success={r['rule']for r in rows if r['recursive_G']['passes']};tested=[];start=time.perf_counter()
for record in rows:
    if not record['recursive_G']['passes'] or mirror(record['rule'])in success:continue
    first=record['first_floor'];rule=mirror(record['rule']);left,right=map(int,first['reference'].split(':')[1:]);q=f'pair:{-right}:{-left}'
    matches=[r for r in old if r['rule']==rule and r['ry']==2 and r['recipe'][0]['mask']==first['recipe'][0]['mask'] and r['recipe'][0]['shift']==-first['recipe'][0]['shift'] and r['reference']==q and r['order']==first['order']]
    assert len(matches)==1;rec=matches[0]
    assert rec['joint_raw'] if record['recursive_G']['mode']=='raw' else rec['joint_centered']
    s,states,pa,kids,mid=build(rec);bk=child_keys(kids[0],mid)
    targets={'native':(kids[0]^kids[1])[...,mid],'source':np.broadcast_to(s[:,mid,None,None],(len(s),4,4)),'parent':np.broadcast_to(pa[0][:,None,:,mid],(len(s),4,4))}
    unique,first_indices,inv,vals,gates=groups(bk,targets);good=all(v['passes']for v in gates.values());assert good
    g=solve_g(rec,s,states,pa,kids,mid,bk,unique,vals);assert g['passes']
    r={'rule':rule,'mirrored_from_rule':record['rule'],'first_floor':rec,'source_width':s.shape[-1],'source_origin_index':mid,'gates':gates,'first_order_pass':good,'recursive_G':g};tested.append(r)
    print(json.dumps({'rule':rule,'mirrored_from':record['rule'],'passes':g['passes'],'recipe':rec['recipe'],'reference':q,'order':rec['order']}),flush=True)
(out/'candidates.jsonl').write_text(''.join(json.dumps(r)+'\n'for r in tested));(out/'manifest.json').write_text(json.dumps({'seconds':time.perf_counter()-start,'rules':len(tested),'operation':'horizontal reflection of already successful source/rule/recipe'},indent=2)+'\n')
