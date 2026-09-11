#!/usr/bin/env python3
"""Depth-one certificate (protocol frozen 2026-09-11, gate-1 sign-off by Codex at
c23c3a3 after one correction round, before this implementation; see the
protocol's Section 6).

For observations psi in {232, 4, 32, 200, 22, 102, 90, 150} and every rule r:
exhaustive depth-one sets D_psi(n) = {r : h_* <= 1} on rings 3..14, the 256-vertex
depth-one pair graph G_{psi,r} (vertices four-cell pair blocks, edges five-cell
pair blocks agreeing on psi and on psi of the successor at the centre), the
violating three-edge walks read off the 16384 seven-cell pair blocks (two-step
observed successors disagree at the centre), the ring criterion
  r not in D_psi(n)  iff  some (v0..v3) has (A^(n-3))[v3, v0] = 1   (n >= 4),
the certificate (k, p) with A^(k+p) = A^k found within the frozen cap of
POWER_CAP powers (else censored), the observation-level least eventual period
P_psi and onset ring N_psi, the all-ring set (intersection over n >= 4) and the
full-shift depth-one set.

L1  divisibility D(kn) subset of D(n) on exhaustive rings (theorem control).
L2  criterion == exhaustive on rings 4..14; reference consistency with the
    recorded depth tables of units seven to ten at rings 6..12.
L3  certificates reported, with censoring.
L4  (a) 232, 4, 32, 200 constant from ring 10 (bet); (b) P_22 == 3 (bet);
    (c) D_102(n) == the parity 248 for n >= 6 (theorem control).
L5  150 all 256 off multiples of 3, 90 odd n >= 7 == the 248 (theorem); 90 even
    rings and 150 multiples of 3 reported.
L6  complement and reflection covariance at rings 4..14.
L7  all-ring depth one == full-shift depth one (bet).
"""
from __future__ import annotations
import hashlib, json, math, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
MAJORITY = ROOT / 'results/block_majority_20260911.json'
ISOLATED = ROOT / 'results/isolated_cell_20260911.json'
COMPLEMENT = ROOT / 'results/complement_observation_20260911.json'
LINEAR = ROOT / 'results/linear_observations_20260911.json'
OUT = ROOT / 'results/depth_one_certificate_20260911.json'
OBS = (232, 4, 32, 200, 22, 102, 90, 150); FOUR = (232, 4, 32, 200); LINEAR_OBS = (102, 90, 150)
RINGS = tuple(range(3, 15)); GRAPH_RINGS = tuple(range(4, 15)); REF_RINGS = tuple(range(6, 13))
POWER_CAP = 1024          # frozen: powers A^0..A^POWER_CAP, first repeat or censored
AFFINE = [0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195, 204, 240, 255]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64); return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)
def lut(r): return np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
def step(S, r):
    t = lut(r); return t[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
def ints(S): return (S.astype(np.int64) << (S.shape[1] - 1 - np.arange(S.shape[1]))).sum(axis=1)
def conj(r): return sum((((r >> (7 - i)) & 1) ^ 1) << i for i in range(8))
def mirror(r): return sum(((r >> (((i & 4) >> 2) | (i & 2) | ((i & 1) << 2))) & 1) << i for i in range(8))
def num(v):
    try: return int(v)
    except (TypeError, ValueError): return 10 ** 6
def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    raise TypeError(type(o))

# ---------------------------------------------------------------- exhaustive depth one
def exhaustive_depth_one(psi, n):
    S = all_states(n); y0 = ints(step(S, psi)); out = []
    for r in range(256):
        F1 = step(S, r); y1 = ints(step(F1, psi)); y2 = ints(step(step(F1, r), psi))
        key = y0 * (1 << n) + y1; order = np.argsort(key, kind='stable'); k, z = key[order], y2[order]
        if not np.any((k[1:] == k[:-1]) & (z[1:] != z[:-1])): out.append(r)
    return out

# ---------------------------------------------------------------- blocks and local maps
def pair_blocks(L):
    """All 4^L pair blocks as (x, y) arrays of shape (4^L, L); code MSB first, x bit above y bit per cell."""
    codes = np.arange(4 ** L, dtype=np.int64)
    cells = (codes[:, None] >> (2 * (L - 1 - np.arange(L)))) & 3
    return ((cells >> 1) & 1).astype(np.uint8), (cells & 1).astype(np.uint8)
def local(rule, X):
    """Apply an elementary rule along the last axis without wrap: output length L-2."""
    t = lut(rule); return t[4 * X[:, :-2] + 2 * X[:, 1:-1] + X[:, 2:]]
def vertex_codes(X, Y, start):
    """Codes of the four-cell pair block at columns start..start+3."""
    c = np.zeros(X.shape[0], dtype=np.int64)
    for j in range(4): c = c * 4 + (2 * X[:, start + j].astype(np.int64) + Y[:, start + j])
    return c
X5, Y5 = pair_blocks(5); X7, Y7 = pair_blocks(7)

def depth_one_graph(psi, r):
    """Adjacency (256x256, uint8) and the violating (v0, v3) list for (psi, r)."""
    ok = (local(psi, X5)[:, 1] == local(psi, Y5)[:, 1]) & (local(psi, local(r, X5))[:, 0] == local(psi, local(r, Y5))[:, 0])
    A = np.zeros((256, 256), dtype=np.uint8); A[vertex_codes(X5, Y5, 0)[ok], vertex_codes(X5, Y5, 1)[ok]] = 1
    fx, fy = local(r, X7), local(r, Y7)                                   # cells 1..5
    e = local(psi, X7) == local(psi, Y7)                                  # psi agreement at cells 1..5
    e1 = local(psi, fx) == local(psi, fy)                                 # psi F agreement at cells 2..4
    admissible = e[:, 1] & e[:, 2] & e[:, 3] & e1[:, 0] & e1[:, 1] & e1[:, 2]
    viol = admissible & (local(psi, local(r, fx))[:, 0] != local(psi, local(r, fy))[:, 0])
    walks = sorted(set(zip(vertex_codes(X7, Y7, 0)[viol].tolist(), vertex_codes(X7, Y7, 3)[viol].tolist())))
    return A, walks

def bool_powers(A):
    """A^0.. until first repeat or POWER_CAP; returns (powers, k, p) with p None when censored."""
    Af = A.astype(np.float32); powers = [np.eye(256, dtype=np.uint8)]; seen = {powers[0].tobytes(): 0}
    for _ in range(POWER_CAP):
        M = ((powers[-1].astype(np.float32) @ Af) > 0).astype(np.uint8); key = M.tobytes()
        if key in seen: k = seen[key]; return powers, k, len(powers) - k
        seen[key] = len(powers); powers.append(M)
    return powers, None, None

def full_shift_ok(A, walks):
    R = A.copy()                                                          # transitive closure by repeated squaring
    while True:
        Rf = R.astype(np.float32); R2 = R | ((Rf @ Rf) > 0).astype(np.uint8)
        if np.array_equal(R2, R): break
        R = R2
    on = np.array([R[v, v] for v in range(256)], dtype=bool)
    frm = on | (R[on].any(axis=0) if on.any() else np.zeros(256, dtype=bool))
    to = on | (R[:, on].any(axis=1) if on.any() else np.zeros(256, dtype=bool))
    ext = [(v0, v3) for v0, v3 in walks if frm[v0] and to[v3]]                # bi-infinitely extendable violating walks
    if not ext: return True, None
    # Gate-2 artifact-completeness addition (Codex, 2026-09-11): a deterministic witness for a
    # full-shift failure, with the reachability facts needed to audit it. `walks` is sorted, so
    # the first extendable walk is canonical. SCC of a vertex = vertices mutually reachable.
    v0, v3 = ext[0]
    def scc(v): return sorted(int(u) for u in range(256) if u == v or (R[u, v] and R[v, u]))
    witness = {'v0': int(v0), 'v3': int(v3), 'v0_on_cycle': bool(on[v0]), 'v0_reachable_from_cycle': bool(frm[v0]),
               'v3_on_cycle': bool(on[v3]), 'v3_reaches_cycle': bool(to[v3]), 'v3_reaches_v0': bool(R[v3, v0]),
               'v0_strong_component': scc(int(v0)), 'v3_strong_component': scc(int(v3)),
               'extendable_violating_walks': [[int(a), int(b)] for a, b in ext], 'violating_walks_total': len(walks)}
    return False, witness

class Cert:
    __slots__ = ('powers', 'k', 'p', 'walks', 'nwalks', 'full_shift', 'fs_witness')
def certificate(psi, r):
    A, walks = depth_one_graph(psi, r); powers, k, p = bool_powers(A)
    c = Cert(); c.powers, c.k, c.p, c.walks, c.nwalks = powers, k, p, walks, len(walks); c.full_shift, c.fs_witness = full_shift_ok(A, walks)
    return c
def member(c, n):
    """r in D(n) by the ring criterion; None when the exponent n-3 is beyond the computed powers of a censored pair."""
    e = n - 3
    if e >= len(c.powers):
        if c.p is None: return None
        e = c.k + (e - c.k) % c.p
    M = c.powers[e]
    return not any(M[v3, v0] for v0, v3 in c.walks)

def analyse(psi):
    certs = {r: certificate(psi, r) for r in range(256)}
    censored = [r for r in range(256) if certs[r].p is None]
    if censored:
        N0 = None; L = None; horizon = POWER_CAP + 3
    else:
        N0 = max(certs[r].k for r in range(256)) + 3; L = 1
        for r in range(256): L = L * certs[r].p // math.gcd(L, certs[r].p)
        horizon = max(N0 + 2 * L, 14)
    D = {}
    for n in range(4, horizon + 1):
        ms = [member(certs[r], n) for r in range(256)]
        D[n] = None if any(m is None for m in ms) else [r for r in range(256) if ms[r]]
    P = N = None
    if not censored:
        for q in sorted(d for d in range(1, L + 1) if L % d == 0):
            if all(D[n + q] == D[n] for n in range(N0, N0 + L)): P = q; break
        N = N0
        while N > 4 and D[N - 1 + P] == D[N - 1]: N -= 1
    inf = None if censored else sorted(set(range(256)).intersection(*[set(D[n]) for n in range(4, N0 + L + 1)]))
    fs = [r for r in range(256) if certs[r].full_shift]
    return {'certs': certs, 'censored': censored, 'N0': N0, 'L': L, 'horizon': horizon, 'D': D, 'P': P, 'N': N, 'all_ring': inf, 'full_shift': fs}

def main():
    maj = json.loads(MAJORITY.read_text()); iso = json.loads(ISOLATED.read_text()); com = json.loads(COMPLEMENT.read_text()); lin = json.loads(LINEAR.read_text())
    tables = {232: maj['h_star'], 4: iso['h_star']['4'], 32: com['h_star']['32'], 200: com['h_star']['200'], 22: com['h_star']['22'],
              102: lin['h_star']['102'], 90: lin['h_star']['90'], 150: lin['h_star']['150']}
    ref = {psi: {n: sorted(int(r) for r, v in tables[psi][str(n)].items() if num(v) <= 1) for n in REF_RINGS} for psi in OBS}
    PARITY_248 = ref[102][8]; assert len(PARITY_248) == 248
    EX = {psi: {n: exhaustive_depth_one(psi, n) for n in RINGS} for psi in OBS}
    G = {psi: analyse(psi) for psi in OBS}
    Gc = {psi: analyse(conj(psi)) for psi in OBS}
    Gm = {psi: analyse(mirror(psi)) for psi in OBS if mirror(psi) != psi}
    P = {}
    l1 = {str(psi): [[n, kn] for n in RINGS for kn in RINGS if kn > n and kn % n == 0 and not set(EX[psi][kn]) <= set(EX[psi][n])] for psi in OBS}
    P['L1_divisibility'] = {'violations': l1, 'pass': all(not v for v in l1.values())}
    l2 = {'criterion_equals_exhaustive': {str(psi): {str(n): G[psi]['D'][n] == EX[psi][n] for n in GRAPH_RINGS} for psi in OBS},
          'exhaustive_equals_recorded_depth_tables': {str(psi): {str(n): EX[psi][n] == ref[psi][n] for n in REF_RINGS} for psi in OBS}}
    l2['pass'] = all(v for d in l2['criterion_equals_exhaustive'].values() for v in d.values()) and all(v for d in l2['exhaustive_equals_recorded_depth_tables'].values() for v in d.values())
    P['L2_criterion_exact'] = l2
    l3 = {}
    for psi in OBS:
        g = G[psi]; c = g['certs']
        l3[str(psi)] = {'censored_rules': g['censored'], 'max_k': None if g['censored'] else max(c[r].k for r in range(256)),
                        'lcm_p': g['L'], 'least_eventual_period_P': g['P'], 'onset_ring_N': g['N'],
                        'k_p_by_rule': {str(r): ([c[r].k, c[r].p] if c[r].p is not None else 'censored') for r in range(256)},
                        'violating_walk_counts': {str(r): c[r].nwalks for r in range(256)},
                        'certified_depth_one_sets': None if g['censored'] else {str(n): g['D'][n] for n in range(4, g['N'] + g['P'])},
                        'depth_one_counts_to_horizon': {str(n): (len(g['D'][n]) if g['D'][n] is not None else None) for n in range(4, g['horizon'] + 1)}}
    P['L3_certificates'] = l3
    def censored(psi): return bool(G[psi]['censored'])
    l4a = {str(psi): ('censored' if censored(psi) else [n for n in range(10, G[psi]['horizon'] + 1) if G[psi]['D'][n] != G[psi]['D'][10]]) for psi in FOUR}
    l4a_detail = {str(psi): ('censored' if censored(psi) else {str(n): {'entering': sorted(set(G[psi]['D'][n]) - set(G[psi]['D'][10])), 'leaving': sorted(set(G[psi]['D'][10]) - set(G[psi]['D'][n]))}
                             for n in range(10, G[psi]['horizon'] + 1) if G[psi]['D'][n] != G[psi]['D'][10]}) for psi in FOUR}
    l4b = 'censored' if censored(22) else G[22]['P']
    l4c = 'censored' if censored(102) else [n for n in range(6, G[102]['horizon'] + 1) if G[102]['D'][n] != PARITY_248]
    l4 = {'a_four_constant_from_10_violations': l4a, 'a_detail': l4a_detail, 'b_period_under_22': l4b, 'c_parity_248_violations': l4c}
    l4['pass'] = all(v == [] for v in l4a.values()) and l4b == 3 and l4c == []; P['L4_stabilization'] = l4
    def rings(psi, cond, lo): return [n for n in range(lo, G[psi]['horizon'] + 1) if cond(n)]
    l5 = {'theorem_150_all_off_multiples_of_3': 'censored' if censored(150) else [n for n in rings(150, lambda n: n % 3 != 0, 4) if G[150]['D'][n] != list(range(256))],
          'theorem_90_odd_is_248': 'censored' if censored(90) else [n for n in rings(90, lambda n: n % 2 == 1, 7) if G[90]['D'][n] != PARITY_248],
          'reported_90_even_counts': {str(n): len(G[90]['D'][n]) for n in rings(90, lambda n: n % 2 == 0, 4) if G[90]['D'][n] is not None},
          'reported_150_multiples_of_3_counts': {str(n): len(G[150]['D'][n]) for n in rings(150, lambda n: n % 3 == 0, 6) if G[150]['D'][n] is not None},
          'reported_90_even_sets': {str(n): G[90]['D'][n] for n in rings(90, lambda n: n % 2 == 0, 4) if G[90]['D'][n] is not None},
          'reported_150_multiples_of_3_sets': {str(n): G[150]['D'][n] for n in rings(150, lambda n: n % 3 == 0, 6) if G[150]['D'][n] is not None}}
    l5['pass'] = l5['theorem_150_all_off_multiples_of_3'] == [] and l5['theorem_90_odd_is_248'] == []; P['L5_linear_observations'] = l5
    l6 = {'complement': {str(psi): {str(n): Gc[psi]['D'][n] == sorted(conj(r) for r in G[psi]['D'][n]) for n in GRAPH_RINGS} for psi in OBS},
          'reflection': {str(psi): {str(n): (Gm[psi]['D'][n] if psi in Gm else G[psi]['D'][n]) == sorted(mirror(r) for r in G[psi]['D'][n]) for n in GRAPH_RINGS} for psi in OBS}}
    l6['pass'] = all(v for k in l6 for d in l6[k].values() for v in d.values()); P['L6_symmetries'] = l6
    l7 = {str(psi): ('censored' if censored(psi) else {'all_ring_not_full_shift': [r for r in G[psi]['all_ring'] if r not in G[psi]['full_shift']],
                                                       'full_shift_not_all_ring': [r for r in G[psi]['full_shift'] if r not in G[psi]['all_ring']],
                                                       'witnesses': {str(r): G[psi]['certs'][r].fs_witness for r in G[psi]['all_ring'] if r not in G[psi]['full_shift']}}) for psi in OBS}
    l7['pass'] = all(v != 'censored' and not v['all_ring_not_full_shift'] and not v['full_shift_not_all_ring'] for v in (l7[str(p)] for p in OBS)); P['L7_all_ring_equals_full_shift'] = l7
    report = {'protocol': 'depth-one-certificate-20260911', 'schema': 2, 'observations': list(OBS), 'rings_exhaustive': list(RINGS),
              'parameters': {'power_cap': POWER_CAP, 'decided_rings_when_censored': [4, POWER_CAP + 3]},
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'block_majority_result': sha(MAJORITY), 'isolated_cell_result': sha(ISOLATED),
                                'complement_observation_result': sha(COMPLEMENT), 'linear_observations_result': sha(LINEAR)},
              'parity_248': PARITY_248,
              'exhaustive_depth_one': {str(psi): {str(n): EX[psi][n] for n in RINGS} for psi in OBS},
              'all_ring_depth_one': {str(psi): G[psi]['all_ring'] for psi in OBS},
              'full_shift_depth_one': {str(psi): G[psi]['full_shift'] for psi in OBS},
              'conjugate_summary': {str(conj(psi)): {'censored_rules': Gc[psi]['censored'], 'P': Gc[psi]['P'], 'N': Gc[psi]['N']} for psi in OBS},
              'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary']))
    print('certificates', {p: (l3[str(p)]['max_k'], l3[str(p)]['lcm_p'], l3[str(p)]['least_eventual_period_P'], l3[str(p)]['onset_ring_N'], len(l3[str(p)]['censored_rules'])) for p in OBS})
    print('all-ring sizes', {p: (len(G[p]['all_ring']) if G[p]['all_ring'] is not None else None) for p in OBS})
    print('L4', {'a': l4a, 'b': l4b, 'c': l4c}); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__': main()
