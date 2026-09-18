#!/usr/bin/env python3
"""The dense defect algebra: 28 pair-constraints, stratified by popcount.

Frozen protocol: docs/research/protocols/2026-09-18-dense-defect-algebra.md
(committed before this implementation).

Every column of a height-two strip has both rows read one table entry each.
With Delta = s1 - s0 the difference of the rows' three-cell popcounts:
Delta = 0 reads exposed (base-owned), |Delta| = 1 reads lit, |Delta| >= 2
reads dark -- for BOTH rows at once. The 64 six-bit windows give 8 trivially
agreeing cases and 28 unordered pairs: 6 exposed, 15 lit, 7 dark. That
CHARACTERIZES the previous unit's 8/14/10 entry partition instead of
enumerating it.

The algebra below is derived here from the read-index definition, not copied
from the protocol, and asserted as control 1.

Controls 1-10 run BEFORE any tier and raise on failure. Measurement helpers
are COPIED from the previous unit with this protocol's seed function, never
imported: importing them would silently draw trajectory seeds from the other
protocol's namespace.

    python experiments/dense_defect_algebra_20260918/run.py --workers 4
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools, json, math, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('bm', ROOT / 'experiments/beam_mechanism_20260918/run.py')
bm = importlib.util.module_from_spec(spec); sys.modules['bm'] = bm; spec.loader.exec_module(bm)
hf, base, strip = bm.hf, bm.base, bm.strip
HandedRule, handed_step, embed, res1, eca_step = hf.HandedRule, hf.handed_step, hf.embed, hf.res1, bm.eca_step
EXPOSED, FREE = hf.EXPOSED, hf.FREE
POS = {e: i for i, e in enumerate(FREE)}

PROTOCOL = 'dense-defect-algebra-20260918'
OUT = ROOT / 'results/dense_defect_algebra_20260918'
BASES = [110, 54, 22, 5, 30, 90, 0, 204, 106, 232, 8, 18, 46, 33, 62, 29, 51, 37, 45, 27]
FROZEN_BASES = [0, 204, 232, 8]
ARMS = ['Upp', 'Uplus', 'Dplus', 'G', 'Gprime', 'K', 'random']
N_ARM = {'Upp': 64, 'Uplus': 16, 'Dplus': 16, 'G': 24, 'Gprime': 16, 'K': 24, 'random': 48}
TRANSVERSE_ARMS = ('random', 'Dplus')
DENSITY = 0.5
W = strip.WIDTH

def seed(*parts):
    h = hashlib.sha256('|'.join(map(str, (PROTOCOL,) + parts)).encode()).digest()
    return int.from_bytes(h[:8], 'little') & 0x7fff_ffff_ffff_ffff

def bits_of(u):
    return [(u >> i) & 1 for i in range(24)]

def u_of(table):
    """Recover the 24-bit completion from a full handed table. The previous
    unit's canonical rows record `table` and not `u`, so controls 6 and 9 have
    to invert the embedding rather than read a key that is not there."""
    return sum(((table >> e) & 1) << POS[e] for e in FREE)

# ------------------------------------------------- the algebra, derived here

def idx_of(own, other):
    L, C, R = own
    return 16*C + 8*L + R + 2*sum(other)

def derive_algebra():
    """Enumerate the 64 six-bit windows and stratify."""
    ES = set(EXPOSED)
    agreeing, pair_windows = 0, {}
    for w in itertools.product((0, 1), repeat=6):
        r0, r1 = w[:3], w[3:]
        i0, i1 = idx_of(r0, r1), idx_of(r1, r0)
        if i0 == i1:
            agreeing += 1
            continue
        pair_windows.setdefault(frozenset((i0, i1)), []).append((w, sum(r1) - sum(r0)))
    expo, lit, dark, mixed = [], [], [], []
    for p, ws in pair_windows.items():
        a, b = sorted(p)
        ds = {abs(d) for _, d in ws}
        if a in ES and b in ES: expo.append((a, b))
        elif a not in ES and b not in ES and ds == {1}: lit.append((a, b))
        elif a not in ES and b not in ES: dark.append((a, b))
        else: mixed.append((a, b))
    return {'agreeing': agreeing, 'pairs': len(pair_windows),
            'exposed': sorted(expo), 'lit': sorted(lit), 'dark': sorted(dark),
            'mixed': sorted(mixed), 'windows': pair_windows}

ALG = derive_algebra()
LIT_PAIRS, DARK_PAIRS, EXPO_PAIRS = ALG['lit'], ALG['dark'], ALG['exposed']

def gf2_rank(pairs):
    rows = []
    for a, b in pairs:
        rows.append((1 << POS[a]) | (1 << POS[b]))
    basis, r = [], 0
    for v in rows:
        for bv in basis: v = min(v, v ^ bv)
        if v: basis.append(v); basis.sort(reverse=True); r += 1
    return r

def components(pairs):
    parent = {e: e for e in FREE}
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    return sorted({find(e) for e in FREE}), find

UPP_COMPS, UPP_FIND = components(LIT_PAIRS + DARK_PAIRS)

def upp_completion(k):
    assign = {c: ((k >> i) & 1) for i, c in enumerate(UPP_COMPS)}
    u = 0
    for e in FREE:
        if assign[UPP_FIND(e)]: u |= 1 << POS[e]
    return u

# the previous unit's twelve, re-derived from the read-index definition
A_TAB = {(0,0):(1,2), (0,1):(19,20), (1,0):(11,12), (1,1):(29,30)}
B_TAB = {(0,0):(2,16), (0,1):(5,19), (1,0):(12,26), (1,1):(15,29)}
C_TAB = {(0,0):(2,8),  (0,1):(5,11), (1,0):(20,26), (1,1):(23,29)}
CONS12 = [A_TAB[k] for k in sorted(A_TAB)] + [B_TAB[k] for k in sorted(B_TAB)] + [C_TAB[k] for k in sorted(C_TAB)]

def viol_mask(us, pairs):
    us = np.asarray(us, dtype=np.uint32)
    out = np.zeros(len(us), dtype=np.uint32)
    for k, (a, b) in enumerate(pairs):
        out |= ((((us >> POS[a]) ^ (us >> POS[b])) & 1) << k).astype(np.uint32)
    return out

# ------------------------------------------------------ base bits beta/gamma

def eca_out(r, L, C, R): return (r >> (4*L + 2*C + R)) & 1
BETA  = [((1,0,0),(0,1,0)), ((0,0,1),(0,1,0)), ((0,1,1),(1,0,1)), ((1,1,0),(1,0,1))]
GAMMA = [((0,0,1),(1,0,0)), ((0,1,1),(1,1,0))]

def beta_bits(r): return [int(eca_out(r,*u) == eca_out(r,*v)) for u, v in BETA]
def gamma_bits(r): return [int(eca_out(r,*u) == eca_out(r,*v)) for u, v in GAMMA]
def is_totalistic(r):
    return all(eca_out(r,L,C,R) == eca_out(r,L2,C2,R2)
               for (L,C,R) in itertools.product((0,1), repeat=3)
               for (L2,C2,R2) in itertools.product((0,1), repeat=3) if L+C+R == L2+C2+R2)

# --------------------------------------------------------- strata accounting

def strata(st):
    """Per-column defect flag and |Delta| stratum for a height-two state."""
    x0, x1 = st[0].astype(np.int16), st[1].astype(np.int16)
    s0 = np.roll(x0,1) + x0 + np.roll(x0,-1)
    s1 = np.roll(x1,1) + x1 + np.roll(x1,-1)
    d = (st[0] != st[1])
    return d, np.abs(s1 - s0)

def strata_counts(st):
    d, ad = strata(st)
    return (int((d & (ad == 0)).sum()), int((d & (ad == 1)).sum()), int((d & (ad >= 2)).sum()))

def n_antiphase_pairs(st):
    """Width-two runs of the disagreement field whose row-0 values differ."""
    d, _ = strata(st)
    x0 = st[0]
    j = np.arange(len(d))
    jp, jm, jpp = (j+1) % len(d), (j-1) % len(d), (j+2) % len(d)
    isolated2 = d & d[jp] & ~d[jm] & ~d[jpp]
    return int((isolated2 & (x0 != x0[jp])).sum())

def clusters(st):
    d, _ = strata(st)
    if not d.any(): return 0
    starts = d & ~np.roll(d, 1)
    return int(starts.sum())

# ------------------------------------------- measurement helpers (COPIED)

def _initial(k, key, rep, kind, flip):
    """This unit's own seed namespace."""
    rng = np.random.default_rng(seed(kind, *key, k, DENSITY, rep))
    st = (rng.random((k, W)) < DENSITY).astype(np.uint8)
    if flip: st = (1 - st).astype(np.uint8)
    return rng, st

def sample_events_strata(rule, k, key, flip=False):
    events = []; total = k * W; ag = []
    strat_tot = np.zeros(3, dtype=np.int64); surv_tot = np.zeros(3, dtype=np.int64)
    clu = []; nap = []; snaps = {}
    for rep in range(strip.EVENT_SEEDS):
        rng, st = _initial(k, key, rep, 'events', flip)
        for _ in range(strip.BURN): st = base.life_step(st, rule)
        flat = np.sort(rng.choice(total, size=min(strip.SITES, total), replace=False))
        ys, xs = flat // W, flat % W
        hist = np.zeros(len(flat), dtype=np.uint8)
        for _ in range(7):
            ag.append(float(np.all(st == st[0], axis=0).mean()))
            hist = ((hist << 1) | st[ys, xs]) & 0xff
            st = base.life_step(st, rule)
        cc = []; hh = []; yy = []; zz = []
        for t in range(strip.SCORE):
            ag.append(float(np.all(st == st[0], axis=0).mean()))
            d, ad = strata(st)
            c0 = int((d & (ad == 0)).sum()); c1 = int((d & (ad == 1)).sum()); c2 = int((d & (ad >= 2)).sum())
            strat_tot += (c0, c1, c2)
            clu.append(clusters(st)); nap.append(n_antiphase_pairs(st))
            if rep == 0 and (t + 1) in (1, 2, 4, 8, 16, 32, 64, 128, 256):
                snaps[t + 1] = (c0, c1, c2)
            cur = st[ys, xs].copy(); hist = ((hist << 1) | cur) & 0xff
            sym = base.life_symbols(st, ys, xs); nxt = base.life_step(st, rule)
            dn, _ = strata(nxt)
            surv_tot += (int((d & (ad == 0) & dn).sum()), int((d & (ad == 1) & dn).sum()),
                         int((d & (ad >= 2) & dn).sum()))
            cc.append(cur); hh.append(hist.copy()); yy.append(nxt[ys, xs].copy()); zz.append(sym)
            st = nxt
        events.append({'current': np.concatenate(cc), 'history': np.concatenate(hh),
                       'target': np.concatenate(yy), 'symbol': np.concatenate(zz)})
    extra = {'strata_column_steps': [int(v) for v in strat_tot],
             'strata_one_step_survival': [int(v) for v in surv_tot],
             'strata_snapshots': {str(k2): list(v) for k2, v in snaps.items()},
             'mean_clusters': float(np.mean(clu)) if clu else 0.0,
             'mean_antiphase_pairs': float(np.mean(nap)) if nap else 0.0,
             'terminal_defects': int((st[0] != st[1]).sum())}
    return events, float(np.mean(ag)), extra

def spread_keyed(rule, k, key, flip=False):
    x1 = []; x2 = []; extinct = 0; total = k * W
    for rep in range(strip.SPREAD_SEEDS):
        rng, st = _initial(k, key, rep, 'spread', flip)
        for _ in range(strip.BURN): st = base.life_step(st, rule)
        for flat in rng.choice(total, size=strip.ORIGINS, replace=False):
            oy, ox = divmod(int(flat), W)
            a = st.copy(); b = st.copy(); b[oy, ox] ^= 1
            aa = bb = None
            for tt in range(1, strip.T2 + 1):
                a = base.life_step(a, rule); b = base.life_step(b, rule)
                if tt == strip.T1: aa = strip.xdiam(a ^ b, ox)
                if tt == strip.T2: bb = strip.xdiam(a ^ b, ox)
            x1.append(aa); x2.append(bb); extinct += int(bb == 0)
    ma = float(np.mean(x1)); mb = float(np.mean(x2))
    alpha = 0.0 if (ma == 0 and mb == 0) else (float(math.log2(mb/ma)) if ma > 0 and mb > 0 else None)
    return {'Dx64': ma, 'Dx128': mb, 'alpha_x': alpha,
            'extinction_fraction': extinct/len(x2), 'spread_trials': len(x2)}

def transverse_plain(table, base_rule, u, flip=False):
    r = HandedRule(f'h{table}', table)
    d64, d128 = [], []
    for rep in range(4):
        rng = np.random.default_rng(seed('transverse', u, rep))
        x = (rng.random(W) < 0.5).astype(np.uint8)
        if flip: x = (1 - x).astype(np.uint8)
        for _ in range(256): x = eca_step(x, base_rule)
        for o in rng.choice(W, size=8, replace=False):
            st = np.vstack([x, x.copy()]); st[1, int(o)] ^= 1
            for t in range(1, 129):
                st = handed_step(st, r)
                nd = int((st[0] != st[1]).sum())
                if t == 64: d64.append(nd)
            d128.append(nd)
    return {'T64': float(np.mean(d64)), 'T128': float(np.mean(d128)),
            'T_ext': float(np.mean([d == 0 for d in d128]))}

def evaluate(table, u, arm, base_rule, flip=False):
    r = HandedRule(f'h{table}', table)
    t0 = time.time()
    events, agree, extra = sample_events_strata(r, 2, ('A', u), flip)
    p, nref, refmode = strip.reference_strip(r, 2)
    R, mu, sd, missing = base.selective_r(events, p)
    M, bll, hll, ntr, nte = base.predictive_gain(events[:4], events[4:6])
    sp = spread_keyed(r, 2, ('A', u), flip)
    row = {'table': table, 'u': u, 'arm': arm, 'base': base_rule,
           'R_star': R, 'M_star': M,
           'S_star': max(0, R) * max(0, M) if math.isfinite(R) else None,
           'agree': agree, 'on_beam': int(agree > 0.98), 'off_beam': int(agree < 0.5),
           **sp, **extra, 'wall_seconds': time.time() - t0}
    if arm in TRANSVERSE_ARMS:
        row.update(transverse_plain(table, base_rule, u, flip))
    return row

# ---------------------------------------------------------- the Pi tier

def beam_state(base_rule, u, rep):
    rng = np.random.default_rng(seed('pair', u, rep))
    x = (rng.random(W) < 0.5).astype(np.uint8)
    for _ in range(256): x = eca_step(x, base_rule)
    return rng, x

def pi_tier(base_rule, us):
    """Plant a width-two anti-phase block (BOTH rows) and follow it 512 steps."""
    horizons = (64, 128, 256, 512); surv = {h: [] for h in horizons}
    for u in us:
        r = HandedRule(f'h{u}', embed(base_rule, bits_of(u)))
        for rep in range(4):
            rng, x = beam_state(base_rule, u, rep)
            for o in rng.choice(W, size=8, replace=False):
                j = int(o); jp = (j + 1) % W; phi = int(rng.integers(0, 2))
                st = np.vstack([x, x.copy()])
                st[0, j] = phi;     st[0, jp] = 1 - phi
                st[1, j] = 1 - phi; st[1, jp] = phi
                for t in range(1, 513):
                    st = handed_step(st, r)
                    if t in surv: surv[t].append(int((st[0] != st[1]).sum() > 0))
    return {f'Pi_{h}': float(np.mean(surv[h])) for h in horizons}

# -------------------------------------------------------------- completions

def build_arms():
    """One namespace, fixed order. U++ is the complete cell, not a sample."""
    rng = np.random.default_rng(seed('completions'))
    allu = np.arange(1 << 24, dtype=np.uint32)
    v12 = viol_mask(allu, CONS12)
    v7 = viol_mask(allu, DARK_PAIRS)
    upp = set(upp_completion(k) for k in range(1 << len(UPP_COMPS)))
    arms = {'Upp': sorted(upp)}
    def draw(mask, n, exclude):
        idx = allu[mask]
        idx = idx[~np.isin(idx, np.array(sorted(exclude), dtype=np.uint32))] if exclude else idx
        return [int(v) for v in rng.choice(idx, size=n, replace=False)]
    arms['Uplus']  = draw(v12 == 0, N_ARM['Uplus'], upp)
    arms['Dplus']  = draw(v7 == 0, N_ARM['Dplus'], upp)
    arms['G']      = draw(v12 == 0x00F, N_ARM['G'], set())
    arms['Gprime'] = draw(v12 == 0xF00, N_ARM['Gprime'], set())
    arms['K']      = draw(((v12 & 0xF0F) == 0) & (((v12 >> 4) & 0xF) != 0), N_ARM['K'], set())
    arms['random'] = draw(np.ones(len(allu), bool), N_ARM['random'], set())
    sizes = {'Upp': len(upp), 'Uplus': int((v12 == 0).sum()), 'Dplus': int((v7 == 0).sum()),
             'G': int((v12 == 0x00F).sum()), 'Gprime': int((v12 == 0xF00).sum()),
             'K': int((((v12 & 0xF0F) == 0) & (((v12 >> 4) & 0xF) != 0)).sum())}
    return arms, sizes

# ------------------------------------------------------------- controls

def controls(arms, sizes):
    c, fail = {}, []

    # 1. algebra, exact
    rl, rd = gf2_rank(LIT_PAIRS), gf2_rank(DARK_PAIRS)
    strat_ok = True
    for p, ws in ALG['windows'].items():
        a, b = sorted(p); ds = {abs(d) for _, d in ws}
        kind = 'exposed' if (a in set(EXPOSED) and b in set(EXPOSED)) else ('lit' if ds == {1} else 'dark')
        for _, d in ws:
            want = 'exposed' if d == 0 else ('lit' if abs(d) == 1 else 'dark')
            if want != kind: strat_ok = False
    tot = [r for r in range(256) if is_totalistic(r)]
    beta_all = [r for r in range(256) if all(beta_bits(r))]
    gamma_on_tot = all(all(gamma_bits(r)) for r in beta_all)
    # the three diagonals must hold on every U+ member (implied by the twelve)
    up = np.arange(1 << 24, dtype=np.uint32)
    v12 = viol_mask(up, CONS12)
    diag = [p for p in LIT_PAIRS if tuple(p) not in {tuple(sorted(x)) for x in CONS12}]
    diag_ok = bool((viol_mask(up[v12 == 0], diag) == 0).all())
    c['1_algebra'] = {'agreeing_windows': ALG['agreeing'], 'pairs': ALG['pairs'],
                      'n_exposed': len(EXPO_PAIRS), 'n_lit': len(LIT_PAIRS), 'n_dark': len(DARK_PAIRS),
                      'n_mixed': len(ALG['mixed']), 'stratification_exact': strat_ok,
                      'rank_lit': rl, 'rank_dark': rd, 'components': len(UPP_COMPS),
                      'n_Upp': sizes['Upp'], 'diagonals_implied': diag_ok,
                      'beta_all_equals_totalistic': sorted(beta_all) == sorted(tot),
                      'n_totalistic': len(tot), 'gamma_holds_on_totalistic': gamma_on_tot}
    if not (ALG['agreeing'] == 8 and ALG['pairs'] == 28 and len(EXPO_PAIRS) == 6
            and len(LIT_PAIRS) == 15 and len(DARK_PAIRS) == 7 and not ALG['mixed']
            and strat_ok and rl == 11 and rd == 7 and sizes['Upp'] == 64 and diag_ok
            and sorted(beta_all) == sorted(tot) and len(tot) == 16 and gamma_on_tot):
        fail.append('control1_algebra')

    # 2. one-step law on real dynamics + strata accounting reproduces agree
    rng = np.random.default_rng(seed('ctl2')); bad = 0; n2 = 0
    for _ in range(64):
        br = int(rng.choice(BASES)); u = int(rng.integers(0, 1 << 24))
        r = HandedRule('t', embed(br, bits_of(u)))
        st = (rng.random((2, W)) < 0.5).astype(np.uint8)
        tab = np.array([(r.table >> i) & 1 for i in range(32)], dtype=np.uint8)
        for _ in range(8):
            x0, x1 = st[0].astype(np.int64), st[1].astype(np.int64)
            s0 = np.roll(x0,1) + x0 + np.roll(x0,-1); s1 = np.roll(x1,1) + x1 + np.roll(x1,-1)
            i0 = 16*x0 + 8*np.roll(x0,1) + np.roll(x0,-1) + 2*s1
            i1 = 16*x1 + 8*np.roll(x1,1) + np.roll(x1,-1) + 2*s0
            pred = tab[i0] ^ tab[i1]
            st = handed_step(st, r)
            got = (st[0] ^ st[1])
            n2 += 1
            if not np.array_equal(pred, got): bad += 1
    c['2_one_step_law'] = {'mismatches': bad, 'of': n2}
    if bad: fail.append('control2_one_step_law')

    # 3. one-step collapse on totalistic bases, with a witness that can fail
    coll_bad = 0; rng3 = np.random.default_rng(seed('ctl3'))
    for br in (0, 22, 232):
        for u in arms['Upp']:
            r = HandedRule('t', embed(br, bits_of(u)))
            for _ in range(4):
                st = (rng3.random((2, W)) < 0.5).astype(np.uint8)
                st = handed_step(st, r)
                if (st[0] != st[1]).any(): coll_bad += 1
    wit = 0
    for u in arms['Upp'][:8]:
        r = HandedRule('t', embed(110, bits_of(u)))
        for _ in range(4):
            st = (rng3.random((2, W)) < 0.5).astype(np.uint8)
            st = handed_step(st, r)
            if (st[0] != st[1]).any(): wit += 1
    c['3_one_step_collapse'] = {'collapse_failures': coll_bad, 'of': 3*64*4, 'witness_nonzero': wit}
    if coll_bad or wit == 0: fail.append('control3_collapse')

    # 4. identity exception through the measurement path, as INTEGER counts
    ex = []
    for br in (204, 51):
        for u in arms['Upp'][:4]:
            r = HandedRule('t', embed(br, bits_of(u)))
            for rep in range(strip.EVENT_SEEDS):
                _, st0 = _initial(2, ('A', u), rep, 'events', False)
                for _ in range(strip.BURN): st0 = base.life_step(st0, r)
                pred = 2 * n_antiphase_pairs(st0)
                st = st0.copy()
                for _ in range(8): st = handed_step(st, r)
                ex.append((int((st[0] != st[1]).sum()), pred))
    perm = 0; tot_p = 0; rng4 = np.random.default_rng(seed('ctl4'))
    for br in (204, 51):
        r0 = None
        for _ in range(32):
            # a random A-and-C completion (B free): the theorem's hypothesis
            while True:
                u = int(rng4.integers(0, 1 << 24))
                v = int(viol_mask([u], CONS12)[0])
                if (v & 0xF0F) == 0: break
            r = HandedRule('t', embed(br, bits_of(u)))
            rng5, x = beam_state(br, u, 0)
            j = int(rng5.integers(0, W)); jp = (j+1) % W; phi = int(rng5.integers(0, 2))
            st = np.vstack([x, x.copy()])
            st[0, j] = phi; st[0, jp] = 1 - phi; st[1, j] = 1 - phi; st[1, jp] = phi
            for _ in range(512): st = handed_step(st, r)
            d = (st[0] != st[1]); tot_p += 1
            if int(d.sum()) == 2 and d[j] and d[jp]: perm += 1
    c['4_identity_exception'] = {'integer_mismatches': sum(1 for a, b in ex if a != b), 'of': len(ex),
                                 'planted_pair_permanence': perm / tot_p, 'planted_trials': tot_p}
    if any(a != b for a, b in ex) or perm != tot_p: fail.append('control4_identity')

    # 5. containment: successors lie in blind columns; lit/dark survival zero
    cont_bad = 0; lit_surv = dark_surv = 0
    for br in BASES[:8]:
        for u in arms['Upp'][:4]:
            r = HandedRule('t', embed(br, bits_of(u)))
            st = (np.random.default_rng(seed('ctl5', br, u)).random((2, W)) < 0.5).astype(np.uint8)
            for _ in range(strip.BURN): st = handed_step(st, r)
            for _ in range(32):
                d, ad = strata(st)
                blind = d & (ad == 0)
                nxt = handed_step(st, r)
                dn, _ = strata(nxt)
                if (dn & ~blind).any(): cont_bad += 1
                lit_surv += int((d & (ad == 1) & dn).sum())
                dark_surv += int((d & (ad >= 2) & dn).sum())
                st = nxt
    c['5_containment'] = {'violations': cont_bad, 'lit_survival': lit_surv, 'dark_survival': dark_surv}
    if cont_bad or lit_surv or dark_surv: fail.append('control5_containment')

    # 6. regeneration against the previous unit's canonical rows.
    # Run in a SUBPROCESS: loading that unit's module in-process would re-execute
    # its loader chain, rebind base.life_step to a wrapper closing over a
    # DIFFERENT HandedRule class, and break every later isinstance dispatch.
    prev = json.loads((ROOT / 'results/defect_algebra_20260918/rows.json').read_text())
    prev_rows = prev['rows'] if isinstance(prev, dict) else prev
    want = [{**{k: pr.get(k) for k in ('table', 'R_star', 'M_star', 'agree', 'alpha_x')},
              'u': u_of(int(pr['table']))} for pr in prev_rows[:16]]
    script = (
        "import importlib.util as i,sys,json\n"
        f"s=i.spec_from_file_location('da6',r'{ROOT}/experiments/defect_algebra_20260918/run.py')\n"
        "m=i.module_from_spec(s);sys.modules['da6']=m;s.loader.exec_module(m)\n"
        "w=json.load(sys.stdin);out=[]\n"
        "for pr in w:\n"
        "    g=m.evaluate(pr['table'],pr['u'],m.seed,flip=False)\n"
        "    out.append({k:g.get(k) for k in ('R_star','M_star','agree','alpha_x')})\n"
        "print(json.dumps(out))\n")
    import subprocess
    pr6 = subprocess.run([sys.executable, '-c', script], input=json.dumps(want),
                         capture_output=True, text=True)
    bad6 = []
    if pr6.returncode != 0:
        bad6.append(('subprocess', pr6.returncode, pr6.stderr[-400:]))
    else:
        got6 = json.loads(pr6.stdout.strip().splitlines()[-1])
        for pr, g in zip(want, got6):
            for key in ('R_star', 'M_star', 'agree', 'alpha_x'):
                x, y = pr.get(key), g.get(key)
                if x is None and y is None: continue
                if x is None or y is None or abs(float(x) - float(y)) > 1e-12:
                    bad6.append((pr['u'], key, x, y))
    c['6_regeneration'] = {'mismatches': len(bad6), 'of': len(want) * 4, 'examples': bad6[:4]}
    if bad6: fail.append('control6_regeneration')

    # 7. beam invariance at heights two and three
    bad7 = []
    for br in BASES:
        for u in arms['Upp'][:8]:
            r = HandedRule('t', embed(br, bits_of(u)))
            for k in (2, 3):
                rng7 = np.random.default_rng(seed('ctl7', br, u, k))
                x = (rng7.random(W) < 0.5).astype(np.uint8)
                st = np.vstack([x] * k); ref = x.copy()
                for _ in range(256):
                    st = handed_step(st, r); ref = eca_step(ref, br)
                    if not (np.all(st == st[0], axis=0).all() and np.array_equal(st[0], ref)):
                        bad7.append((br, u, k)); break
    c['7_beam_invariance'] = {'failures': len(bad7), 'examples': bad7[:4]}
    if bad7: fail.append('control7_beam')

    # 8. matched null pairs, paired draws
    def conj(table):
        t = 0
        for i in range(32):
            if (table >> i) & 1: continue
            c_, w_, n7 = (i >> 4) & 1, (i >> 3) & 1, i & 7
            t |= 1 << (16*(1-c_) + 8*(1-w_) + (7-n7))
        return t
    pairs8 = []
    for u in arms['random'][:8] + arms['Upp'][:8] + arms['G'][:4]:
        pairs8.append((110, 137, u))
    for u in arms['Upp'][:4]:
        pairs8.append((51, 51, u))
    worst = 0.0
    for b1, b2, u in pairs8:
        t1 = embed(b1, bits_of(u)); t2 = conj(t1)
        a = evaluate(t1, u, 'null', b1, flip=False)
        b = evaluate(t2, u, 'null', b2, flip=True)
        for key in ('R_star', 'M_star', 'agree', 'Dx64', 'Dx128', 'mean_clusters', 'mean_antiphase_pairs'):
            va, vb = a.get(key), b.get(key)
            if va is None or vb is None: continue
            worst = max(worst, abs(float(va) - float(vb)))
        if a['strata_column_steps'] != b['strata_column_steps']: worst = max(worst, 1.0)
    c['8_matched_null_pairs'] = {'worst_abs_difference': worst, 'n_pairs': len(pairs8)}
    if worst > 1e-9: fail.append('control8_null_pairs')

    # 9. disjointness from units four/five/six
    prev_us = set()
    for pth in ('results/matched_completion_20260918/rows.json',
                'results/beam_mechanism_20260918/rows.json',
                'results/defect_algebra_20260918/rows.json'):
        try:
            dd = json.loads((ROOT / pth).read_text())
            rows = dd['rows'] if isinstance(dd, dict) else dd
            prev_us |= {int(r['u']) if 'u' in r else u_of(int(r['table'])) for r in rows}
        except Exception: pass
    overlaps = {a: sorted(set(arms[a]) & prev_us) for a in ARMS}
    c['9_disjointness'] = {'overlap_counts': {a: len(v) for a, v in overlaps.items()},
                           'Upp_overlap_recorded': overlaps['Upp']}
    for a in ARMS:
        if a != 'Upp' and overlaps[a]: fail.append(f'control9_disjointness_{a}')

    # 10. grower edge law on trajectories
    bad10 = 0; n10 = 0
    for br in (110, 22, 90, 0):
        for u, arm, direction in [(arms['G'][0], 'G', -1), (arms['G'][1], 'G', -1),
                                  (arms['Gprime'][0], 'Gprime', +1), (arms['Gprime'][1], 'Gprime', +1)]:
            r = HandedRule('t', embed(br, bits_of(u)))
            rng10, x = beam_state(br, u, 1)
            o = int(rng10.integers(0, W))
            st = np.vstack([x, x.copy()]); st[1, o] ^= 1
            prev_edge = None
            for _ in range(32):
                st = handed_step(st, r)
                d, _ = strata(st)
                if not d.any(): break
                pos = np.flatnonzero(d)
                edge = int(pos.min()) if direction < 0 else int(pos.max())
                if prev_edge is not None:
                    step = (edge - prev_edge) % W
                    want = (direction) % W
                    n10 += 1
                    if step != want: bad10 += 1
                prev_edge = edge
    c['10_grower_edge_law'] = {'violations': bad10, 'of': n10}
    if n10 and bad10 > 0.02 * n10: fail.append('control10_edge_law')

    c['failures'] = fail
    return c, fail

# ------------------------------------------------------------------- driver

def work(job):
    br, arm, u = job
    return evaluate(embed(br, bits_of(u)), u, arm, br)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=4)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    arms, sizes = build_arms()
    alg_out = {'agreeing_windows': ALG['agreeing'], 'n_pairs': ALG['pairs'],
               'exposed_pairs': [list(p) for p in EXPO_PAIRS],
               'lit_pairs': [list(p) for p in LIT_PAIRS],
               'dark_pairs': [list(p) for p in DARK_PAIRS],
               'rank_lit': gf2_rank(LIT_PAIRS), 'rank_dark': gf2_rank(DARK_PAIRS),
               'n_components': len(UPP_COMPS), 'n_Upp': sizes['Upp'],
               'totalistic': [r for r in range(256) if is_totalistic(r)],
               'cell_sizes': sizes,
               'base_bits': {str(r): {'beta': beta_bits(r), 'gamma': gamma_bits(r),
                                      'e_G': beta_bits(r)[0] + beta_bits(r)[2],
                                      'e_Gprime': beta_bits(r)[1] + beta_bits(r)[3],
                                      'totalistic': is_totalistic(r)} for r in BASES}}
    (OUT / 'algebra.json').write_text(json.dumps(alg_out, indent=1))
    print(f'[algebra] {ALG["agreeing"]} agreeing, {ALG["pairs"]} pairs = '
          f'{len(EXPO_PAIRS)} exposed + {len(LIT_PAIRS)} lit + {len(DARK_PAIRS)} dark; '
          f'ranks {gf2_rank(LIT_PAIRS)}/{gf2_rank(DARK_PAIRS)}; |U++| = {sizes["Upp"]}', flush=True)

    print('[controls] running before any tier', flush=True)
    ctl, fail = controls(arms, sizes)
    (OUT / 'controls.json').write_text(json.dumps(ctl, indent=1, default=str))
    for k, v in ctl.items():
        if k != 'failures': print(f'  {k}: {v}', flush=True)
    if fail:
        raise SystemExit(f'CONTROLS FAILED: {fail} -- no tier was run, nothing written but controls.json')
    print(f'[controls] all pass ({time.time()-t0:.0f}s)', flush=True)

    jobs = [(br, arm, u) for br in BASES for arm in ARMS for u in arms[arm]]
    print(f'[tiers] {len(jobs)} evaluations over {len(BASES)} bases', flush=True)
    rows = []
    with Pool(a.workers) as pool:
        for i, row in enumerate(pool.imap_unordered(work, jobs, chunksize=4), 1):
            rows.append(row)
            if i % 200 == 0: print(f'  {i}/{len(jobs)} ({time.time()-t0:.0f}s)', flush=True)
    (OUT / 'rows.json').write_text(json.dumps({'protocol': PROTOCOL, 'rows': rows}, default=str))

    print('[pi] pair-survival tier', flush=True)
    pis = {}
    for br in BASES:
        pis[str(br)] = pi_tier(br, arms['Upp'][:16])
        print(f'  base {br}: {pis[str(br)]}', flush=True)
    (OUT / 'pairs.json').write_text(json.dumps({'protocol': PROTOCOL, 'pi': pis,
                                                'arms': {k: v for k, v in arms.items()}}, indent=1))
    print(f'[done] {len(rows)} evaluations in {(time.time()-t0)/60:.1f} min', flush=True)

if __name__ == '__main__':
    main()
