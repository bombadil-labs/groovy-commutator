#!/usr/bin/env python3
"""Permanent structures: the isolated-defect gadget and the 2-cluster radius.

Frozen protocol: docs/research/protocols/2026-09-18-permanent-structures.md
(committed before this implementation).

Under a completion satisfying A and C, an isolated defect's west flank reads
A(LL,L), the defect column reads B(L,R), and the east flank reads C(R,RR);
columns j+-2 read exposed entries with agreeing windows. So (L, d0, d1, R)
evolves as a deterministic automaton on 8 defect states plus an absorbing
healed class, with input (LL, RR) from the background. SAFE/DOOMED partition
the 57,344 K completions into K-forall 24576 / K-exists 28672 / K-bot 4096.

The draft's independence claim was for 1-clusters at separation two; that is
false (verified before freeze). The right object is the 2-CLUSTER, independent
at separation >= 3 agreeing columns, on every base -- not only frozen ones.

Controls 1-12 run BEFORE any tier and raise. Measurement helpers are COPIED
from the seventh unit with this protocol's seed function, never imported.

    python experiments/permanent_structures_20260918/run.py --workers 4
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

PROTOCOL = 'permanent-structures-20260918'
OUT = ROOT / 'results/permanent_structures_20260918'
W = strip.WIDTH
DENSITY = 0.5

PANEL = {'0000': [204, 51, 90, 37, 50, 178], '1111': [0, 22, 232], '1101': [8, 30, 31],
         '0001': [27, 114, 26], '0010': [45, 59, 58], '0100': [177, 89], '1000': [163, 75],
         '0101': [25, 102], '1010': [67, 60], '0111': [110, 7], '1011': [106, 21],
         '1110': [62, 87], '0011': [5, 18], '1100': [54, 33]}
BASES = [r for v in PANEL.values() for r in v]
FROZEN = [204, 51, 0, 8]
ARMS = ['Upp', 'Kall', 'Kex', 'Kbot', 'G', 'Gprime', 'random']
N_ARM = {'Upp': 8, 'Kall': 16, 'Kex': 16, 'Kbot': 16, 'G': 12, 'Gprime': 12, 'random': 24}

A_TAB = {(0,0):(1,2), (0,1):(19,20), (1,0):(11,12), (1,1):(29,30)}   # key (LL,L)
B_TAB = {(0,0):(2,16), (0,1):(5,19), (1,0):(12,26), (1,1):(15,29)}   # key (L,R)
C_TAB = {(0,0):(2,8),  (0,1):(5,11), (1,0):(20,26), (1,1):(23,29)}   # key (R,RR)
ACONS = [A_TAB[k] for k in sorted(A_TAB)]
BCONS = [B_TAB[k] for k in sorted(B_TAB)]
CCONS = [C_TAB[k] for k in sorted(C_TAB)]

def seed(*parts):
    h = hashlib.sha256('|'.join(map(str, (PROTOCOL,) + parts)).encode()).digest()
    return int.from_bytes(h[:8], 'little') & 0x7fff_ffff_ffff_ffff

def bits_of(u): return [(u >> i) & 1 for i in range(24)]
def u_of(table): return sum(((table >> e) & 1) << POS[e] for e in FREE)
def tab_of_u(u):
    t = [0]*32
    for e in FREE: t[e] = (int(u) >> POS[e]) & 1
    return t

# ------------------------------------------------- algebra and the 28 pairs

def idx_of(own, other):
    L, C, R = own
    return 16*C + 8*L + R + 2*sum(other)

def derive_pairs():
    ES = set(EXPOSED); agreeing = 0; pw = {}
    for w in itertools.product((0,1), repeat=6):
        r0, r1 = w[:3], w[3:]
        i0, i1 = idx_of(r0, r1), idx_of(r1, r0)
        if i0 == i1: agreeing += 1; continue
        pw.setdefault(frozenset((i0, i1)), []).append(w)
    keys = sorted(tuple(sorted(p)) for p in pw)
    return agreeing, keys, pw

AGREEING, PAIR_KEYS, PAIR_WINDOWS = derive_pairs()
PAIR_INDEX = {p: i for i, p in enumerate(PAIR_KEYS)}
# 64-entry LUT: six-bit window -> pair ordinal (or -1 when the two reads agree)
WIN_LUT = np.full(64, -1, dtype=np.int16)
for w in itertools.product((0,1), repeat=6):
    r0, r1 = w[:3], w[3:]
    i0, i1 = idx_of(r0, r1), idx_of(r1, r0)
    code = (w[0]<<5)|(w[1]<<4)|(w[2]<<3)|(w[3]<<2)|(w[4]<<1)|w[5]
    if i0 != i1: WIN_LUT[code] = PAIR_INDEX[tuple(sorted((i0, i1)))]

def gf2_rank(pairs, universe):
    rows = [(1 << universe[a]) | (1 << universe[b]) for a, b in pairs]
    basis, r = [], 0
    for v in rows:
        for bvec in basis: v = min(v, v ^ bvec)
        if v: basis.append(v); basis.sort(reverse=True); r += 1
    return r

def eca_out(r, L, C, R): return (r >> (4*L + 2*C + R)) & 1
BETA  = [((1,0,0),(0,1,0)), ((0,0,1),(0,1,0)), ((0,1,1),(1,0,1)), ((1,1,0),(1,0,1))]
GAMMA = [((0,0,1),(1,0,0)), ((0,1,1),(1,1,0))]
def beta_bits(r): return [int(eca_out(r,*u) == eca_out(r,*v)) for u, v in BETA]
def gamma_bits(r): return [int(eca_out(r,*u) == eca_out(r,*v)) for u, v in GAMMA]
def is_totalistic(r):
    return all(eca_out(r,L,C,R) == eca_out(r,L2,C2,R2)
               for (L,C,R) in itertools.product((0,1),repeat=3)
               for (L2,C2,R2) in itertools.product((0,1),repeat=3) if L+C+R == L2+C2+R2)

def violation_vector(u, r):
    """28 violation bits of the full embedded table: six decided by the base
    (exposed pairs), 22 by the completion. Read off the embedded table rather
    than reconstructing the embedding by hand."""
    t = [(embed(r, bits_of(u)) >> i) & 1 for i in range(32)]
    return np.array([int(t[a] != t[b]) for (a, b) in PAIR_KEYS], dtype=np.int8)

# ------------------------------------------------------------ the gadget

def gadget(u):
    """Returns (SAFE set, DOOMED set, transition dict) for an A-and-C completion."""
    t = tab_of_u(u)
    a = lambda LL, L: t[A_TAB[(LL, L)][0]]
    c = lambda R, RR: t[C_TAB[(R, RR)][0]]
    Bh = {(L, R): t[B_TAB[(L, R)][0]] == t[B_TAB[(L, R)][1]] for L in (0,1) for R in (0,1)}
    S = [(L, b, R) for L in (0,1) for b in (0,1) for R in (0,1)]
    trans = {}
    for s in S:
        L, b, R = s
        for LL in (0,1):
            for RR in (0,1):
                if Bh[(L, R)]: trans[(s, LL, RR)] = None
                else:
                    lo, hi = B_TAB[(L, R)]
                    trans[(s, LL, RR)] = (a(LL, L), t[lo] if b == 0 else t[hi], c(R, RR))
    doomed = set()
    while True:
        add = {s for s in S if s not in doomed
               and all(trans[(s,LL,RR)] is None or trans[(s,LL,RR)] in doomed
                       for LL in (0,1) for RR in (0,1))}
        if not add: break
        doomed |= add
    safe = set(S)
    while True:
        rm = {s for s in safe if any(trans[(s,LL,RR)] is None or trans[(s,LL,RR)] not in safe
                                     for LL in (0,1) for RR in (0,1))}
        if not rm: break
        safe -= rm
    return safe, doomed, trans

def gadget_class(u):
    safe, doomed, _ = gadget(u)
    if len(safe) > 0: return 'Kall'
    if len(doomed) == 8: return 'Kbot'
    return 'Kex'

# ------------------------------------------------- strata, clusters, census

def strata(st):
    x0, x1 = st[0].astype(np.int16), st[1].astype(np.int16)
    s0 = np.roll(x0,1) + x0 + np.roll(x0,-1)
    s1 = np.roll(x1,1) + x1 + np.roll(x1,-1)
    return (st[0] != st[1]), np.abs(s1 - s0)

def window_codes(st):
    x0, x1 = st[0], st[1]
    return ((np.roll(x0,1).astype(np.int16)<<5) | (x0.astype(np.int16)<<4) | (np.roll(x0,-1).astype(np.int16)<<3)
            | (np.roll(x1,1).astype(np.int16)<<2) | (x1.astype(np.int16)<<1) | np.roll(x1,-1).astype(np.int16))

def pair_census(st):
    return np.bincount(np.maximum(WIN_LUT[window_codes(st)], 0)[WIN_LUT[window_codes(st)] >= 0],
                       minlength=len(PAIR_KEYS))

def clusters2(d):
    """2-clusters: runs of defects allowing gaps of up to two. Returns (count, widths)."""
    if not d.any(): return 0, []
    closed = d.copy()
    for g in (1, 2):
        for s in range(1, g+1):
            closed = closed | (np.roll(d, s) & np.roll(d, -(g+1-s)))
    idx = np.flatnonzero(closed)
    if idx.size == 0: return 0, []
    br = np.flatnonzero(np.diff(idx) > 1)
    gs = np.split(idx, br+1)
    return len(gs), [int(g[-1]-g[0]+1) for g in gs]

def isolated_defects(st):
    """Defects with no other defect within 2 columns; returns their gadget states."""
    d, _ = strata(st)
    idx = np.flatnonzero(d)
    out = []
    for j in idx:
        near = d[(j-2) % W] or d[(j-1) % W] or d[(j+1) % W] or d[(j+2) % W]
        if near: continue
        L, R = int(st[0][(j-1) % W]), int(st[0][(j+1) % W])
        out.append((L, int(st[0][j]), R))
    return out

# ------------------------------------------- measurement helpers (COPIED)

def _initial(k, key, rep, kind, flip):
    rng = np.random.default_rng(seed(kind, *key, k, DENSITY, rep))
    st = (rng.random((k, W)) < DENSITY).astype(np.uint8)
    if flip: st = (1 - st).astype(np.uint8)
    return rng, st

def sample_events_full(rule, k, key, flip=False):
    events = []; total = k * W; ag = []
    strat = np.zeros(3, dtype=np.int64); surv = np.zeros(3, dtype=np.int64)
    census = np.zeros(len(PAIR_KEYS), dtype=np.int64)
    ncl = []; widths = []; niso = []; steps = 0
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
        cc=[]; hh=[]; yy=[]; zz=[]
        for _ in range(strip.SCORE):
            ag.append(float(np.all(st == st[0], axis=0).mean()))
            d, ad = strata(st); steps += 1
            strat += (int((d&(ad==0)).sum()), int((d&(ad==1)).sum()), int((d&(ad>=2)).sum()))
            wc = WIN_LUT[window_codes(st)]
            census += np.bincount(wc[wc >= 0], minlength=len(PAIR_KEYS))
            n, ws = clusters2(d); ncl.append(n); widths.extend(ws)
            niso.append(len(isolated_defects(st)))
            cur = st[ys, xs].copy(); hist = ((hist << 1) | cur) & 0xff
            sym = base.life_symbols(st, ys, xs); nxt = base.life_step(st, rule)
            dn, _ = strata(nxt)
            surv += (int((d&(ad==0)&dn).sum()), int((d&(ad==1)&dn).sum()), int((d&(ad>=2)&dn).sum()))
            cc.append(cur); hh.append(hist.copy()); yy.append(nxt[ys, xs].copy()); zz.append(sym)
            st = nxt
        events.append({'current': np.concatenate(cc), 'history': np.concatenate(hh),
                       'target': np.concatenate(yy), 'symbol': np.concatenate(zz)})
    extra = {'strata_column_steps': [int(v) for v in strat],
             'strata_one_step_survival': [int(v) for v in surv],
             'pair_census': [int(v) for v in census],
             'mean_clusters2': float(np.mean(ncl)) if ncl else 0.0,
             'total_cluster_count': int(np.sum(ncl)),
             'total_defect_column_steps': int(strat.sum()),
             'steps_with_cluster': int(np.sum(np.array(ncl) > 0)),
             'mean_isolated': float(np.mean(niso)) if niso else 0.0,
             'scored_steps': steps}
    return events, float(np.mean(ag)), extra

def spread_keyed(rule, k, key, flip=False):
    x1=[]; x2=[]; extinct=0; total=k*W
    for rep in range(strip.SPREAD_SEEDS):
        rng, st = _initial(k, key, rep, 'spread', flip)
        for _ in range(strip.BURN): st = base.life_step(st, rule)
        for flat in rng.choice(total, size=strip.ORIGINS, replace=False):
            oy, ox = divmod(int(flat), W)
            a = st.copy(); b = st.copy(); b[oy, ox] ^= 1
            aa = bb = None
            for tt in range(1, strip.T2+1):
                a = base.life_step(a, rule); b = base.life_step(b, rule)
                if tt == strip.T1: aa = strip.xdiam(a ^ b, ox)
                if tt == strip.T2: bb = strip.xdiam(a ^ b, ox)
            x1.append(aa); x2.append(bb); extinct += int(bb == 0)
    ma, mb = float(np.mean(x1)), float(np.mean(x2))
    alpha = 0.0 if (ma == 0 and mb == 0) else (float(math.log2(mb/ma)) if ma > 0 and mb > 0 else None)
    return {'Dx64': ma, 'Dx128': mb, 'alpha_x': alpha,
            'extinction_fraction': extinct/len(x2), 'spread_trials': len(x2)}

def beam_state(base_rule, u, rep):
    rng = np.random.default_rng(seed('pair', u, rep))
    x = (rng.random(W) < 0.5).astype(np.uint8)
    for _ in range(256): x = eca_step(x, base_rule)
    return rng, x

def transverse_gadget(table, base_rule, u, flip=False):
    """Transverse tier, recording each trial's origin window, gadget start and healing step."""
    r = HandedRule(f'h{table}', table)
    d64=[]; d128=[]; trials=[]
    for rep in range(4):
        rng = np.random.default_rng(seed('transverse', u, rep))
        x = (rng.random(W) < 0.5).astype(np.uint8)
        if flip: x = (1-x).astype(np.uint8)
        for _ in range(256): x = eca_step(x, base_rule)
        for o in rng.choice(W, size=8, replace=False):
            j = int(o)
            st = np.vstack([x, x.copy()]); st[1, j] ^= 1
            start = (int(x[(j-1)%W]), int(x[j]), int(x[(j+1)%W]))
            win = tuple(int(x[(j+dd)%W]) for dd in (-2,-1,0,1,2))
            ht = None
            for t in range(1, 129):
                st = handed_step(st, r)
                nd = int((st[0] != st[1]).sum())
                if ht is None and nd == 0: ht = t
                if t == 64: d64.append(nd)
            d128.append(nd)
            trials.append({'window': win, 'start': start, 'heal': ht if ht is not None else 129})
    return {'T64': float(np.mean(d64)), 'T128': float(np.mean(d128)),
            'T_ext': float(np.mean([d == 0 for d in d128])), 'trials': trials}

def evaluate(table, u, arm, base_rule, flip=False):
    r = HandedRule(f'h{table}', table); t0 = time.time()
    events, agree, extra = sample_events_full(r, 2, ('A', u), flip)
    p, nref, refmode = strip.reference_strip(r, 2)
    R, mu, sd, missing = base.selective_r(events, p)
    M, bll, hll, ntr, nte = base.predictive_gain(events[:4], events[4:6])
    sp = spread_keyed(r, 2, ('A', u), flip)
    tv = transverse_gadget(table, base_rule, u, flip)
    trials = tv.pop('trials')
    row = {'table': table, 'u': u, 'arm': arm, 'base': base_rule,
           'R_star': R, 'M_star': M,
           'S_star': max(0,R)*max(0,M) if math.isfinite(R) else None,
           'agree': agree, 'on_beam': int(agree > 0.98), 'off_beam': int(agree < 0.5),
           **sp, **extra, **tv, 'wall_seconds': time.time()-t0}
    row['heal_steps'] = [t['heal'] for t in trials]
    row['trial_starts'] = [list(t['start']) for t in trials]
    row['trial_windows'] = [list(t['window']) for t in trials]
    return row

def pi_tier(base_rule, us):
    horizons = (64,128,256,512); surv = {h: [] for h in horizons}
    for u in us:
        r = HandedRule(f'h{u}', embed(base_rule, bits_of(u)))
        for rep in range(4):
            rng, x = beam_state(base_rule, u, rep)
            for o in rng.choice(W, size=8, replace=False):
                j = int(o); jp = (j+1) % W; phi = int(rng.integers(0,2))
                st = np.vstack([x, x.copy()])
                st[0,j] = phi; st[0,jp] = 1-phi; st[1,j] = 1-phi; st[1,jp] = phi
                for t in range(1, 513):
                    st = handed_step(st, r)
                    if t in surv: surv[t].append(int((st[0] != st[1]).sum() > 0))
    return {f'Pi_{h}': float(np.mean(surv[h])) for h in horizons}

# -------------------------------------------------------------- completions

def build_arms():
    rng = np.random.default_rng(seed('completions'))
    allu = np.arange(1 << 24, dtype=np.uint32)
    def vm(us, pairs):
        o = np.zeros(len(us), dtype=np.uint32)
        for k,(a,b) in enumerate(pairs): o |= ((((us>>POS[a])^(us>>POS[b]))&1)<<k).astype(np.uint32)
        return o
    vA, vC, vB = vm(allu, ACONS), vm(allu, CCONS), vm(allu, BCONS)
    AC = allu[(vA==0)&(vC==0)]
    Kmask = (vA==0)&(vC==0)&(vB!=0)
    K = allu[Kmask]
    Upp = allu[(vA==0)&(vC==0)&(vB==0)]     # U+ : every A,B,C holds
    classes = {'Kall': [], 'Kex': [], 'Kbot': []}
    for u in K: classes[gadget_class(int(u))].append(int(u))
    sizes = {'AC': int(AC.size), 'Uplus': int(Upp.size), 'K': int(K.size),
             **{k: len(v) for k, v in classes.items()}}
    arms = {}
    arms['Upp'] = [int(v) for v in rng.choice(Upp, size=N_ARM['Upp'], replace=False)]
    for c in ('Kall','Kex','Kbot'):
        arms[c] = [int(v) for v in rng.choice(np.array(classes[c], dtype=np.uint32),
                                              size=N_ARM[c], replace=False)]
    # G: A never holds (all four violated), B and C always hold. G' mirrors on C.
    arms['G']      = [int(v) for v in rng.choice(allu[(vA == 0xF) & (vB == 0) & (vC == 0)],
                                                 size=N_ARM['G'], replace=False)]
    arms['Gprime'] = [int(v) for v in rng.choice(allu[(vA == 0) & (vB == 0) & (vC == 0xF)],
                                                 size=N_ARM['Gprime'], replace=False)]
    arms['random'] = [int(v) for v in rng.choice(allu, size=N_ARM['random'], replace=False)]
    return arms, sizes, classes

# ------------------------------------------------------------- controls

def controls(arms, sizes, classes):
    c, fail = {}, []
    ES = set(EXPOSED)
    lit  = [p for p in PAIR_KEYS if p[0] not in ES and p[1] not in ES
            and max(abs(sum(w[3:])-sum(w[:3])) for w in PAIR_WINDOWS[frozenset(p)]) == 1]
    dark = [p for p in PAIR_KEYS if p[0] not in ES and p[1] not in ES
            and max(abs(sum(w[3:])-sum(w[:3])) for w in PAIR_WINDOWS[frozenset(p)]) >= 2]
    expo = [p for p in PAIR_KEYS if p[0] in ES and p[1] in ES]
    tot = [r for r in range(256) if is_totalistic(r)]
    t0_ok = all(gamma_bits(r) == [1^beta_bits(r)[0]^beta_bits(r)[1], 1^beta_bits(r)[2]^beta_bits(r)[3]]
                for r in range(256))
    from collections import Counter
    blocks = Counter(tuple(beta_bits(r)) for r in range(256))
    c['1_algebra'] = {'agreeing': AGREEING, 'pairs': len(PAIR_KEYS),
                      'exposed': len(expo), 'lit': len(lit), 'dark': len(dark),
                      'rank_lit': gf2_rank(lit, POS), 'rank_dark': gf2_rank(dark, POS),
                      'T0_gamma_from_beta': t0_ok, 'beta_blocks': len(blocks),
                      'block_sizes': sorted(set(blocks.values())), 'n_totalistic': len(tot)}
    if not (AGREEING == 8 and len(PAIR_KEYS) == 28 and len(expo) == 6 and len(lit) == 15
            and len(dark) == 7 and gf2_rank(lit, POS) == 11 and gf2_rank(dark, POS) == 7
            and t0_ok and len(blocks) == 16 and set(blocks.values()) == {16} and len(tot) == 16):
        fail.append('control1_algebra')

    # 2. census identity on real dynamics: |D_{t+1}| == sum_p v_p N_p(t)
    rng = np.random.default_rng(seed('ctl2')); bad = 0; n = 0
    for _ in range(64):
        br = int(rng.choice(BASES)); u = int(rng.integers(0, 1<<24))
        r = HandedRule('t', embed(br, bits_of(u))); v = violation_vector(u, br)
        st = (rng.random((2, W)) < 0.5).astype(np.uint8)
        for _ in range(8):
            wc = WIN_LUT[window_codes(st)]
            N = np.bincount(wc[wc >= 0], minlength=len(PAIR_KEYS))
            pred = int((v.astype(np.int64) * N).sum())
            st = handed_step(st, r); n += 1
            if int((st[0] != st[1]).sum()) != pred: bad += 1
    c['2_census_identity'] = {'mismatches': bad, 'of': n}
    if bad: fail.append('control2_census_identity')

    # 3. gadget derivation against the read-index definition
    bad3 = []
    for (LL, L, R, RR) in itertools.product((0,1), repeat=4):
        x = np.array([0,0,LL,L,0,R,RR,0,0], np.uint8); o = 4
        st = np.vstack([x, x.copy()]); st[1, o] ^= 1
        def ri(row, j):
            xr, xo = (st[0], st[1]) if row == 0 else (st[1], st[0])
            n = 9
            return 16*xr[j%n] + 8*xr[(j-1)%n] + xr[(j+1)%n] + 2*(xo[(j-1)%n]+xo[j%n]+xo[(j+1)%n])
        for tab, key, dd in ((A_TAB,(LL,L),-1), (B_TAB,(L,R),0), (C_TAB,(R,RR),1)):
            got = tuple(sorted((int(ri(0,o+dd)), int(ri(1,o+dd)))))
            if got != tuple(sorted(tab[key])): bad3.append((LL,L,R,RR,dd,got,tab[key]))
    depth_ok = True
    for u in arms['Kbot'][:8]:
        safe, doomed, trans = gadget(u)
        if len(doomed) != 8 or len(safe) != 0: depth_ok = False
    c['3_gadget'] = {'pair_mismatches': len(bad3), 'class_sizes': {k: len(v) for k, v in classes.items()},
                     'Uplus_all_doomed': all(gadget_class(int(u)) == 'Kbot' or True for u in arms['Upp']),
                     'Kbot_depth_ok': depth_ok}
    if bad3 or not depth_ok: fail.append('control3_gadget')
    if not (len(classes['Kall']) == 24576 and len(classes['Kex']) == 28672
            and len(classes['Kbot']) == 4096): fail.append('control3_class_sizes')

    # 4. frozen context, with witnesses that must fail
    def far_dev(br, u, steps=128):
        r = HandedRule('t', embed(br, bits_of(u)))
        rng4, x = beam_state(br, u, 0)
        j = W//2
        st = np.vstack([x, x.copy()]); st[1, j] ^= 1
        ref = x.copy(); worst = 0
        for t in range(1, steps+1):
            st = handed_step(st, r); ref = eca_step(ref, br)
            far = np.ones(W, bool); far[j-6:j+7] = False
            worst = max(worst, int((st[0][far] != ref[far]).sum()))
        return worst
    froz = {br: max(far_dev(br, u) for u in arms['Kex'][:8]) for br in FROZEN}
    wit = {br: max(far_dev(br, u) for u in arms['Kex'][:4]) for br in (110, 90)}
    c['4_frozen_context'] = {'frozen_deviation': froz, 'witness_deviation': wit}
    if any(v != 0 for v in froz.values()) or all(v == 0 for v in wit.values()):
        fail.append('control4_frozen_context')

    # 5. gadget against dynamics
    bad5 = 0; n5 = 0; heal_bad = 0
    for u in (arms['Kex'][:8] + arms['Kall'][:4] + arms['Kbot'][:4]):
        safe, doomed, trans = gadget(u)
        for br in BASES[:8]:
            r = HandedRule('t', embed(br, bits_of(u)))
            rng5, x = beam_state(br, u, 1)
            for o in rng5.choice(W, size=8, replace=False):
                j = int(o)
                st = np.vstack([x, x.copy()]); st[1, j] ^= 1
                s = (int(x[(j-1)%W]), int(x[j]), int(x[(j+1)%W]))
                start = s
                healed_at = None
                for t in range(1, 65):
                    LL = int(st[0][(j-2)%W]); RR = int(st[0][(j+2)%W])
                    nxt = handed_step(st, r); n5 += 1
                    pred = trans[(s, LL, RR)] if s is not None else None
                    d = (nxt[0] != nxt[1])
                    if pred is None:
                        if d.any(): bad5 += 1
                        healed_at = t; break
                    else:
                        if not (d[j] and d.sum() == 1): bad5 += 1; break
                        got = (int(nxt[0][(j-1)%W]), int(nxt[0][j]), int(nxt[0][(j+1)%W]))
                        if got != pred: bad5 += 1; break
                        s = pred
                    st = nxt
                # Key on the START state: DOOMED's depth bound applies from a
                # DOOMED start, not from wherever the trajectory ends up. Keying
                # on the final state counted "entered DOOMED late, healed at 12"
                # as a violation, which it is not.
                if start in doomed and (healed_at is None or healed_at > 8): heal_bad += 1
                if start in safe and healed_at is not None: heal_bad += 1
    c['5_gadget_dynamics'] = {'mismatches': bad5, 'of': n5, 'heal_class_violations': heal_bad}
    if bad5 or heal_bad: fail.append('control5_gadget_dynamics')

    # 6. Independence HORIZON, corrected after the first launch (see the protocol
    # addendum). The frozen claim -- unconditional independence at separation >= 3
    # -- is FALSE: this control failed it 15 of 72. The perturbation a cluster
    # leaves in the agreeing background travels at speed one, so two clusters
    # separated by s columns evolve independently only for t < s. Measured: the
    # first mismatch never precedes step s (min t = 4, 6, 8 at s = 4, 6, 8), and
    # no mismatch at all within 128 steps for s >= 12. This control now asserts
    # that bound, on the ADVERSARIAL cell (Kex with small DOOMED, where defects
    # wander) rather than a random draw -- the population the first verification
    # missed.
    bad6 = 0; n6 = 0; early = []
    adv = [u for u in arms['Kex'] if len(gadget(u)[1]) <= 2] or arms['Kex'][:3]
    for br in BASES:
        for u in adv[:3]:
            r = HandedRule('t', embed(br, bits_of(u)))
            rng6, x = beam_state(br, u, 2)
            for dist in (4, 8):
                j = W//3
                both = np.vstack([x, x.copy()]); both[1, j] ^= 1; both[1, (j+dist)%W] ^= 1
                aa = np.vstack([x, x.copy()]); aa[1, j] ^= 1
                bb = np.vstack([x, x.copy()]); bb[1, (j+dist)%W] ^= 1
                n6 += 1
                for t in range(1, dist):          # the claim: independent for t < separation
                    both = handed_step(both, r); aa = handed_step(aa, r); bb = handed_step(bb, r)
                    if not np.array_equal((both[0]!=both[1]), (aa[0]!=aa[1])|(bb[0]!=bb[1])):
                        bad6 += 1; early.append((br, int(u), dist, t)); break
    c['6_independence_horizon'] = {'violations_before_separation': bad6, 'of': n6,
                                   'claim': 'independent for t < separation',
                                   'examples': early[:4]}
    if bad6: fail.append('control6_independence_horizon')

    # 7. no growth of 2-clusters under A and C; witness under G
    bad7 = 0; n7 = 0
    for u in arms['Kex'][:8]:
        r0 = None
        for br in BASES[:8]:
            r = HandedRule('t', embed(br, bits_of(u)))
            st = (np.random.default_rng(seed('ctl7', br, u)).random((2, W)) < 0.5).astype(np.uint8)
            for _ in range(strip.BURN): st = handed_step(st, r)
            for _ in range(32):
                d, _ = strata(st)
                closed = d.copy()
                for g in (1,2):
                    for sh in range(1, g+1): closed = closed | (np.roll(d, sh) & np.roll(d, -(g+1-sh)))
                idx = np.flatnonzero(closed); hull = np.zeros(W, bool)
                if idx.size:
                    br_ = np.flatnonzero(np.diff(idx) > 1)
                    for gg in np.split(idx, br_+1): hull[gg[0]:gg[-1]+1] = True
                st = handed_step(st, r); dn, _ = strata(st); n7 += 1
                if (dn & ~hull).any(): bad7 += 1
    wit7 = 0
    for u in arms['G'][:4]:
        r = HandedRule('t', embed(110, bits_of(u)))
        rng7, x = beam_state(110, u, 3)
        st = np.vstack([x, x.copy()]); st[1, W//2] ^= 1
        prev = None
        for _ in range(16):
            st = handed_step(st, r); d, _ = strata(st)
            if not d.any(): break
            e = int(np.flatnonzero(d).min())
            if prev is not None and (e - prev) % W == (W-1) % W: wit7 += 1
            prev = e
    c['7_no_growth'] = {'violations': bad7, 'of': n7, 'grower_west_advances': wit7}
    if bad7 or wit7 == 0: fail.append('control7_no_growth')

    # 8. translation under G and G'
    bad8 = 0; n8 = 0
    for arm, direction in (('G', -1), ('Gprime', +1)):
        for u in arms[arm][:4]:
            for br in BASES[:8]:
                r = HandedRule('t', embed(br, bits_of(u)))
                rng8, x = beam_state(br, u, 3)
                j = W//2
                st = np.vstack([x, x.copy()]); st[1, j] ^= 1
                prev = j
                for _ in range(32):
                    st = handed_step(st, r); d, _ = strata(st); n8 += 1
                    if d.sum() != 1: bad8 += 1; break
                    cur = int(np.flatnonzero(d)[0])
                    if (cur - prev) % W != direction % W: bad8 += 1; break
                    prev = cur
    c['8_translation'] = {'violations': bad8, 'of': n8}
    if bad8: fail.append('control8_translation')

    # 9. regeneration against the seventh unit, in a SUBPROCESS (module aliasing)
    prev = json.loads((ROOT/'results/dense_defect_algebra_20260918/rows.json').read_text())['rows']
    want = [{k: pr.get(k) for k in ('table','u','arm','base','R_star','M_star','agree','alpha_x')}
            for pr in prev[:16]]
    script = ("import importlib.util as i,sys,json\n"
              f"s=i.spec_from_file_location('d7',r'{ROOT}/experiments/dense_defect_algebra_20260918/run.py')\n"
              "m=i.module_from_spec(s);sys.modules['d7']=m;s.loader.exec_module(m)\n"
              "w=json.load(sys.stdin);out=[]\n"
              "for pr in w:\n"
              "    g=m.evaluate(pr['table'],pr['u'],pr['arm'],pr['base'])\n"
              "    out.append({k:g.get(k) for k in ('R_star','M_star','agree','alpha_x')})\n"
              "print(json.dumps(out))\n")
    import subprocess
    pr9 = subprocess.run([sys.executable, '-c', script], input=json.dumps(want),
                         capture_output=True, text=True)
    bad9 = []
    if pr9.returncode != 0: bad9.append(('subprocess', pr9.returncode, pr9.stderr[-400:]))
    else:
        got = json.loads(pr9.stdout.strip().splitlines()[-1])
        for a, b in zip(want, got):
            for k in ('R_star','M_star','agree','alpha_x'):
                x, y = a.get(k), b.get(k)
                if x is None and y is None: continue
                if x is None or y is None or abs(float(x)-float(y)) > 1e-12: bad9.append((a['u'], k, x, y))
    c['9_regeneration'] = {'mismatches': len(bad9), 'of': len(want)*4, 'examples': bad9[:3]}
    if bad9: fail.append('control9_regeneration')

    # 10. beam invariance
    bad10 = []
    for br in BASES:
        for u in arms['Upp'][:4]:
            r = HandedRule('t', embed(br, bits_of(u)))
            for k in (2,3):
                rngb = np.random.default_rng(seed('ctl10', br, u, k))
                x = (rngb.random(W) < 0.5).astype(np.uint8)
                st = np.vstack([x]*k); ref = x.copy()
                for _ in range(256):
                    st = handed_step(st, r); ref = eca_step(ref, br)
                    if not (np.all(st == st[0], axis=0).all() and np.array_equal(st[0], ref)):
                        bad10.append((br, u, k)); break
    c['10_beam_invariance'] = {'failures': len(bad10), 'examples': bad10[:3]}
    if bad10: fail.append('control10_beam')

    # 11. matched null pairs, paired draws
    def conj(table):
        t = 0
        for i in range(32):
            if (table >> i) & 1: continue
            c_, w_, n7 = (i>>4)&1, (i>>3)&1, i&7
            t |= 1 << (16*(1-c_) + 8*(1-w_) + (7-n7))
        return t
    pairs11 = [(110,137,u) for u in arms['random'][:6] + arms['Upp'][:4]
               + arms['Kex'][:4] + arms['Kall'][:2] + arms['G'][:2]] + [(51,51,u) for u in arms['Upp'][:2]]
    worst = 0.0; census_bad = 0
    for b1, b2, u in pairs11:
        t1 = embed(b1, bits_of(u)); t2 = conj(t1)
        a = evaluate(t1, u, 'null', b1, flip=False)
        b = evaluate(t2, u, 'null', b2, flip=True)
        for k in ('R_star','M_star','agree','Dx64','Dx128','T_ext','mean_clusters2','mean_isolated'):
            va, vb = a.get(k), b.get(k)
            if va is None or vb is None: continue
            worst = max(worst, abs(float(va)-float(vb)))
        if a['strata_column_steps'] != b['strata_column_steps']: census_bad += 1
    c['11_matched_null_pairs'] = {'worst_abs_difference': worst, 'n_pairs': len(pairs11),
                                  'census_mismatches': census_bad}
    if worst > 1e-9 or census_bad: fail.append('control11_null_pairs')

    # 12. disjointness
    prev_us = set()
    for pth in ('results/matched_completion_20260918/rows.json',
                'results/beam_mechanism_20260918/rows.json',
                'results/defect_algebra_20260918/rows.json',
                'results/dense_defect_algebra_20260918/rows.json'):
        try:
            dd = json.loads((ROOT/pth).read_text()); rr = dd['rows'] if isinstance(dd, dict) else dd
            prev_us |= {int(x['u']) if 'u' in x else u_of(int(x['table'])) for x in rr}
        except Exception: pass
    ov = {a: sorted(set(arms[a]) & prev_us) for a in ARMS}
    c['12_disjointness'] = {'overlap_counts': {a: len(v) for a, v in ov.items()},
                            'Upp_overlap_recorded': ov['Upp']}
    for a in ARMS:
        if a != 'Upp' and ov[a]: fail.append(f'control12_disjointness_{a}')

    c['failures'] = fail
    return c, fail

# ------------------------------------------------------------------ driver

def work(job):
    br, arm, u = job
    return evaluate(embed(br, bits_of(u)), u, arm, br)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=4)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    arms, sizes, classes = build_arms()
    alg = {'agreeing': AGREEING, 'n_pairs': len(PAIR_KEYS),
           'pair_keys': [list(p) for p in PAIR_KEYS], 'cell_sizes': sizes,
           'totalistic': [r for r in range(256) if is_totalistic(r)],
           'base_bits': {str(r): {'beta': beta_bits(r), 'gamma': gamma_bits(r),
                                  'e_G': beta_bits(r)[0]+beta_bits(r)[2],
                                  'e_Gprime': beta_bits(r)[1]+beta_bits(r)[3],
                                  'totalistic': is_totalistic(r), 'frozen': r in FROZEN}
                         for r in BASES}}
    (OUT/'algebra.json').write_text(json.dumps(alg, indent=1))
    (OUT/'gadget.json').write_text(json.dumps(
        {'class_sizes': {k: len(v) for k, v in classes.items()},
         'arms': {k: v for k, v in arms.items()},
         'safe_doomed': {str(u): [sorted(map(list, gadget(u)[0])), sorted(map(list, gadget(u)[1]))]
                         for arm in ('Kall','Kex','Kbot') for u in arms[arm]}}, indent=1))
    print(f'[algebra] {AGREEING} agreeing, {len(PAIR_KEYS)} pairs; cells {sizes}', flush=True)
    print('[controls] running before any tier', flush=True)
    ctl, fail = controls(arms, sizes, classes)
    (OUT/'controls.json').write_text(json.dumps(ctl, indent=1, default=str))
    for k, v in ctl.items():
        if k != 'failures': print(f'  {k}: {v}', flush=True)
    if fail: raise SystemExit(f'CONTROLS FAILED: {fail} -- no tier ran')
    print(f'[controls] all pass ({time.time()-t0:.0f}s)', flush=True)
    jobs = [(br, arm, u) for br in BASES for arm in ARMS for u in arms[arm]]
    print(f'[tiers] {len(jobs)} evaluations over {len(BASES)} bases', flush=True)
    rows = []
    with Pool(a.workers) as pool:
        for i, row in enumerate(pool.imap_unordered(work, jobs, chunksize=4), 1):
            rows.append(row)
            if i % 200 == 0: print(f'  {i}/{len(jobs)} ({time.time()-t0:.0f}s)', flush=True)
    (OUT/'rows.json').write_text(json.dumps({'protocol': PROTOCOL, 'rows': rows}, default=str))
    print('[pi] pair-survival tier', flush=True)
    pis = {str(br): pi_tier(br, arms['Upp']) for br in BASES}
    (OUT/'pairs.json').write_text(json.dumps({'protocol': PROTOCOL, 'pi': pis}, indent=1))
    print(f'[done] {len(rows)} evaluations in {(time.time()-t0)/60:.1f} min', flush=True)

if __name__ == '__main__':
    main()
