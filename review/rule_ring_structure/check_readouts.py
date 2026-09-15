"""Independent readout/selection checks from reconstructed pair distances."""
import ast
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UNIT = ROOT / 'experiments/rule_ring_structure_20260915'
RULES = [0, 18, 30, 54, 90, 110, 126, 204]
OBS = [f'future_{h}' for h in (1, 2, 4, 8, 16, 32)] + ['basin', 'cycle_length', 'transient_depth']


def load(path):
    return json.loads(path.read_text())


def factors(n):
    out = {}
    for p in range(2, n + 1):
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
    return out


def descriptors(n, m):
    a, b = factors(n), factors(m)
    common, union = set(a) & set(b), set(a) | set(b)
    values = dict(size_gap=m-n, gcd=math.gcd(n,m), lcm=n*m//math.gcd(n,m),
                  n_divides_m=int(m % n == 0), m_divides_n=int(n % m == 0),
                  coprime=int(math.gcd(n,m)==1), same_prime_support=int(set(a)==set(b)),
                  prime_support_jaccard=len(common)/len(union),
                  exponent_l1=sum(abs(a.get(p,0)-b.get(p,0)) for p in union),
                  n_distinct_primes=len(a), m_distinct_primes=len(b),
                  n_total_prime_factors=sum(a.values()), m_total_prime_factors=sum(b.values()),
                  n_prime=int(len(a)==1 and sum(a.values())==1),
                  m_prime=int(len(b)==1 and sum(b.values())==1))
    out = {f'arithmetic.{k}':v for k,v in values.items()}
    for d in (2,3,4,5):
        x,y=int(n%d==0),int(m%d==0)
        for k,v in dict(n=x,m=y,both=x*y,same=int(x==y)).items():out[f'div{d}.{k}']=v
    for p in (2,3,5):
        x,y=a.get(p,0),b.get(p,0)
        for k,v in dict(n=x,m=y,gap=y-x,absolute_gap=abs(y-x)).items():out[f'v{p}.{k}']=v
    return out


def pearson(xs,ys):
    if len(xs)<3:return None,'fewer_than_three_rows'
    x,y=np.array(xs,float),np.array(ys,float)
    if np.all(x==x[0]) or np.all(y==y[0]):return None,'constant_input'
    return float(np.corrcoef(x,y)[0,1]),None


def main():
    predicted={}
    for stage in ('discovery','confirmation'):
        predicted.update({ast.literal_eval(k):v for k,v in load(HERE/f'{stage}-independent-relations.json').items()})
    rows=load(UNIT/'confirmation-evidence.json')['rows']
    expected_count=math.comb(13,2)*28*9
    assert len(rows)==expected_count==19656
    max_error=0.
    for row in rows:
        obs=row['observation'];n,m=row['rings'];a,b=map(int,row['rules'])
        assert row['ring_features']==descriptors(n,m)
        left,right=predicted[obs,n,a,b],predicted[obs,m,a,b]
        scores=dict(at_n=left['vi_per_bit'],at_m=right['vi_per_bit'],change=right['vi_per_bit']-left['vi_per_bit'],absolute_change=abs(right['vi_per_bit']-left['vi_per_bit']))
        for field,value in scores.items():
            error=abs(row['scores'][field]-value)
            assert error<1e-11,(obs,n,m,a,b,field,error)
            max_error=max(max_error,error)
        for source,(r,w) in zip(row['sources'],((a,n),(b,n),(a,m),(b,m))):
            path=ROOT/f'experiments/rule_ring_structure_20260915/partitions/n{w:02d}_r{r:03d}.npz'
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            assert source==f'{path.relative_to(ROOT)}#sha256={digest};{obs}'
    response={}
    for obs in OBS:
        for n,m in itertools.combinations(range(4,17),2):
            response[obs,n,m]=math.fsum(abs(predicted[obs,n,a,b]['vi_per_bit']-predicted[obs,m,a,b]['vi_per_bit']) for a,b in itertools.combinations(RULES,2))/28
    for row in load(UNIT/'confirmation-responses.json'):
        assert abs(row['mean_absolute_change']-response[row['observation'],*row['rings']])<1e-11
        assert row['rule_pairs']==28
    assoc={};selected=[]
    for stage,widths in (('discovery',range(4,13)),('confirmation',range(13,17))):
        pairs=list(itertools.combinations(widths,2))
        for obs in OBS:
            for feature in descriptors(*pairs[0]):
                value,reason=pearson([descriptors(n,m)[feature] for n,m in pairs],[response[obs,n,m] for n,m in pairs])
                assoc[stage,obs,feature]=dict(observation=obs,feature=feature,pearson=value,undefined_reason=reason,ring_pairs=len(pairs))
        recorded=load(UNIT/f'{stage}-result.json')['associations']
        assert len(recorded)==9*43
        for row in recorded:
            expected=assoc[stage,row['observation'],row['feature']]
            assert row['undefined_reason']==expected['undefined_reason']
            assert row['ring_pairs']==expected['ring_pairs']
            if expected['pearson'] is None:assert row['pearson'] is None
            else:
                delta=abs(row['pearson']-expected['pearson'])
                assert delta<1e-10,(stage,row,expected)
                max_error=max(max_error,delta)
    for obs in OBS:
        available=[v for (stage,name,feature),v in assoc.items() if stage=='discovery' and name==obs and v['pearson'] is not None]
        selected.extend(sorted(available,key=lambda r:(-round(abs(r['pearson']),12),r['feature']))[:3])
    saved=load(UNIT/'discovery-selection.json')
    assert [(r['observation'],r['feature']) for r in selected]==[(r['observation'],r['feature']) for r in saved]
    sign=lambda x:None if x is None or abs(x)<=1e-12 else (1 if x>0 else -1)
    agree=disagree=undefined=0
    verdicts=load(UNIT/'confirmation-result.json')['selected_confirmation']
    assert len(verdicts)==len(selected)==27
    for row in verdicts:
        a=assoc['discovery',row['observation'],row['feature']]['pearson']
        b=assoc['confirmation',row['observation'],row['feature']]['pearson']
        expected=None if sign(a) is None or sign(b) is None else sign(a)==sign(b)
        assert row['sign_agreement']==expected
        if expected is None:undefined+=1
        elif expected:agree+=1
        else:disagree+=1
    result=dict(status='verified',evidence_rows=len(rows),responses=len(response),associations=len(assoc),selected=len(selected),sign_agreements=agree,sign_disagreements=disagree,undefined_sign_verdicts=undefined,maximum_numeric_error=max_error,verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'readout-verification.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
