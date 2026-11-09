"""Reviewer reproduction of the imported asymptotic-closure census (55/88, 41/88).

Reuses the helpers in review_october_20261109.py. Takes a few minutes at width 18.
Optional: --out <file.json> saves every (rule, width) reserve and depth.
"""
import json, sys
import numpy as np
import pathlib
_HERE = pathlib.Path(__file__).resolve().parent
exec((_HERE / 'review_october_20261109.py').read_text(encoding='utf-8').split(chr(10) + 'ok = True')[0])

def refl(r):
    out = 0
    for i in range(8):
        l, c, rr = (i >> 2) & 1, (i >> 1) & 1, i & 1
        out |= ((r >> ((rr << 2) | (c << 1) | l)) & 1) << i
    return out
def conj(r):
    out = 0
    for i in range(8):
        out |= (1 - ((r >> (7 - i)) & 1)) << i
    return out
reps = sorted({min(r, refl(r), conj(r), conj(refl(r))) for r in range(256)})
assert len(reps) == 88
res = {}
for n in (14, 16, 18):
    par = classes(block_parity(n))[1]
    for r in reps:
        H = H_table(r, n)
        lab, rounds = future_quotient(H[H], par)
        res[(r, n)] = (forgotten_bits(lab, n), rounds)
    print("done n", n, flush=True)
corr = [r for r in reps if all(res[(30, n)][0] < res[(r, n)][0] < res[(184, n)][0] for n in (16, 18))]
full = [r for r in corr if res[(r, 18)][1] > res[(r, 14)][1]]
print("corridor passers:", len(corr), "| corridor+growth:", len(full))
print("full passers:", full)
if "--out" in sys.argv:
    json.dump({f"{r}:{n}": v for (r, n), v in res.items()}, open(sys.argv[sys.argv.index("--out") + 1], "w"))
