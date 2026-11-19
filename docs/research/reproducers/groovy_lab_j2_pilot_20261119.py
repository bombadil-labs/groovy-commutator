#!/usr/bin/env python3
"""Independent exact full-line Groovy depth-two jet audit.

Source definition: bombadil-labs/groovy-commutator@4883bd96975a45dec29274630f3b134e309ed3d6.
Python standard library only. Run once, with no inputs, to emit JSON.
"""
from collections import defaultdict
from functools import cache
from itertools import product
import json

def binary(word):
    return "".join(map(str, word))

def audit(rule):
    @cache
    def step(x):
        return tuple((rule >> (4*a+2*b+c)) & 1
                     for a,b,c in zip(x,x[1:],x[2:]))

    @cache
    def residual(k, x):
        if k == 0:
            return tuple(a^b for a,b in zip(x[1:-1],step(x)))
        return tuple(a^b for a,b in zip(residual(k-1,step(x)),
                                       step(residual(k-1,x))))

    def jet(x):
        return tuple(zip(residual(1,x)[1:-1],residual(2,x)))

    radii = {}
    for r in range(1,4):
        seen = defaultdict(dict)
        for x in product((0,1), repeat=7+2*r):
            seen[jet(x)].setdefault(residual(3,x)[r-1], x)
        conflicts = [v for v in seen.values() if len(v) > 1]
        radii[r] = {
            "observed_jet_windows":len(seen), "conflicting_windows":len(conflicts),
            "first_conflict": ({str(y):binary(x) for y,x in conflicts[0].items()}
                               if conflicts else None),
        }
    good = []
    for e in product((0,1), repeat=12):
        l,u = e[:6],e[6:]
        x,y = l+(0,)+u,l+(1,)+u
        if jet(x) == jet(y):
            good.append((binary(x), binary(y)))
    assert radii[3]["conflicting_windows"] == 0
    off_18 = [pair for pair in good if all("11" in x for x in pair)]
    off_126 = [pair for pair in good if all("010" in x for x in pair)]
    singleton = tuple(map(int, "0000001000000"))
    return {"radii":radii,
            "diamonds":{"contexts":4096, "matches":len(good), "first":good[0],
                        "both_words_contain_11":len(off_18), "first_with_11":off_18[0],
                        "both_words_contain_isolated_1":len(off_126), "first_with_isolated_1":off_126[0]},
            "single_seed":{"A0":binary(residual(0,singleton)), "J2":jet(singleton)}}

if __name__ == "__main__":
    print(json.dumps({rule:audit(rule) for rule in (18,126,90)}, indent=2))
