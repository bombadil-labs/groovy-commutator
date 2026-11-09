"""Independent reviewer recomputation of headline October claims.

Written from the definitions in the knowledge entries only (not from the
units' own scripts). Integer-coded states on periodic rings; bit i = cell i;
rule index = 4*cell[i-1] + 2*cell[i] + cell[i+1].
"""
import sys
import numpy as np


def H_table(rule, n):
    x = np.arange(1 << n, dtype=np.uint32)
    mask = np.uint32((1 << n) - 1)
    left = ((x << np.uint32(1)) | (x >> np.uint32(n - 1))) & mask      # bit i = cell i-1
    right = ((x >> np.uint32(1)) | (x << np.uint32(n - 1))) & mask     # bit i = cell i+1
    out = np.zeros_like(x)
    for idx in range(8):
        if (rule >> idx) & 1:
            l, c, r = (idx >> 2) & 1, (idx >> 1) & 1, idx & 1
            m = (left if l else ~left) & (x if c else ~x) & (right if r else ~right) & mask
            out |= m
    return out


def jets(rule, n, depth):
    """A_0 = D = I xor H; A_{k+1}(X) = A_k(H X) xor H(A_k X). Returns [A_1..A_depth]."""
    H = H_table(rule, n)
    x = np.arange(1 << n, dtype=np.uint32)
    A = x ^ H
    out = []
    for _ in range(depth):
        A = A[H] ^ H[A]
        out.append(A)
    return H, out


def classes(*cols):
    """Number of distinct rows and a dense label array for the joint columns."""
    lab = np.zeros(len(cols[0]), dtype=np.int64)
    for c in cols:
        _, inv = np.unique(np.stack([lab, c.astype(np.int64)]), axis=1, return_inverse=True)
        lab = inv.ravel()
    return int(lab.max()) + 1, lab


def forgotten_bits(lab, n):
    counts = np.bincount(lab).astype(float)
    p = counts / counts.sum()
    return n + float((p * np.log2(p)).sum())  # n - H(partition)


def future_quotient(F, obs_lab):
    """Coarsest partition refining obs that is stable under F; returns (labels, rounds)."""
    lab = obs_lab
    k = int(lab.max()) + 1
    rounds = 0
    while True:
        k2, lab2 = classes(lab, lab[F])
        if k2 == k:
            return lab, rounds
        lab, k, rounds = lab2, k2, rounds + 1


def block_parity(n):
    x = np.arange(1 << n, dtype=np.uint32)
    p = np.zeros_like(x)
    for j in range(n // 2):
        p |= (((x >> np.uint32(2 * j)) ^ (x >> np.uint32(2 * j + 1))) & np.uint32(1)) << np.uint32(j)
    return p


ok = True


def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}")


# ---- near-ring / 4-200 mechanism (#316) ----
n = 12
H4, H200 = H_table(4, n), H_table(200, n)
x = np.arange(1 << n, dtype=np.uint32)
check("4 xor 200 = identity map", np.array_equal(H4 ^ H200, x))
check("4, 200 idempotent", np.array_equal(H4[H4], H4) and np.array_equal(H200[H200], H200))
check("4o200 = 200o4 = 0", not H4[H200].any() and not H200[H4].any())
bad = []
for rule in range(256):
    H, (G,) = jets(rule, 10, 1)
    xx = np.arange(1 << 10, dtype=np.uint32)
    c = H[0]
    Hb = H ^ c
    D = xx ^ H
    R = Hb[xx ^ D] ^ Hb[xx] ^ Hb[D]
    if not np.array_equal(R, G ^ G[0]) or G[0] != H[0]:
        bad.append(rule)
check("centered G = R_Hbar(I, D) and G(0) = H(0), all 256 rules", not bad, str(bad[:5]))

# ---- jet (#324): derivative maps and cadence identity ----
check("D_110 is rule 162, D_62 is rule 242",
      np.array_equal(x ^ H_table(110, n), H_table(162, n)) and np.array_equal(x ^ H_table(62, n), H_table(242, n)))
bad = []
for rule in range(256):
    H, (G, Q, Rr) = jets(rule, 10, 3)
    H2 = H[H]
    lhs = G[H2] ^ H2[G]                       # C_{H^2}(G)
    P = H[H[G] ^ Q] ^ H[H[G]] ^ H[Q] ^ H[0]   # B_H(H o G, C_H(G)) normalised so B(0,0)=0
    if not np.array_equal(lhs, Rr ^ P ^ H[0]):
        bad.append(rule)
check("C_{H^2}(G) = R xor B_H(H(G),Q) xor H(0), all 256 rules", not bad, str(bad[:5]))

# ---- asymptotic closure (#318-320): reserve R(n) = n - H(stable parity quotient), F = H^2 ----
want = {16: {30: 0.000244, 54: 0.7441, 110: 0.5385, 184: 4.0045},
        18: {30: 0.000130, 54: 0.7724, 110: 0.6059, 184: 4.5020}}
big = "--big" in sys.argv
for n in ([16, 18] if big else [16]):
    par = block_parity(n)
    for rule, target in want[n].items():
        H = H_table(rule, n)
        lab, rounds = future_quotient(H[H], classes(par)[1])
        r = forgotten_bits(lab, n)
        check(f"reserve rule {rule} n={n}", abs(r - target) < 6e-4 * max(1, target) + 5e-6,
              f"mine {r:.6f} vs note {target}  (refinement rounds {rounds})")

# ---- latent Q (#323): O = (parity, G) under F = H^2 merges exactly two pairs ----
for n in ([6, 8, 10, 12, 14, 16, 18] if big else [6, 8, 10, 12, 14, 16]):
    H, (G,) = jets(110, n, 1)
    _, obs = classes(block_parity(n), G)
    lab, _ = future_quotient(H[H], obs)
    k = int(lab.max()) + 1
    sizes = np.bincount(lab)
    merged = [tuple(np.flatnonzero(lab == c)) for c in np.flatnonzero(sizes > 1)]
    alt = (int("01" * (n // 2), 2), int("10" * (n // 2), 2))
    uni = (0, (1 << n) - 1)
    check(f"(P,G) quotient n={n}: 2^n-2 classes, merges = uniform & alternating pairs",
          k == (1 << n) - 2 and sorted(merged) == sorted([uni, alt]), f"classes {k}")

# ---- matched history (#321): next parity is a function of whole current (P,G) for 110, not for 62 ----
for n in (12, 14, 16):
    par = block_parity(n)
    res = {}
    for rule in (110, 62):
        H, (G,) = jets(rule, n, 1)
        G0 = G ^ G[0]
        k_obs, obs = classes(par, G0)
        k_joint, _ = classes(obs, par[H[H]])
        res[rule] = (k_obs == k_joint)
    check(f"n={n}: whole-field (P,G°) determines next parity for 110, fails for 62",
          res[110] and not res[62], str(res))

# ---- jet ring injectivity (#329 and its review) ----
n = 18
H, J = jets(54, n, 5)
k5, _ = classes(*J)
check("Rule 54 J5 retains 261,985 of 262,144 states at n=18", k5 == 261985, f"mine {k5}")
n = 20 if big else 16
print(f"bits forgotten by J3=(G,Q,R) on the n={n} ring (review quotes n=20: 30 8e-6, 54 2.9e-3, 110 1.1e-5, 62 0.16):")
for rule in (30, 54, 110, 62):
    H, J = jets(rule, n, 3)
    _, lab = classes(*J)
    print(f"   rule {rule:3d}: {forgotten_bits(lab, n):.6f}")

print("\nALL PASS" if ok else "\nSOME FAILED")
sys.exit(0 if ok else 1)
