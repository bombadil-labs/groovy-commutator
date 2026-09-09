"""Aggregate exact sharded Research028 block-3 representation-design results."""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path

EXPECTED_TARGETS=127
EXPECTED_CANONICAL_CLOSURES=1656
EXPECTED_NONCLOSED=256*127-EXPECTED_CANONICAL_CLOSURES


def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    files=sorted(args.input_dir.rglob('*.json'))
    shards=[json.loads(p.read_text()) for p in files]
    shards=[x for x in shards if x.get('experiment')=='block3-representation-design']
    if not shards: raise SystemExit('no block3 representation-design shard JSON found')
    schemas={x['schema'] for x in shards};widths={x['ring_width'] for x in shards};cadences={x['cadence'] for x in shards}
    hashes={json.dumps(x['source_hashes'],sort_keys=True) for x in shards}
    if schemas!={1} or widths!={12} or cadences!={3} or len(hashes)!=1:
        raise AssertionError({'schemas':schemas,'widths':widths,'cadences':cadences,'hash_sets':len(hashes)})
    rules=[];rows=[]
    for s in shards:
        if s['target_count']!=EXPECTED_TARGETS: raise AssertionError(('target_count',s['target_count']))
        rules.extend(s['rules']);rows.extend(s['rows'])
    if sorted(rules)!=list(range(256)) or len(set(rules))!=256:
        raise AssertionError('shards do not cover every ECA rule exactly once')
    if sorted(r['rule'] for r in rows)!=list(range(256)):
        raise AssertionError('row coverage mismatch')
    targets=[t for r in rows for t in r['targets']]
    if len(targets)!=256*EXPECTED_TARGETS: raise AssertionError(len(targets))
    closed=[t for t in targets if t['closed']];nonclosed=[t for t in targets if not t['closed']]
    if len(closed)!=EXPECTED_CANONICAL_CLOSURES or len(nonclosed)!=EXPECTED_NONCLOSED:
        raise AssertionError({'closed':len(closed),'nonclosed':len(nonclosed)})
    closed_rules=len({t['rule'] for t in closed})
    if closed_rules!=141: raise AssertionError(('closed fine rules',closed_rules))

    failures=sorted([t for t in nonclosed if not t['greedy_optimal']],key=lambda t:(t['rule'],t['target']))
    success=len(nonclosed)-len(failures)
    regret=[t['regret'] for t in failures]
    relative=[t['relative_regret'] for t in failures]
    by_balance={}
    for bal in (1,2,3,4):
        g=[t for t in nonclosed if t['balance']==bal];f=[t for t in g if not t['greedy_optimal']]
        by_balance[str(bal)]={'nonclosed':len(g),'failures':len(f),'success_fraction':(len(g)-len(f))/len(g) if g else None,
                              'mean_regret':sum(t['regret'] for t in f)/len(f) if f else 0.0,
                              'max_regret':max([t['regret'] for t in f],default=0.0)}
    by_class={}
    for cls in ('I','II','III','IV'):
        g=[t for t in nonclosed if t['wclass']==cls];f=[t for t in g if not t['greedy_optimal']]
        by_class[cls]={'nonclosed':len(g),'failures':len(f),'success_fraction':(len(g)-len(f))/len(g) if g else None}

    dim_tested=sum(t['diminishing']['tested'] for t in targets)
    dim_viol=sum(t['diminishing']['violations'] for t in targets)
    norm_viol=sum(t['diminishing']['normalized_violations'] for t in targets)
    dim_targets=sum(t['diminishing']['violations']>0 for t in targets)
    fail_with_dim=sum(t['diminishing']['violations']>0 for t in failures)
    nofail_with_dim=sum(t['diminishing']['violations']>0 for t in nonclosed if t['greedy_optimal'])

    first=None
    if failures:
        t=failures[0]
        first={'rule':t['rule'],'wclass':t['wclass'],'target':t['target'],'balance':t['balance'],'target_hstar':t['target_hstar'],
               'greedy_added_bits':t['greedy_added_bits'],'global_min_added_bits':t['global_min_added_bits'],'regret':t['regret'],
               'relative_regret':t['relative_regret'],'greedy_path':t['greedy_path'],'global_optima':t['global_optima'],
               'counterexample':t.get('counterexample'),'diminishing':t['diminishing']}

    summary={'ok':True,'experiment':'block3-representation-design','ring_width':12,'cadence':3,'rules':256,'canonical_binary_targets':127,
             'target_cases':len(targets),'closed_targets':len(closed),'nonclosed_targets':len(nonclosed),'closed_fine_rules':closed_rules,
             'greedy_global_optimal':success,'greedy_failures':len(failures),'greedy_success_fraction':success/len(nonclosed),
             'primary_hypothesis_counterexample_exists':bool(failures),'mean_failure_regret':sum(regret)/len(regret) if regret else 0.0,
             'max_failure_regret':max(regret,default=0.0),'max_relative_regret':max(relative,default=0.0),
             'by_balance':by_balance,'by_wolfram_class_exploratory':by_class,
             'diminishing_returns':{'comparisons':dim_tested,'violations':dim_viol,'violation_fraction':dim_viol/dim_tested if dim_tested else 0.0,
                                    'normalized_violations':norm_viol,'targets_with_violations':dim_targets,
                                    'greedy_failures_with_violations':fail_with_dim,'greedy_successes_with_violations':nofail_with_dim},
             'first_counterexample':first,'source_hashes':shards[0]['source_hashes']}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
