"""Aggregate sharded Research032 symbolic causal-witness runs."""
from __future__ import annotations
import argparse,json,statistics
from collections import Counter
from pathlib import Path

EXPECTED_H3={(35,'00000001','2-6'),(49,'00000001','2-3'),(59,'01111111','1-5'),(115,'01111111','4-5')}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 shards=[json.loads(p.read_text()) for p in sorted(args.input_dir.rglob('*.json'))]
 shards=[x for x in shards if x.get('experiment')=='causal-witness-automaton']
 if not shards: raise SystemExit('no causal-witness-automaton shards')
 assert {x['schema'] for x in shards}=={1}
 assert {x['hmax'] for x in shards}=={5}
 assert {x['node_budget'] for x in shards}=={5_000_000}
 assert len({json.dumps(x['source_hashes'],sort_keys=True) for x in shards})==1
 coverage=[];rows=[]
 for x in shards:
  coverage += list(range(x['rule_start'],x['rule_end'])); rows += x['rows']
 assert sorted(coverage)==list(range(256)) and len(set(coverage))==256
 assert sorted(r['rule'] for r in rows)==list(range(256))
 events=[(r['rule'],e) for r in rows for e in r['events_h3_plus']]
 byh=Counter(e['horizon'] for _,e in events)
 h3={(r,e['target'],e['pair']) for r,e in events if e['horizon']==3}
 assert h3==EXPECTED_H3,(h3,EXPECTED_H3)
 assert byh[3]==4
 assert byh[4]==0,[(r,e) for r,e in events if e['horizon']==4][:20]
 fresh_h5=[{'rule':r,**e} for r,e in events if e['horizon']==5 and r>=64]
 pilot_h5=[{'rule':r,**e} for r,e in events if e['horizon']==5 and r<64]
 censored=[{'rule':r['rule'],**r['censored']} for r in rows if r['censored']]
 horizon_stats={}
 for h in range(6):
  rec=[(r['rule'],x) for r in rows for x in r['horizons'] if x['horizon']==h]
  if not rec: continue
  max_build=max(x['build_node_count'] for _,x in rec)
  horizon_stats[str(h)]={
   'rules_built':len(rec),
   'new_births':sum(x['new_births'] for _,x in rec),
   'median_build_nodes':statistics.median(x['build_node_count'] for _,x in rec),
   'max_build_nodes':max_build,
   'max_build_rule':next(rule for rule,x in rec if x['build_node_count']==max_build),
   'median_query_nodes':statistics.median(x['query_node_count'] for _,x in rec),
   'max_query_nodes':max(x['query_node_count'] for _,x in rec),
  }
 out={
  'ok':True,'experiment':'causal-witness-automaton-h5','rules':256,'hmax':5,'node_budget':5_000_000,
  'h3_regression_events':sorted([{'rule':r,'target':e['target'],'pair':e['pair']} for r,e in events if e['horizon']==3],key=lambda x:x['rule']),
  'h4_births':byh[4],
  'pilot_h5_births_rules_0_63':len(pilot_h5),
  'fresh_h5_births_rules_64_255':len(fresh_h5),
  'fresh_h5_events':fresh_h5,
  'censored':censored,
  'horizon_stats':horizon_stats,
  'unresolved_after_run':sum(r['unresolved_final'] for r in rows),
  'source_hashes':shards[0]['source_hashes'],
 }
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
 if censored: raise SystemExit('phase-1 census censored by node budget')
if __name__=='__main__':main()
