"""Exploratory check for issue #62 (2026-09-10). Not a frozen protocol.
Rule 110, observation P = D = S XOR F(S), ring n = 8, exhaustive over all 2^n states.
Conventions: cell i has neighbors (i-1, i, i+1) mod n; state k -> bits MSB-first.
Exact successor set  B_set(y) = {P(F(s)) : P(s) = y}  (set of complete fields).
Local window transformer at radius R: per cell, the set of next-P values ever produced by
the (2R+1)-window of P around that cell, over all states; product over cells = sound superset.
"""
import sys, itertools; sys.path.insert(0, 'src')
from fractions import Fraction
import numpy as np
from groovy.ca import apply_rule

n, rule = 8, 110
def states():
    for k in range(2**n):
        yield np.array([(k >> (n-1-i)) & 1 for i in range(n)], dtype=np.uint8)
P = lambda s: s ^ apply_rule(s, rule)

succ = {}
for s in states():
    succ.setdefault(tuple(P(s)), set()).add(tuple(P(apply_rule(s, rule))))
sizes = [len(v) for v in succ.values()]
print(f"reachable y = {len(succ)}; singleton = {sum(z == 1 for z in sizes)}; "
      f"mean |B_set| = {Fraction(sum(sizes), len(sizes))} = {sum(sizes)/len(sizes):.4f}; max = {max(sizes)}")
print(f"cell-occurrence denominator = 2^n * n = {2**n * n}")

for R in (0, 1, 2, 3):
    table = {}
    for s in states():
        y, ynext = P(s), P(apply_rule(s, rule))
        for i in range(n):
            w = tuple(y[(i+j) % n] for j in range(-R, R+1))
            table.setdefault(w, set()).add(int(ynext[i]))
    det = tot = 0
    exact_match = 0; prod_sizes = []
    for y, exact in succ.items():
        cells = [table[tuple(y[(i+j) % n] for j in range(-R, R+1))] for i in range(n)]
        prod = 1
        for c in cells: prod *= len(c)
        prod_sizes.append(prod)
        assert all(all(f[i] in cells[i] for i in range(n)) for f in exact)   # soundness
        exact_match += (prod == len(exact))
    for s in states():
        y = P(s)
        for i in range(n):
            tot += 1; det += len(table[tuple(y[(i+j) % n] for j in range(-R, R+1))]) == 1
    print(f"R={R}: windows={len(table)}, singleton windows={sum(len(v)==1 for v in table.values())}, "
          f"cell-occurrences determined={det}/{tot}={det/tot:.4f}; "
          f"whole-field: product==exact for {exact_match}/{len(succ)} y, "
          f"mean product size={Fraction(sum(prod_sizes), len(prod_sizes))}={sum(prod_sizes)/len(prod_sizes):.3f}, "
          f"max product size={max(prod_sizes)}")
