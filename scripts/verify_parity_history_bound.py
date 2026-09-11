#!/usr/bin/env python3
"""Parity history-bound certificate (protocol frozen 2026-09-11; run authorized by
Myk 2026-09-11 with no other-model review at freeze; see the protocol header).

Objects (fifth-unit definitions): g_r(l,m,r) = r(l,m,r) xor r(~l,~m,~r);
A_1 = g_r^{-1}(1); W_1 = states with g_r(X) == 1 everywhere; L = W_1 & F^{-1}(W_1).

D1  every L-admissible 8-word (all 3-windows in A_1, all 3-windows of its F-image
    in A_1) has equal adjacent g_r(F^2 .) values; by the frozen lemma this proves
    h_* <= 2 on every ring. Violations are listed with whether the word lies on a
    cycle of L's de Bruijn graph (nodes 4-words, edges admissible 5-words).
D2  h_* >= 2 on some ring iff a W_1-admissible 6-word with unequal adjacent
    g_r(F .) values lies on a cycle of W_1's graph (nodes 2-words, edges A_1).
    Predicted depth-2 set: {22, 73, 104, 109, 146, 151, 182, 233}; the smallest
    ring realizing depth 2 is reported (4 + shortest return path).
D3  fifth-unit refinement() (imported, code unchanged) at n in {7, 9, 11, 14}.
D4  h_* invariant under complement conjugation and reflection.
"""
from __future__ import annotations
import hashlib, importlib.util, json, pathlib, sys
from collections import deque
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
PRIOR = ROOT / 'results/parity_coarse_graining_20260911.json'
OUT = ROOT / 'results/parity_history_bound_20260911.json'
D3_RINGS = (7, 9, 11, 14)
PREDICTED_DEPTH2 = [22, 73, 104, 109, 146, 151, 182, 233]
spec = importlib.util.spec_from_file_location('parity', ROOT / 'scripts/verify_parity_coarse_graining.py')
parity = importlib.util.module_from_spec(spec); spec.loader.exec_module(parity)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def lut(r): return [(r >> i) & 1 for i in range(8)]
def g_table(r): t = lut(r); return [t[i] ^ t[7 - i] for i in range(8)]
def conj(r): return sum((((r >> (7 - i)) & 1) ^ 1) << i for i in range(8))
def mirror(r): return sum(((r >> (((i & 4) >> 2) | (i & 2) | ((i & 1) << 2))) & 1) << i for i in range(8))
def bits(w, m): return [(w >> (m - 1 - k)) & 1 for k in range(m)]
def F_word(x, t): return [t[4 * x[i - 1] + 2 * x[i] + x[i + 1]] for i in range(1, len(x) - 1)]      # open word, length - 2
def g_word(x, g): return F_word(x, g)                                                               # g applied to 3-windows

def sccs(nodes, edges):
    """Tarjan; returns dict node -> component id."""
    index = {}; low = {}; stack = []; on = set(); comp = {}; counter = [0]; cid = [0]
    sys.setrecursionlimit(10000)
    def visit(v):
        index[v] = low[v] = counter[0]; counter[0] += 1; stack.append(v); on.add(v)
        for w in edges.get(v, ()):
            if w not in index: visit(w); low[v] = min(low[v], low[w])
            elif w in on: low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            while True:
                w = stack.pop(); on.discard(w); comp[w] = cid[0]
                if w == v: break
            cid[0] += 1
    for v in nodes:
        if v not in index: visit(v)
    return comp

def path_on_cycle(path_nodes, edges, comp):
    """A path lies on a cycle iff all its nodes are in one SCC and that SCC has a cycle (size > 1 or a self-loop)."""
    cs = {comp[v] for v in path_nodes}
    if len(cs) != 1: return False
    v0 = path_nodes[0]; members = [v for v in comp if comp[v] == comp[v0]]
    return len(members) > 1 or v0 in edges.get(v0, ())

def shortest_return(src, dst, edges):
    if src == dst: return 0
    dist = {src: 0}; q = deque([src])
    while q:
        v = q.popleft()
        for w in edges.get(v, ()):
            if w not in dist:
                dist[w] = dist[v] + 1
                if w == dst: return dist[w]
                q.append(w)
    return None

def certificate(r):
    t = lut(r); g = g_table(r); A1 = {c for c in range(8) if g[c] == 1}
    def w1_ok(x): return all((4 * x[i - 1] + 2 * x[i] + x[i + 1]) in A1 for i in range(1, len(x) - 1))
    def L_ok(x): return w1_ok(x) and w1_ok(F_word(x, t))
    # L graph: nodes 4-words, edges admissible 5-words
    L_nodes = set(); L_edges = {}
    for w in range(32):
        x = bits(w, 5)
        if L_ok(x):
            a = tuple(x[:4]); b = tuple(x[1:]); L_nodes.add(a); L_nodes.add(b); L_edges.setdefault(a, set()).add(b)
    L_comp = sccs(L_nodes, L_edges)
    d1_viol = []; admissible = 0
    for w in range(256):
        x = bits(w, 8)
        if not L_ok(x): continue
        admissible += 1
        v = g_word(F_word(F_word(x, t), t), g)           # two values, positions 3 and 4
        if v[0] != v[1]:
            nodes = [tuple(x[i:i + 4]) for i in range(5)]
            d1_viol.append({'word': ''.join(map(str, x)), 'on_L_cycle': path_on_cycle(nodes, L_edges, L_comp)})
    # W1 graph: nodes 2-words, edges A_1 3-words
    W_nodes = set(); W_edges = {}
    for c in A1:
        x = bits(c, 3); a = tuple(x[:2]); b = tuple(x[1:]); W_nodes.add(a); W_nodes.add(b); W_edges.setdefault(a, set()).add(b)
    W_comp = sccs(W_nodes, W_edges)
    d2_words = []; min_ring = None
    for w in range(64):
        x = bits(w, 6)
        if not w1_ok(x): continue
        v = g_word(F_word(x, t), g)                       # two values
        if v[0] != v[1]:
            nodes = [tuple(x[i:i + 2]) for i in range(5)]
            on = path_on_cycle(nodes, W_edges, W_comp)
            rec = {'word': ''.join(map(str, x)), 'on_W1_cycle': on}
            if on:
                d = shortest_return(nodes[-1], nodes[0], W_edges); rec['ring'] = 4 + d
                min_ring = rec['ring'] if min_ring is None else min(min_ring, rec['ring'])
            d2_words.append(rec)
    return {'admissible_8_words': admissible, 'd1_violations': d1_viol,
            'd1_all_admissible_pass': not d1_viol, 'd1_no_cycle_embedded_violation': not any(v['on_L_cycle'] for v in d1_viol),
            'd2_violating_6_words': d2_words, 'depth2_on_some_ring': any(v['on_W1_cycle'] for v in d2_words), 'smallest_depth2_ring': min_ring}

def main():
    prior = json.loads(PRIOR.read_text())
    closed = prior['predictions']['C1_closure_classification']['by_ring']['8']['closed']
    nonclosed = [r for r in range(256) if r not in closed]
    report = {'protocol': 'parity-history-bound-20260911', 'schema': 1,
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'parity_coarse_graining_script': sha(ROOT / 'scripts/verify_parity_coarse_graining.py'), 'parity_coarse_graining_result': sha(PRIOR)},
              'closed_rules': closed}
    P = {}
    cert = {str(r): certificate(r) for r in range(256)}
    # D1
    d1 = {'per_rule': {str(r): {k: cert[str(r)][k] for k in ('admissible_8_words', 'd1_violations', 'd1_all_admissible_pass', 'd1_no_cycle_embedded_violation')} for r in nonclosed},
          'rules_failing_literal': [r for r in nonclosed if not cert[str(r)]['d1_all_admissible_pass']],
          'rules_with_cycle_embedded_violation': [r for r in nonclosed if not cert[str(r)]['d1_no_cycle_embedded_violation']],
          'closed_rules_also_pass': all(cert[str(r)]['d1_all_admissible_pass'] for r in closed)}
    d1['pass'] = not d1['rules_failing_literal']
    d1['bound_certified_all_rings'] = not d1['rules_with_cycle_embedded_violation']
    P['D1_certificate'] = d1
    # D2
    depth2 = sorted(r for r in nonclosed if cert[str(r)]['depth2_on_some_ring'])
    d2 = {'depth2_rules': depth2, 'predicted': PREDICTED_DEPTH2, 'equals_predicted': depth2 == PREDICTED_DEPTH2,
          'smallest_depth2_ring': {str(r): cert[str(r)]['smallest_depth2_ring'] for r in depth2},
          'depth1_rules_count': len(nonclosed) - len(depth2),
          'closed_rules_have_no_depth2': not any(cert[str(r)]['depth2_on_some_ring'] for r in closed),
          'certified_depth': {str(r): (0 if r in closed else 2 if r in depth2 else 1) for r in range(256)}}
    d2['pass'] = d2['equals_predicted'] and d2['closed_rules_have_no_depth2']
    P['D2_exact_depth'] = d2
    # D3
    d3 = {'by_ring': {}}
    for n in D3_RINGS:
        hs = {str(r): parity.refinement(r, n)['h_star'] for r in range(256)}
        mism = [r for r in range(256) if hs[str(r)] != d2['certified_depth'][str(r)]]
        d3['by_ring'][str(n)] = {'h_star': hs, 'mismatches_with_certified': mism,
                                 'histogram': {str(k): sum(1 for v in hs.values() if v == k) for k in sorted(set(hs.values()))}}
    d3['pass'] = all(not v['mismatches_with_certified'] for v in d3['by_ring'].values())
    P['D3_exhaustive_unvisited_rings'] = d3
    # D4
    cd = d2['certified_depth']
    d4 = {'certified_depth_invariant_conj': all(cd[str(r)] == cd[str(conj(r))] for r in range(256)),
          'certified_depth_invariant_mirror': all(cd[str(r)] == cd[str(mirror(r))] for r in range(256)),
          'd3_invariant_conj': all(v['h_star'][str(r)] == v['h_star'][str(conj(r))] for v in d3['by_ring'].values() for r in range(256)),
          'd3_invariant_mirror': all(v['h_star'][str(r)] == v['h_star'][str(mirror(r))] for v in d3['by_ring'].values() for r in range(256)),
          'depth2_conj_pairs': sorted({tuple(sorted((r, conj(r)))) for r in depth2}), 'depth2_mirror_symmetric': all(mirror(r) == r for r in depth2)}
    d4['pass'] = all(d4[k] for k in ('certified_depth_invariant_conj', 'certified_depth_invariant_mirror', 'd3_invariant_conj', 'd3_invariant_mirror'))
    P['D4_symmetry'] = d4
    report['predictions'] = P
    report['summary'] = {k: v['pass'] for k, v in P.items()}
    report['summary']['D1_bound_certified_all_rings'] = d1['bound_certified_all_rings']
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=parity.jsonable) + '\n')
    print(json.dumps(report['summary'])); print('depth2:', depth2, 'min rings:', d2['smallest_depth2_ring'])
    print('D1 literal failures:', d1['rules_failing_literal'], 'cycle-embedded:', d1['rules_with_cycle_embedded_violation'])
    print('D3 histograms:', {n: v['histogram'] for n, v in d3['by_ring'].items()}); print('written', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main()
