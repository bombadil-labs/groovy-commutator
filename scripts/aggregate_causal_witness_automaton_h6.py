"""Aggregate the fresh Research032 horizon-6 symbolic causal-witness pass."""
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
 assert {x['schema'] for x in shards}=={1};assert {x['hmax'] for x in shards}=={6};assert {x['node_budget'] for x in shards}=={5_000_000}
 assert len({json.dumps(x['source_hashes'],sort_keys=True) for x in shards})==1
 coverage=[];rows=[]
 for x in shards: coverage+=list(range(x['rule_start'],x['rule_end']));rows+=x['rows']
 assert sorted(coverage)==list(range(256)) and len(set(coverage))==256
 events=[(r['rule'],e) for r in rows for e in r['events_h3_plus']]
 byh=Counter(e['horizon'] for _,e in events)
 h3={(r,e['target'],e['pair']) for r,e in events if e['horizon']==3}
 assert h3==EXPECTED_H3 and byh[3]==4
 assert byh[4]==0 and byh[5]==0
 h6=[{'rule':r,**e} for r,e in events if e['horizon']==6]
 censored=[{'rule':r['rule'],**r['censored']} for r in rows if r['censored']]
 rec=[(r['rule'],x) for r in rows for x in r['horizons'] if x['horizon']==6]
 if rec:
  max_build=max(x['build_node_count'] for _,x in rec)
  h6stats={'rules_built':len(rec),'new_births':sum(x['new_births'] for _,x in rec),'median_build_nodes':statistics.median(x['build_node_count'] for _,x in rec),'max_build_nodes':max_build,'max_build_rule':next(rule for rule,x in rec if x['build_node_count']==max_build),'median_query_nodes':statistics.median(x['query_node_count'] for _,x in rec),'max_query_nodes':max(x['query_node_count'] for _,x in rec)}
 else: h6stats={}
 out={'ok':True,'complete':not censored,'experiment':'causal-witness-automaton-h6','rules':256,'hmax':6,'node_budget':5_000_000,'h3_regression_count':byh[3],'h4_births':byh[4],'h5_births':byh[5],'fresh_h6_births':len(h6),'fresh_h6_events':h6,'censored':censored,'h6_state_growth':h6stats,'unresolved_after_run':sum(r['unresolved_final'] for r in rows),'source_hashes':shards[0]['source_hashes']}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
