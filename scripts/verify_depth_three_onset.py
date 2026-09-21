#!/usr/bin/env python3
"""The depth-three onset N3_psi, certified at every ring by sparse boolean powers
restricted to the carrying strong components (protocol frozen 2026-09-13,
re-frozen after Codex's gate-1 round one B1/B2, gate-1 approval by Codex
(OpenAI GPT-5.6 Sol) on the exact head
5a557f91605a1886c648c6cc6f71c8ffca4c0408 before this implementation; see the
protocol's Section 5).

Observations psi in {232, 4, 32, 200, 22, 102, 90, 150} with their complement
conjugates as controls; rules r in 0..255. The depth-three pair graph
G3_{psi,r} is the sixteenth unit's `pair_graph(psi, r, 3)`, imported from
scripts/verify_full_shift_depth_three.py and NOT rebuilt here: 4^8 = 65,536
eight-cell pair-block vertices, an edge per nine-cell pair block whose centre
agrees on psi F^k for k = 0..3, a violating three-edge walk per eleven-cell pair
block whose psi F^4 disagrees at the centre, recorded by its end pair (v0, v3).
Out-degree is at most four at every depth (an edge appends one of four pair
cells); the verifier asserts it and reports the measured maximum.

Ring criterion (theorem, thirteenth/fourteenth/eighteenth units). For n >= 4,
  r not in D3_psi(n)  iff  some (v0, v3) in V3_cl has (A^(n-3))[v3, v0] = 1,
where V3_cl are the violating walks whose ends lie in one strong component (the
eighteenth unit's pruning lemma and the nineteenth unit's Lemma A). A rule with
V3_cl empty is trivially certified at every ring with no power computed.

RESTRICTION LEMMA (protocol Section 1, the new object of this unit; gate-1
checked). Let U be the union of the CARRYING strong components -- those holding
an end of some closed violating walk -- and let A_U be A restricted to U with
only the edges internal to a single carrying component kept (the direct sum of
the carrying components' adjacency matrices). Then for every (v0, v3) in V3_cl
and every m >= 0,

      (A^m)[v3, v0]  =  (A_U^m)[v3, v0].

Proof: a walk v3 ~> v0 of length m in G3 has every vertex reachable from v3 and
reaching v0, hence lies in the strong component of v3 = that of v0, so every
edge of the walk is internal to that component and the walk exists in A_U;
conversely every walk in A_U is a walk in A. So the hit sequence
b_m = [exists (v0, v3) in V3_cl : (A^m)[v3, v0] = 1] -- and with it the ring
membership r in D3_psi(n) iff b_(n-3) = 0 -- is computed exactly from the powers
of A_U. This is the lever the eighteenth unit lacked: a packed power of the full
65,536-vertex matrix is 2^32 bits = 512 MiB and about 20.8 s, while |U| has
median 1,726 and maximum 14,168 over the nineteenth unit's 790 pairs with a
closed violation, at which 64 ms per power.

THE RESTRICTED CERTIFICATE (k, p) IS A PROPERTY OF A_U, NOT OF A. It may differ
from the (k, p) the full matrix would give, and is reported as the restricted
certificate; every derived quantity (b, the membership sequence, its eventual
period, the rule onset, N3_psi, P3_psi, D3_psi(n), D3_psi^inf) is a function of
b alone and is therefore the same under either matrix by the lemma.

Powers, repeat detection, cap and censoring: the eighteenth unit's, unchanged
except that the vertex count and the words per row are parameters of the
restricted matrix. A_U^m[u, :] = OR over w in out_U(u) of A_U^(m-1)[w, :], at
most four row gathers and three ORs on packed uint64 rows. The SHA-256 of each
power is stored against its exponent; on a hash hit A_U^k is recomputed from
A_U^0 and compared byte for byte before the certificate (k, p) is accepted, so a
collision can only delay a certificate, never falsify one. A pair whose powers
have not repeated by A_U^POWER_CAP (1024, frozen) is CENSORED: its membership is
decided only for 4 <= n <= cap + 3, and no observation-level all-ring verdict is
inferred through it.

Onsets. m_r(n) = [r in D3_psi(n)] for n >= 4; p_r is the least eventual period of
b (the eighteenth unit's `rule_period`); given the observation-level period P,
the rule onset N_r(P) is the least N >= 4 with m_r(n + P) = m_r(n) for all
n >= N (the eighteenth unit's `rule_onset`, which starts at max(4, k + 3) and
walks back one newly exposed equality at a time -- exact because periodicity is
certified from the RESTRICTED k, with no assumption that it equals any
full-matrix k). Trivially certified rules have N_r = 4. P3_psi = lcm_r p_r,
N3_psi = max_r N_r(P3_psi), and D3_psi^inf is the intersection over one period
from the onset.

T1  theorem and consistency controls, all against data read with its hash:
    (a) the restricted method at DEPTH TWO reproduces the eighteenth unit's
        certified D2_psi(n), P2_psi = 1, 2, 2, 1, 12, 1, 4, 6 and
        N2_psi = 14, 13, 13, 13, 31, 4, 9, 7 for all 2,048 pairs, nothing
        censored, with the restricted (k, p) reported beside the eighteenth
        unit's full-matrix (k, p) and NO bet on their equality;
    (b) depth three against the sixteenth/seventeenth units' recorded rings
        4..14, with FS3 subset of every certified D3_psi(n) and divisibility;
    (c) depth three against the nineteenth unit's record: b vanishes below
        n_min - 3 and fires there, the eventual period of b equals p_r, b on the
        certified tail is the indicator of R_r, P3_psi = 1, 2, 2, 1, 1, 2, 6 and
        the eventual sets and D3_psi^inf are reproduced;
    (d) the restriction itself, by two independent unrestricted paths -- exact
        length frontier reachability on the unpacked 65,536-vertex adjacency for
        b_1..b_40 on the frozen sample (the three smallest rules with V3_cl
        nonempty per source observation), and six packed powers of the FULL
        65,536-vertex matrix agreeing with A_U^1..A_U^6 on every queried entry
        for one pair per source observation.
    A failure of any part of T1 is an implementation error or a flaw in the
    restriction lemma and stops the unit.
T2  per-pair certificate status, restricted (k, p), |U|, carrying-component
    count, max out-degree; per observation the largest k, lcm of periods,
    P3_psi, N3_psi, the certified list D3_psi(4..N3+P3-1), D3_psi^inf, status
    counts, powers taken, hash collisions; per rule the onset N_r.
T3  the unit's bets: (a) N3_232 = 65 realized by rules 94 and 133 alone, no
    other rule under 232 above onset 20; (b) every other observation's onset at
    most the depth-two record 31, with N3_200 <= 22, N3_4 = N3_32 <= 15,
    N3_22 <= 16, N3_90 <= 10, N3_150 <= 7; (c) N3_psi - max_r n_min(r) >= 6
    somewhere and = 0 somewhere; (d) no rule onset above 65 and nothing
    censored.  Theorem background, period-aware (protocol Section 5, B1):
    N_r(P) >= max(4, n_min(r) - P + 1), hence N3_psi >= max_r max(4, n_min - P + 1).
T4  complement and reflection transport of certificate status, restricted
    (k, p), |U|, N_r, P3_psi, N3_psi and every certified ring set; and, on the
    frozen T1(d) sample, the explicit vertex maps carrying U and the internal
    edge set of A_U onto the image pair's (complement v -> v xor (4^8 - 1);
    reflection v -> reversed cells, which transposes A and swaps the violating
    ends).

Usage:
    python scripts/verify_depth_three_onset.py                  # canonical run
    python scripts/verify_depth_three_onset.py --self-test      # < 2 min, writes nothing
    python scripts/verify_depth_three_onset.py --probe 232 --rules 94,133
                                                                # probe, writes nothing
The self test exercises the restriction lemma on synthetic graphs with two
carrying components of coprime periods plus transient structure and
cross-component edges outside U, against explicit dense unrestricted powers; the
onset machinery against a brute-force membership sequence from those dense
powers; the repeat scan under a deliberately weakened hash and past the cap; the
restricted method at depth two under one observation against the eighteenth
unit's certified list; and the T4 transport machinery at depth two under
complement and reflection including the explicit vertex maps on U and A_U. It
writes nothing.
"""
from __future__ import annotations
import hashlib, importlib.util, json, math, pathlib, sys, time
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
SIXTEENTH_SCRIPT = ROOT / 'scripts/verify_full_shift_depth_three.py'
EIGHTEENTH_SCRIPT = ROOT / 'scripts/verify_depth_two_certificate.py'
NINETEENTH_SCRIPT = ROOT / 'scripts/verify_closed_violation_depth_three.py'
DEPTH_TWO_CERT = ROOT / 'results/depth_two_certificate_20260912.json'
CLOSED_VIOLATION_THREE = ROOT / 'results/closed_violation_depth_three_20260913.json'
FULL_SHIFT_THREE = ROOT / 'results/full_shift_depth_three_20260912.json'
FULL_SHIFT_THREE_LINEAR = ROOT / 'results/full_shift_depth_three_linear_20260912.json'
OUT = ROOT / 'results/depth_three_onset_20260913.json'

OBS = (232, 4, 32, 200, 22, 102, 90, 150)
DEPTH_THREE_OBS = (232, 4, 32, 200, 22, 90, 150)   # 102 has FS3 = all 256, nothing outside it
RINGS = tuple(range(3, 15))                        # rings recorded by the sixteenth/seventeenth units
GRAPH_RINGS = tuple(range(4, 15))                  # rings the criterion covers within that range
POWER_CAP = 1024                                   # frozen: A_U^0..A_U^cap, first confirmed repeat or censored
MAX_OUT_DEGREE = 4                                 # structural at every depth; asserted, never assumed silently
FRONTIER_SAMPLE_RULES = 3                          # frozen T1(d) sample: smallest rules with V3_cl nonempty
FRONTIER_POWERS = 40                               # frozen: b_1..b_40 against unrestricted frontier reachability
FULL_MATRIX_POWERS = 6                             # frozen: A^1..A^6 of the full 65,536-vertex matrix
FULL_MATRIX_ROW_CHUNK = 2048                       # gather in row chunks so the temporary stays ~128 MiB
SELF_TEST_OBS = 232                                # self test only: the depth-two reproduction observation
SELF_TEST_TRANSPORT_RULES = 6                      # self test only: pairs compared under the vertex maps
SELF_TEST_DENSE_POWERS = 60                        # self test only: dense unrestricted reference length

# The eighteenth unit's certified depth-two account, for T1(a); values re-read from its result file at
# run time and these constants are the frozen expectation the protocol names.
P2_CERTIFIED = {232: 1, 4: 2, 32: 2, 200: 1, 22: 12, 102: 1, 90: 4, 150: 6}
N2_CERTIFIED = {232: 14, 4: 13, 32: 13, 200: 13, 22: 31, 102: 4, 90: 9, 150: 7}
# The nineteenth unit's recorded depth-three observation periods, for T1(c).
P3_RECORDED = {232: 1, 4: 2, 32: 2, 200: 1, 22: 1, 90: 2, 150: 6}
# T3's frozen bets.
BET_A_ONSET_232 = 65
BET_A_RULES_232 = (94, 133)
BET_A_OTHER_ONSET_CEILING = 20
BET_B_CEILING = {200: 22, 4: 15, 32: 15, 22: 16, 90: 10, 150: 7}
BET_B_DEPTH_TWO_RECORD = 31
BET_C_MARGIN = 6
BET_D_ONSET_CEILING = 65

# ---------------------------------------------------------------- prior units, imported not reimplemented
def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
U16 = _load(SIXTEENTH_SCRIPT, 'verify_full_shift_depth_three')
U18 = _load(EIGHTEENTH_SCRIPT, 'verify_depth_two_certificate')
U19 = _load(NINETEENTH_SCRIPT, 'verify_closed_violation_depth_three')

pair_graph = U16.pair_graph                   # the depth-h pair graph, verbatim (sixteenth unit)
strong_components = U16.strong_components     # iterative Tarjan
depth_two_graph = U18.depth_two_graph         # the fifteenth unit's 4096-vertex graph, for T1(a)
conj = U16.conj; mirror = U16.mirror; sha = U16.sha
member = U18.member                           # ring membership from a certificate (eighteenth unit)
rule_period = U18.rule_period                 # least eventual period of the membership sequence
rule_onset = U18.rule_onset                   # least N >= 4 from which m(n + P) = m(n)
vertex_complement = U19.vertex_complement     # v -> v xor (4^w - 1)
vertex_mirror = U19.vertex_mirror             # v -> reversed cells
vertices = U19.vertices; width = U19.width
read_history = U19.read_history               # the historical sets, read with their hashes
depth_three_domain = U19.depth_three_domain   # the nineteenth unit's frozen domain

assert U18.POWER_CAP == POWER_CAP, 'the frozen cap must match the eighteenth unit'

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
def transport(rules): return sorted(conj(r) for r in rules)

# ---------------------------------------------------------------- the restriction to carrying components
def carrying_restriction(adj, comp, closed):
    """U and the internal edges of the carrying components (the restriction lemma's A_U).

    Returns (order, index, out, max_degree): `order` the sorted global vertices of
    U, `index` the global -> local map, `out` the local adjacency keeping only
    edges internal to a single carrying component, and the measured maximum
    out-degree of that restricted adjacency.
    """
    ids = {comp[v] for pair in closed for v in pair}
    order = [v for v in range(len(adj)) if comp[v] in ids]
    index = {v: i for i, v in enumerate(order)}
    out = []
    maxdeg = 0
    for v in order:
        cv = comp[v]
        row = [index[w] for w in adj[v] if comp[w] == cv]          # internal to v's carrying component
        assert len(row) == len(set(row)), (v, row)
        maxdeg = max(maxdeg, len(row))
        out.append(row)
    assert maxdeg <= MAX_OUT_DEGREE, f'restricted out-degree {maxdeg} exceeds {MAX_OUT_DEGREE}'
    return order, index, out, maxdeg

def graph_max_out_degree(adj):
    return max((len(o) for o in adj), default=0)

# ---------------------------------------------------------------- sparse packed boolean powers of A_U
class Powers:
    """Boolean powers of an n-vertex adjacency of out-degree at most four.

    The eighteenth unit's packed representation with the vertex count and the
    words per row as parameters of the restricted matrix: rows of WORDS unsigned
    64-bit words, bit w of row u is A[u, w], and
      A^m[u, :] = OR over w in out(u) of A^(m-1)[w, :],
    a single fancy-index gather of shape (n, 4, WORDS) and three ORs. One padding
    row of zeros carries the out-degrees below four.
    """
    __slots__ = ('n', 'words', 'nb')
    def __init__(self, out):
        self.n = len(out); self.words = max(1, (self.n + 63) // 64)
        nb = np.full((self.n, MAX_OUT_DEGREE), self.n, dtype=np.int64)
        for u, outs in enumerate(out):
            assert len(outs) == len(set(outs)) <= MAX_OUT_DEGREE, (u, outs)
            for j, w in enumerate(outs): nb[u, j] = w
        self.nb = nb
    def identity(self):
        M = np.zeros((self.n + 1, self.words), dtype=np.uint64)
        idx = np.arange(self.n)
        M[idx, idx >> 6] = np.uint64(1) << (idx & 63).astype(np.uint64)
        return M
    def mul(self, P):
        Q = np.zeros((self.n + 1, self.words), dtype=np.uint64)
        step = max(1, FULL_MATRIX_ROW_CHUNK if self.n > 16384 else self.n)
        for lo in range(0, self.n, step):
            hi = min(self.n, lo + step)
            g = P[self.nb[lo:hi]]                                  # (chunk, 4, words)
            Q[lo:hi] = (g[:, 0] | g[:, 1]) | (g[:, 2] | g[:, 3])
        return Q
    def power(self, m):
        M = self.identity()
        for _ in range(m): M = self.mul(M)
        return M
    def body(self, P): return np.ascontiguousarray(P[:self.n])

def sha_power(P, n): return hashlib.sha256(np.ascontiguousarray(P[:n]).tobytes()).hexdigest()
def weak_hash(P, n): return sha_power(P, n)[:2]     # self test only: forces collisions

# ---------------------------------------------------------------- the repeat scan and the certificate
def scan(out, queries, cap=POWER_CAP, hashfn=sha_power):
    """Take powers of A_U until the first byte-confirmed repeat or the cap.

    `queries` are the closed violations as LOCAL (v0, v3) index pairs. Returns the
    status, k, p, the hit list b (b[m] iff some query has A_U^m[v3, v0] = 1), the
    powers taken including a confirmation's recomputation, and any hash
    collisions. A candidate equality is confirmed by recomputing A_U^k from
    A_U^0 and comparing byte for byte, so a collision only delays the scan.
    """
    P = Powers(out)
    rows = np.array([v3 for _, v3 in queries], dtype=np.int64)
    words = np.array([v0 >> 6 for v0, _ in queries], dtype=np.int64)
    masks = np.array([1 << (v0 & 63) for v0, _ in queries], dtype=np.uint64)
    def hit(M): return bool(np.any(M[rows, words] & masks))
    cur = P.identity(); b = [hit(cur)]; table = {hashfn(cur, P.n): [0]}; taken = 0; collisions = []
    for m in range(1, cap + 1):
        cur = P.mul(cur); taken += 1; b.append(hit(cur)); h = hashfn(cur, P.n)
        seen = table.setdefault(h, [])
        confirmed = None
        for k in seen:                                             # earliest exponent first
            again = P.power(k); taken += k
            if np.array_equal(P.body(again), P.body(cur)): confirmed = k; break
            collisions.append({'hash': h, 'exponent': m, 'candidate_exponent': k})
        if confirmed is not None:
            return {'status': 'certified', 'k': confirmed, 'p': m - confirmed, 'b': b,
                    'powers_taken': taken, 'collisions': collisions}
        seen.append(m)
    return {'status': 'censored', 'k': None, 'p': None, 'b': b, 'powers_taken': taken,
            'collisions': collisions}

TRIVIAL_BY_THEOREM = 'trivially_certified_by_theorem'

def theorem_trivial_cert():
    """A rule in FS^h: V^h_cl is empty by theorem, so it is in D^h(n) at every ring, no graph built."""
    return {'status': 'trivially_certified', 'reason': TRIVIAL_BY_THEOREM, 'k': None, 'p': None,
            'b': None, 'powers_taken': 0, 'collisions': [], 'violating_walks': None,
            'closed_violating_walks': 0, 'restricted_vertices': 0, 'carrying_components': 0,
            'max_out_degree': None, 'restricted_max_out_degree': None, 'computed': False}

def pair_certificate(psi, r, h, cap=POWER_CAP, graph=None):
    """The restricted certificate of (psi, r) at depth h: trivially certified, (k, p), or censored."""
    if graph is None:
        adj, walks = (depth_two_graph(psi, r) if h == 2 else pair_graph(psi, r, h)[:2])
    else:
        adj, walks = graph
    comp = strong_components(adj)
    closed = [(v0, v3) for v0, v3 in walks if comp[v0] == comp[v3]]
    deg = graph_max_out_degree(adj)
    assert deg <= MAX_OUT_DEGREE, f'({psi}, {r}, h={h}) has out-degree {deg}'
    base = {'violating_walks': len(walks), 'closed_violating_walks': len(closed),
            'max_out_degree': deg, 'computed': True}
    if not closed:
        c = {'status': 'trivially_certified', 'reason': 'no_closed_violating_walk', 'k': None, 'p': None,
             'b': None, 'powers_taken': 0, 'collisions': [], 'restricted_vertices': 0,
             'carrying_components': 0, 'restricted_max_out_degree': None}
        c.update(base); return c
    order, index, out, rdeg = carrying_restriction(adj, comp, closed)
    queries = sorted({(index[v0], index[v3]) for v0, v3 in closed})
    c = scan(out, queries, cap=cap)
    c.update(base)
    c.update({'reason': None, 'restricted_vertices': len(order),
              'carrying_components': len({comp[v] for pair in closed for v in pair}),
              'restricted_max_out_degree': rdeg})
    return c

def restricted_parts(psi, r, h):
    """(order, index, out, queries) of A_U, for the T1(d) and T4 cross-checks."""
    adj, walks = (depth_two_graph(psi, r) if h == 2 else pair_graph(psi, r, h)[:2])
    comp = strong_components(adj)
    closed = [(v0, v3) for v0, v3 in walks if comp[v0] == comp[v3]]
    if not closed: return None
    order, index, out, _ = carrying_restriction(adj, comp, closed)
    return {'adj': adj, 'comp': comp, 'closed': closed, 'order': order, 'index': index, 'out': out,
            'queries': sorted({(index[v0], index[v3]) for v0, v3 in closed})}

# ---------------------------------------------------------------- observation-level analysis
def analyse(psi, h, computed_rules, cap=POWER_CAP, verbose=False):
    """Certificates for every rule, then P^h_psi, N^h_psi, the certified ring sets and D^h_psi^inf.

    `computed_rules` is the frozen domain for this observation; every other rule is
    trivially certified BY THEOREM (it lies in FS^h, so V^h_cl is empty and it is
    in D^h(n) at every ring) and no graph is built for it.
    """
    certs = {r: theorem_trivial_cert() for r in range(256)}
    for r in computed_rules:
        certs[r] = pair_certificate(psi, r, h, cap=cap)
        if verbose and certs[r]['closed_violating_walks']:
            print(f'  psi={psi} h={h} r={r:3d} {certs[r]["status"]:12s} k={certs[r]["k"]} p={certs[r]["p"]} '
                  f'|U|={certs[r]["restricted_vertices"]:6d} comps={certs[r]["carrying_components"]} '
                  f'|Vcl|={certs[r]["closed_violating_walks"]}', flush=True)
    censored = [r for r in range(256) if certs[r]['status'] == 'censored']
    trivial = [r for r in range(256) if certs[r]['status'] == 'trivially_certified']
    ks = [certs[r]['k'] for r in range(256) if certs[r]['status'] == 'certified']
    g = {'certs': certs, 'censored': censored, 'trivial': trivial, 'max_k': max(ks) if ks else 0,
         'powers_taken': sum(certs[r]['powers_taken'] for r in range(256)),
         'collisions': [dict(c, rule=r) for r in range(256) for c in certs[r]['collisions']]}
    if censored:
        g.update({'L': None, 'P': None, 'N': None, 'all_ring': None, 'onsets': None,
                  'decided_rings': (4, cap + 3),
                  'D': {n: sorted(r for r in range(256) if member(certs[r], n)) for n in range(4, cap + 4)}})
        return g
    L = lcm_all([certs[r]['p'] for r in range(256) if certs[r]['status'] == 'certified'])
    P = lcm_all([rule_period(certs[r]) for r in range(256)])
    onsets = {r: rule_onset(certs[r], P) for r in range(256)}
    N = max(onsets.values())
    D = {n: sorted(r for r in range(256) if member(certs[r], n)) for n in range(4, max(N + P, 15))}
    # D^inf is the intersection over EVERY ring n >= 4, not only over one period from the onset: a
    # rule can fail at a ring below N and hold from N on.  By periodicity from N every ring n >= N
    # equals one of N..N+P-1, so rings 4..N+P-1 exhaust the intersection (the eighteenth unit's range).
    inf = sorted(set.intersection(*[set(D[n]) for n in range(4, N + P)]))
    g.update({'L': L, 'P': P, 'N': N, 'onsets': onsets, 'all_ring': inf, 'decided_rings': (4, None), 'D': D})
    return g

def membership_set(g, n):
    """D^h(n) from an analysis, computed on demand beyond the stored range."""
    if n in g['D']: return g['D'][n]
    ms = [member(g['certs'][r], n) for r in range(256)]
    return None if any(m is None for m in ms) else sorted(r for r in range(256) if ms[r])

def certified_rings(g):
    return range(4, POWER_CAP + 4) if g['censored'] else range(4, g['N'] + g['P'])

# ---------------------------------------------------------------- unrestricted cross-checks (T1(d))
def frontier_bits(adj, closed, count):
    """b_1..b_count by EXACT-LENGTH frontier reachability on the unrestricted adjacency.

    Independent of the packed powers and of the restriction: for each v3 the set of
    vertices reachable in exactly m steps is advanced as a plain set of ints, and
    b_m is whether any closed violation's v0 lies in its v3's frontier. This is the
    path the nineteenth unit used to re-derive its I1 correction.
    """
    by_v3 = {}
    for v0, v3 in closed: by_v3.setdefault(v3, set()).add(v0)
    frontier = {v3: {v3} for v3 in by_v3}
    bits = []
    for _ in range(count):
        for v3 in frontier:
            nxt = set()
            for u in frontier[v3]: nxt.update(adj[u])
            frontier[v3] = nxt
        bits.append(any(by_v3[v3] & frontier[v3] for v3 in by_v3))
    return bits

def restricted_bits(out, queries, count):
    """b_1..b_count from the packed powers of A_U."""
    P = Powers(out); cur = P.identity(); bits = []
    rows = np.array([v3 for _, v3 in queries], dtype=np.int64)
    words = np.array([v0 >> 6 for v0, _ in queries], dtype=np.int64)
    masks = np.array([1 << (v0 & 63) for v0, _ in queries], dtype=np.uint64)
    for _ in range(count):
        cur = P.mul(cur); bits.append(bool(np.any(cur[rows, words] & masks)))
    return bits

def full_matrix_entry_check(adj, closed, out, queries, order, count=FULL_MATRIX_POWERS):
    """A^1..A^count of the FULL matrix agree with A_U^1..A_U^count on every queried entry.

    The full matrix is taken by the same gather-OR recurrence with no restriction
    (65,536 rows of 1,024 words = 512 MiB per power); the gather is chunked so the
    temporary stays bounded. Compared entry by entry against the restricted powers.
    """
    full = Powers([list(o) for o in adj]); res = Powers(out)
    fc, rc = full.identity(), res.identity()
    frows = np.array([v3 for _, v3 in closed], dtype=np.int64)
    fwords = np.array([v0 >> 6 for v0, _ in closed], dtype=np.int64)
    fmasks = np.array([1 << (v0 & 63) for v0, _ in closed], dtype=np.uint64)
    rrows = np.array([v3 for _, v3 in queries], dtype=np.int64)
    rwords = np.array([v0 >> 6 for v0, _ in queries], dtype=np.int64)
    rmasks = np.array([1 << (v0 & 63) for v0, _ in queries], dtype=np.uint64)
    # the global closed pairs in the order of `closed`, as local pairs, so entries line up
    loc = {v: i for i, v in enumerate(order)}
    lrows = np.array([loc[v3] for _, v3 in closed], dtype=np.int64)
    lwords = np.array([loc[v0] >> 6 for v0, _ in closed], dtype=np.int64)
    lmasks = np.array([1 << (loc[v0] & 63) for v0, _ in closed], dtype=np.uint64)
    mismatches = []
    for m in range(1, count + 1):
        fc = full.mul(fc); rc = res.mul(rc)
        fe = (fc[frows, fwords] & fmasks) != 0
        re_ = (rc[lrows, lwords] & lmasks) != 0
        if not np.array_equal(fe, re_):
            bad = np.nonzero(fe != re_)[0][:8].tolist()
            mismatches.append({'exponent': m, 'entries': [list(closed[i]) for i in bad]})
        if bool(np.any(fc[frows, fwords] & fmasks)) != bool(np.any(rc[rrows, rwords] & rmasks)):
            mismatches.append({'exponent': m, 'entries': 'hit-bit disagreement'})
    del fc, rc
    return mismatches

# ---------------------------------------------------------------- T4 transport of U and A_U
def restricted_transport(psi, r, h):
    """The explicit vertex maps carry U and the internal edges of A_U onto the image pair's."""
    base = restricted_parts(psi, r, h)
    if base is None: return None
    def internal(parts):
        return {(parts['order'][u], parts['order'][w]) for u, row in enumerate(parts['out']) for w in row}
    res = {'psi': psi, 'rule': r, 'depth': h}
    cq = restricted_parts(conj(psi), conj(r), h)
    if cq is None:
        res['complement'] = 'image pair has no closed violating walk'
    else:
        vc = lambda v: vertex_complement(v, h)
        res['complement_vertices'] = set(cq['order']) == {vc(v) for v in base['order']}
        res['complement_edges'] = internal(cq) == {(vc(u), vc(w)) for u, w in internal(base)}
    mq = restricted_parts(mirror(psi), mirror(r), h)
    if mq is None:
        res['reflection'] = 'image pair has no closed violating walk'
    else:
        vm = lambda v: vertex_mirror(v, h)
        res['reflection_vertices'] = set(mq['order']) == {vm(v) for v in base['order']}
        res['reflection_edges'] = internal(mq) == {(vm(w), vm(u)) for u, w in internal(base)}
    res['pass'] = all(v is True for k, v in res.items() if isinstance(v, bool))
    return res

def cert_key(c):
    """The transported certificate: status, restricted (k, p), |U|, carrying-component count."""
    return [c['status'], c['k'], c['p'], c['restricted_vertices'], c['carrying_components']]

# ---------------------------------------------------------------- self test (writes nothing)
def synthetic(edges, n):
    adj = [[] for _ in range(n)]
    for u, w in edges: adj[u].append(w)
    return adj

def dense_bits(adj, closed, count):
    """b_1..b_count by explicit dense unrestricted boolean powers, an independent reference path."""
    n = len(adj); A = np.zeros((n, n), dtype=np.uint8)
    for u, outs in enumerate(adj):
        for w in outs: A[u, w] = 1
    M = np.eye(n, dtype=np.uint8); bits = []
    for _ in range(count):
        M = ((M.astype(np.float32) @ A.astype(np.float32)) > 0).astype(np.uint8)
        bits.append(any(M[v3, v0] for v0, v3 in closed))
    return bits

def brute_onset(bits, P):
    """Least N >= 4 with m(n + P) = m(n) for every n in [N, hi - P], read off a raw bit sequence.

    `bits[m - 1]` is b_m, so the ring n corresponds to bits[n - 4] and m(n) = not bits[n - 4]. This
    is an independent ascending search, not the eighteenth unit's walk back from k + 3.
    """
    hi = len(bits) + 3
    for N in range(4, hi - P + 1):
        if all(bits[n - 4] == bits[n - 4 + P] for n in range(N, hi - P + 1)): return N
    return hi - P + 1

def brute_period(bits, k, cap):
    """Least q dividing cap with b q-periodic on the certified tail m >= k, from the raw bits."""
    for q in (d for d in range(1, cap + 1) if cap % d == 0):
        if all(bits[m - 1] == bits[m - 1 + q] for m in range(max(1, k), len(bits) - q + 1)): return q
    return cap

def self_test():
    t0 = time.time(); problems = []

    # (a) THE RESTRICTION LEMMA on a synthetic graph with TWO carrying components of different
    #     periods -- a chorded 5-cycle 0..4 (edges i -> i+1 mod 5 and the chord 3 -> 0, so cycle
    #     lengths 5 and 4, component period 1 and a genuine transient) and a plain 4-cycle 5..8
    #     (period 4) -- plus cross-component edges the restriction must drop (4 -> 5 and 8 -> 0) and
    #     transient structure outside U with no return (9 -> 0, 1 -> 10, 10 -> 6).  The
    #     cross-component and outside edges are one-way, so the two components stay distinct.
    #     Closed violations
    #     (0, 3) in the chorded component and (5, 6) in the 4-cycle, so a restriction that kept only
    #     ONE carrying component, or mis-mapped local indices, changes b; and b has a transient
    #     followed by period 1, which makes the onset non-trivial.
    edges = ([(i, (i + 1) % 5) for i in range(5)] + [(3, 0)] + [(5 + i, 5 + (i + 1) % 4) for i in range(4)]
             + [(4, 5), (9, 0), (1, 10), (10, 6)])
    adj = synthetic(edges, 11)
    comp = strong_components(adj)
    closed = [(0, 3), (5, 6)]
    assert comp[0] == comp[3] and comp[5] == comp[6] and comp[0] != comp[5]
    order, index, out, rdeg = carrying_restriction(adj, comp, closed)
    queries = sorted({(index[v0], index[v3]) for v0, v3 in closed})
    internal = {(order[u], order[w]) for u, row in enumerate(out) for w in row}
    want_internal = ({(i, (i + 1) % 5) for i in range(5)} | {(3, 0)}
                     | {(5 + i, 5 + (i + 1) % 4) for i in range(4)})
    ok_u = set(order) == set(range(9)) and internal == want_internal and rdeg <= MAX_OUT_DEGREE
    print(f'restriction: |U|={len(order)} (expect 9) internal_edges_exact={internal == want_internal} '
          f'restricted_max_out_degree={rdeg} full_max_out_degree={graph_max_out_degree(adj)}')
    if not ok_u: problems.append(f'restriction wrong: U={sorted(order)} dropped/kept edges {internal ^ want_internal}')
    got = restricted_bits(out, queries, SELF_TEST_DENSE_POWERS)
    ref = dense_bits(adj, closed, SELF_TEST_DENSE_POWERS)
    print(f'restriction lemma vs dense unrestricted powers over m=1..{SELF_TEST_DENSE_POWERS}: '
          f'equal={got == ref} first_hits={[m + 1 for m, x in enumerate(ref[:12]) if x]}')
    if got != ref:
        problems.append(f'restricted bits differ from dense unrestricted at m='
                        f'{[m + 1 for m in range(len(ref)) if got[m] != ref[m]][:8]}')
    #     sharpness: restricting to ONE carrying component must change b, or the test is vacuous
    one = [(0, 3)]
    o1, i1, out1, _ = carrying_restriction(adj, comp, one)
    q1 = sorted({(i1[v0], i1[v3]) for v0, v3 in one})
    if restricted_bits(out1, q1, SELF_TEST_DENSE_POWERS) == ref:
        problems.append('the two-component restriction check is not sharp: one component gives the same b')

    # (b) the certificate and THE ONSET MACHINERY against the dense sequence.  member(),
    #     rule_period() and rule_onset() must agree with independent derivations from the dense
    #     unrestricted bits; the onset must be strictly above 4, or the check is vacuous.
    cert = scan(out, queries)
    cert.update({'restricted_vertices': len(order), 'carrying_components': 2})
    p_r = rule_period(cert); p_brute = brute_period(ref, cert['k'] or 0, cert['p'] or 1)
    bad_member = [n for n in range(4, len(ref) + 4) if member(cert, n) != (not ref[n - 4])]
    N_brute = brute_onset(ref, p_r); N_got = rule_onset(cert, p_r)
    print(f'certificate (k, p)={(cert["k"], cert["p"])} p_r={p_r} (dense reference {p_brute}) '
          f'onset={N_got} (brute force {N_brute}) membership_disagreements={bad_member[:6]} '
          f'b_1..b_16={"".join("1" if x else "0" for x in ref[:16])}')
    if cert['status'] != 'certified': problems.append(f'synthetic scan status {cert["status"]}')
    if p_r != p_brute: problems.append(f'rule_period {p_r} != the dense reference period {p_brute}')
    if bad_member: problems.append(f'member() disagrees with the dense bits at rings {bad_member[:6]}')
    if N_got != N_brute: problems.append(f'rule_onset {N_got} != brute-force onset {N_brute}')
    if N_got <= 4: problems.append(f'the synthetic onset is {N_got}, so the onset check is vacuous')

    # (c) the repeat scan under a deliberately weakened hash, and past the cap.
    cw = scan(out, queries, hashfn=weak_hash)
    print(f'weakened hash: (k, p)={(cw["k"], cw["p"])} collisions={len(cw["collisions"])}')
    if (cw['status'], cw['k'], cw['p']) != (cert['status'], cert['k'], cert['p']):
        problems.append('the weakened-hash scan did not recover the certificate')
    if not cw['collisions']: problems.append('the weakened hash recorded no collision, so the path is untested')
    long_cycle = 2 * POWER_CAP
    cyc = [[(i + 1) % long_cycle] for i in range(long_cycle)]
    cc = scan(cyc, [(0, 3)])
    print(f'cycle of length {long_cycle} vs cap {POWER_CAP}: status={cc["status"]} powers={cc["powers_taken"]}')
    if cc['status'] != 'censored': problems.append('a cycle longer than the cap was not censored')

    # (d) T1(a) in miniature: the restricted method at DEPTH TWO under one observation against the
    #     eighteenth unit's certified list, periods and onset (all 256 rules, its own record).
    rec = json.loads(DEPTH_TWO_CERT.read_text())['predictions']['P2_certificates'][str(SELF_TEST_OBS)]
    g2 = analyse(SELF_TEST_OBS, 2, range(256))
    sets = {int(n): v for n, v in rec['certified_depth_two_sets'].items()}
    bad_rings = [n for n in sorted(sets) if membership_set(g2, n) != sets[n]]
    print(f'depth two psi={SELF_TEST_OBS}: P={g2["P"]} (recorded {rec["least_eventual_period_P"]}) '
          f'N={g2["N"]} (recorded {rec["onset_ring_N"]}) restricted_max_k={g2["max_k"]} '
          f'(full-matrix {rec["max_k"]}) ring_mismatches={bad_rings} censored={len(g2["censored"])}')
    if bad_rings: problems.append(f'depth-two certified sets differ from the record at rings {bad_rings}')
    if g2['P'] != rec['least_eventual_period_P']: problems.append('depth-two period differs from the record')
    if g2['N'] != rec['onset_ring_N']: problems.append('depth-two onset differs from the record')
    if g2['censored']: problems.append(f'depth-two censored rules under {SELF_TEST_OBS}: {g2["censored"]}')
    bad_counts = [r for r in range(256)
                  if g2['certs'][r]['closed_violating_walks'] != rec['closed_violating_walks'][str(r)]]
    if bad_counts: problems.append(f'|V2_cl| differs from the record at rules {bad_counts[:8]}')

    # (e) T4's transport machinery at depth two, on the rules where it is sharp (a closed violation
    #     under 232 and under its conjugate 223): certificate keys and onsets must transport, and the
    #     explicit vertex maps must carry U and the internal edges of A_U onto the image's.
    live = [r for r in range(256) if g2['certs'][r]['closed_violating_walks']][:SELF_TEST_TRANSPORT_RULES]
    if not live: problems.append('no rule under 232 has a closed violating walk at depth two')
    cq = conj(SELF_TEST_OBS)
    bad_t = []
    for r in live:
        a = g2['certs'][r]; b = pair_certificate(cq, conj(r), 2)
        if cert_key(a) != cert_key(b): bad_t.append([r, cert_key(a), cert_key(b)])
    maps = [restricted_transport(SELF_TEST_OBS, r, 2) for r in live]
    bad_m = [m for m in maps if m is not None and not m['pass']]
    print(f'T4 depth two: {len(live)} pairs, certificate-key mismatches={len(bad_t)}, '
          f'vertex-map failures={len(bad_m)} of {len(maps)}')
    if bad_t: problems.append(f'complement certificate transport failed: {bad_t[:3]}')
    if bad_m: problems.append(f'the vertex maps did not carry U/A_U: {bad_m[:2]}')
    if not any(m is not None and m.get('complement_vertices') for m in maps):
        problems.append('the T4 vertex-map check never ran, so the transport machinery is untested')

    print(f'self test {"PASS" if not problems else "FAIL"} in {time.time() - t0:.1f}s')
    for p in problems: print('   ', p)
    return 1 if problems else 0

# ---------------------------------------------------------------- probe (writes nothing)
def probe(psi, rules, h=3):
    H = read_history()
    dom = depth_three_domain(H)
    rules = rules if rules else dom[psi]['deep'][:3]
    for r in rules:
        t0 = time.time(); c = pair_certificate(psi, r, h)
        b = c['b'] or []
        print(f'psi={psi} r={r:3d} h={h} {c["status"]:12s} k={c["k"]} p={c["p"]} '
              f'|U|={c["restricted_vertices"]} comps={c["carrying_components"]} '
              f'|Vcl|={c["closed_violating_walks"]} deg={c["max_out_degree"]}/{c["restricted_max_out_degree"]} '
              f'first_hit={next((m for m in range(1, len(b)) if b[m]), None)} '
              f'powers={c["powers_taken"]} in {time.time() - t0:.1f}s', flush=True)
    return 0

# ---------------------------------------------------------------- canonical run
def main(argv):
    if '--self-test' in argv: return self_test()
    if '--probe' in argv:
        psi = int(argv[argv.index('--probe') + 1])
        rules = [int(x) for x in argv[argv.index('--rules') + 1].split(',')] if '--rules' in argv else None
        return probe(psi, rules)
    t_start = time.time()
    H = read_history()
    dom = depth_three_domain(H)
    d2rec = json.loads(DEPTH_TWO_CERT.read_text())['predictions']['P2_certificates']
    d19 = json.loads(CLOSED_VIOLATION_THREE.read_text())
    F19 = d19['pair_facts_depth_three']
    Q4_19 = d19['predictions']['Q4_eventual_periods']
    P = {}

    # ---------------- T1(a): the restricted method at depth two, all 2,048 pairs
    G2 = {}
    for psi in OBS:
        t0 = time.time(); G2[psi] = analyse(psi, 2, range(256))
        print(f'depth two psi={psi} P={G2[psi]["P"]} N={G2[psi]["N"]} restricted_max_k={G2[psi]["max_k"]} '
              f'censored={len(G2[psi]["censored"])} powers={G2[psi]["powers_taken"]} '
              f'in {time.time() - t0:.1f}s', flush=True)
    t1a = {}
    for psi in OBS:
        g = G2[psi]; rec = d2rec[str(psi)]
        sets = {int(n): v for n, v in rec['certified_depth_two_sets'].items()}
        t1a[str(psi)] = {
            'period_P': g['P'], 'recorded_period_P': rec['least_eventual_period_P'],
            'frozen_period_P': P2_CERTIFIED[psi], 'onset_N': g['N'], 'recorded_onset_N': rec['onset_ring_N'],
            'frozen_onset_N': N2_CERTIFIED[psi], 'censored_rules': g['censored'],
            'ring_mismatches': [n for n in sorted(sets) if membership_set(g, n) != sets[n]],
            'closed_count_mismatches': [[r, g['certs'][r]['closed_violating_walks'],
                                         rec['closed_violating_walks'][str(r)]] for r in range(256)
                                        if g['certs'][r]['closed_violating_walks']
                                        != rec['closed_violating_walks'][str(r)]],
            'restricted_max_k': g['max_k'], 'full_matrix_max_k': rec['max_k'],
            # reported side by side with NO bet on equality (protocol Section 1 and Section 4)
            'restricted_vs_full_k_p': {str(r): {'restricted': [g['certs'][r]['k'], g['certs'][r]['p']],
                                                'full_matrix': rec['k_p_by_rule'][str(r)],
                                                'restricted_vertices': g['certs'][r]['restricted_vertices']}
                                       for r in range(256) if g['certs'][r]['status'] == 'certified'},
            'restricted_k_p_differs_from_full': sorted(
                r for r in range(256) if g['certs'][r]['status'] == 'certified'
                and rec['k_p_by_rule'][str(r)] != [g['certs'][r]['k'], g['certs'][r]['p']])}
    t1a_pass = all(not v['ring_mismatches'] and not v['closed_count_mismatches'] and not v['censored_rules']
                   and v['period_P'] == v['recorded_period_P'] == v['frozen_period_P']
                   and v['onset_N'] == v['recorded_onset_N'] == v['frozen_onset_N'] for v in t1a.values())

    # ---------------- depth three over the nineteenth unit's frozen domain
    G3 = {}
    for psi in sorted(dom):
        t0 = time.time(); G3[psi] = analyse(psi, 3, dom[psi]['deep'])
        g = G3[psi]
        print(f'depth three psi={psi} ({dom[psi]["role"]}) deep={len(dom[psi]["deep"])} '
              f'powered={sum(1 for r in range(256) if g["certs"][r]["closed_violating_walks"])} '
              f'max_k={g["max_k"]} P={g["P"]} N={g["N"]} censored={len(g["censored"])} '
              f'powers={g["powers_taken"]} in {time.time() - t0:.1f}s', flush=True)

    def live_rules(psi): return [r for r in dom[psi]['deep'] if G3[psi]['certs'][r]['closed_violating_walks']]

    # ---------------- T1(b): depth three against the recorded rings 4..14
    t1b = {}
    for psi in sorted(dom):
        g = G3[psi]
        recd = H['D3'][psi]
        t1b[str(psi)] = {
            'ring_mismatches': [n for n in GRAPH_RINGS if membership_set(g, n) != recd[n]],
            'FS3_not_subset_at_rings': [n for n in certified_rings(g)
                                        if not set(H['FS3'][psi]) <= set(membership_set(g, n))],
            'divisibility_violations': []}
        rs = list(certified_rings(g))
        for n in rs:
            for kn in rs:
                if kn > n and kn % n == 0 and not set(membership_set(g, kn)) <= set(membership_set(g, n)):
                    t1b[str(psi)]['divisibility_violations'].append([n, kn])
    t1b_pass = all(not v['ring_mismatches'] and not v['FS3_not_subset_at_rings']
                   and not v['divisibility_violations'] for v in t1b.values())

    # ---------------- T1(c): depth three against the nineteenth unit's record
    t1c = {}
    for psi in sorted(dom):
        g = G3[psi]; rec = F19[str(psi)]
        first_hit, periods, residues = [], [], []
        for r in dom[psi]['deep']:
            c = g['certs'][r]; f = rec[str(r)]
            if not c['closed_violating_walks']:
                if not f['all_ring']: first_hit.append([r, None, f['n_min']])
                continue
            b = c['b']; m_min = f['n_min'] - 3
            if any(b[m] for m in range(1, min(m_min, len(b)))) or not (m_min < len(b) and b[m_min]):
                first_hit.append([r, next((m for m in range(1, len(b)) if b[m]), None), f['n_min']])
            if c['status'] != 'certified': continue
            if rule_period(c) != f['eventual_period']:
                periods.append([r, rule_period(c), f['eventual_period']])
            L = f['residue_modulus']; R = set(f['residues']); k, p = c['k'], c['p']
            bad = [m for m in range(k, k + p) if b[m] != ((m % L) in R)]
            if bad: residues.append([r, bad[:6]])
        ev = Q4_19[str(psi)]['eventual_sets']
        t1c[str(psi)] = {
            'first_hit_mismatches': first_hit, 'rule_period_mismatches': periods,
            'residue_indicator_mismatches': residues,
            'period_P': g['P'], 'recorded_period_P': Q4_19[str(psi)]['eventual_period_P'],
            'frozen_period_P': P3_RECORDED.get(psi),
            'eventual_set_mismatch_rings': (None if g['censored'] else
                                            [n for n in range(g['N'], g['N'] + g['P'])
                                             if membership_set(g, n) != ev[str(n % g['P'])]]),
            'all_ring_equal': (None if g['censored'] else
                               g['all_ring'] == d19['all_ring_depth_three'][str(psi)]),
            'all_ring_symmetric_difference': (None if g['censored'] else
                                              sorted(set(g['all_ring']) ^ set(d19['all_ring_depth_three'][str(psi)])))}
    t1c_pass = all(not v['first_hit_mismatches'] and not v['rule_period_mismatches']
                   and not v['residue_indicator_mismatches'] and v['period_P'] == v['recorded_period_P']
                   and not v['eventual_set_mismatch_rings'] and v['all_ring_equal'] is True
                   for v in t1c.values()) and all(
                       t1c[str(psi)]['period_P'] == P3_RECORDED[psi] for psi in DEPTH_THREE_OBS)

    # ---------------- T1(d): the restriction against two unrestricted paths
    sample = {psi: live_rules(psi)[:FRONTIER_SAMPLE_RULES] for psi in DEPTH_THREE_OBS}
    frontier, fullm = [], []
    for psi in DEPTH_THREE_OBS:
        for j, r in enumerate(sample[psi]):
            t0 = time.time(); parts = restricted_parts(psi, r, 3)
            got = restricted_bits(parts['out'], parts['queries'], FRONTIER_POWERS)
            ref = frontier_bits(parts['adj'], parts['closed'], FRONTIER_POWERS)
            frontier.append({'psi': psi, 'rule': r, 'powers': FRONTIER_POWERS,
                             'mismatching_exponents': [m + 1 for m in range(FRONTIER_POWERS) if got[m] != ref[m]],
                             'pass': got == ref})
            print(f'T1(d) frontier psi={psi} r={r} pass={frontier[-1]["pass"]} '
                  f'in {time.time() - t0:.1f}s', flush=True)
            if j == 0:                                        # the smallest such rule: full-matrix powers
                t0 = time.time()
                mm = full_matrix_entry_check(parts['adj'], parts['closed'], parts['out'],
                                             parts['queries'], parts['order'])
                fullm.append({'psi': psi, 'rule': r, 'powers': FULL_MATRIX_POWERS, 'mismatches': mm,
                              'pass': not mm})
                print(f'T1(d) full 65,536-vertex powers psi={psi} r={r} pass={not mm} '
                      f'in {time.time() - t0:.1f}s', flush=True)
            del parts
    t1d_pass = all(x['pass'] for x in frontier) and all(x['pass'] for x in fullm)

    P['T1_criterion_restriction_and_account'] = {
        'a_depth_two_reproduction': t1a, 'pass_a': t1a_pass,
        'b_recorded_rings': t1b, 'pass_b': t1b_pass,
        'c_nineteenth_unit': t1c, 'pass_c': t1c_pass,
        'd_frozen_sample': {str(psi): sample[psi] for psi in DEPTH_THREE_OBS},
        'd_frontier_cross_check': frontier, 'd_full_matrix_cross_check': fullm, 'pass_d': t1d_pass,
        'pass': t1a_pass and t1b_pass and t1c_pass and t1d_pass}
    if not P['T1_criterion_restriction_and_account']['pass']:
        print('T1 failed: the restriction lemma or the implementation is wrong; the protocol stops the '
              'unit here.', flush=True)

    # ---------------- T2: the certificates
    t2 = {}
    for psi in sorted(dom):
        g = G3[psi]; c = g['certs']
        t2[str(psi)] = {
            'role': dom[psi]['role'],
            'status_counts': {'trivially_certified_by_theorem': sum(1 for r in range(256) if not c[r]['computed']),
                              'trivially_certified_no_closed_violation':
                                  sum(1 for r in range(256) if c[r]['computed']
                                      and c[r]['status'] == 'trivially_certified'),
                              'certified': sum(1 for r in range(256) if c[r]['status'] == 'certified'),
                              'censored': len(g['censored'])},
            'censored_rules': g['censored'], 'max_k': g['max_k'], 'lcm_p': g['L'],
            'least_eventual_period_P': g['P'], 'onset_ring_N': g['N'], 'powers_taken': g['powers_taken'],
            'hash_collisions': g['collisions'],
            'max_out_degree': max((c[r]['max_out_degree'] for r in range(256)
                                   if c[r]['max_out_degree'] is not None), default=None),
            'k_p_by_rule': {str(r): ('trivially_certified' if c[r]['status'] == 'trivially_certified'
                                     else 'censored' if c[r]['status'] == 'censored' else [c[r]['k'], c[r]['p']])
                            for r in dom[psi]['deep']},
            'restricted_vertices_by_rule': {str(r): c[r]['restricted_vertices'] for r in live_rules(psi)},
            'carrying_components_by_rule': {str(r): c[r]['carrying_components'] for r in live_rules(psi)},
            'closed_violating_walks_by_rule': {str(r): c[r]['closed_violating_walks'] for r in live_rules(psi)},
            'onset_by_rule': (None if g['onsets'] is None else
                              {str(r): g['onsets'][r] for r in range(256) if g['onsets'][r] != 4}),
            'certified_depth_three_sets': (None if g['censored'] else
                                           {str(n): membership_set(g, n) for n in range(4, g['N'] + g['P'])}),
            'all_ring_depth_three': g['all_ring'],
            'restricted_vertices_summary': None}
        us = sorted(c[r]['restricted_vertices'] for r in live_rules(psi))
        if us:
            t2[str(psi)]['restricted_vertices_summary'] = {
                'pairs': len(us), 'min': us[0], 'median': us[len(us) // 2], 'max': us[-1]}
    P['T2_certificates'] = t2

    # ---------------- T3: the onsets
    max_n_min = {psi: max((F19[str(psi)][str(r)]['n_min'] for r in live_rules(psi)), default=None)
                 for psi in sorted(dom)}
    t3 = {'onsets': {str(psi): (None if G3[psi]['censored'] else G3[psi]['N']) for psi in sorted(dom)},
          'periods': {str(psi): (None if G3[psi]['censored'] else G3[psi]['P']) for psi in sorted(dom)},
          'max_n_min': {str(psi): max_n_min[psi] for psi in sorted(dom)},
          'rule_onsets_above_4': {str(psi): (None if G3[psi]['onsets'] is None else
                                             {str(r): G3[psi]['onsets'][r] for r in range(256)
                                              if G3[psi]['onsets'][r] > 4}) for psi in sorted(dom)},
          'period_aware_lower_bound': {str(psi): (None if G3[psi]['censored'] or max_n_min[psi] is None else
                                                  max(4, max_n_min[psi] - G3[psi]['P'] + 1))
                                       for psi in sorted(dom)}}
    t3['lower_bound_respected'] = {str(psi): (None if t3['period_aware_lower_bound'][str(psi)] is None else
                                              G3[psi]['N'] >= t3['period_aware_lower_bound'][str(psi)])
                                   for psi in sorted(dom)}
    g232 = G3[232]
    above20 = ([] if g232['onsets'] is None else
               sorted(r for r in range(256) if g232['onsets'][r] > BET_A_OTHER_ONSET_CEILING))
    t3['a_bet'] = {'expected_onset': BET_A_ONSET_232, 'expected_realizing_rules': list(BET_A_RULES_232),
                   'observed_onset': t3['onsets']['232'],
                   'rules_at_the_onset': ([] if g232['onsets'] is None else
                                          sorted(r for r in range(256) if g232['onsets'][r] == g232['N'])),
                   'rules_above_20': above20,
                   'onsets_of_94_and_133': ([] if g232['onsets'] is None else
                                            [g232['onsets'][r] for r in BET_A_RULES_232]),
                   'k_p_of_94_and_133': [[g232['certs'][r]['k'], g232['certs'][r]['p']] for r in BET_A_RULES_232]}
    t3['pass_a'] = (t3['onsets']['232'] == BET_A_ONSET_232
                    and sorted(above20) == sorted(BET_A_RULES_232))
    t3['b_bet'] = {'ceiling_overall': BET_B_DEPTH_TWO_RECORD, 'per_observation_ceiling':
                   {str(k): v for k, v in BET_B_CEILING.items()},
                   'observed': {str(psi): t3['onsets'][str(psi)] for psi in BET_B_CEILING},
                   'violations': {}}
    for psi, ceil_ in BET_B_CEILING.items():
        N = t3['onsets'][str(psi)]
        if N is None or N > ceil_ or N > BET_B_DEPTH_TWO_RECORD:
            g = G3[psi]
            rules = ([] if g['onsets'] is None else sorted(r for r in range(256) if g['onsets'][r] > ceil_))
            t3['b_bet']['violations'][str(psi)] = {
                'onset': N, 'ceiling': ceil_, 'rules_above_ceiling': rules,
                'departure_rings': {str(r): [n for n in range(4, (N or 4) + (g['P'] or 1))
                                             if member(g['certs'][r], n)
                                             != member(g['certs'][r], n + (g['P'] or 1))]
                                    for r in rules[:8]}}
    t3['pass_b'] = not t3['b_bet']['violations']
    t3['c_bet'] = {'margin_required': BET_C_MARGIN,
                   'onset_minus_max_n_min': {str(psi): (None if t3['onsets'][str(psi)] is None
                                                        or max_n_min[psi] is None else
                                                        t3['onsets'][str(psi)] - max_n_min[psi])
                                             for psi in DEPTH_THREE_OBS}}
    diffs = [v for v in t3['c_bet']['onset_minus_max_n_min'].values() if v is not None]
    t3['pass_c'] = any(v >= BET_C_MARGIN for v in diffs) and any(v == 0 for v in diffs)
    worst = {}
    for psi in sorted(dom):
        g = G3[psi]
        worst[str(psi)] = None if g['onsets'] is None else max(g['onsets'].values())
    t3['d_bet'] = {'ceiling': BET_D_ONSET_CEILING, 'max_rule_onset': worst,
                   'censored': {str(psi): G3[psi]['censored'] for psi in sorted(dom)},
                   'rules_above_ceiling': {str(psi): ([] if G3[psi]['onsets'] is None else
                                                      sorted(r for r in range(256)
                                                             if G3[psi]['onsets'][r] > BET_D_ONSET_CEILING))
                                           for psi in sorted(dom)}}
    t3['pass_d'] = (all(not v for v in t3['d_bet']['censored'].values())
                    and all(not v for v in t3['d_bet']['rules_above_ceiling'].values()))
    t3['pass_theorem_background'] = all(v is not False for v in t3['lower_bound_respected'].values())
    t3['pass'] = t3['pass_a'] and t3['pass_b'] and t3['pass_c'] and t3['pass_d']
    P['T3_onsets'] = t3

    # ---------------- T4: complement and reflection transport
    t4 = {'complement_certificates': {}, 'reflection_certificates': {}, 'complement_sets': {},
          'reflection_sets': {}, 'observation_level': {}, 'restricted_maps': []}
    for psi in DEPTH_THREE_OBS:
        q = conj(psi)
        gq = G3.get(q)
        t4['complement_certificates'][str(psi)] = {
            'conjugate_observation': q,
            'mismatches': ([] if gq is None else
                           [[r, cert_key(G3[psi]['certs'][r]), cert_key(gq['certs'][conj(r)])]
                            for r in dom[psi]['deep']
                            if cert_key(G3[psi]['certs'][r]) != cert_key(gq['certs'][conj(r)])]),
            'onset_mismatches': ([] if gq is None or gq['onsets'] is None or G3[psi]['onsets'] is None else
                                 [r for r in range(256) if G3[psi]['onsets'][r] != gq['onsets'][conj(r)]]),
            'compared': 0 if gq is None else len(dom[psi]['deep'])}
        assert mirror(psi) == psi, f'observation {psi} is not mirror-symmetric'
        t4['reflection_certificates'][str(psi)] = {
            'within_observation': True,
            'mismatches': [[r, cert_key(G3[psi]['certs'][r]), cert_key(G3[psi]['certs'][mirror(r)])]
                           for r in dom[psi]['deep'] if mirror(r) in set(dom[psi]['deep'])
                           and cert_key(G3[psi]['certs'][r]) != cert_key(G3[psi]['certs'][mirror(r)])],
            'onset_mismatches': ([] if G3[psi]['onsets'] is None else
                                 [r for r in range(256) if G3[psi]['onsets'][r] != G3[psi]['onsets'][mirror(r)]])}
        if gq is not None and not G3[psi]['censored'] and not gq['censored']:
            hi = max(G3[psi]['N'] + G3[psi]['P'], gq['N'] + gq['P'], 15)
            t4['complement_sets'][str(psi)] = [n for n in range(4, hi)
                                               if membership_set(gq, n) != transport(membership_set(G3[psi], n))]
            t4['reflection_sets'][str(psi)] = [n for n in range(4, G3[psi]['N'] + G3[psi]['P'])
                                               if membership_set(G3[psi], n)
                                               != sorted(mirror(r) for r in membership_set(G3[psi], n))]
            t4['observation_level'][str(psi)] = {'P_equal': G3[psi]['P'] == gq['P'],
                                                'N_equal': G3[psi]['N'] == gq['N'],
                                                'P': G3[psi]['P'], 'conjugate_P': gq['P'],
                                                'N': G3[psi]['N'], 'conjugate_N': gq['N']}
        else:
            t4['complement_sets'][str(psi)] = None; t4['reflection_sets'][str(psi)] = None
            t4['observation_level'][str(psi)] = None
    for psi in DEPTH_THREE_OBS:
        for r in sample[psi]:
            m = restricted_transport(psi, r, 3)
            if m is not None: t4['restricted_maps'].append(m)
    t4['pass'] = (all(not v['mismatches'] and not v['onset_mismatches']
                      for v in t4['complement_certificates'].values())
                  and all(not v['mismatches'] and not v['onset_mismatches']
                          for v in t4['reflection_certificates'].values())
                  and all(v is not None and not v for v in t4['complement_sets'].values())
                  and all(v is not None and not v for v in t4['reflection_sets'].values())
                  and all(v is not None and v['P_equal'] and v['N_equal'] for v in t4['observation_level'].values())
                  and all(x['pass'] for x in t4['restricted_maps']))
    P['T4_symmetries'] = t4

    report = {'protocol': 'depth-three-onset-20260913', 'schema': 1,
              'observations': list(OBS), 'depth_three_observations': list(DEPTH_THREE_OBS),
              'rings_from_sixteenth_seventeenth_units': list(RINGS),
              'parameters': {'power_cap': POWER_CAP, 'max_out_degree': MAX_OUT_DEGREE,
                             'vertices_by_depth': {str(h): vertices(h) for h in (2, 3)},
                             'frontier_sample_rules_per_observation': FRONTIER_SAMPLE_RULES,
                             'frontier_powers': FRONTIER_POWERS,
                             'full_matrix_powers': FULL_MATRIX_POWERS,
                             'full_matrix_row_chunk': FULL_MATRIX_ROW_CHUNK,
                             'decided_rings_when_censored': [4, POWER_CAP + 3],
                             'depth_three_domain': {str(psi): {'role': dom[psi]['role'],
                                                               'deep_rules': len(dom[psi]['deep'])}
                                                    for psi in sorted(dom)},
                             'restricted_certificate_is_a_property_of_A_U': True},
              'source_hashes': {'script': sha(pathlib.Path(__file__)),
                                'full_shift_depth_three_script': sha(SIXTEENTH_SCRIPT),
                                'depth_two_certificate_script': sha(EIGHTEENTH_SCRIPT),
                                'closed_violation_depth_three_script': sha(NINETEENTH_SCRIPT),
                                'depth_two_certificate_result': sha(DEPTH_TWO_CERT),
                                'closed_violation_depth_three_result': sha(CLOSED_VIOLATION_THREE),
                                'full_shift_depth_three_result': sha(FULL_SHIFT_THREE),
                                'full_shift_depth_three_linear_result': sha(FULL_SHIFT_THREE_LINEAR)},
              'onsets': {str(psi): (None if G3[psi]['censored'] else G3[psi]['N']) for psi in sorted(dom)},
              'periods': {str(psi): (None if G3[psi]['censored'] else G3[psi]['P']) for psi in sorted(dom)},
              'all_ring_depth_three': {str(psi): G3[psi]['all_ring'] for psi in sorted(dom)},
              # serialized explicitly rather than left out of the per-observation dictionaries, which
              # was the nineteenth unit's one bounded artifact-completeness deviation
              'theorem_trivial_observations': {
                  '102': {'onset_N': 4, 'period_P': 1,
                          'reason': 'FS3_102 = D3_102(n) = all 256 rules (fifteenth unit M4), so every '
                                    'rule is trivially certified at every ring and the onset is 4 with '
                                    'no power computed'}},
              'depth_two_onsets_reproduced': {str(psi): G2[psi]['N'] for psi in OBS},
              'depth_two_periods_reproduced': {str(psi): G2[psi]['P'] for psi in OBS},
              'predictions': P, 'summary': {k: v.get('pass', 'reported') for k, v in P.items()}}
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=jsonable) + '\n')
    elapsed = round(time.time() - t_start, 1)      # stdout only; never serialized, for determinism
    print(json.dumps(report['summary']))
    print('onsets', report['onsets'])
    print('periods', report['periods'])
    print('max n_min', t3['max_n_min'])
    print('written', OUT.relative_to(ROOT), f'in {elapsed}s')
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
