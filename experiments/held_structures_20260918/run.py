#!/usr/bin/env python3
"""Held structures: the structural census, the six-bit gadget and the edge automaton.

Frozen protocol: docs/research/protocols/2026-09-18-held-structures.md
(committed before this implementation).

Each of the 28 read-pairs is read by exactly one local defect structure, decided
by the column's two junctions. The stratum partition of the previous two units
cuts THROUGH those structures: the lit stratum holds both singletons (every
column completion-held) and the interiors of alternating runs (which exist only
while base-held edges shield them). The structural census is therefore the pair
census grouped by structure -- one classifier, not two that could drift.

Controls 1-14 run BEFORE any tier and raise. Control 14 is the rule earned from
PR #278: the evaluator's scored key set must equal the protocol's frozen list.

Measurement helpers are COPIED from the eighth unit with this protocol's seed
function, never imported.

    python experiments/held_structures_20260918/run.py --workers 4
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools, json, math, re, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('bm', ROOT / 'experiments/beam_mechanism_20260918/run.py')
bm = importlib.util.module_from_spec(spec); sys.modules['bm'] = bm; spec.loader.exec_module(bm)
hf, base, strip = bm.hf, bm.base, bm.strip
HandedRule, handed_step, embed, eca_step = hf.HandedRule, hf.handed_step, hf.embed, bm.eca_step
EXPOSED, FREE = hf.EXPOSED, hf.FREE
POS = {e: i for i, e in enumerate(FREE)}

PROTOCOL = 'held-structures-20260918'
PROTOCOL_FILE = ROOT / 'docs/research/protocols/2026-09-18-held-structures.md'
OUT = ROOT / 'results/held_structures_20260918'
W = strip.WIDTH
DENSITY = 0.5

BLOCK0 = [36, 37, 50, 51, 76, 77, 90, 91, 164, 165, 178, 179, 204, 205, 218, 219]
PANEL = BLOCK0 + [0, 22, 232, 8, 30, 110, 27, 26, 45, 59, 177, 89, 163, 5, 18, 54, 33]
BASES = PANEL
PAIR_PERMANENT = [50, 51, 76, 77, 178, 179, 204, 205]
CENTRE_ONLY = [0, 51, 204, 255]
FROZEN_ANCHORS = [204, 51, 0, 8]
ARMS = ['Kall_plus', 'Kall_minus', 'Kex', 'Uplus', 'G', 'random']
N_ARM = {'Kall_plus': 12, 'Kall_minus': 8, 'Kex': 16, 'Uplus': 4, 'G': 8, 'random': 16}

A_TAB = {(0,0):(1,2), (0,1):(19,20), (1,0):(11,12), (1,1):(29,30)}
B_TAB = {(0,0):(2,16), (0,1):(5,19), (1,0):(12,26), (1,1):(15,29)}
C_TAB = {(0,0):(2,8),  (0,1):(5,11), (1,0):(20,26), (1,1):(23,29)}
ACONS = [A_TAB[k] for k in sorted(A_TAB)]
BCONS = [B_TAB[k] for k in sorted(B_TAB)]
CCONS = [C_TAB[k] for k in sorted(C_TAB)]
ALPHA = {0: [1,2,8], 1: [5,11,12], 2: [19,20,26], 3: [23,29,30]}

def seed(*parts):
    h = hashlib.sha256('|'.join(map(str, (PROTOCOL,) + parts)).encode()).digest()
    return int.from_bytes(h[:8], 'little') & 0x7fff_ffff_ffff_ffff

def bits_of(u): return [(u >> i) & 1 for i in range(24)]
def u_of(table): return sum(((table >> e) & 1) << POS[e] for e in FREE)
def tab_of_u(u):
    t = [0]*32
    for e in FREE: t[e] = (int(u) >> POS[e]) & 1
    return t

# ------------------------------------------- the structural dictionary (T1)

def idx_of(own, other):
    L, C, R = own
    return 16*C + 8*L + R + 2*sum(other)

def classify_window(w):
    """The local structure that reads this six-bit window's centre column."""
    r0, r1 = w[:3], w[3:]
    d = [r0[k] != r1[k] for k in range(3)]
    if not d[1]:
        if not d[0] and not d[2]: return 'agreeing'
        if d[0] and d[2]:         return 'one_gap'            # between two defects
        return 'flank'                                        # A (east of nothing) or C
    left  = 'edge' if not d[0] else ('alt' if r0[0] != r0[1] else 'same')
    right = 'edge' if not d[2] else ('alt' if r0[1] != r0[2] else 'same')
    if left == 'edge' and right == 'edge': return 'singleton'
    if left == 'edge':  return 'alt_edge_w' if right == 'alt' else 'inphase_edge_w'
    if right == 'edge': return 'alt_edge_e' if left  == 'alt' else 'inphase_edge_e'
    if left == 'alt' or right == 'alt':    return 'alt_interior'
    return 'inphase_interior'

def derive_dictionary():
    pw = {}
    for w in itertools.product((0,1), repeat=6):
        r0, r1 = w[:3], w[3:]
        i0, i1 = idx_of(r0, r1), idx_of(r1, r0)
        if i0 == i1: continue
        pw.setdefault(tuple(sorted((i0, i1))), []).append(w)
    keys = sorted(pw)
    struct = {}
    multi = 0
    for p, ws in pw.items():
        kinds = {classify_window(w) for w in ws}
        if len(kinds) > 1: multi += 1
        struct[p] = sorted(kinds)[0]
    return keys, struct, multi, pw

PAIR_KEYS, PAIR_STRUCT, DICT_MULTI, PAIR_WINDOWS = derive_dictionary()
PAIR_INDEX = {p: i for i, p in enumerate(PAIR_KEYS)}
STRUCTS = ['singleton', 'alt_interior', 'inphase_interior', 'alt_edge_w', 'alt_edge_e',
           'inphase_edge_w', 'inphase_edge_e', 'flank', 'one_gap']
STRUCT_OF_PAIR = np.array([STRUCTS.index(PAIR_STRUCT[p]) for p in PAIR_KEYS], dtype=np.int8)
# blind = the base-held structures; the rest are completion-held
BLIND_STRUCTS = {'alt_edge_w', 'alt_edge_e'}
NONBLIND_DEFECT = {'singleton', 'alt_interior', 'inphase_interior',
                   'inphase_edge_w', 'inphase_edge_e'}

WIN_LUT = np.full(64, -1, dtype=np.int16)
for w in itertools.product((0,1), repeat=6):
    r0, r1 = w[:3], w[3:]
    i0, i1 = idx_of(r0, r1), idx_of(r1, r0)
    code = (w[0]<<5)|(w[1]<<4)|(w[2]<<3)|(w[3]<<2)|(w[4]<<1)|w[5]
    if i0 != i1: WIN_LUT[code] = PAIR_INDEX[tuple(sorted((i0, i1)))]

def gf2_rank(pairs):
    rows = [(1 << POS[a]) | (1 << POS[b]) for a, b in pairs]
    basis, r = [], 0
    for v in rows:
        for bv in basis: v = min(v, v ^ bv)
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
def is_pair_permanent(r):
    e = lambda i: (r >> i) & 1
    return e(1) == e(4) == e(5) and e(2) == e(3) == e(6) and e(1) != e(2)
def matching_pattern(r): return (1 - eca_out(r,0,1,0), 1 - eca_out(r,1,0,1))
def is_centre_only(r): return all(eca_out(r,L,C,0) == eca_out(r,L,C,1)
                                  for L in (0,1) for C in (0,1)) and \
                              all(eca_out(r,0,C,R) == eca_out(r,1,C,R)
                                  for C in (0,1) for R in (0,1))

# ------------------------------------------------------- the six-bit gadget

SIX = [1, 5, 19, 23, 15, 16]
def gadget(u):
    t = tab_of_u(u)
    a = lambda LL, L: t[A_TAB[(LL,L)][0]]
    c = lambda R, RR: t[C_TAB[(R,RR)][0]]
    Bh = {(L,R): t[B_TAB[(L,R)][0]] == t[B_TAB[(L,R)][1]] for L in (0,1) for R in (0,1)}
    S = [(L,b,R) for L in (0,1) for b in (0,1) for R in (0,1)]
    trans = {}
    for s in S:
        L, b, R = s
        for LL in (0,1):
            for RR in (0,1):
                if Bh[(L,R)]: trans[(s,LL,RR)] = None
                else:
                    lo, hi = B_TAB[(L,R)]
                    trans[(s,LL,RR)] = (a(LL,L), t[lo] if b == 0 else t[hi], c(R,RR))
    dm = set()
    while True:
        add = {s for s in S if s not in dm and all(trans[(s,LL,RR)] is None or trans[(s,LL,RR)] in dm
                                                   for LL in (0,1) for RR in (0,1))}
        if not add: break
        dm |= add
    sf = set(S)
    while True:
        rm = {s for s in sf if any(trans[(s,LL,RR)] is None or trans[(s,LL,RR)] not in sf
                                   for LL in (0,1) for RR in (0,1))}
        if not rm: break
        sf -= rm
    return sf, dm, trans

def gadget_class(u):
    sf, dm, _ = gadget(u)
    if len(sf) > 0: return 'Kall'
    if len(dm) == 8: return 'Kbot'
    return 'Kex'

def six_type(u):
    t = tab_of_u(u); return tuple(t[b] for b in SIX)
def alphas(u):
    t = tab_of_u(u); return t[5], t[19]

# ------------------------------------------------ census, runs, structures

def defects(st): return (st[0] != st[1])

def window_codes(st):
    x0, x1 = st[0].astype(np.int16), st[1].astype(np.int16)
    return ((np.roll(x0,1)<<5) | (x0<<4) | (np.roll(x0,-1)<<3)
            | (np.roll(x1,1)<<2) | (x1<<1) | np.roll(x1,-1))

def structural_census(st):
    wc = WIN_LUT[window_codes(st)]
    ok = wc >= 0
    pc = np.bincount(wc[ok], minlength=len(PAIR_KEYS))
    out = np.zeros(len(STRUCTS), dtype=np.int64)
    for i, n in enumerate(pc):
        if n: out[STRUCT_OF_PAIR[i]] += n
    return pc, out

def runs_of(d, allow_gap=0):
    if not d.any(): return []
    closed = d.copy()
    for g in range(1, allow_gap+1):
        for s in range(1, g+1):
            closed = closed | (np.roll(d, s) & np.roll(d, -(g+1-s)))
    idx = np.flatnonzero(closed)
    if idx.size == 0: return []
    br = np.flatnonzero(np.diff(idx) > 1)
    return [(int(g[0]), int(g[-1])) for g in np.split(idx, br+1)]

def run_census(st):
    d = defects(st); x0 = st[0]
    out = {'n_runs': 0, 'n_isolated': 0, 'widths': [], 'alt': 0, 'inphase': 0, 'mixed': 0}
    for lo, hi in runs_of(d):
        out['n_runs'] += 1; out['widths'].append(hi-lo+1)
        if all(not d[(lo-k) % W] for k in (1,2)) and all(not d[(hi+k) % W] for k in (1,2)):
            out['n_isolated'] += 1
        js = {('alt' if x0[j % W] != x0[(j+1) % W] else 'same') for j in range(lo, hi)}
        out['alt' if js == {'alt'} else ('inphase' if js == {'same'} else 'mixed')] += 1
    return out

def isolated_structures(st):
    """Isolated runs with their kind and, for singletons, the gadget state."""
    d = defects(st); x0 = st[0]; out = []
    for lo, hi in runs_of(d):
        if not (all(not d[(lo-k) % W] for k in (1,2)) and all(not d[(hi+k) % W] for k in (1,2))):
            continue
        width = hi - lo + 1
        if width == 1:
            out.append(('singleton', lo, hi,
                        (int(x0[(lo-1) % W]), int(x0[lo]), int(x0[(lo+1) % W]))))
        else:
            js = {('alt' if x0[j % W] != x0[(j+1) % W] else 'same') for j in range(lo, hi)}
            kind = 'alt_run' if js == {'alt'} else ('inphase_run' if js == {'same'} else 'mixed_run')
            out.append((kind, lo, hi, None))
    return out

# ------------------------------------------- measurement helpers (COPIED)

def _initial(k, key, rep, kind, flip):
    rng = np.random.default_rng(seed(kind, *key, k, DENSITY, rep))
    st = (rng.random((k, W)) < DENSITY).astype(np.uint8)
    if flip: st = (1 - st).astype(np.uint8)
    return rng, st

def sample_events_struct(rule, k, key, flip=False):
    events = []; total = k * W; ag = []
    struct = np.zeros(len(STRUCTS), dtype=np.int64)
    census = np.zeros(len(PAIR_KEYS), dtype=np.int64)
    psurv = np.zeros(len(PAIR_KEYS), dtype=np.int64)
    tot_def = 0
    runs = {'n_runs': 0, 'n_isolated': 0, 'alt': 0, 'inphase': 0, 'mixed': 0}
    widths = []; steps = 0; snap = {}
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
        for t in range(strip.SCORE):
            ag.append(float(np.all(st == st[0], axis=0).mean()))
            pc, sc = structural_census(st); struct += sc; census += pc; steps += 1
            if rep == 0:
                rc = run_census(st)
                for k2 in ('n_runs','n_isolated','alt','inphase','mixed'): runs[k2] += rc[k2]
                widths.extend(rc['widths'])
                if t in (0, strip.SCORE-1):
                    snap[str(t)] = [(kind, lo, hi, gs) for kind, lo, hi, gs in isolated_structures(st)]
            d = defects(st)
            cur = st[ys, xs].copy(); hist = ((hist << 1) | cur) & 0xff
            sym = base.life_symbols(st, ys, xs); nxt = base.life_step(st, rule)
            dn = defects(nxt)
            tot_def += int(d.sum())
            wc = WIN_LUT[window_codes(st)]
            psurv += np.bincount(wc[(wc >= 0) & dn], minlength=len(PAIR_KEYS))
            cc.append(cur); hh.append(hist.copy()); yy.append(nxt[ys, xs].copy()); zz.append(sym)
            st = nxt
        events.append({'current': np.concatenate(cc), 'history': np.concatenate(hh),
                       'target': np.concatenate(yy), 'symbol': np.concatenate(zz)})
    surv = np.zeros(len(STRUCTS), dtype=np.int64)
    for i, n in enumerate(psurv): surv[STRUCT_OF_PAIR[i]] += n
    extra = {'structural_census': [int(v) for v in struct],
             'structural_survival': [int(v) for v in surv],
             'pair_census': [int(v) for v in census],
             'pair_survival': [int(v) for v in psurv],
             'total_defect_column_steps': int(tot_def),
             'run_census': {k2: int(v) for k2, v in runs.items()},
             'mean_width': float(np.mean(widths)) if widths else 0.0,
             'isolated_snapshots': snap, 'scored_steps': steps}
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

def free_stream(base_rule, u, rep, origin, steps=128):
    """The unperturbed beam's j-2 and j+2 columns -- base-only, so cached per key."""
    rng = np.random.default_rng(seed('transverse', u, rep))
    x = (rng.random(W) < 0.5).astype(np.uint8)
    for _ in range(256): x = eca_step(x, base_rule)
    out = []
    for _ in range(steps):
        x = eca_step(x, base_rule)
        out.append((int(x[(origin-2) % W]), int(x[(origin+2) % W])))
    return out

def gadget_heal(trans, start, stream):
    """Iterate the isolated-defect gadget on an observed 2-bit input stream.

    Returns (healing step or None, steps simulated). `stream` is the sequence of
    (LL, RR) the automaton reads; the free-stream version feeds the UNPERTURBED
    beam's columns, the driven version the perturbed strip's own.
    """
    s = start
    for t, (LL, RR) in enumerate(stream, 1):
        nx = trans.get((s, LL, RR))
        if nx is None: return t, t
        s = nx
    return None, len(stream)

def transverse_streams(table, base_rule, u, flip=False):
    """Transverse trials with BOTH input streams and the gadget's two predictions.

    The free stream is the unperturbed beam under the base ECA -- a base-only
    object, so it is computed once per rep and read per origin. The driven stream
    is what the perturbed strip actually presents. P4 asks whether the free one
    suffices; the divergence step is recorded either way.
    """
    r = HandedRule(f'h{table}', table)
    _, _, trans = gadget(u)
    d64=[]; d128=[]; trials=[]
    for rep in range(4):
        rng = np.random.default_rng(seed('transverse', u, rep))
        x = (rng.random(W) < 0.5).astype(np.uint8)
        if flip: x = (1-x).astype(np.uint8)
        for _ in range(256): x = eca_step(x, base_rule)
        free = np.empty((128, W), dtype=np.uint8); fx = x.copy()
        for t in range(128):
            fx = eca_step(fx, base_rule); free[t] = fx
        for o in rng.choice(W, size=8, replace=False):
            j = int(o)
            st = np.vstack([x, x.copy()]); st[1, j] ^= 1
            start = (int(x[(j-1)%W]), int(x[j]), int(x[(j+1)%W]))
            win = tuple(int(x[(j+dd)%W]) for dd in (-2,-1,0,1,2))
            ht = None; driven = []
            for t in range(1, 129):
                st = handed_step(st, r)
                driven.append((int(st[0][(j-2)%W]), int(st[0][(j+2)%W])))
                nd = int(defects(st).sum())
                if ht is None and nd == 0: ht = t
                if t == 64: d64.append(nd)
            d128.append(nd)
            fs = [(int(free[t][(j-2)%W]), int(free[t][(j+2)%W])) for t in range(128)]
            div = next((t+1 for t in range(128) if fs[t] != driven[t]), None)
            hd, _ = gadget_heal(trans, start, driven)
            hf_, _ = gadget_heal(trans, start, fs)
            trials.append({'origin': j, 'window': list(win), 'start': list(start),
                           'heal': ht if ht is not None else 129,
                           'heal_driven_pred': hd if hd is not None else 129,
                           'heal_free_pred': hf_ if hf_ is not None else 129,
                           'stream_divergence': div if div is not None else 129,
                           'rep': rep})
    return {'T64': float(np.mean(d64)), 'T128': float(np.mean(d128)),
            'T_ext': float(np.mean([d == 0 for d in d128])),
            'T_ext_free_pred': float(np.mean([t['heal_free_pred'] <= 128 for t in trials])),
            'T_ext_driven_pred': float(np.mean([t['heal_driven_pred'] <= 128 for t in trials])),
            'trials': trials}

def evaluate(table, u, arm, base_rule, flip=False):
    r = HandedRule(f'h{table}', table); t0 = time.time()
    events, agree, extra = sample_events_struct(r, 2, ('A', u), flip)
    p, nref, refmode = strip.reference_strip(r, 2)
    R, mu, sd, missing = base.selective_r(events, p)
    M, bll, hll, ntr, nte = base.predictive_gain(events[:4], events[4:6])
    sp = spread_keyed(r, 2, ('A', u), flip)
    tv = transverse_streams(table, base_rule, u, flip)
    trials = tv.pop('trials')
    sf, dm, _ = gadget(u)
    row = {'table': table, 'u': u, 'arm': arm, 'base': base_rule,
           'R_star': R, 'M_star': M, 'agree': agree,
           'on_beam': int(agree > 0.98), 'off_beam': int(agree < 0.5),
           'n_safe': len(sf), 'n_doomed': len(dm), 'six_type': list(six_type(u)),
           'alphas': list(alphas(u)), 'gadget_class': gadget_class(u),
           **sp, **extra, **tv, 'trials': trials, 'wall_seconds': time.time()-t0}
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
                    if t in surv: surv[t].append(int(defects(st).sum() > 0))
    return {f'Pi_{h}': float(np.mean(surv[h])) for h in horizons}

# -------------------------------------------------------------- completions

def build_arms():
    rng = np.random.default_rng(seed('completions'))
    allu = np.arange(1 << 24, dtype=np.uint32)
    def vm(us, ps):
        o = np.zeros(len(us), dtype=np.uint32)
        for k,(a,b) in enumerate(ps): o |= ((((us>>POS[a])^(us>>POS[b]))&1)<<k).astype(np.uint32)
        return o
    vA, vB, vC = vm(allu, ACONS), vm(allu, BCONS), vm(allu, CCONS)
    AC = (vA == 0) & (vC == 0)
    K = allu[AC & (vB != 0)]
    Uplus = allu[AC & (vB == 0)]
    cls = {'Kall': [], 'Kex': [], 'Kbot': []}
    for u in K: cls[gadget_class(int(u))].append(int(u))
    sizes = {'AC': int(AC.sum()), 'Uplus': int(Uplus.size), 'K': int(K.size),
             **{k: len(v) for k, v in cls.items()}}
    # B01 holds  <=>  alpha1 == alpha2
    kall = np.array(cls['Kall'], dtype=np.uint32)
    a1 = ((kall >> POS[5]) & 1); a2 = ((kall >> POS[19]) & 1)
    arms = {}
    plus01 = kall[(a1 == 0) & (a2 == 1)]; plus10 = kall[(a1 == 1) & (a2 == 0)]
    arms['Kall_plus'] = ([int(v) for v in rng.choice(plus01, size=6, replace=False)]
                         + [int(v) for v in rng.choice(plus10, size=6, replace=False)])
    arms['Kall_minus'] = [int(v) for v in rng.choice(kall[a1 == a2], size=8, replace=False)]
    kex = np.array(cls['Kex'], dtype=np.uint32)
    small = np.array([u for u in cls['Kex'] if len(gadget(u)[1]) <= 2], dtype=np.uint32)
    rest = np.array([u for u in cls['Kex'] if len(gadget(u)[1]) > 2], dtype=np.uint32)
    arms['Kex'] = ([int(v) for v in rng.choice(small, size=4, replace=False)]
                   + [int(v) for v in rng.choice(rest, size=12, replace=False)])
    arms['Uplus'] = [int(v) for v in rng.choice(Uplus, size=4, replace=False)]
    arms['G'] = [int(v) for v in rng.choice(allu[(vA == 0xF) & (vB == 0) & (vC == 0)],
                                            size=8, replace=False)]
    arms['random'] = [int(v) for v in rng.choice(allu, size=16, replace=False)]
    arms['pi'] = [int(v) for v in rng.choice(Uplus, size=8, replace=False)]
    return arms, sizes, cls

def frozen_keys():
    """Parse the protocol's machine-readable frozen prediction list (control 14)."""
    txt = PROTOCOL_FILE.read_text()
    m = re.search(r'```frozen-prediction-keys\n(.*?)\n```', txt, re.S)
    if not m: raise SystemExit('control14: no frozen-prediction-keys block in the protocol')
    return sorted(m.group(1).split())

# ------------------------------------------------------------- controls

DEFECT_STRUCTS = ['singleton','alt_interior','inphase_interior',
                  'alt_edge_w','alt_edge_e','inphase_edge_w','inphase_edge_e']
def struct_idx(name): return STRUCTS.index(name)

def controls(arms, sizes, cls, workers=4):
    c, fail = {}, []

    # 1. algebra and dictionary, asserted
    lit  = [p for p in PAIR_KEYS if p[0] in set(FREE) and p[1] in set(FREE)
            and max(abs(sum(w[3:])-sum(w[:3])) for w in PAIR_WINDOWS[p]) == 1]
    dark = [p for p in PAIR_KEYS if p[0] in set(FREE) and p[1] in set(FREE)
            and max(abs(sum(w[3:])-sum(w[:3])) for w in PAIR_WINDOWS[p]) >= 2]
    types = {}
    rng1 = np.random.default_rng(seed('ctl1'))
    allK = cls['Kall'] + cls['Kex'] + cls['Kbot']
    for u in rng1.choice(np.array(allK, dtype=np.uint32), size=4000, replace=False):
        types.setdefault(six_type(int(u)), set()).add(gadget_class(int(u)))
    flankbad = 0
    for u in rng1.choice(np.array(allK, dtype=np.uint32), size=800, replace=False):
        t = tab_of_u(int(u))
        for cl in ALPHA.values():
            if len({t[i] for i in cl}) != 1: flankbad += 1
    c['1_algebra'] = {'dictionary_multi': DICT_MULTI, 'n_pairs': len(PAIR_KEYS),
                      'n_lit': len(lit), 'n_dark': len(dark),
                      'rank_lit': gf2_rank(lit), 'rank_dark': gf2_rank(dark),
                      'six_types_seen': len(types),
                      'types_mixed_class': sum(1 for v in types.values() if len(v) > 1),
                      'flank_class_violations': flankbad,
                      'pair_permanent': [r for r in range(256) if is_pair_permanent(r)],
                      'n_totalistic': sum(1 for r in range(256) if is_totalistic(r)),
                      'block0_size': len(BLOCK0), 'cell_sizes': sizes}
    if not (DICT_MULTI == 0 and len(PAIR_KEYS) == 28 and len(lit) == 15 and len(dark) == 7
            and gf2_rank(lit) == 11 and gf2_rank(dark) == 7 and flankbad == 0
            and sum(1 for v in types.values() if len(v) > 1) == 0
            and [r for r in range(256) if is_pair_permanent(r)] == PAIR_PERMANENT
            and len(BLOCK0) == 16 and sizes['Kall'] == 24576 and sizes['Kex'] == 28672
            and sizes['Kbot'] == 4096):
        fail.append('control1_algebra')

    # 2. structural census identity on real dynamics
    rng = np.random.default_rng(seed('ctl2')); bad = 0; n = 0
    for _ in range(48):
        br = int(rng.choice(BASES)); u = int(rng.integers(0, 1<<24))
        t = [(embed(br, bits_of(u)) >> i) & 1 for i in range(32)]
        v = np.array([int(t[a] != t[b]) for (a, b) in PAIR_KEYS], dtype=np.int64)
        r = HandedRule('t', embed(br, bits_of(u)))
        st = (rng.random((2, W)) < 0.5).astype(np.uint8)
        for _ in range(6):
            pc, sc = structural_census(st)
            pred = int((v * pc).sum())
            st = handed_step(st, r); n += 1
            if int(defects(st).sum()) != pred: bad += 1
    c['2_census_identity'] = {'mismatches': bad, 'of': n}
    if bad: fail.append('control2_census')

    # 3. position lock on the adversarial cell, with a witness that must fail
    def lock_violations(bases, us, acfree=False):
        moved = 0; tracked = 0
        for br in bases:
            for u in us:
                r = HandedRule('t', embed(br, bits_of(u)))
                st = (np.random.default_rng(seed('ctl3', br, u)).random((2, W)) < 0.5).astype(np.uint8)
                for _ in range(strip.BURN): st = handed_step(st, r)
                prev = {(lo, hi) for _, lo, hi, _ in isolated_structures(st)}
                for _ in range(48):
                    st = handed_step(st, r)
                    cur = {(lo, hi) for _, lo, hi, _ in isolated_structures(st)}
                    nxt = set()
                    for (lo, hi) in prev:
                        tracked += 1
                        inside = [x for x in cur if x[0] >= lo and x[1] <= hi]
                        if inside: nxt.add(inside[0])
                        else:
                            over = [x for x in cur if not (x[1] < lo-2 or x[0] > hi+2)]
                            if over: moved += 1
                    prev = nxt
        return moved, tracked
    smallD = [u for u in arms['Kex'][:4]]
    mv, tr = lock_violations([90, 91, 218, 219, 37, 110, 30], smallD)
    rngw = np.random.default_rng(seed('ctl3w'))
    wmv, wtr = lock_violations([90, 110], [int(rngw.integers(0, 1<<24)) for _ in range(3)])
    c['3_position_lock'] = {'violations': mv, 'tracked': tr,
                            'witness_violations': wmv, 'witness_tracked': wtr}
    if mv or wmv == 0: fail.append('control3_position_lock')

    # 4. edge automaton, BOTH branches, with an exercise assertion (amended)
    alt_err = same_err = 0; alt_n = same_n = 0
    rng4 = np.random.default_rng(seed('ctl4'))
    cand = arms['Kall_plus'] + arms['Kall_minus'] + arms['Kex']
    for br in [50, 51, 76, 204, 205, 178, 90, 91, 37, 0, 22, 110]:
        for u in cand[:12]:
            t = tab_of_u(u); a1, a2 = t[5], t[19]
            r = HandedRule('t', embed(br, bits_of(u)))
            rng5, x = beam_state(br, u, 0)
            for width in (3,4,5,6,7,8):
                j0 = (W//3 + 13*width) % W
                st = np.vstack([x, x.copy()])
                for k2 in range(width):
                    st[0,(j0+k2)%W] = k2 % 2; st[1,(j0+k2)%W] = 1-(k2 % 2)
                lo = j0
                for _ in range(24):
                    d = defects(st)
                    if not d.any(): break
                    rs = [g for g in runs_of(d) if g[0] <= lo <= g[1]]
                    if not rs: break
                    lo, hi = rs[0]
                    if hi - lo + 1 < 3: break
                    L = int(st[0][(lo-1)%W]); LL = int(st[0][(lo-2)%W]); a = int(st[0][lo])
                    jn = 'alt' if st[0][lo] != st[0][(lo+1)%W] else 'same'
                    nxt = handed_step(st, r); dn = defects(nxt)
                    if jn == 'alt':
                        alt_n += 1
                        surv_p = eca_out(br,L,a,1-a) != eca_out(br,L,1-a,a)
                        if bool(dn[lo]) != surv_p: alt_err += 1
                        elif surv_p:
                            if int(nxt[0][lo]) != eca_out(br,L,a,1-a): alt_err += 1
                            elif int(nxt[0][(lo-1)%W]) != t[A_TAB[(LL,L)][0]]: alt_err += 1
                    else:
                        same_n += 1
                        pair = (4,17) if L == 0 else (14,27)
                        surv_p = t[pair[0]] != t[pair[1]]
                        if bool(dn[lo]) != surv_p: same_err += 1
                    st = nxt
    c['4_edge_automaton'] = {'alt_steps': alt_n, 'alt_errors': alt_err,
                             'same_steps': same_n, 'same_errors': same_err,
                             'same_branch_exercised_at_least_50': same_n >= 50}
    if alt_err or same_err or same_n < 50: fail.append('control4_edge_automaton')

    # 5. permanent runs; witness on JUNCTION TYPE (amended)
    kept = 0; tot = 0; conv = 0; convtot = 0
    for br in PAIR_PERMANENT:
        want = matching_pattern(br)
        for label, pat in (('match', want), ('opp', (1-want[0], 1-want[1]))):
            us = [u for u in cls['Kall'] + cls['Kex'] if alphas(u) == pat][:3]
            for u in us:
                r = HandedRule('t', embed(br, bits_of(u)))
                rng6, x = beam_state(br, u, 0)
                for width in range(2, 9):
                    j = (W//3 + 17*width) % W
                    st = np.vstack([x, x.copy()])
                    for k2 in range(width):
                        st[0,(j+k2)%W] = k2 % 2; st[1,(j+k2)%W] = 1-(k2 % 2)
                    one = handed_step(st, r)
                    if label == 'opp':
                        convtot += 1
                        d1 = defects(one)
                        rs = [g for g in runs_of(d1) if g[0] <= j <= g[1]]
                        if rs:
                            lo, hi = rs[0]
                            js = {('alt' if one[0][k2 % W] != one[0][(k2+1) % W] else 'same')
                                  for k2 in range(lo, hi)}
                            if js != {'alt'}: conv += 1
                        else: conv += 1
                    else:
                        tot += 1
                        cur = st
                        for _ in range(256): cur = handed_step(cur, r)
                        rs = [g for g in runs_of(defects(cur)) if g[0] <= j <= g[1]]
                        if rs and rs[0][1]-rs[0][0]+1 == width and rs[0][0] % W == j % W: kept += 1
    c['5_permanent_runs'] = {'matching_kept': kept, 'of': tot,
                             'opposite_junction_converted': conv, 'opposite_trials': convtot}
    if kept != tot or conv == 0: fail.append('control5_permanent_runs')

    # 7. free == driven on the centre-only bases; witnesses must diverge
    def streams_agree(br, u, reps=2):
        r = HandedRule('t', embed(br, bits_of(u)))
        worst = None
        for rep in range(reps):
            rng7 = np.random.default_rng(seed('transverse', u, rep))
            x = (rng7.random(W) < 0.5).astype(np.uint8)
            for _ in range(256): x = eca_step(x, br)
            for o in rng7.choice(W, size=4, replace=False):
                j = int(o); st = np.vstack([x, x.copy()]); st[1, j] ^= 1
                fx = x.copy()
                for t2 in range(1, 33):
                    st = handed_step(st, r); fx = eca_step(fx, br)
                    dr = (int(st[0][(j-2)%W]), int(st[0][(j+2)%W]))
                    fr = (int(fx[(j-2)%W]), int(fx[(j+2)%W]))
                    if dr != fr:
                        worst = t2 if worst is None else min(worst, t2); break
        return worst
    agree_ok = {br: streams_agree(br, arms['Kex'][0]) for br in (0, 51, 204, 8)}
    wit = {br: streams_agree(br, arms['Kex'][0]) for br in (90, 110)}
    c['7_free_equals_driven'] = {'centre_only_first_divergence': agree_ok, 'witness': wit}
    if any(v is not None for v in agree_ok.values()) or any(v is None or v > 4 for v in wit.values()):
        fail.append('control7_streams')

    # 9. beam invariance
    bad9 = []
    for br in BASES:
        for u in arms['Uplus']:
            r = HandedRule('t', embed(br, bits_of(u)))
            for k2 in (2,3):
                rngb = np.random.default_rng(seed('ctl9', br, u, k2))
                x = (rngb.random(W) < 0.5).astype(np.uint8)
                st = np.vstack([x]*k2); ref = x.copy()
                for _ in range(256):
                    st = handed_step(st, r); ref = eca_step(ref, br)
                    if not (np.all(st == st[0], axis=0).all() and np.array_equal(st[0], ref)):
                        bad9.append((br, u, k2)); break
    c['9_beam_invariance'] = {'failures': len(bad9)}
    if bad9: fail.append('control9_beam')

    # 12. panel assertions
    pb = {str(r): beta_bits(r) for r in BASES}
    c['12_panel'] = {'n_bases': len(BASES), 'block0_complete': sorted(BLOCK0) ==
                     sorted([r for r in range(256) if beta_bits(r) == [0,0,0,0]]),
                     'pair_permanent_in_panel': all(r in BASES for r in PAIR_PERMANENT),
                     'centre_only': [r for r in CENTRE_ONLY if r in BASES]}
    if not (len(BASES) == 33 and c['12_panel']['block0_complete']
            and c['12_panel']['pair_permanent_in_panel']): fail.append('control12_panel')

    c['failures'] = fail
    return c, fail

    # 6. the gadget on the DRIVEN stream, all 33 bases
    bad6 = 0; n6 = 0; heal6 = 0
    for u in (arms['Kex'][:2] + arms['Kall_plus'][:1]):
        safe, doomed, trans = gadget(u)
        for br in BASES:
            r = HandedRule('t', embed(br, bits_of(u)))
            rng6, x = beam_state(br, u, 1)
            for o in rng6.choice(W, size=4, replace=False):
                j = int(o)
                st = np.vstack([x, x.copy()]); st[1, j] ^= 1
                s = (int(x[(j-1)%W]), int(x[j]), int(x[(j+1)%W])); start = s
                healed = None
                for t2 in range(1, 65):
                    LL = int(st[0][(j-2)%W]); RR = int(st[0][(j+2)%W])
                    nxt = handed_step(st, r); n6 += 1
                    pred = trans[(s, LL, RR)]
                    d = defects(nxt)
                    if pred is None:
                        if d.any(): bad6 += 1
                        healed = t2; break
                    if not (d[j] and d.sum() == 1): bad6 += 1; break
                    got = (int(nxt[0][(j-1)%W]), int(nxt[0][j]), int(nxt[0][(j+1)%W]))
                    if got != pred: bad6 += 1; break
                    s = pred; st = nxt
                if start in doomed and (healed is None or healed > 8): heal6 += 1
                if start in safe and healed is not None: heal6 += 1
    c['6_driven_gadget'] = {'mismatches': bad6, 'of': n6, 'heal_class_violations': heal6,
                            'bases': len(BASES)}
    if bad6 or heal6: fail.append('control6_driven_gadget')

    # 8. regeneration against the EIGHTH unit, in a SUBPROCESS (module aliasing)
    prev = json.loads((ROOT/'results/permanent_structures_20260918/rows.json').read_text())['rows']
    want = [{k: pr.get(k) for k in ('table','u','arm','base','R_star','M_star','agree','alpha_x')}
            for pr in prev[:16]]
    script = ("import importlib.util as i,sys,json\n"
              f"s=i.spec_from_file_location('p8',r'{ROOT}/experiments/permanent_structures_20260918/run.py')\n"
              "m=i.module_from_spec(s);sys.modules['p8']=m;s.loader.exec_module(m)\n"
              "w=json.load(sys.stdin);out=[]\n"
              "for pr in w:\n"
              "    g=m.evaluate(pr['table'],pr['u'],pr['arm'],pr['base'])\n"
              "    out.append({k:g.get(k) for k in ('R_star','M_star','agree','alpha_x')})\n"
              "print(json.dumps(out))\n")
    import subprocess
    pr8 = subprocess.run([sys.executable, '-c', script], input=json.dumps(want),
                         capture_output=True, text=True)
    bad8 = []
    if pr8.returncode != 0: bad8.append(('subprocess', pr8.returncode, pr8.stderr[-400:]))
    else:
        got = json.loads(pr8.stdout.strip().splitlines()[-1])
        for a_, b_ in zip(want, got):
            for k in ('R_star','M_star','agree','alpha_x'):
                xx, yy = a_.get(k), b_.get(k)
                if xx is None and yy is None: continue
                if xx is None or yy is None or abs(float(xx)-float(yy)) > 1e-12:
                    bad8.append((a_['u'], k, xx, yy))
    c['8_regeneration'] = {'mismatches': len(bad8), 'of': len(want)*4, 'examples': bad8[:3]}
    if bad8: fail.append('control8_regeneration')

    # 10. matched null pairs -- PAIRED DRAWS (the same u, the conjugate table,
    # complemented initial states), every scalar to 1e-9 and every census vector
    # as integers. Result 15's lesson: comparing two independent samples of
    # deduced-identical objects rejects at the nominal rate by construction.
    def conj(table):
        t = 0
        for i in range(32):
            if (table >> i) & 1: continue
            c_, w_, n7 = (i>>4)&1, (i>>3)&1, i & 7
            t |= 1 << (16*(1-c_) + 8*(1-w_) + (7-n7))
        return t
    spec10 = ([(110, 137, u, 'random') for u in arms['random'][:3]]
              + [(110, 137, u, 'Kex') for u in arms['Kex'][:2]]
              + [(110, 137, u, 'Kall_plus') for u in arms['Kall_plus'][:2]]
              + [(110, 137, u, 'G') for u in arms['G'][:1]]
              + [(51, 51, u, 'Uplus') for u in arms['Uplus'][:2]])
    worst = 0.0; census_bad = 0; pilot_rows = []
    for b1, b2, u, armname in spec10:
        t1 = embed(b1, bits_of(u)); t2 = conj(t1)
        a_ = evaluate(t1, u, armname, b1, flip=False)
        b_ = evaluate(t2, u, armname, b2, flip=True)
        for k in ('R_star','M_star','agree','Dx64','Dx128','T_ext','T64','T128','mean_width'):
            va, vb = a_.get(k), b_.get(k)
            if va is None or vb is None: continue
            worst = max(worst, abs(float(va)-float(vb)))
        for k in ('structural_census','structural_survival','pair_census'):
            if a_[k] != b_[k]: census_bad += 1
        pilot_rows.append(a_)
    c['10_matched_null_pairs'] = {'worst_abs_difference': worst, 'n_pairs': len(spec10),
                                  'census_mismatches': census_bad}
    if worst > 1e-9 or census_bad: fail.append('control10_null_pairs')

    # 11. disjointness from units 4-8, with the U+ coincidence recorded
    prev_us = set()
    for pth in ('results/matched_completion_20260918/rows.json',
                'results/beam_mechanism_20260918/rows.json',
                'results/defect_algebra_20260918/rows.json',
                'results/dense_defect_algebra_20260918/rows.json',
                'results/permanent_structures_20260918/rows.json'):
        try:
            dd = json.loads((ROOT/pth).read_text()); rr = dd['rows'] if isinstance(dd, dict) else dd
            prev_us |= {int(x['u']) if 'u' in x else u_of(int(x['table'])) for x in rr}
        except Exception: pass
    ov = {a_: sorted(set(arms[a_]) & prev_us) for a_ in ARMS}
    c['11_disjointness'] = {'overlap_counts': {a_: len(v) for a_, v in ov.items()},
                            'Uplus_overlap_recorded': ov['Uplus']}
    for a_ in ARMS:
        if a_ != 'Uplus' and ov[a_]: fail.append(f'control11_disjointness_{a_}')

    # 14. THE RULE EARNED FROM PR #278: the evaluator's scored key set must equal
    # the protocol's frozen list, checked against real pilot rows before any tier.
    # A prediction the evaluator does not score must appear with an explicit
    # not_evaluated reason, so "unscored" is a recorded verdict and never an absence.
    want_keys = frozen_keys()
    OUT.mkdir(parents=True, exist_ok=True)
    pilot = OUT / '_pilot_rows.json'
    pilot.write_text(json.dumps({'protocol': PROTOCOL, 'rows': pilot_rows}, default=str))
    got_keys, err = [], None
    try:
        pr14 = subprocess.run([sys.executable, str(HERE/'evaluate.py'), '--pilot', str(pilot)],
                              capture_output=True, text=True, timeout=600)
        if pr14.returncode != 0: err = f'exit {pr14.returncode}: {pr14.stderr[-600:]}'
        else: got_keys = sorted(json.loads(pr14.stdout.strip().splitlines()[-1])['predictions'])
    except Exception as e:
        err = repr(e)
    finally:
        pilot.unlink(missing_ok=True)
    c['14_frozen_key_set'] = {'frozen': want_keys, 'scored': got_keys,
                              'missing': [k for k in want_keys if k not in got_keys],
                              'extra': [k for k in got_keys if k not in want_keys],
                              'pilot_rows': len(pilot_rows), 'error': err}
    if err or got_keys != want_keys: fail.append('control14_frozen_key_set')

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
    arms, sizes, cls = build_arms()
    alg = {'pairs': [list(p) for p in PAIR_KEYS],
           'structs': STRUCTS,
           'struct_of_pair': [STRUCTS[i] for i in STRUCT_OF_PAIR],
           'dictionary_multi': DICT_MULTI,
           'alpha_classes': {str(k): v for k, v in ALPHA.items()},
           'cell_sizes': sizes,
           'pair_permanent': PAIR_PERMANENT,
           'centre_only': CENTRE_ONLY,
           'base_bits': {str(r): {'beta': beta_bits(r), 'gamma': gamma_bits(r),
                                  'totalistic': is_totalistic(r),
                                  'pair_permanent': is_pair_permanent(r),
                                  'centre_only': is_centre_only(r),
                                  'matching_pattern': list(matching_pattern(r))}
                         for r in BASES}}
    (OUT/'algebra.json').write_text(json.dumps(alg, indent=1))
    (OUT/'gadget.json').write_text(json.dumps(
        {'class_sizes': {k: len(v) for k, v in cls.items()},
         'arms': arms,
         'six_types': {str(u): list(six_type(u)) for arm in ARMS for u in arms[arm]},
         'safe_doomed': {str(u): [sorted(map(list, gadget(u)[0])), sorted(map(list, gadget(u)[1]))]
                         for arm in ('Kall_plus','Kall_minus','Kex') for u in arms[arm]}}, indent=1))
    print(f'[algebra] {len(PAIR_KEYS)} pairs, {len(STRUCTS)} structures; cells {sizes}', flush=True)
    print('[controls] running before any tier', flush=True)
    ctl, fail = controls(arms, sizes, cls, a.workers)
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
    pis = {str(br): pi_tier(br, arms['pi']) for br in BASES}
    (OUT/'pairs.json').write_text(json.dumps({'protocol': PROTOCOL, 'pi': pis}, indent=1))
    print(f'[done] {len(rows)} evaluations in {(time.time()-t0)/60:.1f} min', flush=True)

if __name__ == '__main__':
    main()
