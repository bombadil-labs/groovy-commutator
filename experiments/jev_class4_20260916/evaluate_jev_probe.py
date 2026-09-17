#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,statistics
from collections import defaultdict
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent

def auc(pos,neg):
    wins=ties=0
    for p in pos:
        for n in neg:
            wins += p>n; ties += p==n
    return (wins+0.5*ties)/(len(pos)*len(neg)) if pos and neg else None

def rank_desc(scores,target):
    x=scores[target]
    return 1 + sum(v>x for v in scores.values()) + 0.5*sum(v==x for k,v in scores.items() if k!=target)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('responses',nargs='?',default='jev_raw_responses.jsonl');args=ap.parse_args()
    truth=json.loads((ROOT/'truth_private.json').read_text())
    path=Path(args.responses); path=path if path.is_absolute() else ROOT/path
    rows=[json.loads(x) for x in path.read_text().splitlines() if x.strip()]
    ok=[r for r in rows if r.get('status')=='ok' and r['mode']=='semantic']
    by=defaultdict(list)
    models=defaultdict(int)
    for r in ok:
        models[r.get('model','')]+=1
        for q,p in r['nouls'].items(): by[(r['alias'],q)].append(float(p))
    aliases=sorted(truth)
    qs=sorted({q for _,q in by})
    report={'response_file':str(path),'models':dict(models),'questions':{}}
    hard=(9,30,73,90,122,126)
    rule_to_alias={v['rule']:a for a,v in truth.items()}
    for q in qs:
        scores={}; ranges={}; nsuccess={}
        for a in aliases:
            vals=by.get((a,q),[]); nsuccess[a]=len(vals)
            if len(vals)>=2:
                scores[a]=statistics.median(vals);ranges[a]=max(vals)-min(vals)
        p_alias=[rule_to_alias[54],rule_to_alias[110]]
        primary_neg=[a for a in aliases if truth[a]['class'] in (1,2,3)]
        c3=[a for a in aliases if truth[a]['class']==3]
        if not all(a in scores for a in p_alias): continue
        lower=min(scores[a] for a in p_alias)
        negatives_at=[a for a in primary_neg if a in scores and scores[a]>=lower]
        ranks={str(truth[a]['rule']):rank_desc(scores,a) for a in p_alias}
        lower_rank=max(ranks.values())
        gate='strong' if lower_rank<=5 and len(negatives_at)<=3 else 'moderate' if lower_rank<=10 and len(negatives_at)<=8 else 'none'
        stable=all(ranges.get(a,1)>-1 and ranges.get(a,1)<=0.10 for a in p_alias)
        item={'positive_scores':{str(truth[a]['rule']):scores[a] for a in p_alias},
              'positive_ranks':ranks,'lower_positive_rank':lower_rank,'negatives_at_or_above_lower_positive':len(negatives_at),
              'negative_rules_at_or_above':[truth[a]['rule'] for a in sorted(negatives_at,key=lambda a:scores[a],reverse=True)],
              'auc_all':auc([scores[a] for a in p_alias],[scores[a] for a in primary_neg if a in scores]),
              'auc_class3':auc([scores[a] for a in p_alias],[scores[a] for a in c3 if a in scores]),
              'hard_controls':{str(r):scores.get(rule_to_alias[r]) for r in hard},
              'disputed':{str(r):scores.get(rule_to_alias[r]) for r in (41,106)},
              'positive_ranges':{str(truth[a]['rule']):ranges.get(a) for a in p_alias},
              'successful_attempts_core':{str(truth[a]['rule']):nsuccess.get(a,0) for a in p_alias},
              'gate':gate,'stable_core_ranges':stable}
        # finite pair-rank null: fraction of all eligible pairs whose worse rank is as good or better
        eligible=[a for a in aliases if a in scores and not truth[a]['disputed']]
        sorted_scores={a:scores[a] for a in eligible}
        observed=max(rank_desc(sorted_scores,a) for a in p_alias)
        pair_worse=[]
        for i,a in enumerate(eligible):
            for b in eligible[i+1:]: pair_worse.append(max(rank_desc(sorted_scores,a),rank_desc(sorted_scores,b)))
        item['pair_null_fraction_worse_rank_le_observed']=sum(x<=observed for x in pair_worse)/len(pair_worse)
        report['questions'][q]=item
    (ROOT/'jev_primary_evaluation.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':main()
