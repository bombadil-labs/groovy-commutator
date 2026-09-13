#!/usr/bin/env python3
"""Full-shift depth three under the linear observations 90 and 150 (protocol
frozen 2026-09-12, gate-1 approval by an independent reviewer, OpenAI GPT-6
Astra Pro, at protocol-only head 06265e7 before this implementation; see the
protocol's Section 5).

Observations psi in {90, 150} and 90's complement conjugate 165 (150 is
self-dual); rules r in 0..255. The machinery is the sixteenth unit's
(scripts/verify_full_shift_depth_three.py), reused verbatim at the same depth
h = 3: the pair graph G^h_{psi,r} has the 4^(2h+2) (2h+2)-cell pair blocks as
vertices, an edge per (2h+3)-cell pair block whose centre agrees on psi F^k for
k = 0..h, and a violating three-edge walk per (2h+5)-cell pair block whose
psi F^(h+1) disagrees at the centre. r is in FS^h_psi iff no violating walk is
bi-infinitely extendable (start reachable from a cycle, end reaching a cycle),
decided by strong components and two breadth-first searches on the sparse edge
list. Here h = 3 (65,536 vertices, 4,194,304 violating blocks); h = 2 is
rebuilt only to realize the fifteenth unit's 18 depth-two separations under 90
and 150 as eventually periodic pairs. No matrix power is taken and no ring
certificate at depth two or three is claimed.

Historical sets C, FS1, D1(n), FS2, D2(n) are read from the thirteenth to
fifteenth units' result files for 90 and 150 and DERIVED for 165 by the
transport r -> conj(r); nothing historical is read for 165. Unlike the
sixteenth unit's treatment of observation 32, FS3_165 and D3_165(n) are
computed directly, as the covariance regression of O6. The seventh unit's
h_star tables (exact partition refinement over kernel cosets, rings 6 to 12)
are read for the cross-implementation consistency control in O1 and for the
pen-decided part of O2.

O1  theorem and consistency controls: FS2 in FS3; FS3 in D3(n); D2(n) in
    D3(n); divisibility; c_FS >= c_R; D3_90(n) = 256 on odd rings and
    D3_150(n) = 256 off multiples of 3; D3(n) against the seventh unit's
    h_star <= 3 sets for rings 6 to 12.
O2  control: the twelve pen-decided rules (22, 151 under 90; 25, 37, 61, 67,
    91, 103, 152, 188, 194, 230 under 150) are outside FS3, each with an
    extendable violating walk. Reported with no bet: the split of the
    remaining 18 rules outside FS2_90 and 24 outside FS2_150.
O3  bet: the rings-3-to-14 depth-three gap is nonempty under each of 90, 150;
    the ring-14 gap reported without a bet.
O4  ladder cross-tab reported; bet: class c_FS = 3 nonempty under each.
O5  the 18 depth-two witness pairs pass the trimmed replay (margin 4).
O6  complement covariance 90 <-> 165 against the directly computed conjugate
    sets, complement invariance of the self-dual 150, reflection invariance.

Usage: python scripts/verify_full_shift_depth_three_linear.py
       python scripts/verify_full_shift_depth_three_linear.py --self-test
The self test exercises the shared machinery on observation 232, outside this
unit's domain, against an independent brute-force implementation, and writes
nothing.
"""
from __future__ import annotations
import hashlib, json, pathlib, sys
from collections import deque
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
CLOSURE = ROOT / 'results/ring_closure_certificate_20260911.json'
DEPTH_ONE = ROOT / 'results/depth_one_certificate_20260911.json'
DEPTH_TWO = ROOT / 'results/full_shift_depth_two_20260911.json'
LINEAR = ROOT / 'results/linear_observations_20260911.json'
OUT = ROOT / 'results/full_shift_depth_three_linear_20260912.json'
OBS = (90, 150); RINGS = tuple(range(3, 15)); H = 3
PERIODS = 3; SCC_LIST_CAP = 64; TOP = 4                  # class 4 means depth at least four
PEN_DEEP = {90: (22, 151), 150: (25, 37, 61, 67, 91, 103, 152, 188, 194, 230)}
H_STAR_RINGS = tuple(range(6, 13))                       # the seventh unit's rings

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def all_states(n):
    k = np.arange(2 ** n, dtype=np.int64); return ((k[:, None] >> (n - 1 - np.arange(n))) & 1).astype(np.uint8)
def lut(r): return np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
def step(S, r):
    t = lut(r); return t[4 * np.roll(S, 1, axis=1) + 2 * S + np.roll(S, -1, axis=1)]
def ints(S): return (S.astype(np.int64) << (S.shape[1] - 1 - np.arange(S.shape[1]))).sum(axis=1)
def conj(r): return sum((((r >> (7 - i)) & 1) ^ 1) << i for i in range(8))
def mirror(r): return sum(((r >> (((i & 4) >> 2) | (i & 2) | ((i & 1) << 2))) & 1) << i for i in range(8))
def transport(rules): return sorted(conj(r) for r in rules)
def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    raise TypeError(type(o))

# ---------------------------------------------------------------- exhaustive depth three
def exhaustive_depth(psi, n, h):
    """Rules whose h+1 observed steps determine the next on every state of the ring."""
    S = all_states(n); ys = [ints(step(S, psi))]; out = []
    for r in range(256):
        F = S; obs = [ys[0]]
        for _ in range(h + 1): F = step(F, r); obs.append(ints(step(F, psi)))
        key = obs[0].copy()
        for o in obs[1:-1]: key = key * (1 << n) + o
        order = np.argsort(key, kind='stable'); k, z = key[order], obs[-1][order]
        if not np.any((k[1:] == k[:-1]) & (z[1:] != z[:-1])): out.append(r)
    return out

def exhaustive_depth_bruteforce(psi, n, h):
    """Independent dictionary implementation of exhaustive_depth, for the self test only."""
    S = all_states(n); out = []
    for r in range(256):
        F = S; obs = [ints(step(S, psi))]
        for _ in range(h + 1): F = step(F, r); obs.append(ints(step(F, psi)))
        seen = {}; ok = True
        for i in range(2 ** n):
            key = tuple(int(o[i]) for o in obs[:-1]); z = int(obs[-1][i])
            if seen.setdefault(key, z) != z: ok = False; break
        if ok: out.append(r)
    return out

# ---------------------------------------------------------------- blocks, local maps, graphs
def pair_blocks(L):
    """All 4^L pair blocks as (x, y) uint8 arrays of shape (4^L, L); code MSB first, x bit above y bit per cell."""
    codes = np.arange(4 ** L, dtype=np.int64); X = np.empty((4 ** L, L), dtype=np.uint8); Y = np.empty_like(X)
    for j in range(L):
        c = (codes >> (2 * (L - 1 - j))) & 3; X[:, j] = c >> 1; Y[:, j] = c & 1
    return X, Y
def local(rule, X):
    """Apply an elementary rule along the last axis without wrap: output index j is cell j+1."""
    t = lut(rule); return t[4 * X[:, :-2] + 2 * X[:, 1:-1] + X[:, 2:]]
def codes(X, Y, start, width):
    c = np.zeros(X.shape[0], dtype=np.int64)
    for j in range(width): c = c * 4 + (2 * X[:, start + j].astype(np.int64) + Y[:, start + j])
    return c
def decode(code, width):
    cells = [(code >> (2 * (width - 1 - j))) & 3 for j in range(width)]
    return [c >> 1 for c in cells], [c & 1 for c in cells]
def agree_chain(psi, r, X, Y, depth):
    """Agreement arrays of psi F^k for k = 0..depth; array k has index j at cell j+1+k."""
    out = []; fx, fy = X, Y
    for k in range(depth + 1):
        out.append(local(psi, fx) == local(psi, fy))
        if k < depth: fx, fy = local(r, fx), local(r, fy)
    return out
BLOCKS = {}
def blocks(L):
    if L not in BLOCKS: BLOCKS[L] = pair_blocks(L)
    return BLOCKS[L]

def pair_graph(psi, r, h):
    """Adjacency lists on 4^(2h+2) vertices, the sorted violating (v0, v3) list, and the violating block codes."""
    w, e, b = 2 * h + 2, 2 * h + 3, 2 * h + 5
    EX, EY = blocks(e); ag = agree_chain(psi, r, EX, EY, h); c = h + 1                    # centre cell of the edge block
    ok = np.ones(4 ** e, dtype=bool)
    for k in range(h + 1): ok &= ag[k][:, c - 1 - k]
    adj = [[] for _ in range(4 ** w)]
    for s, d in zip(codes(EX, EY, 0, w)[ok].tolist(), codes(EX, EY, 1, w)[ok].tolist()): adj[s].append(d)
    BX, BY = blocks(b); ag = agree_chain(psi, r, BX, BY, h + 1); c0 = h + 1                # centres c0, c0+1, c0+2 of the three sub-blocks
    edges = np.ones(4 ** b, dtype=bool)
    for k in range(h + 1):
        for off in range(3): edges &= ag[k][:, c0 + off - 1 - k]
    viol = edges & ~ag[h + 1][:, c0 + 1 - 1 - (h + 1)]                                      # psi F^(h+1) disagrees at the centre c0+1
    vb = np.nonzero(viol)[0]
    walks = sorted(set(zip(codes(BX, BY, 0, w)[vb].tolist(), codes(BX, BY, 3, w)[vb].tolist())))
    return adj, walks, vb, codes(BX, BY, 0, w)[vb], codes(BX, BY, 3, w)[vb]

def strong_components(adj):
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
def reverse(adj):
    radj = [[] for _ in adj]
    for v in range(len(adj)):
        for w in adj[v]: radj[w].append(v)
    return radj
def cycle_facts(adj):
    n = len(adj); comp = strong_components(adj); size = {}
    for c in comp: size[c] = size.get(c, 0) + 1
    on = [size[comp[v]] > 1 or v in adj[v] for v in range(n)]
    seeds = [v for v in range(n) if on[v]]
    return on, reach(adj, seeds), reach(reverse(adj), seeds), comp
def full_shift(adj, walks):
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

def analyse(psi, h):
    fs, counts, ext_counts, witnesses = [], {}, {}, {}
    for r in range(256):
        adj, walks, *_ = pair_graph(psi, r, h); ok, w, k = full_shift(adj, walks)
        counts[r] = len(walks); ext_counts[r] = k
        if ok: fs.append(r)
        else: witnesses[r] = w
    return {'full_shift': fs, 'violating_walk_counts': counts, 'extendable_counts': ext_counts, 'witnesses': witnesses}

# ---------------------------------------------------------------- explicit witness pairs (O5)
def bfs_path(adj, start, goal):
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
    if u in adj[u]: return [u, u]
    best = None
    for w in adj[u]:
        p = bfs_path(adj, w, lambda v: v == u)
        if p is not None and (best is None or len(p) < len(best) - 1): best = [u] + p
    return best

def witness_pair(psi, r, v0, v3, h):
    """Eventually periodic pair realizing the recorded extendable walk (v0, v3) in G^h, with the finite replay (margin h+2)."""
    w, b, margin = 2 * h + 2, 2 * h + 5, h + 2
    adj, walks, vb, b0, b3 = pair_graph(psi, r, h)
    sel = np.nonzero((b0 == v0) & (b3 == v3))[0]; block = int(vb[sel[0]]); bx, by = decode(block, b)
    on, frm, to, comp = cycle_facts(adj); radj = reverse(adj)
    left = [v0] if on[v0] else bfs_path(radj, v0, lambda v: on[v])[::-1]; u = left[0]; cyc_l = shortest_cycle(adj, u)
    right = [v3] if on[v3] else bfs_path(adj, v3, lambda v: on[v]); wv = right[-1]; cyc_r = shortest_cycle(adj, wv)
    X1, Y1 = np.array([bx], dtype=np.uint8), np.array([by], dtype=np.uint8)
    v1, v2 = int(codes(X1, Y1, 1, w)[0]), int(codes(X1, Y1, 2, w)[0])
    walk = cyc_l[:-1] * PERIODS + left + [v1, v2] + right + cyc_r[1:] * PERIODS
    p0 = len(cyc_l[:-1]) * PERIODS + len(left) - 1
    x, y = list(decode(walk[0], w)[0]), list(decode(walk[0], w)[1])
    for v in walk[1:]:
        cx, cy = decode(v, w); x.append(cx[-1]); y.append(cy[-1])
    X, Y = np.array([x], dtype=np.uint8), np.array([y], dtype=np.uint8); L = len(x); centre = p0 + h + 2
    ag = agree_chain(psi, r, X, Y, h + 1); lo, hi = margin, L - 1 - margin
    passes = [bool(ag[k][0][lo - 1 - k:hi - k].all()) for k in range(h + 1)]
    disagree = not bool(ag[h + 1][0][centre - 1 - (h + 1)])
    assert x[centre - (h + 2):centre + h + 3] == bx and y[centre - (h + 2):centre + h + 3] == by
    def word(vs): return {'x': ''.join(str(decode(v, w)[0][-1]) for v in vs), 'y': ''.join(str(decode(v, w)[1][-1]) for v in vs)}
    return {'psi': psi, 'rule': r, 'depth': h, 'v0': v0, 'v3': v3, 'violating_block': {'x': ''.join(map(str, bx)), 'y': ''.join(map(str, by))},
            'left_cycle_word': word(cyc_l[1:]), 'left_path_word': word(left[1:]), 'right_path_word': word(right[1:]), 'right_cycle_word': word(cyc_r[1:]),
            'left_period': len(cyc_l) - 1, 'right_period': len(cyc_r) - 1, 'window_length': L, 'centre': centre, 'trimmed_margin': margin,
            'window': {'x': ''.join(map(str, x)), 'y': ''.join(map(str, y))},
            'agreement_passes_by_depth': passes, 'disagreement_at_centre': disagree, 'pass': all(passes) and disagree}

# ---------------------------------------------------------------- self test (writes nothing, out of domain)
def self_test():
    """Exercise the shared machinery on observation 232, outside this unit's domain of 90, 150, 165."""
    psi = 232
    for n in (5, 6, 7):
        fast, slow = exhaustive_depth(psi, n, 1), exhaustive_depth_bruteforce(psi, n, 1)
        assert fast == slow, (n, set(fast) ^ set(slow))
        print(f'self test: exhaustive_depth(232, n={n}, h=1) agrees with the brute force, {len(fast)} rules')
    for r in (30, 232):
        adj, walks, vb, b0, b3 = pair_graph(psi, r, 1)
        assert len(adj) == 4 ** 4 and len(vb) == len(b0) == len(b3)
        ok, wit, k = full_shift(adj, walks)
        on, frm, to, comp = cycle_facts(adj)
        assert ok == (k == 0)
        assert all(frm[v0] and to[v3] for v0, v3 in walks) == (k == len(walks))
        print(f'self test: G^1_(232,{r}) has {len(adj)} vertices, {len(walks)} violating walks, {k} extendable, in FS1 = {ok}')
        if wit is not None:
            p = witness_pair(psi, r, wit['v0'], wit['v3'], 1)
            assert p['pass'], p
            print(f"self test: witness pair for (232, {r}) at depth 1 replays, window {p['window_length']} cells")
    print('self test: passed; nothing written')

# ---------------------------------------------------------------- main
def main():
    d13, d14, d15 = json.loads(CLOSURE.read_text()), json.loads(DEPTH_ONE.read_text()), json.loads(DEPTH_TWO.read_text())
    d7 = json.loads(LINEAR.read_text())
    hist = {}                                                              # historical sets for 90 and 150, read
    for psi in OBS:
        p = str(psi)
        hist[psi] = {'C': d13['full_shift_closed'][p], 'FS1': d14['full_shift_depth_one'][p], 'FS2': d15['full_shift_depth_two'][p],
                     'D0': {n: d13['exhaustive_closed'][p][str(n)] for n in RINGS}, 'D1': {n: d14['exhaustive_depth_one'][p][str(n)] for n in RINGS},
                     'D2': {n: d15['exhaustive_depth_two'][p][str(n)] for n in RINGS}}
    conjs = sorted({conj(p) for p in OBS} - set(OBS))                      # 165 only; 150 is self-dual
    for q in conjs:                                                        # derived by transport, never read
        src = [p for p in OBS if conj(p) == q][0]; hsrc = hist[src]
        hist[q] = {'C': transport(hsrc['C']), 'FS1': transport(hsrc['FS1']), 'FS2': transport(hsrc['FS2']),
                   'D0': {n: transport(hsrc['D0'][n]) for n in RINGS}, 'D1': {n: transport(hsrc['D1'][n]) for n in RINGS}, 'D2': {n: transport(hsrc['D2'][n]) for n in RINGS}}
    m5 = d15['predictions']['M5_depth_two_gap']['witnesses_all_tested_ring_gap']
    deep18 = [(psi, int(r)) for psi in OBS for r in sorted(m5[str(psi)], key=int)]
    h_star = {psi: {n: d7['h_star'][str(psi)][str(n)] for n in H_STAR_RINGS} for psi in OBS}
    all_obs = list(OBS) + conjs
    EX = {psi: {n: exhaustive_depth(psi, n, H) for n in RINGS} for psi in all_obs}
    G = {psi: analyse(psi, H) for psi in all_obs}; FS3 = {psi: G[psi]['full_shift'] for psi in all_obs}
    def inter(sets): return sorted(set(range(256)).intersection(*[set(sets[n]) for n in RINGS]))
    def c_fs(psi, r):
        h = hist[psi]
        return 0 if r in h['C'] else 1 if r in h['FS1'] else 2 if r in h['FS2'] else 3 if r in FS3[psi] else TOP
    ringsets = {psi: [inter(hist[psi]['D0']), inter(hist[psi]['D1']), inter(hist[psi]['D2']), inter(EX[psi])] for psi in all_obs}
    def c_r(psi, r):
        for k, s in enumerate(ringsets[psi]):
            if r in s: return k
        return TOP
    classes = {psi: {r: [c_fs(psi, r), c_r(psi, r)] for r in range(256)} for psi in all_obs}
    P = {}
    o1 = {'FS2_subset_FS3': {str(psi): sorted(set(hist[psi]['FS2']) - set(FS3[psi])) for psi in all_obs},
          'FS3_subset_D3': {str(psi): [n for n in RINGS if not set(FS3[psi]) <= set(EX[psi][n])] for psi in all_obs},
          'D2_subset_D3': {str(psi): [n for n in RINGS if not set(hist[psi]['D2'][n]) <= set(EX[psi][n])] for psi in all_obs},
          'divisibility': {str(psi): [[n, kn] for n in RINGS for kn in RINGS if kn > n and kn % n == 0 and not set(EX[psi][kn]) <= set(EX[psi][n])] for psi in all_obs},
          'cFS_ge_cR_violations': {str(psi): [r for r in range(256) if classes[psi][r][0] < classes[psi][r][1]] for psi in all_obs},
          'D3_90_all_256_on_odd_rings': {str(n): len(EX[90][n]) == 256 for n in RINGS if n % 2},
          'D3_150_all_256_off_multiples_of_three': {str(n): len(EX[150][n]) == 256 for n in RINGS if n % 3},
          'h_star_consistency': {str(psi): {str(n): EX[psi][n] == sorted(int(r) for r, h in h_star[psi][n].items() if h <= H) for n in H_STAR_RINGS} for psi in OBS}}
    def flat(v):
        if isinstance(v, dict): return all(flat(x) for x in v.values())
        if isinstance(v, bool): return v
        return not v
    o1['pass'] = all(flat(v) for k, v in o1.items()); P['O1_theorem_and_consistency_controls'] = o1
    pen = [[psi, r] for psi in OBS for r in PEN_DEEP[psi]]
    pen_in3 = [[psi, r] for psi, r in pen if r in FS3[psi]]
    rest = {psi: [r for r in range(256) if r not in hist[psi]['FS2'] and r not in PEN_DEEP[psi]] for psi in OBS}
    o2 = {'pen_decided': pen, 'pen_decided_unexpectedly_in_FS3': pen_in3,
          'pen_decided_excluding_rings': {f'{psi}:{r}': [n for n in RINGS if r not in EX[psi][n]] for psi, r in pen},
          'pen_decided_h_star': {f'{psi}:{r}': {str(n): h_star[psi][n][str(r)] for n in H_STAR_RINGS} for psi, r in pen},
          'pen_decided_witnesses': {f'{psi}:{r}': G[psi]['witnesses'][r] for psi, r in pen if r not in FS3[psi]},
          'remaining_outside_FS2': {str(psi): rest[psi] for psi in OBS},
          'remaining_depth_exactly_three': {str(psi): [r for r in rest[psi] if r in FS3[psi]] for psi in OBS},
          'remaining_depth_at_least_four': {str(psi): [r for r in rest[psi] if r not in FS3[psi]] for psi in OBS},
          'remaining_witnesses_at_least_four': {str(psi): {str(r): G[psi]['witnesses'][r] for r in rest[psi] if r not in FS3[psi]} for psi in OBS}}
    o2['pass'] = not pen_in3; P['O2_deep_rules'] = o2
    gap_all = {psi: [r for r in ringsets[psi][3] if r not in FS3[psi]] for psi in all_obs}
    gap_14 = {psi: [r for r in EX[psi][14] if r not in FS3[psi]] for psi in all_obs}
    o3 = {'all_tested_ring_gap': {str(psi): gap_all[psi] for psi in all_obs}, 'ring_14_gap': {str(psi): gap_14[psi] for psi in all_obs},
          'all_tested_ring_depth_three': {str(psi): ringsets[psi][3] for psi in all_obs},
          'witnesses_all_tested_ring_gap': {str(psi): {str(r): G[psi]['witnesses'][r] for r in gap_all[psi]} for psi in OBS},
          'witnesses_ring_14_gap_only': {str(psi): {str(r): G[psi]['witnesses'][r] for r in gap_14[psi] if r not in gap_all[psi]} for psi in OBS}}
    o3['pass'] = all(gap_all[psi] for psi in OBS); P['O3_depth_three_gap'] = o3
    def crosstab(psi):
        t = {f'{a}x{b}': 0 for a in range(TOP + 1) for b in range(TOP + 1)}
        for r in range(256): a, b = classes[psi][r]; t[f'{a}x{b}'] += 1
        return {k: v for k, v in t.items() if v}
    o4 = {'classes': {str(psi): {str(r): classes[psi][r] for r in range(256)} for psi in all_obs},
          'crosstab_cFS_x_cR': {str(psi): crosstab(psi) for psi in all_obs},
          'class_sizes_cFS': {str(psi): [sum(1 for r in range(256) if classes[psi][r][0] == k) for k in range(TOP + 1)] for psi in all_obs},
          'class_sizes_cR': {str(psi): [sum(1 for r in range(256) if classes[psi][r][1] == k) for k in range(TOP + 1)] for psi in all_obs},
          'class_three_rules': {str(psi): [r for r in range(256) if classes[psi][r][0] == 3] for psi in all_obs}}
    o4['pass'] = all(o4['class_three_rules'][str(psi)] for psi in OBS); P['O4_ladder'] = o4
    pairs = [witness_pair(psi, r, m5[str(psi)][str(r)]['v0'], m5[str(psi)][str(r)]['v3'], 2) for psi, r in deep18]
    o5 = {'pairs': pairs, 'failing': [[p['psi'], p['rule']] for p in pairs if not p['pass']]}; o5['pass'] = not o5['failing']; P['O5_witness_pairs'] = o5
    o6 = {'complement_FS3': {str(psi): FS3[conj(psi)] == transport(FS3[psi]) for psi in OBS},
          'complement_D3': {str(psi): {str(n): EX[conj(psi)][n] == transport(EX[psi][n]) for n in RINGS} for psi in OBS},
          'self_dual_observations': {str(psi): conj(psi) == psi for psi in OBS},
          'reflection_symmetric_observations': {str(psi): mirror(psi) == psi for psi in all_obs},
          'reflection_FS3': {str(psi): FS3[psi] == sorted(mirror(r) for r in FS3[psi]) for psi in all_obs},
          'reflection_D3': {str(psi): {str(n): EX[psi][n] == sorted(mirror(r) for r in EX[psi][n]) for n in RINGS} for psi in all_obs}}
    o6['pass'] = all(o6['complement_FS3'].values()) and all(o6['reflection_FS3'].values()) and all(o6['reflection_symmetric_observations'].values()) \
        and all(v for d in o6['complement_D3'].values() for v in d.values()) and all(v for d in o6['reflection_D3'].values() for v in d.values())
    P['O6_symmetries'] = o6
    report = {'protocol': 'full-shift-depth-three-linear-20260912', 'schema': 1, 'observations': list(OBS), 'conjugate_observations': conjs, 'rings_exhaustive': list(RINGS),
              'parameters': {'depth': H, 'vertices': 4 ** (2 * H + 2), 'edge_blocks': 4 ** (2 * H + 3), 'violation_blocks': 4 ** (2 * H + 5),
                             'witness_depth': 2, 'witness_trimmed_margin': 4, 'periods_per_side': PERIODS, 'scc_list_cap': SCC_LIST_CAP, 'top_class_means_at_least': TOP,
                             'h_star_rings': list(H_STAR_RINGS)},
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'ring_closure_certificate_result': sha(CLOSURE),
                                'depth_one_certificate_result': sha(DEPTH_ONE), 'full_shift_depth_two_result': sha(DEPTH_TWO),
                                'linear_observations_result': sha(LINEAR)},
              'historical_set_transport': {'rule': 'X_{conj(psi)} = {conj(r) : r in X_psi} for C, FS1, D1(n), FS2, D2(n); conj(r)(a,b,c) = not r(not a, not b, not c)',
                                           'derived_for': conjs, 'read_for': list(OBS),
                                           'note': '150 is self-dual, so its transport is the identity; 165 = conj(90) is absent from the thirteenth to fifteenth units and its historical sets are derived, while FS3_165 and D3_165(n) are computed directly as the covariance regression of O6'},
              'pen_decided_deep_rules': {str(psi): list(PEN_DEEP[psi]) for psi in OBS},
              'seventh_unit_h_star_rings': list(H_STAR_RINGS),
              'exhaustive_depth_three': {str(psi): {str(n): EX[psi][n] for n in RINGS} for psi in all_obs},
              'full_shift_depth_three': {str(psi): FS3[psi] for psi in all_obs},
              'violating_walk_counts': {str(psi): {str(r): G[psi]['violating_walk_counts'][r] for r in range(256)} for psi in all_obs},
              'extendable_violation_counts': {str(psi): {str(r): G[psi]['extendable_counts'][r] for r in range(256)} for psi in all_obs},
              'predictions': P, 'summary': {k: v['pass'] for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary']))
    print('FS3 sizes', {p: len(FS3[p]) for p in all_obs}); print('D3(14) sizes', {p: len(EX[p][14]) for p in all_obs})
    print('O2 pen unexpectedly in FS3', pen_in3)
    print('O2 remaining exactly three', {p: o2['remaining_depth_exactly_three'][str(p)] for p in OBS})
    print('O2 remaining at least four', {p: o2['remaining_depth_at_least_four'][str(p)] for p in OBS})
    print('gap[3,14]', {p: gap_all[p] for p in OBS}); print('gap14 sizes', {p: len(gap_14[p]) for p in OBS})
    print('class three', {p: o4['class_three_rules'][str(p)] for p in OBS})
    print('crosstab', {p: o4['crosstab_cFS_x_cR'][str(p)] for p in OBS}); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    if '--self-test' in sys.argv[1:]: self_test()
    else: main()
