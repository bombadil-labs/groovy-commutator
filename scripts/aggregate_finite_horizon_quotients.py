"""Aggregate exact sharded Research030 finite-horizon quotient results."""
from __future__ import annotations
import argparse,json,statistics
from collections import Counter
from pathlib import Path

FATAL={(24,'01000010'),(24,'01000110'),(231,'01000010'),(231,'01100010')}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 shards=[json.loads(p.read_text()) for p in sorted(args.input_dir.rglob('*.json'))]
 shards=[x for x in shards if x.get('experiment')=='finite-horizon-quotients']
 if not shards:raise SystemExit('no finite-horizon quotient shards')
 assert {x['schema'] for x in shards}=={1};assert {x['ring_width'] for x in shards}=={12};assert {x['block_size'] for x in shards}=={3};assert {x['cadence'] for x in shards}=={3}
 assert len({json.dumps(x['source_hashes'],sort_keys=True) for x in shards})==1
 coverage=[];rr=[]
 for x in shards:coverage+=list(range(x['rule_start'],x['rule_end']));rr+=x['rows']
 assert sorted(coverage)==list(range(256)) and len(set(coverage))==256
 assert sorted(r['rule'] for r in rr)==list(range(256))
 targets=[t for r in rr for t in r['targets']];non=[t for t in targets if not t['closed']];closed=[t for t in targets if t['closed']]
 assert len(targets)==32512 and len(closed)==1656 and len(non)==30856
 assert sum(any(t['closed'] for t in r['targets']) for r in rr)==141
 assert all(t['quotient_discovery_time']<=t['hstar'] for t in targets)
 assert all(t['change_chain'][-1]['quotient']==t['final_quotient'] for t in targets)
 early=sum(t['quotient_early'] for t in non);halfq=sum(t['quotient_by_half_hstar'] for t in non);halfinfo=sum(t['half_info_before_half_hstar'] for t in non)
 dqdist=Counter(t['quotient_discovery_time'] for t in non);chainlen=Counter(len(t['change_chain']) for t in non);finalclasses=Counter(len(set(t['final_quotient'])) for t in non);ratios=[t['dq_over_hstar'] for t in non]
 byclass={}
 for c in ('I','II','III','IV'):
  g=[t for t in non if t['wclass']==c]
  byclass[c]={'nonclosed':len(g),'early_count':sum(t['quotient_early'] for t in g),'early_fraction':sum(t['quotient_early'] for t in g)/len(g),'median_dq_over_hstar':statistics.median(t['dq_over_hstar'] for t in g),'half_info_before_half_hstar_count':sum(t['half_info_before_half_hstar'] for t in g),'half_info_before_half_hstar_fraction':sum(t['half_info_before_half_hstar'] for t in g)/len(g)}
 long=[t for t in non if t['hstar']>=10]
 fatal=[]
 for t in non:
  if (t['rule'],t['target']) in FATAL:fatal.append({'rule':t['rule'],'target':t['target'],'hstar':t['hstar'],'dQ':t['quotient_discovery_time'],'final_quotient':t['final_quotient'],'bridge_1_6_birth':t.get('fatal_bridge_1_6_birth'),'change_chain':t['change_chain']})
 assert len(fatal)==4
 maxh=max(t['hstar'] for t in non);extremes=[]
 for t in sorted((x for x in non if x['hstar']==maxh),key=lambda x:(x['rule'],x['target'])):extremes.append({'rule':t['rule'],'wclass':t['wclass'],'target':t['target'],'hstar':t['hstar'],'dQ':t['quotient_discovery_time'],'dq_over_hstar':t['dq_over_hstar'],'change_chain':t['change_chain']})
 summary={'ok':True,'experiment':'finite-horizon-quotients','ring_width':12,'block_size':3,'cadence':3,'target_cases':len(targets),'closed_targets':len(closed),'nonclosed_targets':len(non),'closed_fine_rules':141,'early_quotient_count':early,'early_quotient_fraction':early/len(non),'quotient_by_half_hstar_count':halfq,'quotient_by_half_hstar_fraction':halfq/len(non),'half_info_before_half_hstar_count':halfinfo,'half_info_before_half_hstar_fraction':halfinfo/len(non),'quotient_discovery_time_distribution':{str(k):v for k,v in sorted(dqdist.items())},'max_quotient_discovery_time':max(dqdist),'median_dq_over_hstar':statistics.median(ratios),'mean_dq_over_hstar':statistics.mean(ratios),'max_hstar':maxh,'change_chain_length_distribution':{str(k):v for k,v in sorted(chainlen.items())},'final_quotient_class_distribution':{str(k):v for k,v in sorted(finalclasses.items())},'long_memory_hstar_ge_10':{'cases':len(long),'all_early':all(t['quotient_early'] for t in long),'all_dq_one':all(t['quotient_discovery_time']==1 for t in long),'median_dq_over_hstar':statistics.median(t['dq_over_hstar'] for t in long)},'by_wolfram_class':byclass,'fatal_synergy_cases':fatal,'max_hstar_cases':extremes,'source_hashes':shards[0]['source_hashes']}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
