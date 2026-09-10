"""Exploratory check for issue #67 (2026-09-10). Not a frozen protocol.
Codex's deduction: on the shared invariant family B = K_1(full shift) of Rule 32, the two
completions H128(U,V)=(F32(U)^V, F128(V)) and H160(U,V)=(F32(U)^V, F160(V)) agree, and the
depth-one second-lift correction coordinates are related by (u, v) -> (u, v ^ H(u) ^ H'(u)),
u = A_0(X) = X ^ H(X).  Ring n = 8, exhaustive over all 2^n source states.
"""
import sys; sys.path.insert(0, 'src')
import numpy as np
from groovy.ca import apply_rule
n = 8
def states():
    for k in range(2**n):
        yield np.array([(k >> (n-1-i)) & 1 for i in range(n)], dtype=np.uint8)
F = lambda s: apply_rule(s, 32)
A0 = lambda s: s ^ F(s)
A1 = lambda s: A0(F(s)) ^ F(A0(s))
def H(top):
    return lambda X: (F(X[0]) ^ X[1], apply_rule(X[1], top))
H128, H160 = H(128), H(160)
xor = lambda X, Y: (X[0] ^ Y[0], X[1] ^ Y[1])
def A0H(Hf): return lambda X: xor(X, Hf(X))
def A1H(Hf):
    a0 = A0H(Hf)
    return lambda X: xor(a0(Hf(X)), Hf(a0(X)))
agree_on_B = leaves_B = recode_ok = 0
fam = [(A0(s), A1(s)) for s in states()]
B = {(tuple(u), tuple(v)) for u, v in fam}
for X in fam:
    agree_on_B += all(np.array_equal(a, b) for a, b in zip(H128(X), H160(X)))
    u = A0H(H128)(X)
    leaves_B += (tuple(u[0]), tuple(u[1])) not in B
    v128, v160 = A1H(H128)(X), A1H(H160)(X)
    pred = xor(v128, xor(H128(u), H160(u)))
    recode_ok += all(np.array_equal(a, b) for a, b in zip(pred, v160))
print(f"family size {len(fam)} (distinct {len(B)}); H128==H160 on family: {agree_on_B}/{len(fam)}")
print(f"A_0(X) leaves family: {leaves_B}/{len(fam)}")
print(f"depth-one recoding (u, v^H(u)^H'(u)) holds: {recode_ok}/{len(fam)}")
