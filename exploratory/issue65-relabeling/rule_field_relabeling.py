"""Exploratory check for issue #65 (2026-09-10). Not a frozen protocol.
Local Z2 relabeling of rule fields.  For site field c in {0,1}^n:
  S' = S XOR c,   r'_i(l,m,r) = r_i(l XOR c_{i-1}, m XOR c_i, r XOR c_{i+1}) XOR c_i
Claim 1:  F_{R'}(S XOR c) = F_R(S) XOR c.
Claim 2 (covariant transport): if the original transport writes R_j at site i under gate
  g(S_i), the transformed transport writes phi_i(phi_j^{-1}(R'_j)) at site i under gate
  g(S'_i XOR c_i); then transport commutes with the relabeling.  Plain copying of R'_j does not.
Uses nonuniform.step_gated_diffusion (live cell copies LEFT neighbor's rule; R persists).
Rule-number bit convention: groovy.ca.rule_lut (index 4l+2m+r).
"""
import sys, itertools; sys.path.insert(0, 'src')
import numpy as np
from groovy.ca import rule_lut
from groovy.nonuniform import apply_rule_field, step_gated_diffusion

def phi_table(r, cl, cm, cr):
    """conjugate one 8-bit table r by neighbor relabelings (cl, cm, cr)."""
    lut = rule_lut(int(r)); out = 0
    for idx in range(8):
        l, m, rr = (idx >> 2) & 1, (idx >> 1) & 1, idx & 1
        src = ((l ^ cl) << 2) | ((m ^ cm) << 1) | (rr ^ cr)
        out |= (int(lut[src]) ^ cm) << idx
    return out
def conj_field(R, c):
    n = len(R)
    return np.array([phi_table(R[i], c[(i-1) % n], c[i], c[(i+1) % n]) for i in range(n)])
def phi_inv_table(r, cl, cm, cr):
    return phi_table(r, cl, cm, cr)   # each phi_i is an involution (XOR twice)

rng = np.random.default_rng(1); n = 12
ok1 = all(np.array_equal(apply_rule_field(S ^ c, conj_field(R, c)), apply_rule_field(S, R) ^ c)
          for S, R, c in ((rng.integers(0, 2, n).astype(np.uint8), rng.integers(0, 256, n),
                           rng.integers(0, 2, n).astype(np.uint8)) for _ in range(200)))
print("Claim 1 on 200 random (S,R,c), n=12:", ok1)

def covariant_gated_diffusion(Sp, Rp, c):
    """transformed transport: gate reads decoded state; copied table is re-conjugated."""
    n = len(Sp); Sn = apply_rule_field(Sp, Rp); Rn = Rp.copy()
    for i in range(n):
        if (Sp[i] ^ c[i]) == 1:
            j = (i - 1) % n
            raw = phi_inv_table(Rp[j], c[(j-1) % n], c[j], c[(j+1) % n])   # back to untransformed
            Rn[i] = phi_table(raw, c[(i-1) % n], c[i], c[(i+1) % n])      # forward at site i
    return Sn, Rn

ok2 = True; plain_differs = 0
for _ in range(200):
    S = rng.integers(0, 2, n).astype(np.uint8); R = rng.integers(0, 256, n); c = rng.integers(0, 2, n).astype(np.uint8)
    S1, R1 = step_gated_diffusion(S, R)                         # original transport
    Sp1, Rp1 = covariant_gated_diffusion(S ^ c, conj_field(R, c), c)
    ok2 &= np.array_equal(Sp1, S1 ^ c) and np.array_equal(Rp1, conj_field(R1, c))
    Sq, Rq = step_gated_diffusion(S ^ c, conj_field(R, c))       # unchanged implementation on transformed data
    plain_differs += not (np.array_equal(Sq, S1 ^ c) and np.array_equal(Rq, conj_field(R1, c)))
print("Claim 2 covariant transport commutes on 200 random cases:", ok2)
print("unchanged transport on transformed data disagrees in", plain_differs, "of 200 cases")

n4 = 4; pure = set()
for r in range(256):
    for cc in itertools.product([0, 1], repeat=n4):
        pure.add(tuple(conj_field(np.full(n4, r), np.array(cc, dtype=np.uint8))))
print(f"n=4: pure-gauge rule fields = {len(pure)} of 256^4 = {256**n4}")
print("rule 110 uniform, c=(1,0,0,0) ->", conj_field(np.full(4, 110), np.array([1,0,0,0], dtype=np.uint8)))
