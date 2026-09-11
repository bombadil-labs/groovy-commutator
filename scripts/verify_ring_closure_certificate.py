#!/usr/bin/env python3
"""Ring-closure certificate (protocol frozen 2026-09-11, gate-1 sign-off by Codex at
05276a5 after two correction rounds, before this implementation; see the protocol's
Section 6).

For observations psi in {232, 4, 32, 200, 22, 102, 90, 150}: exhaustive closed sets
C_psi(n) on rings 3..14, the 16-vertex pair graph G_psi (vertices two-cell pair
blocks, edges psi-agreeing three-cell pair blocks), the violating three-edge walks
V_psi(r) read off the 1024 five-cell pair blocks, the ring criterion
  r not in C_psi(n)  iff  some (v0..v3) in V_psi(r) has (A^(n-3))[v3, v0] = 1   (n >= 4),
the certificate (k, p) with A^(k+p) = A^k, the certified list C_psi(4..k+p+2), the
all-ring closed set (intersection over n >= 4) and the full-shift closed set (no
bi-infinitely extendable violating walk).

K1  divisibility C(kn) subset of C(n) on exhaustive rings (theorem control).
K2  ring criterion == exhaustive on rings 4..14; reference consistency with the
    twelfth unit (232, 4, 32, 200, 22) and seventh unit (102, 90, 150) at 6..12.
K3  certificate (k, p) and the certified list, reported.
K4  232, 4, 32, 200, 22, 102: C(n) == all-ring set for every n >= 7 (bet).
K5  linear: (a) affine rules closed everywhere, (b) 150 all 256 when 3 does not
    divide n, (c) 90 odd n >= 7 == the 32 (theorem parts); (d) 90 even n >= 6 and
    (e) 150 with 3 | n, n >= 6 exactly the 16 affine rules (bets).
K6  complement covariance C_conj(psi)(n) == conj(C_psi(n)); reflection covariance.
K7  all-ring closed set == full-shift closed set (bet).
"""
from __future__ import annotations
import hashlib, json, pathlib
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
FACTOR = ROOT / 'results/factor_radius_20260911.json'
LINEAR = ROOT / 'results/linear_observations_20260911.json'
OUT = ROOT / 'results/ring_closure_certificate_20260911.json'
OBS = (232, 4, 32, 200, 22, 102, 90, 150); SIX = (232, 4, 32, 200, 22, 102); LINEAR_OBS = (102, 90, 150)
RINGS = tuple(range(3, 15)); GRAPH_RINGS = tuple(range(4, 15)); REF_RINGS = tuple(range(6, 13))
AFFINE = [0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195, 204, 240, 255]
MAX_POWERS = 100000

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64); return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)
def lut(r): return np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
def step(S, r):
    t = lut(r); return t[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
def ints(S): return (S.astype(np.int64) << (S.shape[1] - 1 - np.arange(S.shape[1]))).sum(axis=1)
def conj(r): return sum((((r >> (7 - i)) & 1) ^ 1) << i for i in range(8))
def mirror(r): return sum(((r >> (((i & 4) >> 2) | (i & 2) | ((i & 1) << 2))) & 1) << i for i in range(8))
def relabel(keys): _, inv = np.unique(keys, return_inverse=True); return inv
def local(r, a, b, c): return (r >> (4 * a + 2 * b + c)) & 1
def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    raise TypeError(type(o))

# ---------------------------------------------------------------- exhaustive closure
def exhaustive_closed(psi, n):
    S = all_states(n); fiber = relabel(ints(step(S, psi))); order = np.argsort(fiber, kind='stable'); f = fiber[order]
    same = f[1:] == f[:-1]; closed = []
    for r in range(256):
        z = ints(step(step(S, r), psi))[order]
        if not np.any(same & (z[1:] != z[:-1])): closed.append(r)
    return closed

# ---------------------------------------------------------------- pair graph and walks
def vertex(xa, ya, xb, yb): return 8 * xa + 4 * ya + 2 * xb + yb
def pair_graph(psi):
    A = np.zeros((16, 16), dtype=np.uint8)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                ax, ay, bx, by, cx, cy = a >> 1, a & 1, b >> 1, b & 1, c >> 1, c & 1
                if local(psi, ax, bx, cx) == local(psi, ay, by, cy): A[vertex(ax, ay, bx, by), vertex(bx, by, cx, cy)] = 1
    return A

def violating_walks(psi, r):
    """(v0, v3) for every psi-admissible five-cell pair block whose observed successor disagrees at the centre."""
    out = set()
    for code in range(1024):
        x = [(code >> (9 - 2 * i)) & 1 for i in range(5)]; y = [(code >> (8 - 2 * i)) & 1 for i in range(5)]
        if any(local(psi, x[i - 1], x[i], x[i + 1]) != local(psi, y[i - 1], y[i], y[i + 1]) for i in (1, 2, 3)): continue
        fx = [local(r, x[i - 1], x[i], x[i + 1]) for i in (1, 2, 3)]; fy = [local(r, y[i - 1], y[i], y[i + 1]) for i in (1, 2, 3)]
        if local(psi, *fx) != local(psi, *fy): out.add((vertex(x[0], y[0], x[1], y[1]), vertex(x[3], y[3], x[4], y[4])))
    return sorted(out)

def bool_powers(A):
    """A^0, A^1, ... until the first repeat; returns (powers, k, p) with powers[k+p] == powers[k]."""
    powers = [np.eye(16, dtype=np.uint8)]; seen = {powers[0].tobytes(): 0}
    while True:
        M = ((powers[-1].astype(np.int32) @ A.astype(np.int32)) > 0).astype(np.uint8); key = M.tobytes()
        if key in seen: k = seen[key]; return powers, k, len(powers) - k
        seen[key] = len(powers); powers.append(M)
        if len(powers) > MAX_POWERS: raise RuntimeError('no repeat found')

def graph_closed(psi, n, powers, k, p, walks):
    """Ring criterion at ring n >= 4 using A^(n-3), reduced into the periodic range when needed."""
    e = n - 3
    if e >= len(powers): e = k + (e - k) % p
    M = powers[e]
    return [r for r in range(256) if not any(M[v3, v0] for v0, v3 in walks[r])]

def full_shift_closed(A, walks):
    T = np.zeros((16, 16), dtype=np.uint8); M = np.eye(16, dtype=np.uint8)
    for _ in range(16):
        M = ((M.astype(np.int32) @ A.astype(np.int32)) > 0).astype(np.uint8); T |= M
    on_cycle = np.array([T[v, v] for v in range(16)], dtype=bool)
    from_cycle = on_cycle | np.array([any(on_cycle[u] and T[u, v] for u in range(16)) for v in range(16)])
    to_cycle = on_cycle | np.array([any(on_cycle[u] and T[v, u] for u in range(16)) for v in range(16)])
    return [r for r in range(256) if not any(from_cycle[v0] and to_cycle[v3] for v0, v3 in walks[r])], {
        'on_cycle': [int(v) for v in range(16) if on_cycle[v]], 'reachable_from_cycle': [int(v) for v in range(16) if from_cycle[v]],
        'reaches_cycle': [int(v) for v in range(16) if to_cycle[v]]}

def analyse(psi):
    A = pair_graph(psi); walks = {r: violating_walks(psi, r) for r in range(256)}
    powers, k, p = bool_powers(A)
    last = k + p + 2; horizon = max(last, 7 + p, 14)
    certified = {n: graph_closed(psi, n, powers, k, p, walks) for n in range(4, horizon + 1)}
    all_ring = sorted(set(range(256)).intersection(*[set(certified[n]) for n in range(4, last + 1)]))
    fs, comps = full_shift_closed(A, walks)
    return {'A': A, 'edges': [[int(u), int(v)] for u in range(16) for v in range(16) if A[u, v]], 'walks': walks, 'k': k, 'p': p,
            'last': last, 'horizon': horizon, 'certified': certified, 'all_ring': all_ring, 'full_shift': fs, 'components': comps}

def main():
    factor = json.loads(FACTOR.read_text()); linear = json.loads(LINEAR.read_text())
    ref = {psi: {n: sorted(int(r) for r in factor['closed_by_ring'][str(psi)][str(n)]) for n in REF_RINGS} for psi in (232, 4, 32, 200, 22)}
    ref.update({psi: {n: sorted(int(r) for r in linear['closed_sets'][str(psi)][str(n)]) for n in REF_RINGS} for psi in LINEAR_OBS})
    THIRTY_TWO = sorted(int(r) for r in linear['closed_sets']['102']['8'])
    EX = {psi: {n: exhaustive_closed(psi, n) for n in RINGS} for psi in OBS}
    G = {psi: analyse(psi) for psi in OBS}
    Gc = {psi: analyse(conj(psi)) for psi in OBS}
    Gm = {psi: analyse(mirror(psi)) for psi in OBS if mirror(psi) != psi}
    P = {}
    k1 = {str(psi): [[n, kn] for n in RINGS for kn in RINGS if kn > n and kn % n == 0 and not set(EX[psi][kn]) <= set(EX[psi][n])] for psi in OBS}
    P['K1_divisibility'] = {'violations': k1, 'pass': all(not v for v in k1.values())}
    k2 = {'criterion_equals_exhaustive': {str(psi): {str(n): G[psi]['certified'][n] == EX[psi][n] for n in GRAPH_RINGS} for psi in OBS},
          'exhaustive_equals_earlier_units': {str(psi): {str(n): EX[psi][n] == ref[psi][n] for n in REF_RINGS} for psi in OBS}}
    k2['pass'] = all(v for d in k2['criterion_equals_exhaustive'].values() for v in d.values()) and all(v for d in k2['exhaustive_equals_earlier_units'].values() for v in d.values())
    P['K2_criterion_exact'] = k2
    P['K3_certificate'] = {str(psi): {'k': G[psi]['k'], 'p': G[psi]['p'], 'certified_rings': f"4..{G[psi]['last']}", 'eventual_period_of_closed_sets': None} for psi in OBS}
    for psi in OBS:
        c = G[psi]['certified']; last = G[psi]['last']; k, p = G[psi]['k'], G[psi]['p']
        per = next(q for q in range(1, p + 1) if p % q == 0 and all(c[n] == c[n + q] for n in range(k + 3, last + 1 - q)))
        P['K3_certificate'][str(psi)]['eventual_period_of_closed_sets'] = per
    def first_extra(psi):
        c = G[psi]['certified']; inf = set(G[psi]['all_ring']); out = {}
        for n in range(7, G[psi]['horizon'] + 1):
            for r in c[n]:
                if r not in inf and r not in out: out[r] = n
        return out
    k4 = {str(psi): first_extra(psi) for psi in SIX}
    P['K4_six_constant_from_7'] = {'extra_rule_smallest_ring': k4, 'rule_223_under_22': {str(n): 223 in G[22]['certified'][n] for n in range(4, G[22]['horizon'] + 1)},
                                   'pass': all(not v for v in k4.values())}
    def rings(psi, cond, lo): return [n for n in range(lo, G[psi]['horizon'] + 1) if cond(n)]
    k5 = {'a_affine_closed': {str(psi): [n for n in range(4, G[psi]['horizon'] + 1) if not set(AFFINE) <= set(G[psi]['certified'][n])] for psi in LINEAR_OBS},
          'b_150_all_when_3_not_dividing': [n for n in rings(150, lambda n: n % 3 != 0, 4) if G[150]['certified'][n] != list(range(256))],
          'c_90_odd_is_32': [n for n in rings(90, lambda n: n % 2 == 1, 7) if G[90]['certified'][n] != THIRTY_TWO],
          'd_90_even_is_affine': [n for n in rings(90, lambda n: n % 2 == 0, 6) if G[90]['certified'][n] != AFFINE],
          'e_150_multiple_of_3_is_affine': [n for n in rings(150, lambda n: n % 3 == 0, 6) if G[150]['certified'][n] != AFFINE],
          'reported': {'90_ring_4': EX[90][4], '90_ring_5': EX[90][5], '150_ring_3': EX[150][3]}}
    k5['theorem_parts_pass'] = all(not v for v in k5['a_affine_closed'].values()) and not k5['b_150_all_when_3_not_dividing'] and not k5['c_90_odd_is_32']
    k5['bet_parts_pass'] = not k5['d_90_even_is_affine'] and not k5['e_150_multiple_of_3_is_affine']
    k5['pass'] = k5['theorem_parts_pass'] and k5['bet_parts_pass']; P['K5_linear_observations'] = k5
    k6 = {'complement': {str(psi): {str(n): Gc[psi]['certified'][n] == sorted(conj(r) for r in G[psi]['certified'][n]) for n in GRAPH_RINGS} for psi in OBS},
          'reflection': {str(psi): {str(n): (Gm[psi]['certified'][n] if psi in Gm else G[psi]['certified'][n]) == sorted(mirror(r) for r in G[psi]['certified'][n]) for n in GRAPH_RINGS} for psi in OBS}}
    k6['pass'] = all(v for k in k6 for d in k6[k].values() for v in d.values()); P['K6_symmetries'] = k6
    k7 = {str(psi): {'all_ring_not_full_shift': [r for r in G[psi]['all_ring'] if r not in G[psi]['full_shift']],
                     'full_shift_not_all_ring': [r for r in G[psi]['full_shift'] if r not in G[psi]['all_ring']]} for psi in OBS}
    k7['pass'] = all(not d['all_ring_not_full_shift'] and not d['full_shift_not_all_ring'] for d in (k7[str(p)] for p in OBS)); P['K7_all_ring_equals_full_shift'] = k7
    report = {'protocol': 'ring-closure-certificate-20260911', 'schema': 1, 'observations': list(OBS), 'rings_exhaustive': list(RINGS),
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'factor_radius_result': sha(FACTOR), 'linear_observations_result': sha(LINEAR)},
              'exhaustive_closed': {str(psi): {str(n): EX[psi][n] for n in RINGS} for psi in OBS},
              'pair_graph_edges': {str(psi): G[psi]['edges'] for psi in OBS},
              'violating_walk_counts': {str(psi): {str(r): len(G[psi]['walks'][r]) for r in range(256)} for psi in OBS},
              'certificate': {str(psi): {'k': G[psi]['k'], 'p': G[psi]['p'], 'certified_closed': {str(n): G[psi]['certified'][n] for n in range(4, G[psi]['last'] + 1)},
                                         'closed_counts_to_horizon': {str(n): len(G[psi]['certified'][n]) for n in range(4, G[psi]['horizon'] + 1)}} for psi in OBS},
              'all_ring_closed': {str(psi): G[psi]['all_ring'] for psi in OBS},
              'full_shift_closed': {str(psi): G[psi]['full_shift'] for psi in OBS},
              'graph_components': {str(psi): G[psi]['components'] for psi in OBS},
              'conjugate_certificates': {str(conj(psi)): {'k': Gc[psi]['k'], 'p': Gc[psi]['p']} for psi in OBS},
              'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary'])); print('certificate', {p: (G[p]['k'], G[p]['p'], P['K3_certificate'][str(p)]['eventual_period_of_closed_sets']) for p in OBS})
    print('all-ring sizes', {p: len(G[p]['all_ring']) for p in OBS}); print('K4 extras', k4); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__': main()
