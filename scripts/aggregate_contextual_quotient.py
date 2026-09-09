"""Aggregate Research029 contextual-quotient and greedy-safety shards."""
from __future__ import annotations
import argparse,json,math
from collections import Counter
from pathlib import Path

TOL=1e-10
EXPECTED_FAILURES={(24,'01000010'),(24,'01000110'),(231,'01000010'),(231,'01100010')}
EXPECTED_QUOTIENTS={
 (24,'01000010'):'01230243',(231,'01000010'):'01230243',
 (24,'01000110'):'01230453',(231,'01100010'):'01230453',
}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 shards=[json.loads(p.read_text()) for p in sorted(args.input_dir.rglob('*.json'))]
 shards=[x for x in shards if x.get('experiment')=='contextual-quotient']
 if not shards:raise SystemExit('no contextual-quotient shards')
 if {x['schema'] for x in shards}!={1} or {x['ring_width'] for x in shards}!={12} or {x['block_size'] for x in shards}!={3} or {x['cadence'] for x in shards}!={3}:
  raise AssertionError('schema/domain mismatch')
 hashes={json.dumps(x['source_hashes'],sort_keys=True) for x in shards}
 if len(hashes)!=1:raise AssertionError('mixed source/protocol hashes')
 coverage=[];rows=[]
 for s in shards:
  coverage.extend(range(s['rule_start'],s['rule_end']));rows.extend(s['rows'])
 if sorted(coverage)!=list(range(256)) or len(set(coverage))!=256:raise AssertionError('rule coverage mismatch')
 targets=[t for r in rows for t in r['targets']]
 if len(targets)!=256*127:raise AssertionError(('target count',len(targets)))
 closed=[t for t in targets if t['closed']];nonclosed=[t for t in targets if not t['closed']]
 if len(closed)!=1656 or len(nonclosed)!=30856:raise AssertionError({'closed':len(closed),'nonclosed':len(nonclosed)})
 closed_rules=len({t['rule'] for t in closed})
 if closed_rules!=141:raise AssertionError(('closed rules',closed_rules))

 cf={(t['rule'],t['target']) for t in nonclosed if not t['canonical_optimal']}
 if cf!=EXPECTED_FAILURES:raise AssertionError({'canonical failure mismatch':sorted(cf)})
 for t in nonclosed:
  key=(t['rule'],t['target'])
  if key in EXPECTED_QUOTIENTS and t['quotient']!=EXPECTED_QUOTIENTS[key]:
   raise AssertionError((key,t['quotient'],EXPECTED_QUOTIENTS[key]))
 failures=[t for t in nonclosed if not t['canonical_optimal']]
 if any(t['canonical_first_unsafe'] is None or abs(t['canonical_first_unsafe']['margin'])>TOL for t in failures):
  raise AssertionError('known failures are not zero-margin under direct quotient')
 if any(t['canonical_strict_negative_steps'] for t in nonclosed):
  raise AssertionError('strictly negative canonical safety margin found despite frozen Research028 failure family')

 cost_fail=[t for t in nonclosed if not t['cost_optimal']]
 path_diff=[t for t in nonclosed if t['paths_differ']]
 diff_both=[t for t in path_diff if t['canonical_optimal'] and t['cost_optimal']]
 success=[t for t in nonclosed if t['canonical_optimal']]
 finite_abs=[t['canonical_min_abs_margin'] for t in success if t['canonical_min_abs_margin'] is not None]
 positive=[t['canonical_min_positive_margin'] for t in success if t['canonical_min_positive_margin'] is not None]
 near={str(x):sum(v<x for v in finite_abs) for x in (1e-6,1e-4,1e-2)}
 quotient_classes=Counter(len(set(t['quotient'])) for t in nonclosed)
 by_class={}
 for cls in ('I','II','III','IV'):
  g=[t for t in nonclosed if t['wclass']==cls]
  by_class[cls]={'cases':len(g),'canonical_failures':sum(not t['canonical_optimal'] for t in g),'cost_failures':sum(not t['cost_optimal'] for t in g),
                 'path_differences':sum(t['paths_differ'] for t in g)}
 by_balance={}
 for bal in (1,2,3,4):
  g=[t for t in nonclosed if min(t['target'].count('0'),t['target'].count('1'))==bal]
  by_balance[str(bal)]={'cases':len(g),'canonical_failures':sum(not t['canonical_optimal'] for t in g),'cost_failures':sum(not t['cost_optimal'] for t in g),
                       'path_differences':sum(t['paths_differ'] for t in g)}
 summary={
  'ok':True,'experiment':'contextual-quotient','ring_width':12,'block_size':3,'cadence':3,'rules':256,'target_cases':len(targets),
  'closed_targets':len(closed),'nonclosed_targets':len(nonclosed),'closed_fine_rules':closed_rules,
  'canonical_failures':len(failures),'canonical_failure_cases':sorted([{'rule':t['rule'],'target':t['target'],'quotient':t['quotient'],'margin':t['canonical_first_unsafe']['margin']} for t in failures],key=lambda x:(x['rule'],x['target'])),
  'strict_negative_margin_cases':sum(t['canonical_strict_negative_steps']>0 for t in nonclosed),
  'canonical_zero_margin_steps':sum(t['canonical_zero_margin_steps'] for t in nonclosed),
  'cost_aware_failures':len(cost_fail),'cost_aware_prediction_pass':len(cost_fail)==0,
  'cost_aware_failure_cases':sorted([{'rule':t['rule'],'target':t['target'],'quotient':t['quotient'],'first_unsafe':t['cost_first_unsafe']} for t in cost_fail],key=lambda x:(x['rule'],x['target'])),
  'cost_aware_zero_margin_steps':sum(t['cost_zero_margin_steps'] for t in nonclosed),
  'paths_differ':len(path_diff),'paths_differ_but_both_optimal':len(diff_both),
  'successful_canonical_near_zero_min_abs_margin':near,
  'minimum_positive_canonical_safety_margin':min(positive) if positive else None,
  'quotient_class_count_distribution':{str(k):v for k,v in sorted(quotient_classes.items())},
  'by_wolfram_class_exploratory':by_class,'by_target_balance':by_balance,
  'source_hashes':shards[0]['source_hashes']}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
