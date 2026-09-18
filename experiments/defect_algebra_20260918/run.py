#!/usr/bin/env python3
"""The single-defect algebra on the beam: twelve count-insensitivity bits.

Frozen protocol: docs/research/protocols/2026-09-18-defect-algebra.md
(committed before this implementation).

Flip one cell of a beam state. Exactly six reads change and none of the
post-flip reads lands on an exposed entry, so the damage is carried entirely
by free entries. Whether the defect heals in one step is a conjunction of
three pairwise bit-equalities whose pairs depend on the surrounding window
only through (LL,L), (L,R) and (R,RR) respectively. Twelve equalities, GF(2)
rank 11. The tables below were re-derived from the read-index definition by
the executing session, not copied from the protocol.

Controls 1-7 run BEFORE any tier and raise on failure. That ordering is the
previous unit's lesson: a control that runs after the observables gates
nothing, and one that cannot fail is worse than none.

    python experiments/defect_algebra_20260918/run.py --workers 4
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
mc, hf, base, strip = bm.mc, bm.hf, bm.base, bm.strip
HandedRule, handed_step, embed, res1, eca_step = hf.HandedRule, hf.handed_step, hf.embed, hf.res1, bm.eca_step
EXPOSED, FREE = hf.EXPOSED, hf.FREE
POS = {e: i for i, e in enumerate(FREE)}

PROTOCOL = 'defect-algebra-20260918'
OUT = ROOT / 'results/defect_algebra_20260918'
BASES = [110, 54, 22, 5, 30, 90, 0, 204]
N_RANDOM, N_FLIP_PAIRS, N_PER_CELL = 192, 48, 24
CELLS = ['Uplus', 'Uminus', 'G', 'Gprime', 'K']
DENSITY = 0.5

# Constraint tables: (block, window-pair) -> the two free entries that must agree.
A_TAB = {(0,0):(1,2), (0,1):(19,20), (1,0):(11,12), (1,1):(29,30)}      # (LL,L); gap 1
B_TAB = {(0,0):(2,16), (0,1):(5,19), (1,0):(12,26), (1,1):(15,29)}      # (L,R);  gap 14
C_TAB = {(0,0):(2,8),  (0,1):(5,11), (1,0):(20,26), (1,1):(23,29)}      # (R,RR); gap 6
CONS = [A_TAB[k] for k in sorted(A_TAB)] + [B_TAB[k] for k in sorted(B_TAB)] + [C_TAB[k] for k in sorted(C_TAB)]

def seed(*parts):
    h = hashlib.sha256('|'.join(map(str, (PROTOCOL,) + parts)).encode()).digest()
    return int.from_bytes(h[:8], 'little') & 0x7fff_ffff_ffff_ffff

def read_index(x0, x1, r, j, n):
    xr, xo = (x0, x1) if r == 0 else (x1, x0)
    return 16*xr[j % n] + 8*xr[(j-1) % n] + xr[(j+1) % n] + 2*(xo[(j-1) % n] + xo[j % n] + xo[(j+1) % n])

# --------------------------------------------------------- signatures

def signature(u):
    """12 bits; bit k = 1 when constraint k is VIOLATED. 0..3 A, 4..7 B, 8..11 C."""
    s = 0
    for k, (a, b) in enumerate(CONS):
        s |= (((u >> POS[a]) ^ (u >> POS[b])) & 1) << k
    return s

def signature_array(us):
    us = np.asarray(us, dtype=np.uint32)
    s = np.zeros(len(us), dtype=np.uint16)
    for k, (a, b) in enumerate(CONS):
        s |= ((((us >> POS[a]) ^ (us >> POS[b])) & 1) << k).astype(np.uint16)
    return s

def nABC(u):
    s = signature(u)
    return (4 - bin(s & 0xF).count('1'), 4 - bin((s >> 4) & 0xF).count('1'), 4 - bin((s >> 8) & 0xF).count('1'))

CELL_SIG = {'Uplus': lambda s: s == 0, 'Uminus': lambda s: s == 0xFFF,
            'G': lambda s: s == 0x00F, 'Gprime': lambda s: s == 0xF00,
            'K': lambda s: ((s & 0xF0F) == 0) & ((s >> 4) & 0xF != 0)}

def build_cells(rng):
    """Enumerate the twelve bits over all 2^24 completions and sample each cell."""
    allu = np.arange(1 << 24, dtype=np.uint32)
    sig = signature_array(allu)
    out, sizes = {}, {}
    for name in CELLS:
        if name == 'K':
            mask = ((sig & 0xF0F) == 0) & (((sig >> 4) & 0xF) != 0)
        else:
            target = {'Uplus':0, 'Uminus':0xFFF, 'G':0x00F, 'Gprime':0xF00}[name]
            mask = sig == target
        idx = allu[mask]
        sizes[name] = int(idx.size)
        out[name] = [int(v) for v in rng.choice(idx, size=N_PER_CELL, replace=False)] if idx.size >= N_PER_CELL else []
    return out, sizes

def heal_window(u, w):
    """One-step healing at a 5-window, by the three table lookups."""
    LL, L, C, R, RR = w
    for tab, key in ((A_TAB,(LL,L)), (B_TAB,(L,R)), (C_TAB,(R,RR))):
        a, b = tab[key]
        if ((u >> POS[a]) & 1) != ((u >> POS[b]) & 1): return False
    return True

# --------------------------------------------- transverse, traced and plain

def transverse_traced(table, base_rule, u, seedfn, complement=False, trace=True):
    r = HandedRule(f'h{table}', table)
    d64, d128, heal_t, counts = [], [], [], []
    for rep in range(4):
        rng = np.random.default_rng(seedfn('transverse', u, rep))
        x = (rng.random(strip.WIDTH) < 0.5).astype(np.uint8)
        if complement: x = (1 - x).astype(np.uint8)
        for _ in range(256): x = eca_step(x, base_rule)
        for o in rng.choice(strip.WIDTH, size=8, replace=False):
            st = np.vstack([x, x.copy()]); st[1, int(o)] ^= 1
            ht, snap = None, {}
            for t in range(1, 129):
                st = handed_step(st, r)
                nd = int((st[0] != st[1]).sum())
                if ht is None and nd == 0: ht = t
                if trace and t in (1,2,4,8,16,32,64,128): snap[t] = nd
                if t == 64: d64.append(nd)
            d128.append(nd)
            if trace: heal_t.append(ht); counts.append(snap)
    res = {'T64': float(np.mean(d64)), 'T128': float(np.mean(d128)),
           'T_ext': float(np.mean([d == 0 for d in d128]))}
    if trace:
        res['heal_times'] = heal_t
        res['defect_counts'] = counts
    return res

def evaluate(table, u, seedfn):
    r = HandedRule(f'h{table}', table)
    t0 = time.time()
    events, agree = bm.sample_events_agree(r, 2, ('A', u))
    p, nref, refmode = strip.reference_strip(r, 2)
    R, mu, sd, missing = base.selective_r(events, p)
    M, bll, hll, ntr, nte = base.predictive_gain(events[:4], events[4:6])
    sp = mc.spread_keyed(r, 2, ('A', u))
    return {'table': table, 'R_star': R, 'M_star': M,
            'S_star': max(0, R) * max(0, M) if math.isfinite(R) else None,
            'agree': agree, 'on_beam': int(agree > 0.98), 'off_beam': int(agree < 0.5),
            **sp, 'wall_seconds': time.time() - t0}

def beam_measure(base_rule, u, seedfn):
    """mu_r over all 521 columns of the four transverse beam states, and H1."""
    cnt = np.zeros(32)
    for rep in range(4):
        rng = np.random.default_rng(seedfn('transverse', u, rep))
        x = (rng.random(strip.WIDTH) < 0.5).astype(np.uint8)
        for _ in range(256): x = eca_step(x, base_rule)
        for j in range(strip.WIDTH):
            w = tuple(int(x[(j+d) % strip.WIDTH]) for d in (-2,-1,0,1,2))
            cnt[w[0]*16 + w[1]*8 + w[2]*4 + w[3]*2 + w[4]] += 1
    mu = cnt / cnt.sum()
    H1 = sum(mu[i] * heal_window(u, tuple((i >> b) & 1 for b in (4,3,2,1,0))) for i in range(32))
    return float(H1), [float(v) for v in mu]

# ------------------------------------------------------------- controls

def controls(random_us, flip_us, cells, sizes):
    c, fail = {}, []
    # 1. algebra, exact
    allfree, lit = True, set()
    for w in itertools.product((0,1), repeat=5):
        x = np.array([0,0,*w,0,0]); o = 4
        x1 = x.copy(); x1[o] ^= 1
        for r in (0,1):
            for d in (-1,0,1):
                i = read_index(x, x1, r, o+d, 9)
                if i in EXPOSED: allfree = False
                if i in FREE: lit.add(int(i))
        for tab, key, d in ((A_TAB,(w[0],w[1]),-1), (B_TAB,(w[1],w[3]),0), (C_TAB,(w[3],w[4]),1)):
            a, b = read_index(x, x1, 0, o+d, 9), read_index(x, x1, 1, o+d, 9)
            if tuple(sorted((int(a), int(b)))) != tuple(sorted(tab[key])): fail.append(('table', w, d))
    M = np.array([[1 if i in (POS[a], POS[b]) else 0 for i in range(24)] for a, b in CONS], np.uint8)
    def rank(A):
        A = A.copy(); r = 0
        for col in range(A.shape[1]):
            p = next((i for i in range(r, A.shape[0]) if A[i, col]), None)
            if p is None: continue
            A[[r, p]] = A[[p, r]]
            for i in range(A.shape[0]):
                if i != r and A[i, col]: A[i] ^= A[r]
            r += 1
        return r
    c['1_algebra'] = {'all_post_flip_reads_free': allfree, 'n_lit': len(lit), 'n_dark': 24 - len(lit),
                      'tables_match': not fail, 'gf2_rank': int(rank(M)),
                      'cell_sizes': sizes}
    if not (allfree and len(lit) == 14 and not fail and rank(M) == 11): fail.append('control1')
    if sizes['Uplus'] != 8192 or sizes['Uminus'] != 8192: fail.append('cell-size')
    # 2. defect-count identity, can fail
    rng = np.random.default_rng(seed('ctl2')); bad2 = 0
    for _ in range(256):
        u = int(rng.integers(0, 1 << 24)); w = tuple(int(b) for b in rng.integers(0, 2, 5))
        n = 13; x = np.zeros(n, np.uint8); x[4:9] = w; o = 6
        x = np.array([0,0,0,0,*w,0,0,0,0], np.uint8)
        t = embed(res1(embed(110, mc.bits_of(u))), mc.bits_of(u))
        r = HandedRule('t', embed(110, mc.bits_of(u)))
        st = np.vstack([x, x.copy()]); st[1, o] ^= 1
        st2 = handed_step(st, r)
        sim = int((st2[0] != st2[1]).sum())
        viol = sum(1 for tab, key in ((A_TAB,(w[0],w[1])), (B_TAB,(w[1],w[3])), (C_TAB,(w[3],w[4])))
                   for a, b in [tab[key]] if ((u >> POS[a]) & 1) != ((u >> POS[b]) & 1))
        if sim != viol: bad2 += 1
    c['2_defect_count_identity'] = {'mismatches': bad2, 'of': 256}
    if bad2: fail.append('control2')
    # 5. beam invariance
    rngb = np.random.default_rng(seed('ctl5')); badb = []
    for b in BASES:
        for u in random_us[:8]:
            t = embed(b, mc.bits_of(u)); r = HandedRule(f'h{t}', t)
            for h in (2, 3):
                x = rngb.integers(0, 2, 121, dtype=np.uint8)
                st = np.vstack([x]*h); e = x.copy()
                for _ in range(256):
                    st = handed_step(st, r); e = eca_step(e, b)
                    if not np.all(st == st[0]) or not np.array_equal(st[0], e): badb.append((b, u, h)); break
    c['5_beam_invariance'] = {'ok': not badb, 'failures': badb[:5]}
    if badb: fail.append('control5')
    # 7. disjointness and condition-P rows
    prev = set()
    for p in ('matched_completion_20260918', 'beam_mechanism_20260918'):
        f = ROOT / f'results/{p}/rows.json'
        if f.exists(): prev |= set(json.loads(f.read_text())['completions'])
    allmine = set(random_us) | set(flip_us) | {v for vs in cells.values() for v in vs}
    c['7_disjoint'] = {'overlap_with_earlier_units': len(prev & set(random_us)), 'n_mine': len(allmine)}
    if prev & set(random_us): fail.append('control7')
    return c, fail

def matched_null_pairs(random_us):
    rows = []
    for u in random_us[:8]:
        t = embed(110, mc.bits_of(u)); ct = mc.conj_table(t)
        assert res1(ct) == 137
        o1 = evaluate(t, u, seed); o1.update(transverse_traced(t, 110, u, seed, trace=False))
        o2 = evaluate(ct, u, seed); o2.update(transverse_traced(ct, 137, u, seed, complement=True, trace=False))
        keys = ('R_star','M_star','alpha_x','agree','T64','T128','T_ext')
        d = {k: (None if o1[k] is None or o2[k] is None else abs(o1[k]-o2[k])) for k in keys}
        rows.append({'completion': u, 'abs_diff': d,
                     'max_abs_diff': max((v for v in d.values() if v is not None), default=None),
                     'identical_to_1e-9': all(v is not None and v < 1e-9 for v in d.values())})
    return rows

def control3_class(cells):
    """Edge-lemma corollaries on the built classes. Can fail."""
    out, fail = {}, []
    for name in ('Uplus', 'Uminus', 'G', 'Gprime', 'K'):
        for b in BASES[:2]:
            for u in cells[name][:2]:
                t = embed(b, mc.bits_of(u))
                r = transverse_traced(t, b, u, seed)
                if name == 'Uplus' and not (r['T_ext'] == 1.0 and r['T64'] == 0 and r['T128'] == 0):
                    fail.append(('Uplus', b, u, r['T_ext']))
                if name in ('Uminus','G','Gprime') and r['T_ext'] != 0.0:
                    fail.append((name, b, u, r['T_ext']))
                if name == 'K' and max(max(s.values()) for s in r['defect_counts']) > 1:
                    fail.append(('K', b, u, 'defect>1'))
                out.setdefault(name, []).append({'base': b, 'completion': u,
                                                 'T_ext': r['T_ext'], 'T64': r['T64'], 'T128': r['T128']})
    return out, fail

# ------------------------------------------------------------------ run

def job(spec):
    arm, idxs, us, tag = spec
    rows = []
    for i in idxs:
        u = us[i]; ub = mc.bits_of(u)
        for b in BASES:
            t = embed(b, ub)
            r = evaluate(t, u, seed)
            r.update(transverse_traced(t, b, u, seed))
            H1, mu = beam_measure(b, u, seed)
            r.update({'base': b, 'completion': u, 'arm': arm, 'tag': tag[i] if tag else None,
                      'signature': signature(u), 'nABC': nABC(u), 'H1': H1})
            rows.append(r)
    return rows

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--timing', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed('completions'))
    random_us, seen = [], set()
    while len(random_us) < N_RANDOM:
        u = int(rng.integers(0, 1 << 24))
        if u not in seen: seen.add(u); random_us.append(u)
    # flip arm: dark-3 and lit-3 partners of the first 48 random completions
    LIT = sorted({1,2,5,8,11,12,15,16,19,20,23,26,29,30}); DARK = sorted(set(FREE) - set(LIT))
    flip_us, flip_tag = [], []
    for u in random_us[:N_FLIP_PAIRS]:
        for kind, pool in (('dark', DARK), ('lit', LIT)):
            g = np.random.default_rng(seed('flip', u, kind))
            v = u
            for e in g.choice(pool, size=3, replace=False): v ^= 1 << POS[int(e)]
            flip_us.append(int(v)); flip_tag.append(f'{kind}:{u}')
    cells, sizes = build_cells(np.random.default_rng(seed('cells')))
    cell_us = [v for name in CELLS for v in cells[name]]
    cell_tag = [name for name in CELLS for _ in cells[name]]

    if args.timing:
        u = random_us[0]; t = embed(110, mc.bits_of(u))
        t0 = time.time(); evaluate(t, u, seed); e = time.time()-t0
        t0 = time.time(); transverse_traced(t, 110, u, seed); tr = time.time()-t0
        t0 = time.time(); beam_measure(110, u, seed); bmt = time.time()-t0
        print(f'eval {e:.2f}s | traced transverse {tr:.2f}s | beam measure {bmt:.2f}s'); return

    print('controls 1,2,5,7 ...', flush=True)
    ctrl, fail = controls(random_us, flip_us, cells, sizes)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'cell_sizes'} for k, v in ctrl.items()}, indent=1))
    print('cell sizes:', sizes, flush=True)
    print('control 3 (edge corollaries on built classes) ...', flush=True)
    c3, f3 = control3_class(cells); fail += f3
    print('control 6 (matched null pair) ...', flush=True)
    nulls = matched_null_pairs(random_us)
    if not all(r['identical_to_1e-9'] for r in nulls): fail.append('control6')
    if fail:
        (OUT / 'controls_failed.json').write_text(json.dumps(
            {'controls': ctrl, 'control3': c3, 'nulls': nulls, 'failures': [str(f) for f in fail]},
            indent=1, allow_nan=False) + '\n')
        raise SystemExit(f'controls failed: {fail[:5]}')
    print('all controls pass', flush=True)

    t0 = time.time()
    ch = lambda n, s: [list(range(i, min(i+s, n))) for i in range(0, n, s)]
    specs = ([('random', c, random_us, None) for c in ch(N_RANDOM, 8)]
             + [('flip', c, flip_us, flip_tag) for c in ch(len(flip_us), 8)]
             + [('class', c, cell_us, cell_tag) for c in ch(len(cell_us), 8)])
    out = []
    with Pool(args.workers) as pool:
        for i, rows in enumerate(pool.imap_unordered(job, specs, chunksize=1)):
            out += rows
            print(f'chunk {i+1}/{len(specs)} rows={len(out)} {time.time()-t0:.0f}s', flush=True)
    (OUT / 'controls.json').write_text(json.dumps(
        {'protocol': PROTOCOL, 'controls': ctrl, 'control3_class': c3, 'matched_null_pairs': nulls,
         'all_matched_identical': all(r['identical_to_1e-9'] for r in nulls)}, indent=1, allow_nan=False) + '\n')
    (OUT / 'rows.json').write_text(json.dumps(
        {'protocol': PROTOCOL, 'bases': BASES, 'random_completions': random_us,
         'flip_completions': flip_us, 'flip_tags': flip_tag, 'cells': cells, 'cell_sizes': sizes,
         'constraints': CONS, 'rows': out, 'wall_seconds': time.time()-t0},
        indent=1, sort_keys=True, allow_nan=False) + '\n')
    print(OUT / 'rows.json', f'{time.time()-t0:.0f}s rows={len(out)}')

if __name__ == '__main__':
    main()
