"""Post-enumeration independent polynomial audit of the selector findings.

Expands selector indicator polynomials directly over GF(2), independently of
experiment_shared_state_rule.local_sweep's truth-table Mobius transform.
"""
import json, math, hashlib
from pathlib import Path
import numpy as np
from experiment_shared_state_rule import ROOT, local_table, OFFSETS

def toggle(s,x):
    if x in s:s.remove(x)
    else:s.add(x)

def polynomial(p, axis):
    address=(6,8,2) if axis=='horizontal' else (0,8,4)
    terms=set()
    for k in range(8):
        product={1<<p[k]}
        for j,var in enumerate(address):
            factor={1<<var} if (k>>(2-j))&1 else {0,1<<var}
            nxt=set()
            for a in product:
                for b in factor:toggle(nxt,a|b)
            product=nxt
        for m in product:toggle(terms,m)
    return terms

def main():
    meta=json.loads((ROOT/'results/shared_state_rule_20260907_metadata.json').read_text())
    checks=0
    for p in meta['encodings']:
        for axis in ['horizontal','vertical']:
            terms=polynomial(p,axis)
            truth=np.array([sum((w&m)==m for m in terms)%2 for w in range(512)])
            assert np.array_equal(truth,local_table(p,axis))
            quartic=[m for m in terms if m.bit_count()==4]
            assert max(m.bit_count() for m in terms)==4 and len(quartic)==6
            address_mask=(1<<8)|((1<<6)|(1<<2) if axis=='horizontal' else (1<<0)|(1<<4))
            intersection=511
            for m in quartic:intersection&=m
            assert intersection==address_mask
            checks+=512
    local=json.loads((ROOT/'results/shared_state_rule_20260907_local.json').read_text())
    # Only swapping the two address-data positions can preserve all free-data coefficients.
    # They are indistinguishable exactly at two of the four addresses with W=E.
    distinct=math.factorial(8)-math.comb(4,2)*math.factorial(6)
    assert distinct==36000
    for axis in ['horizontal','vertical']:
        assert local[axis]['distinct_tables']==distinct
        assert [x['count'] for x in local[axis]['joint_histogram']]==[10080,20160,10080]
    assert local['distinct_tables_both_axes']==2*distinct
    saved=json.loads((ROOT/'results/shared_state_rule_20260907_graphs.json').read_text())
    cycle_steps=0
    for key,detail in saved.items():
        if not key.startswith('selector2d/'):continue
        _,axis,pi,n=key.split('/');n=int(n);p=meta['encodings'][int(pi)]
        cyc=detail['longest_cycle'];assert len(set(cyc))==len(cyc)
        for state,expected in zip(cyc,cyc[1:]+cyc[:1]):
            result=0
            for y in range(n):
                for x in range(n):
                    def cell(dy,dx):return (state>>(((y+dy)%n)*n+(x+dx)%n))&1
                    a,b=(cell(0,-1),cell(0,1)) if axis=='horizontal' else (cell(-1,0),cell(1,0))
                    q=4*a+2*cell(0,0)+b
                    result|=cell(*OFFSETS[p[q]])<<(y*n+x)
            assert result==expected
            cycle_steps+=1
    out={'polynomial_output_checks':checks,'scalar_longest_cycle_steps':cycle_steps,'quartic_terms_per_selector':6,'distinct_tables_per_axis':distinct,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'post-enumeration audit; proofs and combinatorial counts in Research note'}
    (ROOT/'results/shared_state_rule_20260907_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    tables=[{'encoding':i,'axis':axis,'outputs_0_through_511':''.join(map(str,local_table(p,axis)))}
            for i,p in enumerate(meta['encodings']) for axis in ['horizontal','vertical']]
    (ROOT/'results/shared_state_rule_20260907_tables.json').write_text(json.dumps(tables,indent=2)+'\n')
    print(json.dumps(out))
if __name__=='__main__':main()
