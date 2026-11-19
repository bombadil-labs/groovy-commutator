#!/usr/bin/env python3
"""Independent bit-plane replay of the Groovy J2 audit and exact guards."""
from itertools import product
from fractions import Fraction

def tables(rule, w=13):
    # Each bit-plane contains the values at a spatial index for all 2**w blocks.
    m=1<<w
    univ=(1<<m)-1
    src=[sum(1<<k for k in range(m) if k>>i&1) for i in range(w)]
    def law(row):
        out=[]
        for k in range(1,len(row)-1):
            a,b,c=row[k-1:k+2]
            r=0
            for ai,bi,ci in product((0,1),repeat=3):
                if rule>>((ai<<2)|(bi<<1)|ci)&1:
                    r|=(a if ai else univ^a)&(b if bi else univ^b)&(c if ci else univ^c)
            out.append(r)
        return out
    def residual(row, n):
        e=law(row)
        if n==0:
            return [x^y for x,y in zip(row[1:-1],e)]
        one=residual(e,n-1)
        two=law(residual(row,n-1))
        return [x^y for x,y in zip(one,two)]
    def at(row,k,lo,hi):
        pad=(w-len(row))//2
        return tuple(row[i-pad]>>k&1 for i in range(lo,hi+1))
    g,q=[residual(src,n) for n in (1,2)]
    ng,nq=[residual(law(src),n) for n in (1,2)]
    c=w//2
    def obs(k,r):return at(g,k,c-r,c+r)+at(q,k,c-r,c+r)
    def nxt(k):return at(ng,k,c,c)+at(nq,k,c,c)
    for rad in [1,2,3]:
        lookup={}; bad=set(); examples={}
        for k in range(m):
            o=obs(k,rad); n=nxt(k)
            if o in lookup and lookup[o][0]!=n:
                bad.add(o)
                examples[o]=(lookup[o][1],k)
            lookup.setdefault(o,(n,k))
        print(rule,rad,len(lookup),len(bad),next(iter(examples.values()),None))
    good=[]
    for k in range(m):
        if (k>>c)&1==0 and obs(k,3)==obs(k^(1<<c),3):
            good.append(k)
    print(rule, len(good), Fraction(len(good),2**(w-1)*7), f'{good[0]:013b}')
    S=set(good); I=[i for i in range(w) if i!=c and any(k^(1<<i) not in S for k in S)]
    offsets, guards = {18: ([-1,1], {(1,1)}),
                       126: ([-2,-1,1,2], {(0,1,0,1),(1,0,1,0)}),
                       90: ([], {()})}[rule]
    assert S == {k for k in range(m) if not (k>>c)&1
                 and tuple(k>>(c+d)&1 for d in offsets) in guards}
    print("gate", sorted({tuple(k>>i&1 for i in I) for k in good}))
    e=law(src)
    print("good contexts with unequal one-step full source field",sum(at(e,k,c-1,c+1)!=at(e,k^(1<<c),c-1,c+1) for k in good))
for rule in [18,126,90]:
    tables(rule)
