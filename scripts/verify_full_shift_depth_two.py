#!/usr/bin/env python3
"""Full-shift depth at most two by sparse reachability, and the depth gap
(protocol frozen 2026-09-11, re-frozen after Codex's gate-1 round 1, gate-1
approval by Codex at 4801d91 before this implementation; see the protocol's
Section 5).

For observations psi in {232, 4, 32, 200, 22, 102, 90, 150} and every rule r:
exhaustive depth-two sets D2_psi(n) = {r : h_* <= 2} on rings 3..14; the
depth-two pair graph G2_{psi,r} (4096 vertices = six-cell pair blocks, an edge
per seven-cell pair block whose centre agrees on psi, psi F and psi F^2); the
violating three-edge walks read off the 262144 nine-cell pair blocks (psi F^3
disagrees at the centre); the full-shift criterion by sparse reachability
(no violating walk with v0 reachable from a cycle and v3 reaching a cycle);
no matrix power and no ring certificate at depth two.

M1  FS2 subset of D2(n), 3 <= n <= 14 (theorem control).
M2  FS1 subset of FS2; D1(n) subset of D2(n); D2(kn) subset of D2(n) (theorem).
M3  all fourteenth-unit L7 gap pairs lie in FS2 (bet).
M4  FS2_102 == all 256 (theorem control by the deduction in Section 1).
M5  ring-14 gap G14 = D2(14) \\ FS2 and all-tested-ring gap G[3,14] =
    (intersection of D2(n), 3 <= n <= 14) \\ FS2; bet: G[3,14] nonempty for
    exactly {232, 200, 22}; G14 reported without a bet.
M6  the fourteenth unit's L7 witnesses realized as eventually periodic pairs,
    finite-window replay with trimmed margin 3 (implementation control; the
    graph path is the certificate).
M7  complement and reflection covariance of FS2 and D2(n).
"""
from __future__ import annotations
import hashlib, json, pathlib
from collections import deque
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
DEPTH_ONE = ROOT / 'results/depth_one_certificate_20260911.json'
OUT = ROOT / 'results/full_shift_depth_two_20260911.json'
OBS = (232, 4, 32, 200, 22, 102, 90, 150); RINGS = tuple(range(3, 15)); GAP_BET = (232, 200, 22)
MARGIN = 3               # frozen trimmed margin of the finite replay (radius of psi F^2)
PERIODS = 3              # frozen: the finite window covers three periods on each side
SCC_LIST_CAP = 64        # strong components longer than this are recorded by size only

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64); return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)
def lut(r): return np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
def step(S, r):
    t = lut(r); return t[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
def ints(S): return (S.astype(np.int64) << (S.shape[1] - 1 - np.arange(S.shape[1]))).sum(axis=1)
def conj(r): return sum((((r >> (7 - i)) & 1) ^ 1) << i for i in range(8))
def mirror(r): return sum(((r >> (((i & 4) >> 2) | (i & 2) | ((i & 1) << 2))) & 1) << i for i in range(8))
def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    raise TypeError(type(o))

# ---------------------------------------------------------------- exhaustive depth two
def exhaustive_depth_two(psi, n):
    """Rules whose three observed steps determine the fourth on every state of the ring."""
    S = all_states(n); y0 = ints(step(S, psi)); out = []
    for r in range(256):
        F1 = step(S, r); F2 = step(F1, r); F3 = step(F2, r)
        y1, y2, y3 = ints(step(F1, psi)), ints(step(F2, psi)), ints(step(F3, psi))
        key = (y0 * (1 << n) + y1) * (1 << n) + y2; order = np.argsort(key, kind='stable'); k, z = key[order], y3[order]
        if not np.any((k[1:] == k[:-1]) & (z[1:] != z[:-1])): out.append(r)
    return out

# ---------------------------------------------------------------- blocks and local maps
def pair_blocks(L):
    """All 4^L pair blocks as (x, y) arrays of shape (4^L, L); code MSB first, x bit above y bit per cell."""
    codes = np.arange(4 ** L, dtype=np.int64)
    cells = (codes[:, None] >> (2 * (L - 1 - np.arange(L)))) & 3
    return ((cells >> 1) & 1).astype(np.uint8), (cells & 1).astype(np.uint8)
def local(rule, X):
    """Apply an elementary rule along the last axis without wrap: output index j is cell j+1."""
    t = lut(rule); return t[4 * X[:, :-2] + 2 * X[:, 1:-1] + X[:, 2:]]
def codes(X, Y, start, width):
    """Codes of the width-cell pair block at columns start..start+width-1."""
    c = np.zeros(X.shape[0], dtype=np.int64)
    for j in range(width): c = c * 4 + (2 * X[:, start + j].astype(np.int64) + Y[:, start + j])
    return c
def decode(code, width):
    cells = [(code >> (2 * (width - 1 - j))) & 3 for j in range(width)]
    return [c >> 1 for c in cells], [c & 1 for c in cells]
X5, Y5 = pair_blocks(5); X7, Y7 = pair_blocks(7); X9, Y9 = pair_blocks(9)

def agree(psi, r, X, Y, depth):
    """Agreement of psi F^depth between x and y, indexed by cell (output index j is cell j+1+depth)."""
    fx, fy = X, Y
    for _ in range(depth): fx, fy = local(r, fx), local(r, fy)
    return local(psi, fx) == local(psi, fy)

# ---------------------------------------------------------------- the depth-two pair graph
def depth_two_graph(psi, r):
    """Adjacency lists on 4096 six-cell-pair vertices and the sorted violating (v0, v3) list."""
    a0, a1, a2 = agree(psi, r, X7, Y7, 0), agree(psi, r, X7, Y7, 1), agree(psi, r, X7, Y7, 2)
    ok = a0[:, 2] & a1[:, 1] & a2[:, 0]                                   # centre cell 3 of the seven-cell block
    src, dst = codes(X7, Y7, 0, 6)[ok].tolist(), codes(X7, Y7, 1, 6)[ok].tolist()
    adj = [[] for _ in range(4096)]
    for s, d in zip(src, dst): adj[s].append(d)
    b0, b1, b2, b3 = agree(psi, r, X9, Y9, 0), agree(psi, r, X9, Y9, 1), agree(psi, r, X9, Y9, 2), agree(psi, r, X9, Y9, 3)
    edges = b0[:, 2] & b0[:, 3] & b0[:, 4] & b1[:, 1] & b1[:, 2] & b1[:, 3] & b2[:, 0] & b2[:, 1] & b2[:, 2]
    viol = edges & ~b3[:, 0]                                              # psi F^3 disagrees at cell 4
    walks = sorted(set(zip(codes(X9, Y9, 0, 6)[viol].tolist(), codes(X9, Y9, 3, 6)[viol].tolist())))
    return adj, walks

def strong_components(adj):
    """Iterative Tarjan; returns component id per vertex."""
    n = len(adj); index = [-1] * n; low = [0] * n; onstack = [False] * n; stack = []; comp = [-1] * n; counter = 0; c = 0
    for s in range(n):
        if index[s] != -1: continue
        work = [(s, 0)]
        while work:
            v, i = work[-1]
            if i == 0 and index[v] == -1:
                index[v] = low[v] = counter; counter += 1; stack.append(v); onstack[v] = True
            if i < len(adj[v]):
                work[-1] = (v, i + 1); w = adj[v][i]
                if index[w] == -1: work.append((w, 0))
                elif onstack[w]: low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work: u = work[-1][0]; low[u] = min(low[u], low[v])
                if low[v] == index[v]:
                    while True:
                        w = stack.pop(); onstack[w] = False; comp[w] = c
                        if w == v: break
                    c += 1
    return comp

def reach(adj, seeds):
    seen = [False] * len(adj); dq = deque()
    for s in seeds: seen[s] = True; dq.append(s)
    while dq:
        v = dq.popleft()
        for w in adj[v]:
            if not seen[w]: seen[w] = True; dq.append(w)
    return seen

def cycle_facts(adj):
    """on-cycle flags, reachable-from-a-cycle flags, reaches-a-cycle flags, component ids."""
    n = len(adj); comp = strong_components(adj); size = {}
    for c in comp: size[c] = size.get(c, 0) + 1
    on = [size[comp[v]] > 1 or v in adj[v] for v in range(n)]
    radj = [[] for _ in range(n)]
    for v in range(n):
        for w in adj[v]: radj[w].append(v)
    seeds = [v for v in range(n) if on[v]]
    return on, reach(adj, seeds), reach(radj, seeds), comp

def full_shift(adj, walks):
    """True iff no violating walk is bi-infinitely extendable; else (False, witness, count)."""
    on, frm, to, comp = cycle_facts(adj)
    ext = [(v0, v3) for v0, v3 in walks if frm[v0] and to[v3]]
    if not ext: return True, None, 0
    v0, v3 = ext[0]
    def scc(v):
        members = [u for u in range(len(adj)) if comp[u] == comp[v]]
        return {'size': len(members), 'members': members if len(members) <= SCC_LIST_CAP else None}
    witness = {'v0': v0, 'v3': v3, 'v0_on_cycle': on[v0], 'v0_reachable_from_cycle': frm[v0], 'v3_on_cycle': on[v3],
               'v3_reaches_cycle': to[v3], 'v0_strong_component': scc(v0), 'v3_strong_component': scc(v3),
               'violating_walks_total': len(walks), 'extendable_violating_walks_total': len(ext)}
    return False, witness, len(ext)

def analyse(psi):
    fs, counts, ext_counts, witnesses = [], {}, {}, {}
    for r in range(256):
        adj, walks = depth_two_graph(psi, r); ok, w, k = full_shift(adj, walks)
        counts[r] = len(walks); ext_counts[r] = k
        if ok: fs.append(r)
        else: witnesses[r] = w
    return {'full_shift': fs, 'violating_walk_counts': counts, 'extendable_counts': ext_counts, 'witnesses': witnesses}

# ---------------------------------------------------------------- explicit witness pairs (M6)
def depth_one_graph(psi, r):
    """The fourteenth unit's 256-vertex graph as adjacency lists, plus the violating seven-cell blocks."""
    ok = (local(psi, X5)[:, 1] == local(psi, Y5)[:, 1]) & (agree(psi, r, X5, Y5, 1)[:, 0])
    adj = [[] for _ in range(256)]
    for s, d in zip(codes(X5, Y5, 0, 4)[ok].tolist(), codes(X5, Y5, 1, 4)[ok].tolist()): adj[s].append(d)
    e, e1 = agree(psi, r, X7, Y7, 0), agree(psi, r, X7, Y7, 1)
    viol = e[:, 1] & e[:, 2] & e[:, 3] & e1[:, 0] & e1[:, 1] & e1[:, 2] & ~agree(psi, r, X7, Y7, 2)[:, 0]
    blocks = np.nonzero(viol)[0]
    return adj, blocks, codes(X7, Y7, 0, 4)[blocks], codes(X7, Y7, 3, 4)[blocks]

def bfs_path(adj, start, goal):
    """Shortest path start -> ... -> goal (goal is a predicate); None if unreachable."""
    parent = {start: None}; dq = deque([start])
    while dq:
        v = dq.popleft()
        for w in adj[v]:
            if w not in parent:
                parent[w] = v; dq.append(w)
                if goal(w):
                    path = [w]
                    while parent[path[-1]] is not None: path.append(parent[path[-1]])
                    return path[::-1]
    return None

def shortest_cycle(adj, u):
    """A shortest cycle u -> ... -> u (at least one edge)."""
    if u in adj[u]: return [u, u]
    best = None
    for w in adj[u]:
        p = bfs_path(adj, w, lambda v: v == u)
        if p is not None and (best is None or len(p) < len(best) - 1): best = [u] + p
    return best

def witness_pair(psi, r, v0, v3):
    """Eventually periodic pair realizing the recorded L7 witness (v0, v3), with the finite-window replay."""
    adj, blocks, b0, b3 = depth_one_graph(psi, r)
    sel = np.nonzero((b0 == v0) & (b3 == v3))[0]
    block = int(blocks[sel[0]])                                           # lexicographically first violating block
    bx, by = decode(block, 7)
    on, frm, to, comp = cycle_facts(adj)
    radj = [[] for _ in range(256)]
    for v in range(256):
        for w in adj[v]: radj[w].append(v)
    # left: a cycle vertex u and a path u -> ... -> v0 (found backward from v0)
    left = [v0] if on[v0] else bfs_path(radj, v0, lambda v: on[v])[::-1]
    u = left[0]; cyc_l = shortest_cycle(adj, u)
    right = [v3] if on[v3] else bfs_path(adj, v3, lambda v: on[v])
    w = right[-1]; cyc_r = shortest_cycle(adj, w)
    v1 = codes(np.array([bx]), np.array([by]), 1, 4)[0]; v2 = codes(np.array([bx]), np.array([by]), 2, 4)[0]
    walk = cyc_l[:-1] * PERIODS + left + [int(v1), int(v2)] + right + cyc_r[1:] * PERIODS
    p0 = len(cyc_l[:-1]) * PERIODS + len(left) - 1                         # position of v0 in the walk
    x, y = list(decode(walk[0], 4)[0]), list(decode(walk[0], 4)[1])
    for v in walk[1:]:
        cx, cy = decode(v, 4); x.append(cx[-1]); y.append(cy[-1])
    X, Y = np.array([x], dtype=np.uint8), np.array([y], dtype=np.uint8); L = len(x); centre = p0 + 3
    a0 = agree(psi, r, X, Y, 0)[0]; a1 = agree(psi, r, X, Y, 1)[0]; a2 = agree(psi, r, X, Y, 2)[0]
    lo, hi = MARGIN, L - 1 - MARGIN                                       # trimmed interior cells lo..hi
    pass0 = bool(a0[lo - 1:hi].all()); pass1 = bool(a1[lo - 2:hi - 1].all()); disagree = not bool(a2[centre - 3])
    assert x[centre - 3:centre + 4] == bx and y[centre - 3:centre + 4] == by
    def word(vs): return {'x': ''.join(str(decode(v, 4)[0][-1]) for v in vs), 'y': ''.join(str(decode(v, 4)[1][-1]) for v in vs)}
    return {'psi': psi, 'rule': r, 'v0': v0, 'v3': v3, 'violating_block': {'x': ''.join(map(str, bx)), 'y': ''.join(map(str, by))},
            'left_cycle_word': word(cyc_l[1:]), 'left_path_word': word(left[1:]), 'right_path_word': word(right[1:]), 'right_cycle_word': word(cyc_r[1:]),
            'left_period': len(cyc_l) - 1, 'right_period': len(cyc_r) - 1, 'window_length': L, 'centre': centre, 'trimmed_margin': MARGIN,
            'window': {'x': ''.join(map(str, x)), 'y': ''.join(map(str, y))},
            'psi_agrees_on_interior': pass0, 'psi_F_agrees_on_interior': pass1, 'psi_F2_disagrees_at_centre': disagree,
            'pass': pass0 and pass1 and disagree}

def main():
    d1 = json.loads(DEPTH_ONE.read_text())
    FS1 = {psi: d1['full_shift_depth_one'][str(psi)] for psi in OBS}
    D1 = {psi: {n: d1['exhaustive_depth_one'][str(psi)][str(n)] for n in RINGS} for psi in OBS}
    L7 = d1['predictions']['L7_all_ring_equals_full_shift']
    gap14 = [(psi, int(r)) for psi in OBS for r in L7[str(psi)]['all_ring_not_full_shift']]
    all_obs = sorted(set(OBS) | {conj(p) for p in OBS} | {mirror(p) for p in OBS})
    EX = {psi: {n: exhaustive_depth_two(psi, n) for n in RINGS} for psi in all_obs}
    G = {psi: analyse(psi) for psi in all_obs}
    FS2 = {psi: G[psi]['full_shift'] for psi in all_obs}
    P = {}
    m1 = {str(psi): [n for n in RINGS if not set(FS2[psi]) <= set(EX[psi][n])] for psi in OBS}
    P['M1_full_shift_implies_rings'] = {'violations': m1, 'pass': all(not v for v in m1.values())}
    m2 = {'FS1_subset_FS2': {str(psi): sorted(set(FS1[psi]) - set(FS2[psi])) for psi in OBS},
          'D1_subset_D2': {str(psi): {str(n): sorted(set(D1[psi][n]) - set(EX[psi][n])) for n in RINGS} for psi in OBS},
          'divisibility': {str(psi): [[n, kn] for n in RINGS for kn in RINGS if kn > n and kn % n == 0 and not set(EX[psi][kn]) <= set(EX[psi][n])] for psi in OBS}}
    m2['pass'] = all(not v for v in m2['FS1_subset_FS2'].values()) and all(not v for d in m2['D1_subset_D2'].values() for v in d.values()) and all(not v for v in m2['divisibility'].values())
    P['M2_monotonicity_divisibility'] = m2
    m3 = {'pairs_checked': len(gap14), 'not_in_FS2': [[psi, r] for psi, r in gap14 if r not in FS2[psi]]}
    m3['witnesses'] = {f'{psi}:{r}': G[psi]['witnesses'][r] for psi, r in gap14 if r not in FS2[psi]}
    m3['pass'] = not m3['not_in_FS2']; P['M3_gap_rules_full_shift_depth_two'] = m3
    m4 = {'FS2_102_size': len(FS2[102]), 'missing': sorted(set(range(256)) - set(FS2[102]))}; m4['pass'] = not m4['missing']; P['M4_parity_all_256'] = m4
    inter = {psi: sorted(set(range(256)).intersection(*[set(EX[psi][n]) for n in RINGS])) for psi in OBS}
    gap_14 = {psi: [r for r in EX[psi][14] if r not in FS2[psi]] for psi in OBS}
    gap_all = {psi: [r for r in inter[psi] if r not in FS2[psi]] for psi in OBS}
    m5 = {'ring_14_gap': {str(psi): gap_14[psi] for psi in OBS}, 'all_tested_ring_gap': {str(psi): gap_all[psi] for psi in OBS},
          'all_tested_ring_depth_two': {str(psi): inter[psi] for psi in OBS},
          'bet_nonempty_exactly': list(GAP_BET), 'nonempty_observed': [psi for psi in OBS if gap_all[psi]],
          'witnesses_all_tested_ring_gap': {str(psi): {str(r): G[psi]['witnesses'][r] for r in gap_all[psi]} for psi in OBS},
          'witnesses_ring_14_gap_only': {str(psi): {str(r): G[psi]['witnesses'][r] for r in gap_14[psi] if r not in gap_all[psi]} for psi in OBS}}
    m5['pass'] = m5['nonempty_observed'] == sorted(GAP_BET, key=OBS.index); P['M5_depth_two_gap'] = m5
    pairs = [witness_pair(psi, r, L7[str(psi)]['witnesses'][str(r)]['v0'], L7[str(psi)]['witnesses'][str(r)]['v3']) for psi, r in gap14]
    m6 = {'pairs': pairs, 'failing': [[p['psi'], p['rule']] for p in pairs if not p['pass']]}; m6['pass'] = not m6['failing']; P['M6_witness_pairs'] = m6
    m7 = {'complement_FS2': {str(psi): FS2[conj(psi)] == sorted(conj(r) for r in FS2[psi]) for psi in OBS},
          'complement_D2': {str(psi): {str(n): EX[conj(psi)][n] == sorted(conj(r) for r in EX[psi][n]) for n in RINGS} for psi in OBS},
          'reflection_FS2': {str(psi): FS2[mirror(psi)] == sorted(mirror(r) for r in FS2[psi]) for psi in OBS},
          'reflection_D2': {str(psi): {str(n): EX[mirror(psi)][n] == sorted(mirror(r) for r in EX[psi][n]) for n in RINGS} for psi in OBS}}
    m7['pass'] = all(m7['complement_FS2'].values()) and all(m7['reflection_FS2'].values()) and all(v for d in m7['complement_D2'].values() for v in d.values()) and all(v for d in m7['reflection_D2'].values() for v in d.values())
    P['M7_symmetries'] = m7
    report = {'protocol': 'full-shift-depth-two-20260911', 'schema': 1, 'observations': list(OBS), 'rings_exhaustive': list(RINGS),
              'parameters': {'trimmed_margin': MARGIN, 'periods_per_side': PERIODS, 'scc_list_cap': SCC_LIST_CAP, 'vertices': 4096, 'edge_blocks': 4 ** 7, 'violation_blocks': 4 ** 9},
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'depth_one_certificate_result': sha(DEPTH_ONE)},
              'exhaustive_depth_two': {str(psi): {str(n): EX[psi][n] for n in RINGS} for psi in OBS},
              'full_shift_depth_two': {str(psi): FS2[psi] for psi in OBS},
              'full_shift_depth_one': {str(psi): FS1[psi] for psi in OBS},
              'violating_walk_counts': {str(psi): {str(r): G[psi]['violating_walk_counts'][r] for r in range(256)} for psi in OBS},
              'extendable_violation_counts': {str(psi): {str(r): G[psi]['extendable_counts'][r] for r in range(256)} for psi in OBS},
              'conjugate_full_shift_depth_two_sizes': {str(q): len(FS2[q]) for q in all_obs if q not in OBS},
              'predictions': P, 'summary': {k: v['pass'] for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary']))
    print('FS2 sizes', {p: len(FS2[p]) for p in OBS}); print('D2(14) sizes', {p: len(EX[p][14]) for p in OBS})
    print('gap14', {p: gap_14[p] for p in OBS}); print('gap[3,14]', {p: gap_all[p] for p in OBS}); print('M3 missing', m3['not_in_FS2'])
    print('written', OUT.relative_to(ROOT))

if __name__ == '__main__': main()
