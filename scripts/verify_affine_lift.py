#!/usr/bin/env python3
"""Finite verification of the affine-oriented jet lift and its Groovy identities.

The theorem text being verified is GPT-5.6 Sol's proof state
(`docs/research/proofs/affine-oriented-lift-proof-state-20260917.md`), imported
on 2026-09-17. This script is Fable's independent verification: it implements the
construction from the theorem statement alone (no code from the GPT session was
available), and checks every claim that is finite on a declared domain. It does
not prove the general theorem; it certifies that the objects the proof reasons
about behave as stated on every enumerated case, including the non-ECA parents
(radius-two 1D rules and Conway's Life) that the general entry lemma newly
covers, and the diagonal-rail recursion at D3 for all 256 ECA roots.

Conventions. Translation is tau_v X(p) = X(p + v). The affine gauge encodes a
parent state X of a binary CA H with memory M as six fields

    F0 = X xor tau_{v+} X
    F1 = 1 xor X xor tau_{v-} X
    F2 = X xor H(X)
    F3 = X xor H^2(X)
    F4 = 0
    F5 = X

laid along a new period-six axis; the phase-saturated beam is the set of all
six cyclic row rotations. Entry uses v+ = e, v- = -e with inherited memory
W = M + {-e, 0, e} and new-axis radius 3. Recursion uses v+ = a + e, v- = a - e
(a = newest existing lifted axis) with child memory {-3..3} x M_parent.

Sections and what each establishes (all exact on the stated domain):

  A  entry decoder, all 256 ECAs: for every 9-bit source dependency word and
     every true phase, exactly one candidate rotation passes the local affine
     checks (F4 = 0, both rails, F2 = X xor H X, F3 = X xor H^2 X on the
     positions where the window can evaluate them), and it is the true one;
     recovered X and native output are functions of the 7x5 window (no
     collisions); applying the window rule to the lifted grid of X gives the
     lifted grid of H(X) on rings.
  B  the same decoder for a sample of radius-two 1D rules (2^15 words each)
     and for Conway's Life (3x3 torus exhaustive, plus random tori): the
     general-parent domain of the entry lemma.
  C  pure row algebra is not enough: with the F2/F3 dynamical checks switched
     off, the proof's witnesses for rotations 2, 3, 4 pass; with them on, no
     rotation passes under any of the 256 ECA rules (rule-free refutation).
  D  recursion at D3 for all 256 ECA roots on rings of width 7 (and 8 for a
     subset): the D2 beam of each root is lifted again with diagonal rails and
     the D3 window {-3..3}^2 x {-2..2} determines phase, parent D2 cell and
     native output without collision, and the induced rule intertwines
     exactly (H_3 L_2 = L_2 H_2) on the finite family.
  E  Groovy identities on the 7-ring, all 256 rules: G° = B_H(X, D_H X);
     all-pairs polarization vanishes exactly on the 16 affine rules while
     centered G vanishes on 18 (adding 4 and 200); the affine-jet residual is
     (0,0,K1,K2,0,0) with K1 = G; the horizon cocycle K_{t+1} = G(H^t X) xor
     dH_{H^t D X}(K_t); the signed-translation grading G_{T(v,eps)} = eps.

Runtime is about ten minutes (pure-Python decoder loops); it is not run in CI. Output: results/affine_lift_20260917.json.
"""
from __future__ import annotations
import hashlib, itertools, json, pathlib, sys, time
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/affine_lift_20260917.json'
PROOF = ROOT / 'docs/research/proofs/affine-oriented-lift-proof-state-20260917.md'

# ----------------------------------------------------------------------------
# generic binary CA on a torus, memory given as offsets
# ----------------------------------------------------------------------------

class CA:
    """A binary CA on Z^d (simulated on tori) given by a local rule on a memory set."""
    def __init__(self, memory, local, name):
        self.memory = [tuple(m) for m in memory]   # offsets, 0 included
        self.local = local                          # local(bits tuple in memory order) -> 0/1
        self.name = name
        self.d = len(self.memory[0])
        self._lut = None

    def lut(self):
        if self._lut is None:
            k = len(self.memory)
            self._lut = np.array([self.local(tuple((i >> (k - 1 - j)) & 1 for j in range(k)))
                                  for i in range(1 << k)], dtype=np.uint8)
        return self._lut

    def step(self, X):
        """One synchronous step on a torus array X (shape = d axes)."""
        idx = np.zeros(X.shape, dtype=np.int64)
        for m in self.memory:
            idx = (idx << 1) | np.roll(X, tuple(-c for c in m), axis=tuple(range(self.d)))
        return self.lut()[idx]

    def eval_patch(self, get):
        """Evaluate the local rule where get(offset) returns the bit at that offset."""
        idx = 0
        for m in self.memory:
            idx = (idx << 1) | int(get(m))
        return int(self.lut()[idx])


def eca(rule):
    return CA([(-1,), (0,), (1,)], lambda b: (rule >> (4 * b[0] + 2 * b[1] + b[2])) & 1, f'eca{rule}')

def radius2(table):
    # table: 32-bit int, indexed by the 5-bit word (left to right)
    return CA([(-2,), (-1,), (0,), (1,), (2,)],
              lambda b: (table >> (16 * b[0] + 8 * b[1] + 4 * b[2] + 2 * b[3] + b[4])) & 1, f'r2-{table}')

def life():
    mem = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
    def local(b):
        c = b[4]; n = sum(b) - c
        return int(n == 3 or (c == 1 and n == 2))
    return CA(mem, local, 'life')

# ----------------------------------------------------------------------------
# the affine-oriented six-field lift on tori
# ----------------------------------------------------------------------------

def shift(X, v):
    """tau_v X(p) = X(p+v) on a torus array."""
    return np.roll(X, tuple(-c for c in v), axis=tuple(range(X.ndim)))

def fields(H, X, vp, vm):
    Y = H.step(X); Z = H.step(Y)
    return [X ^ shift(X, vp), 1 ^ X ^ shift(X, vm), X ^ Y, X ^ Z, np.zeros_like(X), X.copy()]

def lift(H, X, vp, vm, phase=0):
    """Child torus with the new axis first (period six): row r carries field (r - phase) mod 6."""
    F = fields(H, X, vp, vm)
    return np.stack([F[(r - phase) % 6] for r in range(6)], axis=0)

# ----------------------------------------------------------------------------
# section A/B: the generic entry decoder (the object the entry lemma reasons about)
# ----------------------------------------------------------------------------

def entry_decode(H, window, e, dynamical=True):
    """window: dict (row offset -3..3, position offset in W) -> bit, for a cell at row 0.

    Returns the list of admissible candidate phases p' (field index of row 0),
    and for each the decoded keys. Positions are offsets relative to the cell,
    W = M + {-e, 0, e}. The local checks are exactly those the proof's entry
    lemma uses: F4 = 0; F0 = F5 xor tau_e F5 and F1 = 1 xor F5 xor tau_{-e} F5
    wherever both ends lie in W; and, if `dynamical`, F2 = F5 xor H(F5) and
    F3 = F5 xor H(F5 xor F2) at the positions {-e, 0, e} whose M-neighbourhood
    lies in W.
    """
    d = H.d
    M = H.memory
    ev = tuple(e); mev = tuple(-c for c in e)
    def add(a, b): return tuple(x + y for x, y in zip(a, b))
    W = sorted({add(m, s) for m in M for s in (mev, (0,) * d, ev)})
    Wset = set(W)
    admissible = []
    for p in range(6):
        def F(i, pos):  # field i at position pos, via the row holding it
            k = (i - p) % 6
            if k > 3: k -= 6           # rows -3..3 cover every field; use the nearer copy
            return window[(k, pos)]
        ok = all(F(4, w) == 0 for w in W)
        ok = ok and all(F(0, w) == (F(5, w) ^ F(5, add(w, ev))) for w in W if add(w, ev) in Wset)
        ok = ok and all(F(1, w) == (1 ^ F(5, w) ^ F(5, add(w, mev))) for w in W if add(w, mev) in Wset)
        if ok and dynamical:
            for g in (mev, (0,) * d, ev):
                if not all(add(g, m) in Wset for m in M):
                    continue
                y = H.eval_patch(lambda m: F(5, add(g, m)))
                ok = ok and (F(2, g) == (F(5, g) ^ y))
                z = H.eval_patch(lambda m: F(5, add(g, m)) ^ F(2, add(g, m)))
                ok = ok and (F(3, g) == (F(5, g) ^ z))
                if not ok:
                    break
        if ok:
            admissible.append(p)
    return admissible

def entry_output(H, window, e, p):
    """Native child output at row 0 given the decoded phase p (affine gauge)."""
    d = H.d; M = H.memory
    ev = tuple(e); mev = tuple(-c for c in e); zero = (0,) * d
    def add(a, b): return tuple(x + y for x, y in zip(a, b))
    def F(i, pos):
        k = (i - p) % 6
        if k > 3: k -= 6
        return window[(k, pos)]
    a = H.eval_patch(lambda m: F(5, m))
    b = H.eval_patch(lambda m: F(5, add(ev, m)))
    c = H.eval_patch(lambda m: F(5, add(mev, m)))
    dd = H.eval_patch(lambda m: F(5, m) ^ F(2, m))
    ee = H.eval_patch(lambda m: F(5, m) ^ F(3, m))
    return [a ^ b, 1 ^ a ^ c, a ^ dd, a ^ ee, 0, a][p], F(5, zero)

def windows_from_torus(H, X, e, cells=((0,),)):
    """(window, true phase, true output, true X) for the six rows above each listed
    cell. Only phase 0 and the listed cells are needed: rotating the child rows
    or translating the torus relabels the same window family consistently, so
    the collision and decoder checks over this family are complete."""
    d = H.d; M = H.memory
    ev = tuple(e); mev = tuple(-c for c in e)
    def add(a, b): return tuple(x + y for x, y in zip(a, b))
    W = sorted({add(m, s) for m in M for s in (mev, (0,) * d, ev)})
    child = lift(H, X, ev, mev, 0)
    child_next = lift(H, H.step(X), ev, mev, 0)
    shape = X.shape
    out = []
    for cell in cells:
        cell = tuple(c % s for c, s in zip(cell, shape)) if len(cell) == len(shape) else (0,) * len(shape)
        for r0 in range(6):
            window = {}
            for k in range(-3, 4):
                row = (r0 + k) % 6
                for w in W:
                    pos = tuple((c + o) % s for c, o, s in zip(cell, w, shape))
                    window[(k, w)] = int(child[(row,) + pos])
            out.append((window, r0, int(child_next[(r0,) + cell]), int(X[cell])))
    return out

def key(window):
    return bytes(window[k] for k in sorted(window))

def run_entry_checks(H, sources, e, label, cells=((0,),)):
    """sources: iterable of torus arrays. Returns a summary dict."""
    n_windows = 0; wrong_phase = 0; multi = 0; none = 0; out_mismatch = 0; rec_mismatch = 0
    table = {}; collisions = 0
    for X in sources:
        for window, phase, true_out, true_x in windows_from_torus(H, X, e, cells):
            n_windows += 1
            adm = entry_decode(H, window, e, dynamical=True)
            if len(adm) == 0: none += 1
            elif len(adm) > 1: multi += 1
            elif adm[0] != phase: wrong_phase += 1
            else:
                o, x = entry_output(H, window, e, adm[0])
                if o != true_out: out_mismatch += 1
                if x != true_x: rec_mismatch += 1
            k = key(window)
            v = (true_out, true_x, phase)
            if table.setdefault(k, v) != v: collisions += 1
    return {'label': label, 'windows': n_windows, 'no_admissible_phase': none,
            'multiple_admissible_phases': multi, 'wrong_unique_phase': wrong_phase,
            'native_output_mismatch': out_mismatch, 'recovery_mismatch': rec_mismatch,
            'distinct_windows': len(table), 'window_collisions': collisions,
            'pass': none == multi == wrong_phase == out_mismatch == rec_mismatch == collisions == 0}

def ring_words(n):
    return [np.array([(w >> i) & 1 for i in range(n)], dtype=np.uint8) for w in range(1 << n)]

# ----------------------------------------------------------------------------
# section C: row-algebra witnesses
# ----------------------------------------------------------------------------

def row_algebra_witnesses():
    """The proof's syntactic false phases (proof section 27). Windows are built
    directly from field rows, not from a trajectory. With the F2/F3 dynamical
    checks off, a wrong rotation passes the rail and F4 checks; with them on,
    no rotation passes under ANY of the 256 ECA rules, because the witness
    cannot be a trajectory of a single local rule (the dynamical contradiction
    the entry lemma uses is rule-free). Candidate p means "row 0 carries field
    p", so the proof's rotation s appears here as p = -s mod 6."""
    e = (1,); W = [(-2,), (-1,), (0,), (1,), (2,)]
    def const_window(rows):
        return {(k, w): rows[k % 6] for k in range(-3, 4) for w in W}
    alt = {}
    for k in range(-3, 4):
        for w in W:
            x = w[0] % 2
            alt[(k, w)] = [1, 0, x, 1, 0, x][k % 6]
    witnesses = {
        'constant_010100_X0_Y0_Z1': const_window([0, 1, 0, 1, 0, 0]),
        'constant_010001_X1_Y1_Z1': const_window([0, 1, 0, 0, 0, 1]),
        'alternating_10X10X_rot3': alt}
    res = {}
    for name, window in witnesses.items():
        syn = entry_decode(eca(90), window, e, dynamical=False)
        dyn = sorted({p for r in range(256) for p in entry_decode(eca(r), window, e, dynamical=True)})
        res[name] = {'syntactic_admissible': syn, 'dynamical_admissible_any_rule': dyn}
    # The false READING is what must be excluded: (X,Y,Z) = (0,0,1) constant is
    # impossible for every local rule (Y = H(X) = 0 forces H(0) = 0, but then
    # Z = H(Y) = H(0) = 0); the alternating witness likewise. Its rotation
    # (X,Y,Z) = (1,1,1) is a genuine trajectory for rules with h(1..1) = 1, and
    # is correctly accepted there: rotation ambiguity is broken by dynamics.
    w1, w2, w3 = (res['constant_010100_X0_Y0_Z1'], res['constant_010001_X1_Y1_Z1'], res['alternating_10X10X_rot3'])
    res['pass'] = (w1['syntactic_admissible'] == [0, 4] and w2['syntactic_admissible'] == [0, 2]
                   and w3['syntactic_admissible'] == [0, 3]
                   and 0 not in w1['dynamical_admissible_any_rule']      # reading (0,0,1) never a trajectory
                   and 2 not in w2['dynamical_admissible_any_rule']      # same reading via the rotated codeword
                   and w3['dynamical_admissible_any_rule'] == [])
    return res

# ----------------------------------------------------------------------------
# section D: recursion at D3 via collision checks on the finite ring family
# ----------------------------------------------------------------------------

def d3_recursion(rule, n):
    """Lift the D2 beam of an ECA root once more with diagonal rails and check
    that the D3 window {-3..3}(a2) x {-3..3}(a1) x {-2..2}(x) is a neighbourhood
    for phase, parent D2 cell and native output, over all 2^n source words.
    Row rotations of either lifted axis relabel the same window family, so
    phase 0 on both axes suffices; the recorded phase is the a2 row index."""
    from numpy.lib.stride_tricks import sliding_window_view
    H = eca(rule)
    vp = (1, 1); vm = (1, -1)   # a1 + e1, a1 - e1 in (a1, x) coordinates
    keys = []; vals = []
    for X in ring_words(n):
        Xs = [X]
        for _ in range(3): Xs.append(H.step(Xs[-1]))
        L = [lift(H, Y, (1,), (-1,), 0) for Y in Xs]            # D2 beams of X, HX, H^2X, H^3X
        X1, X1n, X1nn, X1nnn = L
        F = [X1 ^ shift(X1, vp), 1 ^ X1 ^ shift(X1, vm), X1 ^ X1n, X1 ^ X1nn, np.zeros_like(X1), X1]
        Fn = [X1n ^ shift(X1n, vp), 1 ^ X1n ^ shift(X1n, vm), X1n ^ X1nn, X1n ^ X1nnn, np.zeros_like(X1), X1n]
        child = np.stack(F, axis=0); child_next = np.stack(Fn, axis=0)   # (6,6,n)
        pad = np.pad(child, ((3, 3), (3, 3), (2, 2)), mode='wrap')
        win = sliding_window_view(pad, (7, 7, 5))                        # (6,6,n,7,7,5)
        keys.append(np.packbits(win.reshape(6 * 6 * n, 245), axis=1))
        r2 = np.repeat(np.arange(6), 6 * n)
        r1 = np.tile(np.repeat(np.arange(6), n), 6)
        xx = np.tile(np.arange(n), 36)
        vals.append(np.stack([child_next.reshape(-1), X1[r1, xx], r2], axis=1))
    K = np.concatenate(keys); V = np.concatenate(vals)
    _, first, inv = np.unique(K, axis=0, return_index=True, return_inverse=True)
    inv = inv.reshape(-1)
    collisions = int(np.sum(np.any(V != V[first][inv], axis=1)))
    return {'rule': rule, 'width': n, 'windows': int(len(K)), 'distinct_windows': int(len(first)),
            'collisions': collisions, 'pass': collisions == 0}

# ----------------------------------------------------------------------------
# section E: Groovy identities on the 7-ring
# ----------------------------------------------------------------------------

def groovy_identities(n=7):
    states = ring_words(n)
    zero = np.zeros(n, dtype=np.uint8)
    res = {'ring': n, 'identity_failures': {}, 'centered_G_zero_rules': [], 'all_pairs_polarization_zero_rules': [],
           'cocycle_failures': 0, 'residual_failures': 0, 'grading_failures': 0}
    for rule in range(256):
        H = eca(rule); step = H.step
        def D(X): return X ^ step(X)
        def G(X): return D(step(X)) ^ step(D(X))
        def B(X, U): return step(X ^ U) ^ step(X) ^ step(U) ^ step(zero)
        def dH(X, U): return step(X) ^ step(X ^ U)
        gz = True; fails = 0
        for X in states:
            Gc = G(X) ^ step(zero)
            if not np.array_equal(Gc, B(X, D(X))): fails += 1
            if Gc.any(): gz = False
            # affine-jet residual: Lambda_1(X) xor Lambda_1(H X) xor Lambda_0(D X) = (0,0,K1,K2,0,0)
            U = D(X)
            L1X = fields(H, X, (1,), (-1,))
            L1HX = fields(H, step(X), (1,), (-1,))
            L0U = fields(H, U, (1,), (-1,)); L0U[1] = L0U[1] ^ 1   # m = 0 marker
            resid = [L1X[i] ^ L1HX[i] ^ L0U[i] for i in range(6)]
            K1 = G(X)
            K2 = D(step(step(X))) ^ step(step(U))
            expect = [zero, zero, K1, K2, zero, zero]
            if not all(np.array_equal(resid[i], expect[i]) for i in range(6)): res['residual_failures'] += 1
            # cocycle K_{t+1} = G(H^t X) xor dH_{H^t D X}(K_t) for t = 0..3
            Kt = zero.copy(); Ht = X.copy(); Bt = U.copy()
            for t in range(4):
                Knext = D(step(Ht)) ^ step(Bt)
                if not np.array_equal(Knext, G(Ht) ^ dH(Bt, Kt)): res['cocycle_failures'] += 1
                Kt, Ht, Bt = Knext, step(Ht), step(Bt)
        if fails: res['identity_failures'][rule] = fails
        if gz: res['centered_G_zero_rules'].append(rule)
        if all(not B(X, U).any() for X in states for U in states[::5]):
            res['all_pairs_polarization_zero_rules'].append(rule)
    # signed translations
    for v in (1, -1, 2):
        for eps in (0, 1):
            T = lambda X: (np.roll(X, -v) ^ eps).astype(np.uint8)
            for X in states:
                DT = lambda X: X ^ T(X)
                if not np.array_equal(DT(T(X)) ^ T(DT(X)), np.full(n, eps, dtype=np.uint8)): res['grading_failures'] += 1
    res['pass'] = (not res['identity_failures'] and res['residual_failures'] == 0 and res['cocycle_failures'] == 0
                   and res['grading_failures'] == 0
                   and res['all_pairs_polarization_zero_rules'] == [0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195, 204, 240, 255]
                   and res['centered_G_zero_rules'] == sorted(set([0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195, 204, 240, 255] + [4, 200])))
    return res

# ----------------------------------------------------------------------------

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    t0 = time.time()
    rng = np.random.default_rng(20260917)
    report = {'schema': 'affine-lift-verification-v1', 'date': '2026-09-17',
              'source_hashes': {'script': sha(pathlib.Path(__file__)), 'proof': sha(PROOF)}}

    # A: ECA entry on 9-bit dependency words. Use a ring of width 9: every window then
    # sees exactly the 9 source bits it depends on, and all 512 words are enumerated.
    A = {}
    for rule in range(256):
        A[rule] = run_entry_checks(eca(rule), ring_words(9), (1,), f'eca{rule}')
    report['A_eca_entry'] = {'per_rule_pass': sum(v['pass'] for v in A.values()), 'rules': 256,
                             'windows_per_rule': A[0]['windows'],
                             'failures': {r: v for r, v in A.items() if not v['pass']}}
    print('A', report['A_eca_entry']['per_rule_pass'], '/256', f'{time.time()-t0:.0f}s', flush=True)

    # B1: radius-two rules on 15-bit words (ring 15), 6 random tables + 2 shift rules.
    B1 = []
    tables = [int(x) for x in rng.integers(0, 1 << 32, size=6)] + [0b10101010101010101010101010101010, 0xF0F0F0F0]
    for tb in tables:
        B1.append(run_entry_checks(radius2(tb), ring_words(15), (1,), f'r2-{tb}'))
    report['B1_radius2_entry'] = {'rules': len(B1), 'pass': sum(v['pass'] for v in B1),
                                  'windows_per_rule': B1[0]['windows'], 'tables': tables,
                                  'failures': [v for v in B1 if not v['pass']]}
    print('B1', report['B1_radius2_entry']['pass'], '/', len(B1), f'{time.time()-t0:.0f}s', flush=True)

    # B2: Life. Exhaustive 3x3 torus (512 states) and 400 random 7x7 tori, e = (0,1).
    L = life()
    tori3 = [np.array([(w >> i) & 1 for i in range(9)], dtype=np.uint8).reshape(3, 3) for w in range(512)]
    b2a = run_entry_checks(L, tori3, (0, 1), 'life-3x3-exhaustive')
    tori7 = [rng.integers(0, 2, size=(7, 7), dtype=np.uint8) for _ in range(400)]
    b2b = run_entry_checks(L, tori7, (0, 1), 'life-7x7-random-400', cells=tuple((i, j) for i in range(7) for j in range(7)))
    report['B2_life_entry'] = {'exhaustive_3x3': b2a, 'random_7x7': b2b}
    print('B2', b2a['pass'], b2b['pass'], f'{time.time()-t0:.0f}s', flush=True)

    # C
    report['C_row_algebra_witnesses'] = row_algebra_witnesses()
    print('C', report['C_row_algebra_witnesses'], flush=True)

    # D: recursion at D3, all 256 roots, width 7; width 8 for a 16-rule subset.
    D7 = [d3_recursion(r, 7) for r in range(256)]
    D8 = [d3_recursion(r, 8) for r in (0, 4, 18, 22, 30, 41, 54, 60, 90, 106, 110, 122, 126, 150, 184, 200)]
    report['D_recursion_d3'] = {'width7_pass': sum(v['pass'] for v in D7), 'width7_rules': 256,
                                'width7_windows_per_rule': D7[0]['windows'],
                                'width8_pass': sum(v['pass'] for v in D8), 'width8_rules': [v['rule'] for v in D8],
                                'failures': [v for v in D7 + D8 if not v['pass']]}
    print('D', report['D_recursion_d3']['width7_pass'], '/256;', report['D_recursion_d3']['width8_pass'], '/16', f'{time.time()-t0:.0f}s', flush=True)

    # E
    report['E_groovy_identities'] = groovy_identities(7)
    print('E', report['E_groovy_identities']['pass'], f'{time.time()-t0:.0f}s', flush=True)

    report['summary'] = {
        'A_eca_entry_pass': report['A_eca_entry']['per_rule_pass'] == 256,
        'B1_radius2_pass': report['B1_radius2_entry']['pass'] == len(B1),
        'B2_life_pass': b2a['pass'] and b2b['pass'],
        'C_witnesses_pass': report['C_row_algebra_witnesses']['pass'],
        'D_recursion_pass': report['D_recursion_d3']['width7_pass'] == 256 and report['D_recursion_d3']['width8_pass'] == 16,
        'E_identities_pass': report['E_groovy_identities']['pass'],
        'wall_seconds': round(time.time() - t0, 1)}
    report['summary']['all_pass'] = all(v for k, v in report['summary'].items() if k.endswith('_pass'))
    OUT.write_text(json.dumps(report, indent=1, sort_keys=True) + '\n')
    print(json.dumps(report['summary'], indent=1))
    return 0 if report['summary']['all_pass'] else 1

if __name__ == '__main__':
    sys.exit(main())
