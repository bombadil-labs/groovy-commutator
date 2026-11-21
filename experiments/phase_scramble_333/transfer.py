"""Exhaustive six-cell test of the existing left-copy rule transport."""
from collections import defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np
from groovy.nonuniform import step_gated_diffusion

N=6
START=(18,126)*3
PROTOCOL="10cd015f11606dcc9ff6dd485943236839433526"

def step(s,r):
    x=tuple((r[i] >> (4*s[i-1]+2*s[i]+s[(i+1)%N])) & 1 for i in range(N))
    q=tuple(r[i-1] if s[i] else r[i] for i in range(N))
    y,m=step_gated_diffusion(np.array(s,dtype=np.uint8),np.array(r,dtype=np.uint8))
    assert (x,q)==(tuple(y),tuple(m))
    return x,q

def masks(k):
    for indices in combinations(range(N),k):
        yield tuple(126 if i in indices else 18 for i in range(N))

def calculate():
    groups=defaultdict(list)
    for initial in product((0,1),repeat=N):
        s,r=step(*step(initial,START))
        future,_=step(s,r)
        groups[(s,r.count(126))].append((initial,r,future))
    matched,natural,eligible_groups=0,0,0
    first=None
    shuffle_sum=Fraction(0)
    for (s,k),rows in groups.items():
        if len(rows)<2: continue
        eligible_groups+=1
        shuffled=[step(s,r)[0] for r in masks(k)]
        baseline=step(s,START)[0]
        for a,b in combinations(rows,2):
            matched+=1
            if a[2]==b[2]: continue
            natural+=1
            record=(a,b,s,k)
            first=record if first is None or record<first else first
            assert not (a[2]==baseline==b[2])
            shuffle_sum+=Fraction(shuffled.count(a[2])*shuffled.count(b[2]),len(shuffled)**2)
    rate=None if not natural else str(shuffle_sum/natural)
    return dict(eligible_groups=eligible_groups,matched_pairs=matched,naturally_split=natural,
                first_witness=first,full_and_reset_replay_on_splits=None if not natural else [1,0],
                exact_shuffle_replay_on_splits=rate)

if __name__=="__main__":
    print(json.dumps(dict(protocol_revision=PROTOCOL,
                          runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          **calculate()),indent=2,sort_keys=True))
