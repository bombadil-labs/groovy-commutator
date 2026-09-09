"""Stratified exact audit of the Research029 future-context quotient.

For selected block-3 targets, re-enumerates the complete Research028 refinement
interval and verifies that the direct contextual quotient is the unique global
minimum-entropy closed encoder.
"""
from __future__ import annotations

import argparse,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'scripts'))
from experiment_history_lift_closure import state_map  # noqa:E402
from experiment_block3_representation_design import (  # noqa:E402
    TARGETS,interval,block_codes,ObservationCache,target_future,node_metrics,pkey
)
from experiment_contextual_quotient import contextual_quotient  # noqa:E402

N=12;TOL=1e-9
CASES=[
 (24,'01000010'),(24,'01000110'),(231,'01000010'),(231,'01100010'),
 (30,'01111111'),(30,'00111111'),(30,'00011111'),(30,'00001111'),
 (110,'01111111'),(110,'00111111'),(110,'00011111'),(110,'00001111'),
]
TARGET_BY_KEY={pkey(t):t for t in TARGETS}

def audit_case(rule,key):
 target=TARGET_BY_KEY[key];e=state_map(rule,N);step=e[e[e]];oc=ObservationCache(block_codes(N))
 fut=target_future(step,oc.get(target),128);cinf=fut['labels'];classes=fut['classes'];ints=interval(target)
 nodes={p:node_metrics(p,oc.get(p),cinf,classes,N//3) for p in ints}
 ht=nodes[target]['H_encoder'];closed=[p for p in ints if nodes[p]['closed']]
 min_added=min(nodes[p]['H_encoder']-ht for p in closed)
 opts=sorted((p for p in closed if abs((nodes[p]['H_encoder']-ht)-min_added)<TOL),key=pkey)
 q=contextual_quotient(cinf);qm=nodes[q];qadded=qm['H_encoder']-ht
 return {'rule':rule,'target':key,'interval_nodes':len(ints),'quotient':pkey(q),'quotient_closed':qm['closed'],
         'quotient_added_bits':qadded,'global_min_added_bits':min_added,'global_optima':[pkey(p) for p in opts],
         'quotient_unique_global_optimum':len(opts)==1 and opts[0]==q,
         'passes':qm['closed'] and abs(qadded-min_added)<TOL and len(opts)==1 and opts[0]==q}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 rows=[audit_case(r,t) for r,t in CASES];out={'ok':all(x['passes'] for x in rows),'method':'full Research028 interval enumeration vs direct future-context quotient','cases':rows}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
 if not out['ok']:raise SystemExit(1)
if __name__=='__main__':main()
