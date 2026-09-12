#!/usr/bin/env python3
"""Refinement depth at most two, certified at every ring by sparse boolean powers
(protocol frozen 2026-09-12, gate-1 approval by OpenAI GPT-5.6 Sol at
5c58570b834ed5ea66482c5f0bc731f3d705a122 before this implementation; see the
protocol's Section 5).

For observations psi in {232, 4, 32, 200, 22, 102, 90, 150} and every rule r,
the depth-two pair graph G2_{psi,r} is the fifteenth unit's, imported from
scripts/verify_full_shift_depth_two.py and not rebuilt here: 4096 vertices (the
six-cell pair blocks), an edge per seven-cell pair block whose centre agrees on
psi, psi F and psi F^2, and the violating three-edge walks (v0, v3) read off the
262144 nine-cell pair blocks. Its strong components prune the violating walks to
the closed-violation set V2_cl (both ends in one strong component); a rule with
V2_cl empty is trivially certified at every ring with no power computed.

Ring criterion (protocol Section 1, theorem): for n >= 4,
  r not in D2_psi(n)  iff  some (v0, v3) in V2_cl has (A^(n-3))[v3, v0] = 1,
with A[u, w] = 1 for each edge u -> w. Powers are exact boolean products taken
in the sparse packed form the protocol freezes: out-degree is at most four, so
  A^m[u, :] = OR over w in out(u) of A^(m-1)[w, :],
four row gathers and three ORs on rows of 64 unsigned 64-bit words. The repeat
scan stores the SHA-256 of each power (not the power) against its exponent and,
on a hash hit, recomputes A^k from A^0 and compares byte for byte before
accepting the certificate (k, p), so a collision can only delay a certificate,
never falsify one. A pair whose powers have not repeated by the frozen cap
A^POWER_CAP is censored: its membership is decided only for 4 <= n <= cap + 3,
and no observation-level all-ring verdict is inferred through it.

P1  criterion == the fifteenth unit's recorded D2_psi(n) on rings 4..14; every
    FS1 rule has V2_cl empty (theorem, checked); FS2 subset of every certified
    D2_psi(n); divisibility D2(kn) subset of D2(n) on certified rings; and, on
    the frozen sample (the three smallest rules with V2_cl nonempty per
    observation), the packed powers A^1..A^40 equal dense float-matmul boolean
    powers computed by an independent reference path.
P2  per-pair status and (k, p), |V2|, |V2_cl|, per-observation max k, L, P, N,
    the certified list, D2^inf, status counts, powers taken, hash collisions.
P3  (a) bet P_psi == 1 for 232, 4, 32, 200; (b) bet P_22 == 3; (c) theorem
    controls for 102, 90 odd, 150 off multiples of three; (d) bets P_90 a
    multiple of 4 and P_150 a multiple of 6.
P4  the unit's main bet: the all-ring depth-two gap equals the fifteenth unit's
    rings-3-to-14 gap for every observation.
P5  complement and reflection covariance of D2_psi(n) at every certified ring,
    and equality of certificate status and (k, p) under the explicit vertex
    permutation maps (complement v -> v xor 4095; reflection v -> reversed
    cells, which transposes A), with the graph correspondence itself checked.

Usage:
      python scripts/verify_depth_two_certificate.py                # canonical run
      python scripts/verify_depth_two_certificate.py --self-test    # < 2 min, writes nothing
      python scripts/verify_depth_two_certificate.py --observation 232   # probe, writes nothing
The self test runs the dense-vs-sparse cross-check on a small frozen sample, the
FS1-has-no-closed-violation theorem on a subset, and the repeat-detection scan
on synthetic graphs with known certificates, including a deliberately weakened
hash to exercise the collision path, and writes nothing.
"""
from __future__ import annotations
import hashlib, importlib.util, json, math, pathlib, sys, time
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIFTEENTH_SCRIPT = ROOT / 'scripts/verify_full_shift_depth_two.py'
DEPTH_TWO = ROOT / 'results/full_shift_depth_two_20260911.json'
DEPTH_ONE = ROOT / 'results/depth_one_certificate_20260911.json'
OUT = ROOT / 'results/depth_two_certificate_20260912.json'

OBS = (232, 4, 32, 200, 22, 102, 90, 150)
FOUR = (232, 4, 32, 200)
RINGS = tuple(range(3, 15))                 # the fifteenth unit's exhaustive rings
GRAPH_RINGS = tuple(range(4, 15))           # rings the criterion covers within the recorded range
POWER_CAP = 1024                            # frozen: A^0..A^POWER_CAP, first confirmed repeat or censored
VERTICES = 4096; WORDS = VERTICES // 64     # six-cell pair blocks, rows of 64 words of 64 bits
DENSE_SAMPLE_RULES = 3                      # frozen sample: three smallest rules with V2_cl nonempty
DENSE_SAMPLE_POWERS = 40                    # frozen: A^1..A^40 compared against the dense reference
SELF_TEST_POWERS = 6                        # self test only: a shorter dense comparison
SELF_TEST_FS1_RULES = 12                    # self test only: subset size for the FS1 theorem control

# ---------------------------------------------------------------- the fifteenth unit's graph, reused
def _load_fifteenth():
    spec = importlib.util.spec_from_file_location('verify_full_shift_depth_two', FIFTEENTH_SCRIPT)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
U = _load_fifteenth()
depth_two_graph = U.depth_two_graph           # 4096-vertex pair graph and violating (v0, v3) walks
strong_components = U.strong_components       # iterative Tarjan
conj = U.conj; mirror = U.mirror; sha = U.sha

def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    raise TypeError(type(o))
def lcm(a, b): return a * b // math.gcd(a, b)
def divisors(p): return [q for q in range(1, p + 1) if p % q == 0]

# ---------------------------------------------------------------- vertex permutation maps (P5)
def vertex_complement(v):
    """Complementing both tracks maps each cell code c = 2x + y to 3 - c, i.e. v -> v xor 4095."""
    return v ^ (VERTICES - 1)
def vertex_mirror(v):
    """Reflection reverses the six cells of the block."""
    out = 0
    for j in range(6): out = (out << 2) | ((v >> (2 * j)) & 3)
    return out

# ---------------------------------------------------------------- sparse packed boolean powers
class Powers:
    """Boolean powers of a 4096-vertex adjacency of out-degree at most four.

    Rows are packed as WORDS unsigned 64-bit words; bit w of row u is A[u, w].
    A^m = A . A^(m-1) row by row: A^m[u, :] = OR over w in out(u) of A^(m-1)[w, :].
    One padding row of zeros carries the out-degrees below four, so the gather is
    a single fancy-index of shape (VERTICES, 4, WORDS).
    """
    __slots__ = ('nb',)
    def __init__(self, adj):
        nb = np.full((VERTICES, 4), VERTICES, dtype=np.int64)
        for u, outs in enumerate(adj):
            assert len(outs) == len(set(outs)) <= 4, (u, outs)
            for j, w in enumerate(outs): nb[u, j] = w
        self.nb = nb
    def identity(self):
        M = np.zeros((VERTICES + 1, WORDS), dtype=np.uint64)
        for u in range(VERTICES): M[u, u >> 6] = np.uint64(1) << np.uint64(u & 63)
        return M
    def mul(self, P):
        g = P[self.nb]                                           # (VERTICES, 4, WORDS)
        Q = np.zeros((VERTICES + 1, WORDS), dtype=np.uint64)
        Q[:VERTICES] = (g[:, 0] | g[:, 1]) | (g[:, 2] | g[:, 3])
        return Q
    def power(self, m):
        M = self.identity()
        for _ in range(m): M = self.mul(M)
        return M

def unpack(P):
    """Packed rows as a dense (VERTICES, VERTICES) uint8 matrix, for the cross-check only."""
    return np.unpackbits(np.ascontiguousarray(P[:VERTICES]).view(np.uint8), axis=1, bitorder='little')

def sha_power(P): return hashlib.sha256(np.ascontiguousarray(P[:VERTICES]).tobytes()).hexdigest()
def weak_hash(P): return sha_power(P)[:2]        # self test only: forces collisions

# ---------------------------------------------------------------- the repeat scan and the certificate
def scan(adj, closed, cap=POWER_CAP, hashfn=sha_power):
    """Take powers until the first byte-confirmed repeat or the cap.

    Returns status, k, p, the hit list b (b[m] is True iff some closed violating
    walk has A^m[v3, v0] = 1), the number of powers taken including the
    recomputations of a confirmation, and any hash collisions. The hash table
    keeps every exponent seen for a hash, earliest first; a candidate equality is
    confirmed by recomputing A^k from A^0 and comparing byte for byte, so a
    collision only delays the scan.
    """
    P = Powers(adj)
    rows = np.array([v3 for _, v3 in closed], dtype=np.int64)
    words = np.array([v0 >> 6 for v0, _ in closed], dtype=np.int64)
    masks = np.array([1 << (v0 & 63) for v0, _ in closed], dtype=np.uint64)
    def hit(M): return bool(np.any(M[rows, words] & masks))
    cur = P.identity(); b = [hit(cur)]; table = {hashfn(cur): [0]}; taken = 0; collisions = []
    for m in range(1, cap + 1):
        cur = P.mul(cur); taken += 1; b.append(hit(cur)); h = hashfn(cur)
        seen = table.setdefault(h, [])
        confirmed = None
        for k in seen:                                           # earliest exponent first
            again = P.power(k); taken += k
            if np.array_equal(np.ascontiguousarray(again[:VERTICES]), np.ascontiguousarray(cur[:VERTICES])):
                confirmed = k; break
            collisions.append({'hash': h, 'exponent': m, 'candidate_exponent': k})
        if confirmed is not None:
            return {'status': 'certified', 'k': confirmed, 'p': m - confirmed, 'b': b,
                    'powers_taken': taken, 'collisions': collisions}
        seen.append(m)
    return {'status': 'censored', 'k': None, 'p': None, 'b': b, 'powers_taken': taken, 'collisions': collisions}

def pair_certificate(psi, r, cap=POWER_CAP):
    """Certificate of (psi, r): trivially certified, (k, p), or censored."""
    adj, walks = depth_two_graph(psi, r)
    comp = strong_components(adj)
    closed = [(v0, v3) for v0, v3 in walks if comp[v0] == comp[v3]]
    if not closed:
        return {'status': 'trivially_certified', 'k': None, 'p': None, 'b': None, 'powers_taken': 0,
                'collisions': [], 'violating_walks': len(walks), 'closed_violating_walks': 0}
    c = scan(adj, closed, cap=cap)
    c['violating_walks'] = len(walks); c['closed_violating_walks'] = len(closed)
    return c

def member(c, n):
    """r in D2(n) by the ring criterion; None beyond the decided range of a censored pair."""
    if c['status'] == 'trivially_certified': return True
    e = n - 3; b = c['b']
    if e < len(b): return not b[e]
    if c['p'] is None: return None
    k, p = c['k'], c['p']
    return not b[k + (e - k) % p]

def rule_period(c):
    """Least eventual period of the rule's membership sequence (1 when trivially certified)."""
    if c['status'] == 'trivially_certified': return 1
    if c['status'] == 'censored': return None
    k, p, b = c['k'], c['p'], c['b']
    for q in divisors(p):
        if all(b[k + i] == b[k + ((i + q) % p)] for i in range(p)): return q
    return p

def rule_onset(c, P):
    """Least N >= 4 from which the rule's membership satisfies m(n + P) == m(n) for all n >= N."""
    if c['status'] == 'trivially_certified': return 4
    N = max(4, c['k'] + 3)
    while N > 4 and member(c, N - 1 + P) == member(c, N - 1): N -= 1
    return N

# ---------------------------------------------------------------- observation-level analysis
def analyse(psi, cap=POWER_CAP, verbose=False):
    certs = {}
    for r in range(256):
        certs[r] = pair_certificate(psi, r, cap=cap)
        if verbose and certs[r]['status'] != 'trivially_certified':
            print(f'  psi={psi} r={r:3d} {certs[r]["status"]:19s} k={certs[r]["k"]} p={certs[r]["p"]} '
                  f'|V2|={certs[r]["violating_walks"]} |V2cl|={certs[r]["closed_violating_walks"]}', flush=True)
    censored = [r for r in range(256) if certs[r]['status'] == 'censored']
    trivial = [r for r in range(256) if certs[r]['status'] == 'trivially_certified']
    ks = [certs[r]['k'] for r in range(256) if certs[r]['status'] == 'certified']
    out = {'certs': certs, 'censored': censored, 'trivial': trivial,
           'max_k': max(ks) if ks else 0, 'powers_taken': sum(certs[r]['powers_taken'] for r in range(256)),
           'collisions': [dict(c, rule=r) for r in range(256) for c in certs[r]['collisions']]}
    if censored:
        out.update({'N0': None, 'L': None, 'P': None, 'N': None, 'all_ring': None,
                    'decided_rings': (4, cap + 3), 'D': {n: sorted(r for r in range(256) if member(certs[r], n))
                                                         for n in range(4, cap + 4)}})
        return out
    L = 1
    for r in range(256):
        if certs[r]['status'] == 'certified': L = lcm(L, certs[r]['p'])
    P = 1
    for r in range(256): P = lcm(P, rule_period(certs[r]))
    N = max(rule_onset(certs[r], P) for r in range(256))
    D = {n: sorted(r for r in range(256) if member(certs[r], n)) for n in range(4, max(N + P, 15))}
    inf = sorted(set(range(256)).intersection(*[set(D[n]) for n in range(4, N + P)]))
    out.update({'N0': 3 + out['max_k'], 'L': L, 'P': P, 'N': N, 'all_ring': inf,
                'decided_rings': (4, None), 'D': D})
    return out

def membership_set(g, n):
    """D2(n) from an analysis, computing on demand beyond the stored range."""
    if n in g['D']: return g['D'][n]
    ms = [member(g['certs'][r], n) for r in range(256)]
    return None if any(m is None for m in ms) else sorted(r for r in range(256) if ms[r])

# ---------------------------------------------------------------- the independent dense reference (P1)
def dense_reference_powers(adj, count):
    """A^1..A^count as explicit dense boolean matrices by float matmul, the fourteenth unit's path.

    Deliberately independent of Powers: the matrix is materialized in full, the
    product is taken as M . A (the opposite association to the sparse row gather)
    by a BLAS float32 matmul thresholded at zero, and no packed row ever appears.
    """
    A = np.zeros((VERTICES, VERTICES), dtype=np.uint8)
    for u, outs in enumerate(adj):
        for w in outs: A[u, w] = 1
    Af = A.astype(np.float32); M = A.copy(); out = [M.copy()]
    for _ in range(count - 1):
        M = ((M.astype(np.float32) @ Af) > 0).astype(np.uint8); out.append(M)
    return out

def dense_cross_check(psi, r, count):
    adj, _ = depth_two_graph(psi, r)
    P = Powers(adj); cur = P.identity()
    ref = dense_reference_powers(adj, count)
    mismatches = []
    for m in range(1, count + 1):
        cur = P.mul(cur)
        if not np.array_equal(unpack(cur), ref[m - 1]): mismatches.append(m)
    return {'psi': psi, 'rule': r, 'powers': count, 'mismatching_exponents': mismatches, 'pass': not mismatches}

# ---------------------------------------------------------------- symmetry correspondence (P5)
def permutation_correspondence(psi, r):
    """The complement and reflection vertex maps carry G2_{psi,r} onto its images.

    Complement: v -> v xor 4095 on both endpoints of every edge and of every
    violating walk. Reflection: v -> reversed cells, with edges and violating
    walks reversed, so A transposes.
    """
    adj, walks = depth_two_graph(psi, r)
    edges = {(u, w) for u, outs in enumerate(adj) for w in outs}; W = set(walks)
    adj_c, walks_c = depth_two_graph(conj(psi), conj(r))
    ec = {(u, w) for u, outs in enumerate(adj_c) for w in outs}
    comp_edges_ok = ec == {(vertex_complement(u), vertex_complement(w)) for u, w in edges}
    comp_walks_ok = set(walks_c) == {(vertex_complement(a), vertex_complement(b)) for a, b in W}
    adj_m, walks_m = depth_two_graph(mirror(psi), mirror(r))
    em = {(u, w) for u, outs in enumerate(adj_m) for w in outs}
    mir_edges_ok = em == {(vertex_mirror(w), vertex_mirror(u)) for u, w in edges}
    mir_walks_ok = set(walks_m) == {(vertex_mirror(b), vertex_mirror(a)) for a, b in W}
    return {'complement_edges': comp_edges_ok, 'complement_violating_walks': comp_walks_ok,
            'reflection_edges': mir_edges_ok, 'reflection_violating_walks': mir_walks_ok,
            'pass': comp_edges_ok and comp_walks_ok and mir_edges_ok and mir_walks_ok}

def cert_key(c): return [c['status'], c['k'], c['p']]

# ---------------------------------------------------------------- self test (writes nothing)
def self_test():
    t0 = time.time(); problems = []
    d2 = json.loads(DEPTH_TWO.read_text())
    FS1 = {psi: d2['full_shift_depth_one'][str(psi)] for psi in OBS}

    # (a) dense-vs-sparse cross-check on a small frozen sample
    psi = 232; sample = None
    for r in range(256):
        c = pair_certificate(psi, r, cap=4)
        if c['closed_violating_walks']: sample = r; break
    if sample is None: problems.append('no rule with a closed violating walk under 232')
    else:
        x = dense_cross_check(psi, sample, SELF_TEST_POWERS)
        print(f'cross-check psi=232 r={sample} powers={SELF_TEST_POWERS} pass={x["pass"]}')
        if not x['pass']: problems.append(f'dense cross-check mismatched at exponents {x["mismatching_exponents"]}')

    # (b) the FS1 theorem control on a subset
    bad = []
    for r in FS1[psi][:SELF_TEST_FS1_RULES]:
        adj, walks = depth_two_graph(psi, r); comp = strong_components(adj)
        if [(a, b) for a, b in walks if comp[a] == comp[b]]: bad.append(r)
    print(f'FS1 control psi=232 rules={FS1[psi][:SELF_TEST_FS1_RULES]} closed_violations={bad}')
    if bad: problems.append(f'FS1 rules with a closed violating walk: {bad}')

    # (c) repeat detection on synthetic graphs with known certificates
    cyc5 = [[] for _ in range(VERTICES)]
    for i in range(5): cyc5[i] = [(i + 1) % 5]
    c = scan(cyc5, [(0, 3)])
    expect_b = [(m % 5) == 2 for m in range(len(c['b']))]          # A^m[3, 0] = 1 iff m = 2 mod 5
    ok5 = (c['status'], c['k'], c['p']) == ('certified', 1, 5) and c['b'][1:] == expect_b[1:]
    print(f'synthetic 5-cycle certificate={(c["status"], c["k"], c["p"])} b_ok={c["b"][1:] == expect_b[1:]}')
    if not ok5: problems.append(f'5-cycle certificate wrong: {(c["status"], c["k"], c["p"])}')
    cw = scan(cyc5, [(0, 3)], hashfn=weak_hash)
    print(f'synthetic 5-cycle under a weakened hash certificate={(cw["status"], cw["k"], cw["p"])} '
          f'collisions={len(cw["collisions"])}')
    if (cw['status'], cw['k'], cw['p']) != ('certified', 1, 5):
        problems.append('weakened-hash scan did not recover the 5-cycle certificate')
    if not cw['collisions']: problems.append('weakened hash recorded no collision, so the path is untested')
    long_cycle = 2 * POWER_CAP
    cyc = [[] for _ in range(VERTICES)]
    for i in range(long_cycle): cyc[i] = [(i + 1) % long_cycle]
    cc = scan(cyc, [(0, 3)])
    print(f'synthetic {long_cycle}-cycle status={cc["status"]} powers={cc["powers_taken"]}')
    if cc['status'] != 'censored': problems.append('a cycle longer than the cap was not censored')

    print(f'self test {"PASS" if not problems else "FAIL"} in {time.time() - t0:.1f}s')
    for p in problems: print('   ', p)
    return 1 if problems else 0

# ---------------------------------------------------------------- probe (writes nothing)
def probe(psi):
    d2 = json.loads(DEPTH_TWO.read_text())
    rec = {n: d2['exhaustive_depth_two'][str(psi)][str(n)] for n in RINGS} if str(psi) in d2['exhaustive_depth_two'] else {}
    t0 = time.time(); g = analyse(psi, verbose=True); el = time.time() - t0
    print(f'psi={psi} trivial={len(g["trivial"])} censored={len(g["censored"])} max_k={g["max_k"]} '
          f'L={g["L"]} P={g["P"]} N={g["N"]} powers={g["powers_taken"]} collisions={len(g["collisions"])} in {el:.1f}s')
    for n in GRAPH_RINGS:
        got = membership_set(g, n)
        flag = '' if not rec else ('  ==recorded' if got == rec[n] else f'  != recorded ({len(rec[n])})')
        print(f'  D2({n}) size {len(got)}{flag}')
    if g['all_ring'] is not None:
        gap = [r for r in g['all_ring'] if r not in d2['full_shift_depth_two'][str(psi)]]
        print(f'  all-ring size {len(g["all_ring"])}  gap vs FS2 {gap}')
    return 0

# ---------------------------------------------------------------- canonical run
def main(argv):
    if '--self-test' in argv: return self_test()
    if '--observation' in argv: return probe(int(argv[argv.index('--observation') + 1]))
    d2 = json.loads(DEPTH_TWO.read_text()); d1 = json.loads(DEPTH_ONE.read_text())
    REC = {psi: {n: d2['exhaustive_depth_two'][str(psi)][str(n)] for n in RINGS} for psi in OBS}
    FS1 = {psi: d2['full_shift_depth_one'][str(psi)] for psi in OBS}
    FS2 = {psi: d2['full_shift_depth_two'][str(psi)] for psi in OBS}
    GAP_14 = {psi: d2['predictions']['M5_depth_two_gap']['all_tested_ring_gap'][str(psi)] for psi in OBS}
    D1_PERIODS = {psi: d1['predictions']['L3_certificates'][str(psi)]['least_eventual_period_P'] for psi in OBS}

    all_obs = sorted(set(OBS) | {conj(p) for p in OBS} | {mirror(p) for p in OBS})
    G = {}
    for psi in all_obs:
        t0 = time.time(); G[psi] = analyse(psi)
        print(f'psi={psi} trivial={len(G[psi]["trivial"])} censored={len(G[psi]["censored"])} '
              f'max_k={G[psi]["max_k"]} P={G[psi]["P"]} N={G[psi]["N"]} powers={G[psi]["powers_taken"]} '
              f'in {time.time() - t0:.1f}s', flush=True)

    P = {}
    # ---------------- P1
    crit = {str(psi): {str(n): membership_set(G[psi], n) == REC[psi][n] for n in GRAPH_RINGS} for psi in OBS}
    fs1 = {str(psi): [r for r in FS1[psi] if G[psi]['certs'][r]['closed_violating_walks']] for psi in OBS}
    def certified_rings(psi):
        g = G[psi]
        return range(4, POWER_CAP + 4) if g['censored'] else range(4, g['N'] + g['P'])
    fs2_sub = {str(psi): [n for n in certified_rings(psi) if not set(FS2[psi]) <= set(membership_set(G[psi], n))] for psi in OBS}
    div = {}
    for psi in OBS:
        rs = list(certified_rings(psi)); bad = []
        for n in rs:
            for kn in rs:
                if kn > n and kn % n == 0 and not set(membership_set(G[psi], kn)) <= set(membership_set(G[psi], n)):
                    bad.append([n, kn])
        div[str(psi)] = bad
    sample = {psi: [r for r in range(256) if G[psi]['certs'][r]['closed_violating_walks']][:DENSE_SAMPLE_RULES] for psi in OBS}
    dense = [dense_cross_check(psi, r, DENSE_SAMPLE_POWERS) for psi in OBS for r in sample[psi]]
    p1 = {'criterion_equals_recorded': crit, 'FS1_rules_with_closed_violation': fs1,
          'FS2_not_subset_at_rings': fs2_sub, 'divisibility_violations': div,
          'dense_sample': {str(psi): sample[psi] for psi in OBS}, 'dense_cross_check': dense}
    p1['pass'] = (all(v for d in crit.values() for v in d.values()) and all(not v for v in fs1.values())
                  and all(not v for v in fs2_sub.values()) and all(not v for v in div.values())
                  and all(x['pass'] for x in dense))
    P['P1_criterion_exact'] = p1

    # ---------------- P2
    p2 = {}
    for psi in OBS:
        g = G[psi]; c = g['certs']
        p2[str(psi)] = {
            'status_counts': {'trivially_certified': len(g['trivial']),
                              'certified': sum(1 for r in range(256) if c[r]['status'] == 'certified'),
                              'censored': len(g['censored'])},
            'censored_rules': g['censored'], 'max_k': g['max_k'], 'lcm_p': g['L'],
            'least_eventual_period_P': g['P'], 'onset_ring_N': g['N'], 'powers_taken': g['powers_taken'],
            'hash_collisions': g['collisions'],
            'k_p_by_rule': {str(r): ('trivially_certified' if c[r]['status'] == 'trivially_certified'
                                     else 'censored' if c[r]['status'] == 'censored' else [c[r]['k'], c[r]['p']])
                            for r in range(256)},
            'violating_walks': {str(r): c[r]['violating_walks'] for r in range(256)},
            'closed_violating_walks': {str(r): c[r]['closed_violating_walks'] for r in range(256)},
            'certified_depth_two_sets': (None if g['censored']
                                         else {str(n): membership_set(g, n) for n in range(4, g['N'] + g['P'])}),
            'decided_counts': {str(n): len(membership_set(g, n)) for n in certified_rings(psi)},
            'all_ring_depth_two': g['all_ring'], 'ring_3_from_fifteenth_unit': REC[psi][3]}
    P['P2_certificates'] = p2

    # ---------------- P3
    def censored(psi): return bool(G[psi]['censored'])
    p3a = {str(psi): ('censored' if censored(psi) else G[psi]['P']) for psi in FOUR}
    p3a_fail = {str(psi): ('censored' if censored(psi) else
                           sorted({r for n in range(G[psi]['N'], G[psi]['N'] + G[psi]['P'])
                                   for r in set(membership_set(G[psi], n)) ^ set(membership_set(G[psi], G[psi]['N']))}))
                for psi in FOUR if censored(psi) or G[psi]['P'] != 1}
    p3b = 'censored' if censored(22) else G[22]['P']
    full = list(range(256))
    p3c = {'102_all_256': ('censored' if censored(102) else
                           [n for n in certified_rings(102) if membership_set(G[102], n) != full]),
           '90_odd_all_256': ('censored' if censored(90) else
                              [n for n in certified_rings(90) if n % 2 == 1 and membership_set(G[90], n) != full]),
           '150_off_multiples_of_three_all_256': ('censored' if censored(150) else
                                                  [n for n in certified_rings(150) if n % 3 and membership_set(G[150], n) != full])}
    p3d = {'P_90': 'censored' if censored(90) else G[90]['P'], 'P_150': 'censored' if censored(150) else G[150]['P'],
           'depth_one_periods': {str(psi): D1_PERIODS[psi] for psi in OBS}}
    p3 = {'a_periods_of_the_four': p3a, 'a_oscillating_rules': p3a_fail, 'b_period_under_22': p3b,
          'c_theorem_controls': p3c, 'd_linear_periods': p3d,
          'periods': {str(psi): ('censored' if censored(psi) else G[psi]['P']) for psi in OBS},
          'onsets': {str(psi): ('censored' if censored(psi) else G[psi]['N']) for psi in OBS}}
    p3['pass_a'] = all(v == 1 for v in p3a.values()); p3['pass_b'] = p3b == 3
    p3['pass_c'] = all(v == [] for v in p3c.values())
    p3['pass_d'] = (p3d['P_90'] != 'censored' and p3d['P_150'] != 'censored'
                    and p3d['P_90'] % 4 == 0 and p3d['P_150'] % 6 == 0)
    p3['pass'] = p3['pass_a'] and p3['pass_b'] and p3['pass_c'] and p3['pass_d']
    P['P3_eventual_periods'] = p3

    # ---------------- P4
    p4 = {}
    for psi in OBS:
        if censored(psi): p4[str(psi)] = 'censored'; continue
        g = G[psi]; inf_gap = [r for r in g['all_ring'] if r not in FS2[psi]]
        leaving = {}
        for r in GAP_14[psi]:
            if r not in g['all_ring']:
                n = next(n for n in range(4, g['N'] + g['P']) if r not in membership_set(g, n))
                c = g['certs'][r]
                adj, walks = depth_two_graph(psi, r); comp = strong_components(adj)
                closed = [(v0, v3) for v0, v3 in walks if comp[v0] == comp[v3]]
                M = Powers(adj).power(n - 3)
                w = next(((v0, v3) for v0, v3 in closed if (int(M[v3, v0 >> 6]) >> (v0 & 63)) & 1), None)
                leaving[str(r)] = {'least_ring': n, 'witness_v0': None if w is None else w[0],
                                   'witness_v3': None if w is None else w[1], 'k': c['k'], 'p': c['p']}
        p4[str(psi)] = {'all_ring_gap': inf_gap, 'rings_3_to_14_gap': GAP_14[psi],
                        'equal': inf_gap == GAP_14[psi], 'rules_leaving_after_ring_14': leaving}
    p4['nonempty_observed'] = [psi for psi in OBS if p4[str(psi)] != 'censored' and p4[str(psi)]['all_ring_gap']]
    p4['pass'] = all(p4[str(psi)] != 'censored' and p4[str(psi)]['equal'] for psi in OBS)
    P['P4_all_ring_gap'] = p4

    # ---------------- P5
    def compare_rings(psi, other):
        lo, hi = 4, 14
        for q in (psi, other):
            g = G[q]; hi = max(hi, POWER_CAP + 3 if g['censored'] else g['N'] + g['P'] - 1)
        hi = min(hi, POWER_CAP + 3)
        return range(lo, hi + 1)
    p5 = {'complement_sets': {}, 'reflection_sets': {}, 'complement_certificates': {}, 'reflection_certificates': {},
          'graph_correspondence': {}}
    for psi in OBS:
        cq, mq = conj(psi), mirror(psi)
        p5['complement_sets'][str(psi)] = [n for n in compare_rings(psi, cq)
                                           if membership_set(G[cq], n) != sorted(conj(r) for r in membership_set(G[psi], n))]
        p5['reflection_sets'][str(psi)] = [n for n in compare_rings(psi, mq)
                                          if membership_set(G[mq], n) != sorted(mirror(r) for r in membership_set(G[psi], n))]
        p5['complement_certificates'][str(psi)] = [r for r in range(256)
                                                   if cert_key(G[cq]['certs'][conj(r)]) != cert_key(G[psi]['certs'][r])]
        p5['reflection_certificates'][str(psi)] = [r for r in range(256)
                                                   if cert_key(G[mq]['certs'][mirror(r)]) != cert_key(G[psi]['certs'][r])]
        corr = {r: permutation_correspondence(psi, r) for r in range(256)}
        p5['graph_correspondence'][str(psi)] = {'failing_rules': [r for r in range(256) if not corr[r]['pass']],
                                                'detail': {str(r): corr[r] for r in range(256) if not corr[r]['pass']}}
        print(f'P5 psi={psi} set mismatches {len(p5["complement_sets"][str(psi)])}/'
              f'{len(p5["reflection_sets"][str(psi)])} cert mismatches '
              f'{len(p5["complement_certificates"][str(psi)])}/{len(p5["reflection_certificates"][str(psi)])} '
              f'graph failures {len(p5["graph_correspondence"][str(psi)]["failing_rules"])}', flush=True)
    p5['pass'] = (all(not v for v in p5['complement_sets'].values()) and all(not v for v in p5['reflection_sets'].values())
                  and all(not v for v in p5['complement_certificates'].values())
                  and all(not v for v in p5['reflection_certificates'].values())
                  and all(not v['failing_rules'] for v in p5['graph_correspondence'].values()))
    P['P5_symmetries'] = p5

    report = {'protocol': 'depth-two-certificate-20260912', 'schema': 1, 'observations': list(OBS),
              'rings_from_fifteenth_unit': list(RINGS),
              'parameters': {'power_cap': POWER_CAP, 'vertices': VERTICES, 'packed_words_per_row': WORDS,
                             'max_out_degree': 4, 'edge_blocks': 4 ** 7, 'violation_blocks': 4 ** 9,
                             'dense_sample_rules_per_observation': DENSE_SAMPLE_RULES,
                             'dense_sample_powers': DENSE_SAMPLE_POWERS,
                             'decided_rings_when_censored': [4, POWER_CAP + 3]},
              'source_hashes': {'script': sha(pathlib.Path(__file__)),
                                'full_shift_depth_two_script': sha(FIFTEENTH_SCRIPT),
                                'full_shift_depth_two_result': sha(DEPTH_TWO),
                                'depth_one_certificate_result': sha(DEPTH_ONE)},
              'all_ring_depth_two': {str(psi): G[psi]['all_ring'] for psi in OBS},
              'full_shift_depth_two_from_fifteenth_unit': {str(psi): FS2[psi] for psi in OBS},
              'conjugate_and_mirror_summary': {str(q): {'censored': len(G[q]['censored']), 'P': G[q]['P'], 'N': G[q]['N']}
                                               for q in all_obs if q not in OBS},
              'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary']))
    print('periods', p3['periods']); print('onsets', p3['onsets'])
    print('all-ring sizes', {psi: (len(G[psi]['all_ring']) if G[psi]['all_ring'] is not None else None) for psi in OBS})
    print('all-ring gaps', {psi: (p4[str(psi)]['all_ring_gap'] if p4[str(psi)] != 'censored' else 'censored') for psi in OBS})
    print('written', OUT.relative_to(ROOT))
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
