#!/usr/bin/env python3
# Exact Rule54 finite-support jet witness, no imports from project modules.
from functools import lru_cache

def step(s):
    if not s: return frozenset()
    out=set()
    for i in range(min(s)-1,max(s)+2):
        pattern=4*(i-1 in s)+2*(i in s)+(i+1 in s)
        if (54>>pattern)&1:out.add(i)
    return frozenset(out)

@lru_cache(None)
def a(s,k):
    if k==0:return s^step(s)
    return a(step(s),k-1)^step(a(s,k-1))

for x,y,support in [
    (frozenset([-6]),frozenset([-6,7]),{6,8}),
    (frozenset([6]),frozenset([-7,6]),{-8,-6})
]:
    for k in range(1,6):
        assert a(x,k)^a(y,k)==(frozenset(support) if k in (2,4) else frozenset())
    assert (0 in a(x,6),0 in a(y,6))==(False,True)
print("PASS: sixth jet site on each flank is independently necessary")
