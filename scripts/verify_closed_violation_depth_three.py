#!/usr/bin/env python3
"""Closed violating walks decide the all-ring depth sets: the all-ring depth-three
set, first failing rings and eventual periods from strong components, without
matrix powers (protocol frozen 2026-09-13, re-frozen after Codex's gate-1 round
one B1/B2, gate-1 approval by OpenAI GPT-5.6 Sol on the exact head
aa7e67a07da9224cb1ef75ab13ad287121238bc0 before this implementation; see the
protocol's Section 5).

Observations psi in {232, 4, 32, 200, 22, 102, 90, 150} with their complement
conjugates and mirrors as controls; rules r in 0..255. The depth-h pair graph
G^h_{psi,r} is the sixteenth unit's `pair_graph(psi, r, h)`, imported from
scripts/verify_full_shift_depth_three.py and not rebuilt here: vertices the
4^(2h+2) pair blocks of 2h+2 cells, an edge per (2h+3)-cell pair block whose
centre agrees on psi F^k for k = 0..h, a violating three-edge walk per
(2h+5)-cell pair block whose psi F^(h+1) disagrees at the centre, recorded by
its end pair (v0, v3).

Ring criterion (theorem, thirteenth/fourteenth/eighteenth units). For n >= 4,
  r not in D^h_psi(n)  iff  some (v0, v3) in V^h has (A^(n-3))[v3, v0] = 1.
Closed violations V^h_cl are the violating walks whose ends lie in one strong
component. Lemma A (protocol Section 1, pen, gate-1 checked): V^h_cl nonempty
implies r not in D^h_psi^inf, because a strong component supplies a return walk
v3 ~> v0 of some length m >= 1 (and when v0 = v3 the violating walk itself is a
closed walk of length 3), so the criterion fails at the ring m + 3 >= 4. With
the eighteenth unit's pruning lemma this gives Corollary A,

      D^h_psi^inf  =  { r : V^h_cl = empty },

at every depth and for every observation: the all-ring depth set is decided by
strong components and breadth-first search. NO POWER OF ANY MATRIX IS TAKEN AT
ANY DEPTH. At depth three that is exactly the part of a ring certificate the
eighteenth unit declared out of reach (65,536-vertex powers).

Derived per pair, all from the component structure:
  m_min   least m >= 1 with (A^m)[v3, v0] = 1 over (v0, v3) in V^h_cl: the
          breadth-first distance v3 -> v0 when the ends differ, and the least
          positive closed walk through v3 (girth through v3, at most 3, since
          the violating walk itself closes) when they coincide;
  n_min   m_min + 3, the least ring n >= 4 with r not in D^h_psi(n);
  p_C, c  each carrying component's period (the gcd of level(u) + 1 - level(w)
          over its internal edges from a breadth-first level function) and its
          cyclic classes, Lind-Marcus SS4.5 / Brualdi-Ryser SS3.4;
  R_r     the residue set  U_{(v0,v3) in V^h_cl} { m = c(v0) - c(v3) mod p_C },
          lifted to the common modulus L = lcm of the periods involved;
  p_r     the least period of the indicator of R_r (a divisor of L); the rule is
          eventually out when R_r is everything and eventually oscillating
          otherwise;
  P^h_psi = lcm_r p_r and the eventual sets D^h_{psi,ev}(j) = {r : (j - 3) mod
          P not in R_r} for j in Z/P. The ONSET beyond which D^h_psi(n) follows
          the eventual pattern is NOT determined here (protocol Section 4).

Historical sets are read with their hashes, never recomputed: D1^inf and the
depth-one certificates from results/depth_one_certificate_20260911.json;
D2(n), D2^inf, P2, N2 and the per-rule |V2_cl| from
results/depth_two_certificate_20260912.json; FS2 from
results/full_shift_depth_two_20260911.json; FS3, D3(n) for 3 <= n <= 14 and the
rings-3-to-14 gaps from results/full_shift_depth_three_20260912.json (232, 200,
22, 4 and the conjugates 151, 223, 236; observation 32 by that unit's deduction
F_32 = F_4 o not, so every set under 32 equals the set under 223, and
FS3_251 = {conj r : r in FS3_32}) and
results/full_shift_depth_three_linear_20260912.json (90, 150, 165).
FS3_102 = D3_102(n) = all 256 rules by the fifteenth unit's M4.

Q1  theorem controls on recorded data: (a) depth one, V1_cl empty iff r in
    D1^inf; (b) depth two, the same against D2^inf, and |V2_cl| per rule equals
    the eighteenth unit's recorded count; (c) depth two, n_min equals the least
    recorded failing ring, including the hard numeric control that the twelve
    ring-24 rules under 22 give m_min = 21; (d) depth two, p_r equals the least
    period of the recorded membership sequence, P2_psi = 1, 2, 2, 1, 12, 1, 4, 6
    is reproduced and the eventual sets equal the certified sets on the period
    from N2_psi; (e) depth three, the frozen control sample (the eight smallest
    rules in FS3_psi per observation) has V3_cl empty.
Q2  D3_psi^inf, the all-ring gap Gamma3_{psi,inf} = D3^inf \ FS3, its inclusion
    in the rings-3-to-14 gap (theorem), the empty-gap controls for 102 and 150,
    and bets (a) nonempty under each of 232, 4, 32, 200, 22, 90, (b) the window
    overstates the all-ring gap somewhere, (c) 22 is among the failures.
Q3  n_min at depth three for every rule outside D3^inf, with the consistency
    control against the recorded rings 4..14, the distribution and the maximum.
Q4  p_r, P3_psi and the eventual sets at depth three; theorem controls for 90 on
    odd residues and 150 off multiples of three; bets P3_232 = P3_200 = 1,
    P3_4 = P3_32 = 1, 3 | P3_22, P3_90 = 4, P3_150 = 6.
Q5  per pair: the carrying components, their sizes and periods, general diagonal
    anchoring (any vertex (x, x)) as a reported statistic and constant-diagonal
    anchoring ((x, x) with x constant, which carries a self-loop) as the
    theorem-controlled quantity. Corollary B forbids only the latter for an
    eventually oscillating rule; a general diagonal anchor in an oscillating rule
    is reported, NOT treated as an error (protocol Section 5, correction B1).
    Bet: every eventually-out rule under 232, 200, 22 is diagonal-anchored.
Q6  complement and reflection transport of |V3_cl|, n_min, p_r, R_r (residues
    negated under reflection), component sizes and periods and anchoring, under
    the explicit vertex maps; the set-level transport of D3^inf, Gamma3 and P3;
    and the explicit graph correspondence on a frozen sample.

Usage:
    python scripts/verify_closed_violation_depth_three.py                  # canonical run
    python scripts/verify_closed_violation_depth_three.py --self-test      # < 2 min, writes nothing
    python scripts/verify_closed_violation_depth_three.py --probe 232 --depth 3 --rules 58,78
                                                                          # probe, writes nothing
The self test exercises Corollary A and m_min on synthetic graphs with known
closed violating walks (including both coincident-endpoint cases) against
explicit dense powers, the graph construction against the fourteenth and
eighteenth units' recorded graphs, Q1(a) under one observation, the ring-24
m_min = 21 control at depth two, and Corollary B on a recorded oscillating rule.
"""
from __future__ import annotations
import hashlib, importlib.util, json, math, pathlib, sys, time
from collections import deque
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
SIXTEENTH_SCRIPT = ROOT / 'scripts/verify_full_shift_depth_three.py'
FOURTEENTH_SCRIPT = ROOT / 'scripts/verify_depth_one_certificate.py'
DEPTH_ONE = ROOT / 'results/depth_one_certificate_20260911.json'
DEPTH_TWO_CERT = ROOT / 'results/depth_two_certificate_20260912.json'
FULL_SHIFT_TWO = ROOT / 'results/full_shift_depth_two_20260911.json'
FULL_SHIFT_THREE = ROOT / 'results/full_shift_depth_three_20260912.json'
FULL_SHIFT_THREE_LINEAR = ROOT / 'results/full_shift_depth_three_linear_20260912.json'
OUT = ROOT / 'results/closed_violation_depth_three_20260913.json'

OBS = (232, 4, 32, 200, 22, 102, 90, 150)
DEPTH_THREE_OBS = (232, 4, 32, 200, 22, 90, 150)      # 102 has FS3 = all 256, nothing outside it
RINGS = tuple(range(3, 15))                           # rings recorded by the sixteenth/seventeenth units
GRAPH_RINGS = tuple(range(4, 15))                     # rings the criterion covers within that range
CONTROL_SAMPLE = 8                                    # frozen Q1(e) sample: smallest rules in FS3_psi
GRAPH_CORR_SAMPLE = 2                                 # frozen Q6 sample for the explicit edge/walk maps
GIRTH_CAP = 3                                         # a violating walk closes, so a coincident end has m_min <= 3
RING_24_RULES_UNDER_22 = (104, 105, 106, 107, 108, 109, 110, 111, 120, 121, 124, 125)
RING_24_M_MIN = 21                                    # the eighteenth unit's certified least failing ring 24
P2_CERTIFIED = {232: 1, 4: 2, 32: 2, 200: 1, 22: 12, 102: 1, 90: 4, 150: 6}
SELF_TEST_DENSE_POWERS = 40
SELF_TEST_SANITY_RULES = (0, 58, 110, 232)

# ---------------------------------------------------------------- the sixteenth unit's graph, reused
def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
U16 = _load(SIXTEENTH_SCRIPT, 'verify_full_shift_depth_three')
pair_graph = U16.pair_graph                 # the depth-h pair graph, verbatim
strong_components = U16.strong_components   # iterative Tarjan
conj = U16.conj; mirror = U16.mirror; sha = U16.sha

def jsonable(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, set): return sorted(o)
    raise TypeError(type(o))
def lcm(a, b): return a * b // math.gcd(a, b)
def lcm_all(xs):
    out = 1
    for x in xs: out = lcm(out, x)
    return out
def divisors(p): return [q for q in range(1, p + 1) if p % q == 0]
def transport(rules): return sorted(conj(r) for r in rules)
def width(h): return 2 * h + 2
def vertices(h): return 4 ** width(h)

# ---------------------------------------------------------------- vertex permutation maps (Q6)
def vertex_complement(v, h):
    """Complementing both tracks maps each cell code c = 2x + y to 3 - c, i.e. v -> v xor (4^w - 1)."""
    return v ^ (vertices(h) - 1)
def vertex_mirror(v, h):
    """Reflection reverses the w = 2h + 2 cells of the block."""
    out = 0
    for _ in range(width(h)): out = (out << 2) | (v & 3); v >>= 2
    return out
def diagonal_vertices(h):
    """Vertices (x, x): every cell code is 0 or 3. Code 0 and 4^w - 1 are the constant ones."""
    w = width(h)
    return [sum(3 << (2 * (w - 1 - j)) for j in range(w) if (x >> (w - 1 - j)) & 1) for x in range(2 ** w)]

# ---------------------------------------------------------------- breadth-first search on the pair graph
def reverse_adjacency(adj):
    rev = [[] for _ in adj]
    for u, outs in enumerate(adj):
        for w in outs: rev[w].append(u)
    return rev

def bfs_distances(adj, src, cap=None):
    """Distances from src as a dict, depth-bounded by cap when given (cap 0 means src only)."""
    dist = {src: 0}; frontier = [src]; d = 0
    while frontier and (cap is None or d < cap):
        d += 1; nxt = []
        for u in frontier:
            for w in adj[u]:
                if w not in dist: dist[w] = d; nxt.append(w)
        frontier = nxt
    return dist

def closed_walk_length(adj, rev, v, cap=GIRTH_CAP):
    """Least positive closed-walk length through v, searched to cap; None if none within cap."""
    if v in adj[v]: return 1
    dist = bfs_distances(adj, v, cap=cap - 1)
    cands = [dist[u] + 1 for u in rev[v] if u in dist]
    return min(cands) if cands else None

def m_min_facts(adj, rev, closed):
    """(m_min, witness (v0, v3)) over the closed violations, by bounded breadth-first search.

    The minimum is taken over all closed violating walks; the search is pruned by
    the running best, so a small m_min costs a shallow search. A shortest walk
    v3 -> v0 between mutually reachable vertices never leaves their strong
    component, so unrestricted search is already the component-restricted one.
    """
    by_v3 = {}
    for v0, v3 in closed: by_v3.setdefault(v3, set()).add(v0)
    best, witness = None, None
    for v3 in sorted(by_v3):                                     # coincident ends first: m <= GIRTH_CAP
        if v3 in by_v3[v3]:
            m = closed_walk_length(adj, rev, v3)
            assert m is not None and m <= GIRTH_CAP, (v3, m)
            if best is None or m < best: best, witness = m, (v3, v3)
    for v3 in sorted(by_v3):
        targets = by_v3[v3] - {v3}
        if not targets or (best is not None and best <= 1): continue
        cap = None if best is None else best - 1
        dist = bfs_distances(adj, v3, cap=cap)
        for v0 in sorted(targets):
            m = dist.get(v0)
            if m is not None and m >= 1 and (best is None or m < best): best, witness = m, (v0, v3)
    return best, witness

# ---------------------------------------------------------------- components, periods, cyclic classes
def component_facts(adj, comp, seeds, h):
    """Facts about each strong component carrying a closed violation, keyed by component id.

    period: the gcd of level(u) + 1 - level(w) over the component's internal edges
    from a breadth-first level function rooted anywhere in it (Lind-Marcus SS4.5);
    classes: level mod period, so c(w) = c(u) + 1 along every internal edge.
    """
    ids = sorted({comp[v] for v in seeds})
    members = {i: [] for i in ids}
    for v, c in enumerate(comp):
        if c in members: members[c].append(v)
    diag = [v for v in diagonal_vertices(h) if v < len(comp) and comp[v] in members]   # v < len for synthetic graphs
    const_diag = {0, vertices(h) - 1}
    out = {}
    for i in ids:
        mem = members[i]; mset = set(mem); root = mem[0]
        level = {root: 0}; dq = deque([root])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if w in mset and w not in level: level[w] = level[u] + 1; dq.append(w)
        assert len(level) == len(mem), (i, len(level), len(mem))
        p = 0
        for u in mem:
            for w in adj[u]:
                if w in mset: p = math.gcd(p, abs(level[u] + 1 - level[w]))
        assert p >= 1, (i, p)                                    # a carrying component always has a cycle
        dv = [v for v in diag if comp[v] == i]
        out[i] = {'size': len(mem), 'period': p, 'classes': {v: level[v] % p for v in mem},
                  'diagonal_vertices': len(dv), 'diagonal_anchored': bool(dv),
                  'constant_diagonal_anchored': any(v in const_diag for v in dv)}
    return out

def residue_facts(closed, comp, cfacts):
    """R_r at the common modulus L, its least period p_r, and whether the rule is eventually out."""
    periods = sorted({cfacts[comp[v0]]['period'] for v0, _ in closed})
    L = lcm_all(periods)
    residues = set()
    for v0, v3 in closed:
        cf = cfacts[comp[v0]]; p = cf['period']
        d = (cf['classes'][v0] - cf['classes'][v3]) % p
        residues |= {j for j in range(L) if j % p == d}
    p_r = next(q for q in divisors(L) if all((j in residues) == (((j + q) % L) in residues) for j in range(L)))
    return {'residue_modulus': L, 'residues': sorted(residues), 'component_periods': periods,
            'eventual_period': p_r, 'eventually_out': len(residues) == L}

# ---------------------------------------------------------------- the per-pair analysis
def pair_facts(psi, r, h, keep_classes=False):
    """Everything Corollary A and the eventual-pattern theorem give for (psi, r) at depth h."""
    t0 = time.time()
    adj, walks, *_ = pair_graph(psi, r, h)
    comp = strong_components(adj)
    closed = [(v0, v3) for v0, v3 in walks if comp[v0] == comp[v3]]
    facts = {'psi': psi, 'rule': r, 'depth': h, 'violating_walks': len(walks),
             'closed_violating_walks': len(closed), 'all_ring': not closed}
    if not closed:
        facts.update({'m_min': None, 'n_min': None, 'witness': None, 'components': [],
                      'residue_modulus': 1, 'residues': [], 'component_periods': [],
                      'eventual_period': 1, 'eventually_out': False,
                      'diagonal_anchored': False, 'constant_diagonal_anchored': False,
                      'seconds': round(time.time() - t0, 2)})
        return facts
    rev = reverse_adjacency(adj)
    m_min, witness = m_min_facts(adj, rev, closed)
    seeds = {v for pair in closed for v in pair}
    cf = component_facts(adj, comp, seeds, h)
    res = residue_facts(closed, comp, cf)
    comps = [{'component': i, 'size': c['size'], 'period': c['period'],
              'diagonal_vertices': c['diagonal_vertices'], 'diagonal_anchored': c['diagonal_anchored'],
              'constant_diagonal_anchored': c['constant_diagonal_anchored'],
              'closed_violating_walks': sum(1 for v0, _ in closed if comp[v0] == i)}
             for i, c in sorted(cf.items())]
    facts.update({'m_min': m_min, 'n_min': m_min + 3, 'witness': list(witness), 'components': comps,
                  'diagonal_anchored': any(c['diagonal_anchored'] for c in comps),
                  'constant_diagonal_anchored': any(c['constant_diagonal_anchored'] for c in comps),
                  'witness_component': {'size': cf[comp[witness[0]]]['size'],
                                        'period': cf[comp[witness[0]]]['period']},
                  'seconds': round(time.time() - t0, 2)})
    facts.update({k: v for k, v in res.items()})
    if keep_classes: facts['_classes'] = {i: cf[i]['classes'] for i in cf}
    return facts

def in_residue_set(facts, m):
    """Whether the ring offset m = n - 3 lies in R_r; False when the rule has no closed violation."""
    if not facts['residues']: return False
    return (m % facts['residue_modulus']) in set(facts['residues'])

def observation_eventual(facts_by_rule):
    """P^h_psi and the eventual sets D^h_{psi,ev}(j), j in Z/P (the residue of the ring size)."""
    P = lcm_all([f['eventual_period'] for f in facts_by_rule.values()])
    ev = {j: sorted(r for r, f in facts_by_rule.items() if not in_residue_set(f, (j - 3) % P)) for j in range(P)}
    return P, ev

# ---------------------------------------------------------------- historical sets, read with hashes
def read_history():
    d1 = json.loads(DEPTH_ONE.read_text()); d2c = json.loads(DEPTH_TWO_CERT.read_text())
    fs2 = json.loads(FULL_SHIFT_TWO.read_text()); fs3 = json.loads(FULL_SHIFT_THREE.read_text())
    fs3l = json.loads(FULL_SHIFT_THREE_LINEAR.read_text())
    H = {'D1_inf': {psi: d1['all_ring_depth_one'][str(psi)] for psi in OBS},
         'D1_cert': {psi: d1['predictions']['L3_certificates'][str(psi)] for psi in OBS},
         'D2_inf': {psi: d2c['all_ring_depth_two'][str(psi)] for psi in OBS},
         'D2_cert': {psi: d2c['predictions']['P2_certificates'][str(psi)] for psi in OBS},
         'D2_leaving': {psi: d2c['predictions']['P4_all_ring_gap'][str(psi)].get('rules_leaving_after_ring_14', {})
                        for psi in OBS},
         'FS2': {psi: fs2['full_shift_depth_two'][str(psi)] for psi in OBS}}
    FS3, D3, GAP = {}, {}, {}
    for psi in (232, 200, 22, 4, 151, 223, 236):
        FS3[psi] = fs3['full_shift_depth_three'][str(psi)]
        D3[psi] = {n: fs3['exhaustive_depth_three'][str(psi)][str(n)] for n in RINGS}
        GAP[psi] = fs3['predictions']['N3_depth_three_gap']['all_tested_ring_gap'][str(psi)]
    for psi in (90, 150, 165):
        FS3[psi] = fs3l['full_shift_depth_three'][str(psi)]
        D3[psi] = {n: fs3l['exhaustive_depth_three'][str(psi)][str(n)] for n in RINGS}
        GAP[psi] = fs3l['predictions']['O3_depth_three_gap']['all_tested_ring_gap'][str(psi)]
    FS3[32], D3[32], GAP[32] = FS3[223], D3[223], GAP[223]     # sixteenth unit's deduction F_32 = F_4 o not
    FS3[251] = transport(FS3[32]); D3[251] = {n: transport(D3[32][n]) for n in RINGS}
    GAP[251] = transport(GAP[32])
    FS3[102] = list(range(256)); D3[102] = {n: list(range(256)) for n in RINGS}; GAP[102] = []
    H.update({'FS3': FS3, 'D3': D3, 'GAP3': GAP})
    return H

def recorded_depth_two_sets(H, psi):
    """The eighteenth unit's certified D2_psi(n) as {n: set}, with its onset N and period P."""
    cert = H['D2_cert'][psi]; sets = cert['certified_depth_two_sets']
    return ({int(n): v for n, v in sets.items()}, cert['onset_ring_N'], cert['least_eventual_period_P'])

def recorded_least_failing_ring(H, psi, r):
    """Least n >= 4 with r not in D2_psi(n) from the eighteenth unit's record, or None."""
    sets, _, _ = recorded_depth_two_sets(H, psi)
    for n in sorted(sets):
        if r not in sets[n]: return n
    entry = H['D2_leaving'][psi].get(str(r))
    return None if entry is None else entry['least_ring']

def recorded_rule_period(H, psi, r):
    """Least eventual period of r's recorded depth-two membership, read off the certified window."""
    sets, N, P = recorded_depth_two_sets(H, psi)
    window = [r in sets[N + i] for i in range(P)]
    return next(q for q in divisors(P) if all(window[i] == window[(i + q) % P] for i in range(P)))

# ---------------------------------------------------------------- the computed depth-three domain
def depth_three_domain(H):
    """Section 3's domain: the rules outside FS3 under the seven live observations, the same under the
    conjugate observations, the mirror images of an asymmetric observation's deep rules (vacuous:
    every observation carrying deep rules is mirror-symmetric), and the frozen control sample."""
    dom = {}
    for psi in DEPTH_THREE_OBS:
        deep = [r for r in range(256) if r not in set(H['FS3'][psi])]
        control = sorted(H['FS3'][psi])[:CONTROL_SAMPLE]
        dom[psi] = {'deep': deep, 'control': control, 'role': 'source'}
        q = conj(psi)
        if q != psi:
            dq = [r for r in range(256) if r not in set(H['FS3'][q])]
            dom[q] = {'deep': dq, 'control': sorted(H['FS3'][q])[:CONTROL_SAMPLE], 'role': 'conjugate'}
        m = mirror(psi)
        if m != psi:
            dm = [r for r in range(256) if r not in set(H['FS3'][m])]
            dom[m] = {'deep': dm, 'control': sorted(H['FS3'][m])[:CONTROL_SAMPLE], 'role': 'mirror'}
    return dom

# ---------------------------------------------------------------- explicit graph correspondence (Q6)
def graph_correspondence(psi, r, h):
    """The complement and reflection vertex maps carry G^h_{psi,r} onto its images."""
    adj, walks, *_ = pair_graph(psi, r, h)
    edges = {(u, w) for u, outs in enumerate(adj) for w in outs}; W = set(walks)
    adj_c, walks_c, *_ = pair_graph(conj(psi), conj(r), h)
    ec = {(u, w) for u, outs in enumerate(adj_c) for w in outs}
    comp_edges = ec == {(vertex_complement(u, h), vertex_complement(w, h)) for u, w in edges}
    comp_walks = set(walks_c) == {(vertex_complement(a, h), vertex_complement(b, h)) for a, b in W}
    adj_m, walks_m, *_ = pair_graph(mirror(psi), mirror(r), h)
    em = {(u, w) for u, outs in enumerate(adj_m) for w in outs}
    mir_edges = em == {(vertex_mirror(w, h), vertex_mirror(u, h)) for u, w in edges}
    mir_walks = set(walks_m) == {(vertex_mirror(b, h), vertex_mirror(a, h)) for a, b in W}
    return {'psi': psi, 'rule': r, 'depth': h, 'complement_edges': comp_edges,
            'complement_violating_walks': comp_walks, 'reflection_edges': mir_edges,
            'reflection_violating_walks': mir_walks,
            'pass': comp_edges and comp_walks and mir_edges and mir_walks}

def stat_key(f, negate_residues=False):
    """The transported statistics of a pair: |V_cl|, n_min, p_r, R_r, component sizes/periods, anchoring."""
    L = f['residue_modulus']
    res = sorted((-x) % L for x in f['residues']) if negate_residues else sorted(f['residues'])
    return {'closed_violating_walks': f['closed_violating_walks'], 'n_min': f['n_min'],
            'eventual_period': f['eventual_period'], 'residue_modulus': L, 'residues': res,
            'components': sorted((c['size'], c['period'], c['diagonal_anchored'],
                                  c['constant_diagonal_anchored']) for c in f['components']),
            'diagonal_anchored': f['diagonal_anchored'],
            'constant_diagonal_anchored': f['constant_diagonal_anchored']}

# ---------------------------------------------------------------- self test (writes nothing)
def synthetic(edges, n):
    adj = [[] for _ in range(n)]
    for u, w in edges: adj[u].append(w)
    return adj

def dense_reachable_exponents(adj, v0, v3, count):
    """{m in 1..count : (A^m)[v3, v0] = 1} by explicit dense boolean powers, an independent path."""
    n = len(adj); A = np.zeros((n, n), dtype=np.uint8)
    for u, outs in enumerate(adj):
        for w in outs: A[u, w] = 1
    M = np.eye(n, dtype=np.uint8); hits = []
    for m in range(1, count + 1):
        M = ((M.astype(np.float32) @ A.astype(np.float32)) > 0).astype(np.uint8)
        if M[v3, v0]: hits.append(m)
    return hits

def self_test():
    t0 = time.time(); problems = []
    H = read_history()

    # (a) Corollary A, m_min and the eventual residue pattern on a synthetic graph with a known
    #     closed violating walk: a 5-cycle 0->1->2->3->4->0 with the violating pair (v0, v3) = (0, 3).
    adj = synthetic([(i, (i + 1) % 5) for i in range(5)], 5)
    comp = strong_components(adj); closed = [(0, 3)]
    assert comp[0] == comp[3]
    m_min, witness = m_min_facts(adj, reverse_adjacency(adj), closed)
    cf = component_facts(adj, comp, {0, 3}, 0)
    res = residue_facts(closed, comp, cf)
    hits = dense_reachable_exponents(adj, 0, 3, SELF_TEST_DENSE_POWERS)
    pred = [m for m in range(1, SELF_TEST_DENSE_POWERS + 1) if (m % res['residue_modulus']) in set(res['residues'])]
    ok = (m_min == 2 and witness == (0, 3) and hits == pred and min(hits) == m_min
          and res['residue_modulus'] == 5 and res['eventual_period'] == 5 and not res['eventually_out'])
    print(f'synthetic 5-cycle m_min={m_min} L={res["residue_modulus"]} p_r={res["eventual_period"]} '
          f'residues={res["residues"]} dense_hits_match={hits == pred}')
    if not ok: problems.append(f'synthetic 5-cycle: m_min={m_min} residues={res["residues"]} hits={hits[:8]}')
    #     period 1 means eventually out: add a chord so the component's cycle lengths are 5 and 4
    adj2 = synthetic([(i, (i + 1) % 5) for i in range(5)] + [(3, 0)], 5)
    comp2 = strong_components(adj2); cf2 = component_facts(adj2, comp2, {0, 3}, 0)
    res2 = residue_facts([(0, 3)], comp2, cf2)
    hits2 = dense_reachable_exponents(adj2, 0, 3, SELF_TEST_DENSE_POWERS)
    print(f'synthetic 5-cycle + chord period={cf2[comp2[0]]["period"]} p_r={res2["eventual_period"]} '
          f'eventually_out={res2["eventually_out"]} dense_tail_all_ones={hits2[-6:] == list(range(SELF_TEST_DENSE_POWERS - 5, SELF_TEST_DENSE_POWERS + 1))}')
    if not (res2['eventual_period'] == 1 and res2['eventually_out']):
        problems.append('chorded 5-cycle should be eventually out with p_r = 1')

    # (b) the coincident-endpoint case: a self-loop gives m_min 1, a 3-cycle without one gives 3.
    loop = synthetic([(0, 0), (0, 1), (1, 0)], 2)
    m_loop, w_loop = m_min_facts(loop, reverse_adjacency(loop), [(0, 0)])
    tri = synthetic([(0, 1), (1, 2), (2, 0)], 3)
    m_tri, w_tri = m_min_facts(tri, reverse_adjacency(tri), [(0, 0)])
    print(f'coincident ends: self-loop m_min={m_loop} (expect 1), 3-cycle m_min={m_tri} (expect 3)')
    if (m_loop, m_tri) != (1, 3): problems.append(f'coincident-end m_min wrong: {(m_loop, m_tri)}')
    if dense_reachable_exponents(tri, 0, 0, 6) != [3, 6]:
        problems.append('dense control for the coincident 3-cycle case disagrees')

    # (c) graph-construction sanity against the fourteenth and eighteenth units' recorded graphs.
    U14 = _load(FOURTEENTH_SCRIPT, 'verify_depth_one_certificate')
    bad = []
    for r in SELF_TEST_SANITY_RULES:
        adj1, walks1, *_ = pair_graph(232, r, 1); A, w1 = U14.depth_one_graph(232, r)
        e_new = {(u, w) for u, outs in enumerate(adj1) for w in outs}
        e_old = {(u, w) for u in range(256) for w in range(256) if A[u, w]}
        if e_new != e_old or set(walks1) != set(w1): bad.append(r)
    print(f'depth-one graph equals the fourteenth unit\'s for rules {list(SELF_TEST_SANITY_RULES)}: {not bad}')
    if bad: problems.append(f'depth-one graph differs from the fourteenth unit\'s at rules {bad}')
    f2 = pair_facts(4, 50, 2)
    rec = H['D2_cert'][4]
    ok2 = (f2['violating_walks'] == rec['violating_walks']['50']
           and f2['closed_violating_walks'] == rec['closed_violating_walks']['50'])
    print(f'depth-two counts for (4, 50): |V2|={f2["violating_walks"]} |V2cl|={f2["closed_violating_walks"]} '
          f'recorded {rec["violating_walks"]["50"]}/{rec["closed_violating_walks"]["50"]}')
    if not ok2: problems.append('depth-two violating-walk counts disagree with the eighteenth unit')

    # (d) Q1(a) under one observation: V1_cl empty iff r in D1_psi^inf (256-vertex graphs).
    psi = 232
    got = sorted(r for r in range(256) if pair_facts(psi, r, 1)['all_ring'])
    print(f'Q1(a) psi=232 depth one: |{{V1_cl empty}}|={len(got)} recorded |D1^inf|={len(H["D1_inf"][psi])} '
          f'equal={got == H["D1_inf"][psi]}')
    if got != H['D1_inf'][psi]:
        problems.append(f'Q1(a) under 232 failed: {sorted(set(got) ^ set(H["D1_inf"][psi]))[:8]}')

    # (e) the ring-24 numeric control: the twelve rules under 22 must give m_min = 21 at depth two.
    wrong = []
    for r in RING_24_RULES_UNDER_22:
        f = pair_facts(22, r, 2)
        if f['m_min'] != RING_24_M_MIN: wrong.append([r, f['m_min']])
    print(f'Q1(c) ring-24 control under 22: m_min == {RING_24_M_MIN} for all twelve: {not wrong}')
    if wrong: problems.append(f'ring-24 control failed (rule, m_min): {wrong}')

    # (f) Corollary B on a recorded oscillating rule: rule 50 under 4 has p_r >= 2 and, with period
    #     >= 2 in every carrying component, no constant-diagonal anchor. A general diagonal anchor
    #     here is reported, not an error (protocol Section 5, B1).
    rec_p = recorded_rule_period(H, 4, 50)
    print(f'Corollary B (4, 50): p_r={f2["eventual_period"]} recorded={rec_p} '
          f'component periods={[c["period"] for c in f2["components"]]} '
          f'constant_diagonal_anchored={f2["constant_diagonal_anchored"]} '
          f'diagonal_anchored={f2["diagonal_anchored"]} (reported only)')
    if f2['eventual_period'] != rec_p: problems.append(f'(4, 50) period {f2["eventual_period"]} != recorded {rec_p}')
    if f2['eventual_period'] > 1 and f2['constant_diagonal_anchored']:
        problems.append('(4, 50) oscillates yet is constant-diagonal-anchored, contradicting Corollary B')

    print(f'self test {"PASS" if not problems else "FAIL"} in {time.time() - t0:.1f}s')
    for p in problems: print('   ', p)
    return 1 if problems else 0

# ---------------------------------------------------------------- probe (writes nothing)
def probe(psi, h, rules):
    H = read_history()
    rules = rules if rules else [r for r in range(256) if r not in set(H['FS3'][psi])][:4]
    for r in rules:
        f = pair_facts(psi, r, h)
        print(f'psi={psi} r={r:3d} h={h} |V|={f["violating_walks"]:6d} |V_cl|={f["closed_violating_walks"]:5d} '
              f'n_min={f["n_min"]} p_r={f["eventual_period"]} out={f["eventually_out"]} '
              f'L={f["residue_modulus"]} R={f["residues"][:6]} diag={f["diagonal_anchored"]} '
              f'const_diag={f["constant_diagonal_anchored"]} comps={[(c["size"], c["period"]) for c in f["components"]][:4]} '
              f'{f["seconds"]}s', flush=True)
    return 0

# ---------------------------------------------------------------- canonical run
def main(argv):
    if '--self-test' in argv: return self_test()
    if '--probe' in argv:
        psi = int(argv[argv.index('--probe') + 1])
        h = int(argv[argv.index('--depth') + 1]) if '--depth' in argv else 3
        rules = [int(x) for x in argv[argv.index('--rules') + 1].split(',')] if '--rules' in argv else None
        return probe(psi, h, rules)
    H = read_history(); t_start = time.time()
    P = {}

    # ---------------- depths one and two: all 2,048 pairs each (Q1(a)-(d))
    F1, F2 = {}, {}
    for psi in OBS:
        t0 = time.time()
        F1[psi] = {r: pair_facts(psi, r, 1) for r in range(256)}
        F2[psi] = {r: pair_facts(psi, r, 2) for r in range(256)}
        print(f'depths 1, 2 psi={psi} closed at h=1 {sum(1 for f in F1[psi].values() if not f["all_ring"])} '
              f'h=2 {sum(1 for f in F2[psi].values() if not f["all_ring"])} in {time.time() - t0:.1f}s', flush=True)

    q1a = {str(psi): sorted(set(r for r, f in F1[psi].items() if f['all_ring']) ^ set(H['D1_inf'][psi])) for psi in OBS}
    q1b_sets = {str(psi): sorted(set(r for r, f in F2[psi].items() if f['all_ring']) ^ set(H['D2_inf'][psi])) for psi in OBS}
    q1b_counts = {str(psi): [[r, F2[psi][r]['closed_violating_walks'], H['D2_cert'][psi]['closed_violating_walks'][str(r)]]
                             for r in range(256)
                             if F2[psi][r]['closed_violating_walks'] != H['D2_cert'][psi]['closed_violating_walks'][str(r)]]
                  for psi in OBS}
    q1c = {}
    for psi in OBS:
        bad = []
        for r in range(256):
            f = F2[psi][r]
            rec = recorded_least_failing_ring(H, psi, r)
            if f['all_ring']:
                if rec is not None: bad.append([r, None, rec])
            elif f['n_min'] != rec: bad.append([r, f['n_min'], rec])
        q1c[str(psi)] = bad
    q1c_ring24 = {str(r): F2[22][r]['m_min'] for r in RING_24_RULES_UNDER_22}
    q1c_ring24_pass = all(v == RING_24_M_MIN for v in q1c_ring24.values())
    q1d_periods, q1d_rules, q1d_ev = {}, {}, {}
    for psi in OBS:
        P_psi, ev = observation_eventual(F2[psi])
        q1d_periods[str(psi)] = P_psi
        q1d_rules[str(psi)] = [[r, F2[psi][r]['eventual_period'], recorded_rule_period(H, psi, r)]
                               for r in range(256) if F2[psi][r]['eventual_period'] != recorded_rule_period(H, psi, r)]
        sets, N, Pc = recorded_depth_two_sets(H, psi)
        q1d_ev[str(psi)] = [n for n in range(N, N + Pc) if ev[n % P_psi] != sets[n]]
    q1e = {}
    for psi in DEPTH_THREE_OBS:
        sample = sorted(H['FS3'][psi])[:CONTROL_SAMPLE]
        q1e[str(psi)] = {'sample': sample,
                         'with_closed_violation': [r for r in sample if not pair_facts(psi, r, 3)['all_ring']]}
        print(f'Q1(e) psi={psi} control sample {sample} failures '
              f'{q1e[str(psi)]["with_closed_violation"]}', flush=True)
    q1 = {'a_depth_one_symmetric_difference': q1a, 'b_depth_two_symmetric_difference': q1b_sets,
          'b_closed_count_mismatches': q1b_counts, 'c_n_min_mismatches': q1c,
          'c_ring_24_m_min_under_22': q1c_ring24, 'c_ring_24_expected': RING_24_M_MIN,
          'd_periods': q1d_periods, 'd_certified_periods': {str(k): v for k, v in P2_CERTIFIED.items()},
          'd_rule_period_mismatches': q1d_rules, 'd_eventual_set_mismatch_rings': q1d_ev,
          'e_control_sample': q1e}
    q1['pass'] = (all(not v for v in q1a.values()) and all(not v for v in q1b_sets.values())
                  and all(not v for v in q1b_counts.values()) and all(not v for v in q1c.values())
                  and q1c_ring24_pass and all(not v for v in q1d_rules.values())
                  and all(not v for v in q1d_ev.values())
                  and all(q1d_periods[str(psi)] == P2_CERTIFIED[psi] for psi in OBS)
                  and all(not v['with_closed_violation'] for v in q1e.values()))
    P['Q1_theorem_controls'] = q1
    if not q1['pass']:
        print('Q1 failed: Corollary A or the implementation is wrong; the protocol stops the unit here.', flush=True)

    # ---------------- depth three over the frozen domain
    dom = depth_three_domain(H)
    F3 = {}
    for psi in sorted(dom):
        t0 = time.time(); F3[psi] = {}
        for r in dom[psi]['deep']: F3[psi][r] = pair_facts(psi, r, 3)
        closed_n = sum(1 for f in F3[psi].values() if not f['all_ring'])
        print(f'depth three psi={psi} ({dom[psi]["role"]}) deep={len(dom[psi]["deep"])} '
              f'with closed violations={closed_n} in {time.time() - t0:.1f}s', flush=True)

    def D3_inf(psi):
        return sorted(set(H['FS3'][psi]) | {r for r, f in F3[psi].items() if f['all_ring']})
    def gap(psi): return [r for r in D3_inf(psi) if r not in set(H['FS3'][psi])]

    # ---------------- Q2
    q2 = {'all_ring_depth_three': {str(psi): D3_inf(psi) for psi in sorted(dom)},
          'all_ring_gap': {str(psi): gap(psi) for psi in sorted(dom)},
          'rings_3_to_14_gap': {str(psi): H['GAP3'][psi] for psi in sorted(dom)},
          'gap_subset_of_window': {str(psi): sorted(set(gap(psi)) - set(H['GAP3'][psi])) for psi in sorted(dom)},
          'window_overstates': {str(psi): sorted(set(H['GAP3'][psi]) - set(gap(psi))) for psi in sorted(dom)},
          'theorem_controls': {'102_empty': 'vacuous: FS3_102 is all 256 rules (fifteenth unit M4), so no rule lies outside it',
                              '150_empty': gap(150)},
          'witnesses_window_overstatement': {
              str(psi): {str(r): {'n_min': F3[psi][r]['n_min'], 'witness': F3[psi][r]['witness'],
                                  'witness_component': F3[psi][r].get('witness_component')}
                         for r in sorted(set(H['GAP3'][psi]) - set(gap(psi)))} for psi in sorted(dom)}}
    q2['bet_a_nonempty'] = {str(psi): bool(gap(psi)) for psi in (232, 4, 32, 200, 22, 90)}
    q2['bet_b_window_overstates_somewhere'] = [psi for psi in (232, 4, 32, 200, 22, 90)
                                               if set(gap(psi)) != set(H['GAP3'][psi])]
    q2['pass_theorem'] = not gap(150) and all(not v for v in q2['gap_subset_of_window'].values())
    q2['pass_a'] = all(q2['bet_a_nonempty'].values())
    q2['pass_b'] = bool(q2['bet_b_window_overstates_somewhere'])
    q2['pass_c'] = 22 in q2['bet_b_window_overstates_somewhere']
    q2['pass'] = q2['pass_theorem'] and q2['pass_a'] and q2['pass_b'] and q2['pass_c']
    P['Q2_all_ring_gap'] = q2

    # ---------------- Q3
    q3 = {}
    for psi in sorted(dom):
        out = {r: F3[psi][r] for r in dom[psi]['deep'] if not F3[psi][r]['all_ring']}
        control = []
        for r, f in out.items():
            n = f['n_min']
            if n <= 14:
                okn = r not in set(H['D3'][psi][n]) and all(r in set(H['D3'][psi][m]) for m in range(4, n))
            else:
                okn = all(r in set(H['D3'][psi][m]) for m in GRAPH_RINGS)
            if not okn: control.append([r, n])
        dist = {}
        for f in out.values(): dist[str(f['n_min'])] = dist.get(str(f['n_min']), 0) + 1
        q3[str(psi)] = {'n_min_by_rule': {str(r): f['n_min'] for r, f in sorted(out.items())},
                        'distribution': dist, 'max_n_min': max((f['n_min'] for f in out.values()), default=None),
                        'control_failures': control,
                        'exceeds_depth_two_record_24': [r for r, f in out.items() if f['n_min'] > 24]}
    q3['pass'] = all(not q3[str(psi)]['control_failures'] for psi in sorted(dom))
    P['Q3_first_failing_rings'] = q3

    # ---------------- Q4
    q4 = {}
    for psi in sorted(dom):
        P_psi, ev = observation_eventual(F3[psi])
        q4[str(psi)] = {'eventual_period_P': P_psi,
                        'rule_periods': {str(r): F3[psi][r]['eventual_period'] for r in dom[psi]['deep']},
                        'oscillating_rules': [r for r in dom[psi]['deep']
                                              if not F3[psi][r]['all_ring'] and not F3[psi][r]['eventually_out']],
                        'eventually_out_rules': [r for r in dom[psi]['deep'] if F3[psi][r]['eventually_out']],
                        'eventual_sets_over_the_deep_domain': {str(j): ev[j] for j in range(P_psi)},
                        'residue_sets': {str(r): {'modulus': F3[psi][r]['residue_modulus'],
                                                  'residues': F3[psi][r]['residues']}
                                         for r in dom[psi]['deep'] if F3[psi][r]['residues']}}
    q4['theorem_90_odd_residues_all_in'] = [j for j in range(q4['90']['eventual_period_P'])
                                            if j % 2 == 1 and q4['90']['eventual_sets_over_the_deep_domain'][str(j)]
                                            != sorted(dom[90]['deep'])]
    q4['theorem_150_off_multiples_of_three_all_in'] = [j for j in range(q4['150']['eventual_period_P'])
                                                       if j % 3 and q4['150']['eventual_sets_over_the_deep_domain'][str(j)]
                                                       != sorted(dom[150]['deep'])]
    q4['bets'] = {'P_232': q4['232']['eventual_period_P'], 'P_200': q4['200']['eventual_period_P'],
                  'P_4': q4['4']['eventual_period_P'], 'P_32': q4['32']['eventual_period_P'],
                  'P_22': q4['22']['eventual_period_P'], 'P_90': q4['90']['eventual_period_P'],
                  'P_150': q4['150']['eventual_period_P']}
    q4['pass_theorem'] = not q4['theorem_90_odd_residues_all_in'] and not q4['theorem_150_off_multiples_of_three_all_in']
    q4['pass_bets'] = (q4['bets']['P_232'] == 1 and q4['bets']['P_200'] == 1 and q4['bets']['P_4'] == 1
                       and q4['bets']['P_32'] == 1 and q4['bets']['P_22'] % 3 == 0
                       and q4['bets']['P_90'] == 4 and q4['bets']['P_150'] == 6)
    q4['pass'] = q4['pass_theorem'] and q4['pass_bets']
    P['Q4_eventual_periods'] = q4

    # ---------------- Q5
    q5 = {}
    for psi in sorted(dom):
        detail = {}
        for r in dom[psi]['deep']:
            f = F3[psi][r]
            if f['all_ring']: continue
            detail[str(r)] = {'components': f['components'], 'carrying_components': len(f['components']),
                              'diagonal_anchored': f['diagonal_anchored'],
                              'constant_diagonal_anchored': f['constant_diagonal_anchored'],
                              'eventually_out': f['eventually_out'], 'eventual_period': f['eventual_period']}
        q5[str(psi)] = {'detail': detail,
                        'oscillating_but_constant_diagonal_anchored':
                            [int(r) for r, d in detail.items() if not d['eventually_out'] and d['constant_diagonal_anchored']],
                        'oscillating_and_generally_diagonal_anchored':      # reported, not an error (B1)
                            [int(r) for r, d in detail.items() if not d['eventually_out'] and d['diagonal_anchored']],
                        'eventually_out_without_diagonal_anchor':
                            [int(r) for r, d in detail.items() if d['eventually_out'] and not d['diagonal_anchored']]}
    q5['pass_theorem'] = all(not q5[str(psi)]['oscillating_but_constant_diagonal_anchored'] for psi in sorted(dom))
    q5['pass_bet'] = all(not q5[str(psi)]['eventually_out_without_diagonal_anchor'] for psi in (232, 200, 22))
    q5['pass'] = q5['pass_theorem'] and q5['pass_bet']
    P['Q5_closed_violation_structure'] = q5

    # ---------------- Q6
    q6 = {'statistic_transport_complement': {}, 'statistic_transport_reflection': {}, 'graph_correspondence': [],
          'set_transport': {}}
    for psi in DEPTH_THREE_OBS:
        q = conj(psi)
        mism = [r for r in dom[psi]['deep']
                if conj(r) in F3.get(q, {}) and stat_key(F3[psi][r]) != stat_key(F3[q][conj(r)])]
        q6['statistic_transport_complement'][str(psi)] = {'conjugate_observation': q, 'mismatches': mism,
                                                          'compared': sum(1 for r in dom[psi]['deep'] if conj(r) in F3.get(q, {}))}
        if mirror(psi) == psi:
            mm = [r for r in dom[psi]['deep']
                  if mirror(r) in F3[psi] and stat_key(F3[psi][r], negate_residues=True) != stat_key(F3[psi][mirror(r)])]
            q6['statistic_transport_reflection'][str(psi)] = {'within_observation': True, 'mismatches': mm,
                                                              'compared': sum(1 for r in dom[psi]['deep'] if mirror(r) in F3[psi])}
        else:
            q6['statistic_transport_reflection'][str(psi)] = {'within_observation': False, 'mismatches': [], 'compared': 0}
        q6['set_transport'][str(psi)] = {
            'conjugate_observation': q,
            'D3_inf_transported': (sorted(D3_inf(q)) == transport(D3_inf(psi))) if q in F3 else None,
            'gap_transported': (sorted(gap(q)) == transport(gap(psi))) if q in F3 else None,
            'P_equal': (q4[str(q)]['eventual_period_P'] == q4[str(psi)]['eventual_period_P']) if q in F3 else None}
    for psi in DEPTH_THREE_OBS:
        for r in dom[psi]['deep'][:GRAPH_CORR_SAMPLE]:
            q6['graph_correspondence'].append(graph_correspondence(psi, r, 3))
    q6['deduction_32_checked_directly'] = {'D3_32_inf': D3_inf(32), 'transport_of_D3_4_inf': transport(D3_inf(4)),
                                           'equal': sorted(D3_inf(32)) == transport(D3_inf(4))}
    q6['pass'] = (all(not v['mismatches'] for v in q6['statistic_transport_complement'].values())
                  and all(not v['mismatches'] for v in q6['statistic_transport_reflection'].values())
                  and all(x['pass'] for x in q6['graph_correspondence'])
                  and all(v['D3_inf_transported'] is not False and v['gap_transported'] is not False
                          and v['P_equal'] is not False for v in q6['set_transport'].values())
                  and q6['deduction_32_checked_directly']['equal'])
    P['Q6_symmetries'] = q6

    report = {'protocol': 'closed-violation-depth-three-20260913', 'schema': 1,
              'observations': list(OBS), 'depth_three_observations': list(DEPTH_THREE_OBS),
              'rings_from_sixteenth_seventeenth_units': list(RINGS),
              'parameters': {'depths': [1, 2, 3], 'vertices_by_depth': {str(h): vertices(h) for h in (1, 2, 3)},
                             'control_sample_per_observation': CONTROL_SAMPLE,
                             'graph_correspondence_sample_per_observation': GRAPH_CORR_SAMPLE,
                             'girth_cap_for_coincident_ends': GIRTH_CAP,
                             'matrix_powers_taken': 0,
                             'depth_three_domain': {str(psi): {'role': dom[psi]['role'], 'deep_rules': len(dom[psi]['deep']),
                                                               'control_rules': len(dom[psi]['control'])}
                                                    for psi in sorted(dom)}},
              'source_hashes': {'script': sha(pathlib.Path(__file__)),
                                'full_shift_depth_three_script': sha(SIXTEENTH_SCRIPT),
                                'depth_one_certificate_script': sha(FOURTEENTH_SCRIPT),
                                'depth_one_certificate_result': sha(DEPTH_ONE),
                                'depth_two_certificate_result': sha(DEPTH_TWO_CERT),
                                'full_shift_depth_two_result': sha(FULL_SHIFT_TWO),
                                'full_shift_depth_three_result': sha(FULL_SHIFT_THREE),
                                'full_shift_depth_three_linear_result': sha(FULL_SHIFT_THREE_LINEAR)},
              'historical_reads': {'FS3_32': 'the sixteenth unit\'s deduction F_32 = F_4 o not: every set under 32 equals the set under 223',
                                   'FS3_251': '{conj r : r in FS3_32}',
                                   'FS3_102': 'all 256 rules by the fifteenth unit\'s M4'},
              'pair_facts_depth_three': {str(psi): {str(r): {k: v for k, v in F3[psi][r].items() if not k.startswith('_')}
                                                    for r in dom[psi]['deep']} for psi in sorted(dom)},
              'closed_violation_counts_depth_one': {str(psi): {str(r): F1[psi][r]['closed_violating_walks'] for r in range(256)}
                                                    for psi in OBS},
              'closed_violation_counts_depth_two': {str(psi): {str(r): F2[psi][r]['closed_violating_walks'] for r in range(256)}
                                                    for psi in OBS},
              'all_ring_depth_three': {str(psi): D3_inf(psi) for psi in sorted(dom)},
              'elapsed_seconds': round(time.time() - t_start, 1),
              'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    print(json.dumps(report['summary']))
    print('all-ring gaps', {psi: gap(psi) for psi in DEPTH_THREE_OBS})
    print('periods', q4['bets'])
    print('max n_min', {psi: q3[str(psi)]['max_n_min'] for psi in DEPTH_THREE_OBS})
    print('written', OUT.relative_to(ROOT), f'in {report["elapsed_seconds"]}s')
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
