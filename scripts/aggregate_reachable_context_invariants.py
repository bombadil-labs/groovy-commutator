"""Aggregate exact sharded Research033 reachable-context invariant results."""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path
TOTAL=52712;CONGRUENCE=47352;RESIDUAL=5360
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();sh=[json.loads(p.read_text()) for p in sorted(a.input_dir.rglob('*.json'))];sh=[x for x in sh if x.get('experiment')=='reachable-context-invariants']
 if not sh:raise SystemExit('no Research033 shards')
 assert {x['schema'] for x in sh}=={1} and {x['block_size'] for x in sh}=={3} and {x['cadence'] for x in sh}=={3};assert len({json.dumps(x['source_hashes'],sort_keys=True) for x in sh})==1
 cov=[];rows=[]
 for x in sh:cov+=list(range(x['rule_start'],x['rule_end']));rows+=x['rows']
 assert sorted(cov)==list(range(256)) and len(set(cov))==256 and sorted(r['rule'] for r in rows)==list(range(256))
 absent=sum(r['finite_witness_absent_through_h3'] for r in rows);con=sum(r['congruence_certified'] for r in rows);res=sum(r['noncongruence_residual'] for r in rows);langs=sum(r['residual_seed_languages'] for r in rows);sym=sum(r['new_symbol_certificates'] for r in rows);edge=sum(r['edge_certificates'] for r in rows);only=sum(r['edge_only_certificates'] for r in rows);left=sum(r['remaining_after_edge'] for r in rows)
 assert (absent,con,res)==(TOTAL,CONGRUENCE,RESIDUAL);assert edge>=sym and only==edge-sym and left==res-edge
 first_sym=first_edge=first_left=None;sent=[];newclass=Counter();leftclass=Counter()
 for r in rows:
  for l in r['languages']:
   base={'rule':r['rule'],'wclass':r['wclass'],'pair':l['pair'],'pair_index':l['pair_index'],'generated_symbol_count':l['generated_symbol_count'],'symbol_rounds':l['symbol_rounds'],'generated_edge_count':l['generated_edge_count'],'edge_rounds':l['edge_rounds']}
   for tid in l['symbol_certified_target_ids']:
    newclass[r['wclass']]+=1
    if first_sym is None:first_sym={**base,'target_id':tid,'level':'symbol','generated_symbols':l['generated_symbols']}
   for tid in l['edge_only_target_ids']:
    newclass[r['wclass']]+=1
    if first_edge is None:first_edge={**base,'target_id':tid,'level':'edge-only','edge_rows_hex':l['edge_rows_hex']}
   for tid in l['unresolved_target_ids']:
    leftclass[r['wclass']]+=1
    if first_left is None:first_left={**base,'target_id':tid,'level':'unresolved','edge_rows_hex':l['edge_rows_hex']}
   if r['rule'] in (122,161):sent.append({**base,'residual_target_ids':l['residual_target_ids'],'symbol_certified_target_ids':l['symbol_certified_target_ids'],'edge_certified_target_ids':l['edge_certified_target_ids'],'unresolved_target_ids':l['unresolved_target_ids']})
 out={'ok':True,'experiment':'reachable-context-invariants','rules':256,'block_size':3,'cadence':3,'target_count':127,'finite_witness_absent_through_h6':absent,'research032_congruence_certified':con,'research032_noncongruence_residual':res,'distinct_rule_seed_languages':langs,'new_generated_symbol_certificates':sym,'generated_edge_certificates':edge,'edge_only_certificates':only,'remaining_after_edge':left,'resolved_fraction_of_r032_residual_by_edge':edge/res,'remaining_fraction_of_r032_residual':left/res,'primary_hypotheses':{'generated_symbol_improves_on_congruence':sym>0,'edge_strictly_improves_on_symbol':edge>sym},'new_certificates_by_wolfram_class':dict(sorted(newclass.items())),'remaining_by_wolfram_class':dict(sorted(leftclass.items())),'first_symbol_certificate':first_sym,'first_edge_only_certificate':first_edge,'first_unresolved':first_left,'rule122_161_sentinels':sent,'source_hashes':sh[0]['source_hashes']};a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
