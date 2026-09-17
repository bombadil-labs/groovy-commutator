#!/usr/bin/env python3
"""First-floor forced tables for all 256 ECAs, full input (protocol 2026-09-17-forced-tables.md).

Computes, for every ECA, the ring-free forced table of the affine-oriented
first lift (35-bit window -> output, source bit, phase), its completion-
independent invariants, the pairwise cohabitation matrix and family structure,
the join to the pair-divergence regimes of the full sweep, and an eight-rule
D3 panel. Writes results/forced_tables_20260917/ and scores the frozen
predictions P1-P4 into summary.json (with source_hashes).

    python scripts/forced_tables_20260917.py            # ~ minutes, off Actions
    python scripts/forced_tables_20260917.py --skip-d3  # debug only
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/forced_tables_20260917'
PROTOCOL = ROOT / 'docs/research/protocols/2026-09-17-forced-tables.md'
SWEEP = ROOT / 'results/sweep_full_classified.parquet'
LABELS = ROOT / 'experiments/on_beam_256_4d_20260914/labels.json'
D3_PANEL = [0, 4, 30, 54, 90, 106, 110, 184]
AFFINE = [0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195, 204, 240, 255]
ZERO_G = [0, 4, 60, 90, 102, 150, 170, 200, 204, 240]
ONE_G = [15, 51, 85, 105, 153, 165, 195, 255]

# ----------------------------------------------------------------------------- ECA and lift, batched over words

def eca_step(X, rule):
    l = np.roll(X, 1, axis=-1); r = np.roll(X, -1, axis=-1)
    return ((rule >> (4 * l + 2 * X + r)) & 1).astype(np.uint8)

def words(n):
    w = np.arange(1 << n, dtype=np.int64)
    return ((w[:, None] >> np.arange(n)) & 1).astype(np.uint8)

def lift1(X, rule):
    """Batched first lift, phase 0: (W, n) -> (W, 6, n). tau_v X(p) = X(p+v); v+ = +1, v- = -1."""
    Y = eca_step(X, rule); Z = eca_step(Y, rule)
    F = [X ^ np.roll(X, -1, axis=-1), 1 ^ X ^ np.roll(X, 1, axis=-1), X ^ Y, X ^ Z, np.zeros_like(X), X]
    return np.stack(F, axis=1)

def mirror(r):
    f = [(r >> i) & 1 for i in range(8)]; out = 0
    for i in range(8):
        l, m, rr = (i >> 2) & 1, (i >> 1) & 1, i & 1
        out |= f[4 * rr + 2 * m + l] << i
    return out

def conj(r):
    f = [(r >> i) & 1 for i in range(8)]; return sum((1 - f[7 - i]) << i for i in range(8))

# ----------------------------------------------------------------------------- D2 forced tables

def d2_table(rule):
    """Keys (uint64, 35 bits, row-major rows -3..3 x positions -2..2), outputs, source bits, phases."""
    X = words(9)                                  # (512, 9)
    C = lift1(X, rule)                            # (512, 6, 9)
    Cn = lift1(eca_step(X, rule), rule)
    keys = []; outs = []; xs = []; phases = []
    for r0 in range(6):
        rows = [(r0 + k) % 6 for k in range(-3, 4)]
        pos = [(0 + i) % 9 for i in range(-2, 3)]
        win = C[:, rows][:, :, pos]               # (512, 7, 5)
        bits = win.reshape(512, 35)
        k = np.zeros(512, dtype=np.uint64)
        for j in range(35):
            k |= bits[:, j].astype(np.uint64) << np.uint64(34 - j)
        keys.append(k); outs.append(Cn[:, r0, 0]); xs.append(X[:, 0]); phases.append(np.full(512, r0, dtype=np.uint8))
    keys = np.concatenate(keys); outs = np.concatenate(outs); xs = np.concatenate(xs); phases = np.concatenate(phases)
    order = np.argsort(keys, kind='stable'); keys, outs, xs, phases = keys[order], outs[order], xs[order], phases[order]
    uk, first, inv = np.unique(keys, return_index=True, return_inverse=True)
    inv = inv.reshape(-1)
    collisions = int(np.sum((outs != outs[first][inv]) | (xs != xs[first][inv]) | (phases != phases[first][inv])))
    return {'keys': uk, 'out': outs[first], 'x': xs[first], 'phase': phases[first], 'collisions': collisions}

# ----------------------------------------------------------------------------- GF(2) linear algebra on int rows

def gf2_rank(rows):
    """Rank of a set of GF(2) vectors given as Python ints."""
    basis = []  # list of (pivot_bit, vector) kept reduced
    piv = {}
    for v in rows:
        while v:
            h = v.bit_length() - 1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; break
    return len(piv)

def monomial_index(nvars, maxdeg):
    idx = {}; n = 0
    for d in range(maxdeg + 1):
        for comb in itertools.combinations(range(nvars), d):
            idx[comb] = n; n += 1
    return idx, n

MON2, N2 = monomial_index(35, 2)
MON3, N3 = monomial_index(35, 3)

def monomial_rows(keys, maxdeg):
    idx = MON3 if maxdeg == 3 else MON2
    rows = []
    for k in keys:
        k = int(k); ones = [j for j in range(35) if (k >> (34 - j)) & 1]
        v = 1 << idx[()]
        for d in range(1, maxdeg + 1):
            for comb in itertools.combinations(ones, d):
                v |= 1 << idx[comb]
        rows.append(v)
    return rows

def anf_degree(keys, y, maxdeg=3):
    """Minimal degree d <= maxdeg with y in the span of degree-<=d monomials on keys; None if none."""
    for d in range(maxdeg + 1):
        rows = monomial_rows(keys, 3 if d == 3 else 2)
        N = N3 if d == 3 else N2
        idx = MON3 if d == 3 else MON2
        if d < 2 or (d == 2 and False):
            # restrict to monomials of degree <= d by masking columns
            keep = 0
            for comb, j in idx.items():
                if len(comb) <= d: keep |= 1 << j
            rows = [r & keep for r in rows]
        r0 = gf2_rank(rows)
        r1 = gf2_rank([r | (int(b) << N) for r, b in zip(rows, y)])
        if r1 == r0: return d
    return None

def invariants(rule, T):
    keys = T['keys']; phases = T['phase']
    out = {'rule': rule, 'size': int(len(keys)), 'collisions': T['collisions'],
           'sheet_sizes': [int(np.sum(phases == p)) for p in range(6)],
           'completion_exponent': f'2^35 - {len(keys)}'}
    k0 = int(keys[0])
    out['hull_dim'] = gf2_rank([int(k) ^ k0 for k in keys])
    sheets = []
    for p in range(6):
        ks = keys[phases == p]
        kk0 = int(ks[0])
        sheets.append({'hull_dim': gf2_rank([int(k) ^ kk0 for k in ks]),
                       'h2': gf2_rank(monomial_rows(ks, 2)), 'h3': gf2_rank(monomial_rows(ks, 3))})
    out['sheets'] = sheets
    out['sheet_invariants_phase_independent'] = len({(s['hull_dim'], s['h2'], s['h3']) for s in sheets}) == 1
    out['h2'] = sheets[0]['h2']; out['h3'] = sheets[0]['h3']
    out['output_degree'] = anf_degree(keys, T['out'])
    out['recovery_degree'] = anf_degree(keys, T['x'])
    pd_ = [anf_degree(keys, (phases >> b) & 1) for b in range(3)]
    out['phase_decoder_degree'] = None if any(d is None for d in pd_) else max(pd_)
    out['phase_decoder_bit_degrees'] = pd_
    return out

# ----------------------------------------------------------------------------- pairwise

def pairwise(tables):
    n = 256
    shared = np.zeros((n, n), dtype=np.int32); conflict = np.zeros((n, n), dtype=np.int32); added = np.zeros((n, n), dtype=np.int32)
    for r in range(n):
        kr, orr = tables[r]['keys'], tables[r]['out']
        for s in range(r + 1, n):
            ks, os_ = tables[s]['keys'], tables[s]['out']
            common, ir, is_ = np.intersect1d(kr, ks, assume_unique=True, return_indices=True)
            shared[r, s] = shared[s, r] = len(common)
            c = int(np.sum(orr[ir] != os_[is_])); conflict[r, s] = conflict[s, r] = c
            added[r, s] = len(ks) - len(common); added[s, r] = len(kr) - len(common)
    return shared, conflict, added

def bron_kerbosch(adj, cap_seconds):
    """Maximal cliques with pivoting; adj: dict node -> set. Keeps only the count and the
    largest clique (storing every clique exhausted memory on the first run). Returns
    (count, largest, censored)."""
    t0 = time.time(); state = {'count': 0, 'largest': [], 'censored': False}
    def bk(R, P, X):
        if state['censored']: return
        if time.time() - t0 > cap_seconds: state['censored'] = True; return
        if not P and not X:
            state['count'] += 1
            if len(R) > len(state['largest']): state['largest'] = sorted(R)
            return
        u = max(P | X, key=lambda v: len(adj[v] & P))
        for v in list(P - adj[u]):
            bk(R | {v}, P & adj[v], X & adj[v]); P = P - {v}; X = X | {v}
            if state['censored']: return
    bk(set(), set(adj), set())
    return state['count'], state['largest'], state['censored']

def greedy_clique(adj):
    best = []
    for start in adj:
        c = [start]; cand = set(adj[start])
        while cand:
            v = max(cand, key=lambda x: len(adj[x] & cand)); c.append(v); cand &= adj[v]
        if len(c) > len(best): best = c
    return sorted(best)

def components(adj):
    seen = set(); comps = []
    for v in adj:
        if v in seen: continue
        stack = [v]; comp = []
        while stack:
            x = stack.pop()
            if x in seen: continue
            seen.add(x); comp.append(x); stack.extend(adj[x] - seen)
        comps.append(sorted(comp))
    return comps

# ----------------------------------------------------------------------------- statistics

def chi2_sf(x, df):
    a = df / 2.0; z = x / 2.0
    if z <= 0: return 1.0
    if z < a + 1:
        s = t = 1.0 / a; n = 1
        while abs(t) > 1e-16 * abs(s) and n < 10000: t *= z / (a + n); s += t; n += 1
        return 1.0 - s * math.exp(-z + a * math.log(z) - math.lgamma(a))
    b = z + 1 - a; c = 1e300; d = 1 / b; h = d
    for i in range(1, 10000):
        an = -i * (i - a); b += 2; d = an * d + b; d = 1e-300 if d == 0 else d
        c = b + an / c; c = 1e-300 if c == 0 else c; d = 1 / d; delta = d * c; h *= delta
        if abs(delta - 1) < 1e-16: break
    return math.exp(-z + a * math.log(z) - math.lgamma(a)) * h

def kruskal(groups):
    allv = np.concatenate(groups); n = len(allv)
    order = np.argsort(allv, kind='mergesort'); ranks = np.empty(n); ranks[order] = np.arange(1, n + 1)
    vals = allv[order]; i = 0
    while i < n:
        j = i
        while j + 1 < n and vals[j + 1] == vals[i]: j += 1
        if j > i: ranks[order[i:j + 1]] = (i + j + 2) / 2
        i = j + 1
    h = 0.0; s = 0
    for g in groups: r = ranks[s:s + len(g)]; s += len(g); h += r.sum() ** 2 / len(g)
    h = 12 / (n * (n + 1)) * h - 3 * (n + 1)
    _, counts = np.unique(allv, return_counts=True); c = 1 - np.sum(counts ** 3 - counts) / (n ** 3 - n)
    h = h / c if c > 0 else h
    return float(h), chi2_sf(h, len(groups) - 1)

def auc(pos, neg):
    """AUC of score for positives over negatives (ties count half)."""
    pos = np.asarray(pos, float); neg = np.asarray(neg, float)
    allv = np.concatenate([pos, neg]); order = np.argsort(allv, kind='mergesort'); ranks = np.empty(len(allv)); ranks[order] = np.arange(1, len(allv) + 1)
    vals = allv[order]; i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and vals[j + 1] == vals[i]: j += 1
        if j > i: ranks[order[i:j + 1]] = (i + j + 2) / 2
        i = j + 1
    rp = ranks[:len(pos)].sum()
    return float((rp - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))

# ----------------------------------------------------------------------------- D3 panel

def d3_table(rule):
    """Full-input second-floor forced table on ring 15: keys as 31-byte rows (245 bits), outputs."""
    n = 15
    X = words(n)                                            # (W, 15)
    Xs = [X]
    for _ in range(3): Xs.append(eca_step(Xs[-1], rule))
    L = [lift1(Y, rule) for Y in Xs]                        # each (W, 6, 15): D2 beams of X, HX, H2X, H3X
    X1, X1n, X1nn, X1nnn = L
    def sh(A, da1, dx): return np.roll(np.roll(A, -da1, axis=1), -dx, axis=2)   # tau_(a1,x)
    F = [X1 ^ sh(X1, 1, 1), 1 ^ X1 ^ sh(X1, 1, -1), X1 ^ X1n, X1 ^ X1nn, np.zeros_like(X1), X1]
    Fn = [X1n ^ sh(X1n, 1, 1), 1 ^ X1n ^ sh(X1n, 1, -1), X1n ^ X1nn, X1n ^ X1nnn, np.zeros_like(X1), X1n]
    child = np.stack(F, axis=1); child_next = np.stack(Fn, axis=1)     # (W, 6, 6, 15)
    keys = []; outs = []
    pos = [i % n for i in range(-2, 3)]
    for r2 in range(6):
        for r1 in range(6):
            rows2 = [(r2 + k) % 6 for k in range(-3, 4)]; rows1 = [(r1 + k) % 6 for k in range(-3, 4)]
            win = child[:, rows2][:, :, rows1][:, :, :, pos].reshape(len(X), 245)
            keys.append(np.packbits(win, axis=1)); outs.append(child_next[:, r2, r1, 0])
    K = np.concatenate(keys); O = np.concatenate(outs)
    Kv = np.ascontiguousarray(K).view(np.dtype((np.void, 31))).ravel()
    uk, first, inv = np.unique(Kv, return_index=True, return_inverse=True); inv = inv.reshape(-1)
    collisions = int(np.sum(O != O[first][inv]))
    return {'keys': uk, 'out': O[first], 'collisions': collisions, 'windows': int(len(K))}

# ----------------------------------------------------------------------------- main

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--skip-d3', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); t0 = time.time()
    tables = [d2_table(r) for r in range(256)]
    np.savez_compressed(OUT / 'tables_d2.npz', **{f'keys_{r}': tables[r]['keys'] for r in range(256)},
                        **{f'vals_{r}': (tables[r]['out'] | (tables[r]['x'] << 1) | (tables[r]['phase'] << 2)).astype(np.uint8) for r in range(256)})
    print('tables', f'{time.time()-t0:.0f}s', flush=True)
    inv = [invariants(r, tables[r]) for r in range(256)]
    (OUT / 'invariants.json').write_text(json.dumps(inv, indent=1) + '\n')
    print('invariants', f'{time.time()-t0:.0f}s', flush=True)
    shared, conflict, added = pairwise(tables)
    np.savez_compressed(OUT / 'pairs.npz', shared=shared, conflict=conflict, added=added)
    compat = (conflict == 0); np.fill_diagonal(compat, False)
    nonvac = compat & (shared > 0)
    print('pairs', f'{time.time()-t0:.0f}s', flush=True)

    # families
    adj_c = {v: {u for u in range(256) if compat[v, u]} for v in range(256)}
    adj_nv = {v: {u for u in range(256) if nonvac[v, u]} for v in range(256)}
    adj_conf = {v: {u for u in range(256) if conflict[v, u] > 0} for v in range(256)}
    labels = json.loads(LABELS.read_text())
    orbits = {}
    for r in range(256):
        o = frozenset({r, mirror(r), conj(r), mirror(conj(r))}); orbits[o] = min(o)
    orbit_sets = sorted({tuple(sorted(o)) for o in orbits}, key=lambda t: t[0])
    def is_clique(S, adj): return all(u in adj[v] for v in S for u in S if u != v)
    named = {'affine_16': AFFINE, 'zero_G_10': ZERO_G, 'one_G_8': ONE_G}
    named_checks = {k: {'compatible_clique': is_clique(v, adj_c), 'nonvacuous_clique': is_clique(v, adj_nv)} for k, v in named.items()}
    orbit_checks = {'orbits': len(orbit_sets),
                    'compatible_cliques': sum(is_clique(o, adj_c) for o in orbit_sets if len(o) > 1),
                    'nonvacuous_cliques': sum(is_clique(o, adj_nv) for o in orbit_sets if len(o) > 1),
                    'nontrivial_orbits': sum(1 for o in orbit_sets if len(o) > 1)}
    n_cliques, largest_clique, censored = bron_kerbosch(adj_nv, 300)
    families = {'compatible_edges': int(compat.sum() // 2), 'nonvacuous_edges': int(nonvac.sum() // 2),
                'conflict_edges': int((conflict > 0).sum() // 2),
                'conflict_components': [c for c in components(adj_conf)],
                'compatible_degree': compat.sum(axis=1).tolist(), 'nonvacuous_degree': nonvac.sum(axis=1).tolist(),
                'named_sets': named_checks, 'orbit_cliques': orbit_checks,
                'nonvacuous_greedy_clique': greedy_clique(adj_nv),
                'nonvacuous_maximal_cliques': {'censored': censored, 'count_found': n_cliques,
                                               'max_size_found': len(largest_clique), 'largest_found': largest_clique,
                                               'cap_seconds': 300}}
    (OUT / 'families.json').write_text(json.dumps(families, indent=1) + '\n')
    print('families', f'{time.time()-t0:.0f}s', 'censored' if censored else '', flush=True)

    # regime join
    import pandas as pd
    sw = pd.read_parquet(SWEEP)
    ra = sw['rule_a'].to_numpy(); rb = sw['rule_b'].to_numpy(); reg = sw['regime'].to_numpy()
    conf_pair = conflict[ra, rb]; shared_pair = shared[ra, rb]; nonvac_pair = nonvac[ra, rb]; compat_pair = compat[ra, rb]
    ham = np.array([bin(int(a) ^ int(b)).count('1') for a, b in zip(ra, rb)])
    regimes = ['commute', 'crystalline', 'structured', 'noisy', 'drain']
    per = {g: {'n': int((reg == g).sum()), 'nonvacuous_rate': float(nonvac_pair[reg == g].mean()), 'compatible_rate': float(compat_pair[reg == g].mean()),
               'conflict_median': float(np.median(conf_pair[reg == g])), 'conflict_mean': float(conf_pair[reg == g].mean()),
               'hamming_mean': float(ham[reg == g].mean())} for g in regimes}
    H, p = kruskal([conf_pair[reg == g] for g in regimes])
    is_c = reg == 'commute'
    auc_conf = auc(-conf_pair[is_c], -conf_pair[~is_c]); auc_ham = auc(-ham[is_c], -ham[~is_c])
    regime_join = {'per_regime': per, 'kruskal_conflict': [H, p], 'auc_commute_vs_rest': {'neg_conflict': auc_conf, 'neg_hamming': auc_ham}}
    (OUT / 'regime_join.json').write_text(json.dumps(regime_join, indent=1) + '\n')
    print('regime join', f'{time.time()-t0:.0f}s', flush=True)

    # D3 panel
    d3 = {}
    if not args.skip_d3:
        T3 = {}
        for r in D3_PANEL:
            import gc; gc.collect()
            T3[r] = d3_table(r); d3[str(r)] = {'size': int(len(T3[r]['keys'])), 'windows': T3[r]['windows'], 'collisions': T3[r]['collisions'],
                                              'sha256_keys': hashlib.sha256(T3[r]['keys'].tobytes()).hexdigest()}
            print('d3', r, d3[str(r)]['size'], f'{time.time()-t0:.0f}s', flush=True)
        pairs3 = {}
        for r, s in itertools.combinations(D3_PANEL, 2):
            common, ir, is_ = np.intersect1d(T3[r]['keys'], T3[s]['keys'], assume_unique=True, return_indices=True)
            c3 = int(np.sum(T3[r]['out'][ir] != T3[s]['out'][is_]))
            pairs3[f'{r}-{s}'] = {'d3_shared': int(len(common)), 'd3_conflict': c3, 'd3_compatible': c3 == 0, 'd3_nonvacuous': c3 == 0 and len(common) > 0,
                                  'd2_shared': int(shared[r, s]), 'd2_conflict': int(conflict[r, s]), 'd2_compatible': bool(compat[r, s]), 'd2_nonvacuous': bool(nonvac[r, s])}
        d3['pairs'] = pairs3
    (OUT / 'd3_panel.json').write_text(json.dumps(d3, indent=1) + '\n')

    # predictions
    deg = lambda key: {str(d): sum(1 for i in inv if i[key] == d) for d in (0, 1, 2, 3, None)}
    reps = {}
    for i in inv:
        o = orbits[frozenset({i['rule'], mirror(i['rule']), conj(i['rule']), mirror(conj(i['rule']))})]
        reps.setdefault(o, (i['h2'], i['h3'], int(nonvac[i['rule']].sum())))
    triple_values = len(set(reps.values()))
    P1 = {'all_sheets_equal': all(len(set(i['sheet_sizes'])) == 1 for i in inv), 'all_hull_30': all(i['hull_dim'] == 30 for i in inv),
          'sheet_invariants_phase_independent': all(i['sheet_invariants_phase_independent'] for i in inv),
          'output_degrees': deg('output_degree'), 'recovery_degrees': deg('recovery_degree'), 'phase_degrees': deg('phase_decoder_degree'),
          'compatible_pairs': families['compatible_edges'], 'nonvacuous_pairs': families['nonvacuous_edges'],
          '54_110': {'compatible': bool(compat[54, 110]), 'shared': int(shared[54, 110])}, '106_110': {'compatible': bool(compat[106, 110]), 'shared': int(shared[106, 110])},
          'triple_distinct_values_on_orbits': triple_values, 'collisions_total': sum(i['collisions'] for i in inv)}
    P1['held'] = (P1['all_sheets_equal'] and P1['all_hull_30'] and P1['sheet_invariants_phase_independent']
                  and P1['output_degrees'] == {'0': 0, '1': 4, '2': 51, '3': 201, 'None': 0}
                  and P1['recovery_degrees'] == {'0': 0, '1': 0, '2': 95, '3': 161, 'None': 0}
                  and P1['phase_degrees'] == {'0': 0, '1': 0, '2': 55, '3': 201, 'None': 0}
                  and P1['compatible_pairs'] == 30320 and P1['nonvacuous_pairs'] == 17926
                  and P1['54_110'] == {'compatible': True, 'shared': 36} and P1['106_110'] == {'compatible': False, 'shared': 564}
                  and triple_values == 88 and P1['collisions_total'] == 0)
    others = [g for g in regimes if g != 'commute']
    pooled_nv = float(nonvac_pair[~is_c].mean())
    P2 = {'a_commute_nonvacuous_rate': per['commute']['nonvacuous_rate'], 'a_others_pooled': pooled_nv, 'a_held': per['commute']['nonvacuous_rate'] > pooled_nv,
          'b_kruskal_p': p, 'b_commute_median_lowest': all(per['commute']['conflict_median'] <= per[g]['conflict_median'] for g in others) and any(per['commute']['conflict_median'] < per[g]['conflict_median'] for g in others),
          'b_held': p < 0.01 and all(per['commute']['conflict_median'] <= per[g]['conflict_median'] for g in others),
          'c_auc_conflict': auc_conf, 'c_auc_hamming': auc_ham, 'c_held': auc_conf - auc_ham >= 0.05}
    P2['held'] = P2['a_held'] and P2['b_held'] and P2['c_held']
    refl = all(compat[r, s] == compat[mirror(r), mirror(s)] and shared[r, s] == shared[mirror(r), mirror(s)] and conflict[r, s] == conflict[mirror(r), mirror(s)]
               for r in range(256) for s in range(r + 1, 256))
    compl = sum(1 for r in range(256) for s in range(r + 1, 256) if compat[r, s] != compat[conj(r), conj(s)])
    P3 = {'reflection_invariant': refl, 'affine_clique_compatible': named_checks['affine_16']['compatible_clique'],
          'affine_clique_nonvacuous': named_checks['affine_16']['nonvacuous_clique'], 'complement_compatibility_mismatches': compl,
          'held': refl and named_checks['affine_16']['compatible_clique']}
    if d3.get('pairs'):
        pp = d3['pairs'].values()
        P4 = {'d2_compatible_implies_d3': all(v['d3_compatible'] for v in pp if v['d2_compatible']),
              'nonvacuity_agrees': all(v['d3_nonvacuous'] == v['d2_nonvacuous'] for v in pp),
              'd2_incompatible_but_d3_compatible': [k for k, v in d3['pairs'].items() if (not v['d2_compatible']) and v['d3_compatible']]}
        P4['held'] = P4['d2_compatible_implies_d3'] and P4['nonvacuity_agrees']
    else:
        P4 = {'held': None, 'skipped': True}
    summary = {'protocol': 'forced-tables-20260917', 'rules': 256, 'predictions': {'P1': P1, 'P2': P2, 'P3': P3, 'P4': P4},
               'wall_seconds': round(time.time() - t0, 1),
               'source_hashes': {'script': sha(__file__), 'protocol': sha(PROTOCOL), 'sweep': sha(SWEEP), 'labels': sha(LABELS),
                                 'tables_d2': sha(OUT / 'tables_d2.npz'), 'invariants': sha(OUT / 'invariants.json'), 'pairs': sha(OUT / 'pairs.npz'),
                                 'families': sha(OUT / 'families.json'), 'regime_join': sha(OUT / 'regime_join.json'), 'd3_panel': sha(OUT / 'd3_panel.json')}}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=1, sort_keys=True) + '\n')
    print(json.dumps({k: v.get('held') for k, v in summary['predictions'].items()}, indent=1))
    print(json.dumps({'P1': {k: v for k, v in P1.items() if k != 'held'}, 'P2': P2, 'P3': P3}, indent=1, default=str)[:4000])

if __name__ == '__main__':
    main()
