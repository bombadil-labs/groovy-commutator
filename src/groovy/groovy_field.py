"""The Groovy field as a dynamical system: exact closure tests on the full line.

For an elementary CA with Wolfram rule ``phi`` let ``E`` be its synchronous
update, ``D(S) = S XOR E(S)`` and ``G(S) = E(S) XOR E^2(S) XOR E(D(S))``.
An *observation* is ``O(S) = (G(S), X_1(S), ..., X_r(S))`` where each extra
*track* ``X_i`` is a radius-one Boolean function of the source, given as an
8-bit truth table indexed like a rule (``4*l + 2*c + r``). Track 204 is the
source itself; the empty track list is G alone.

The question for ``(rule, tracks, k, t)`` is whether, on the domain
``E^t({0,1}^Z)`` (all configurations when ``t = 0``), the observation at time
``t+k`` is a function of the observations at times ``t, ..., t+k-1``. By
compactness and the Curtis-Hedlund-Lyndon theorem such a function, when it
exists, is a sliding block code on the valid observation-history subshift.
This does not specify its values on arbitrary ``k``-track configurations.

``decide`` answers exactly. Pairs of source configurations with equal
observation histories at every site form a subshift of finite type on the
pair alphabet, presented by a de Bruijn graph whose edges are pairs of
``W = 2(t+k)+3`` windows. A counterexample exists iff the graph has a
bi-infinite path through three consecutive edges whose centre time-``t+k``
observations differ. That holds iff the three-edge segment starts at a node
with an infinite backward path and ends at a node with an infinite forward
path; both node sets are computed by pruning.

``certify_law`` then finds an explicit radius-``R`` table by exhausting every
source window covering the table's full causal support, and ``witness``
extracts an eventually periodic counterexample pair from the graph. These
negative witnesses are checked by the independent tuple implementation in
``TupleCA``. The local-table search shares packed arithmetic with the decider;
selected laws also have an independent unpacked replay in the review audit.
Resource-limited and decider-only outcomes remain explicitly labelled.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

EDGE_CAP = 15_000_000

# --------------------------------------------------------------------------
# Packed-window arithmetic (numpy). A window of length L is an integer whose
# most significant bit is the leftmost cell.


def _mask(n: int) -> np.uint64:
    return np.uint64((1 << n) - 1)


def shrink(v: np.ndarray, L: int, table: int) -> np.ndarray:
    """Apply a radius-one table to every complete 3-window: length L -> L-2."""
    lut = np.array([(table >> i) & 1 for i in range(8)], dtype=np.uint64)
    out = np.zeros_like(v)
    for t in range(L - 2):
        s = np.uint64(L - 3 - t)
        out |= lut[((v >> s) & np.uint64(7)).astype(np.int64)] << s
    return out


def g_word(v: np.ndarray, L: int, rule: int) -> np.ndarray:
    """Groovy word of a length-L window: length L-4, aligned to cells 2..L-3."""
    e = shrink(v, L, rule)
    ee = shrink(e, L - 2, rule)
    d = ((v >> np.uint64(1)) & _mask(L - 2)) ^ e
    ed = shrink(d, L - 2, rule)
    return ((e >> np.uint64(1)) & _mask(L - 4)) ^ ee ^ ed


def obs_words(v: np.ndarray, L: int, j: int, rule: int, tracks) -> list:
    """Observation words at time j, all trimmed to G's alignment.

    Returns [(word, length)] for G then each track.
    """
    x, n = v, L
    for _ in range(j):
        x, n = shrink(x, n, rule), n - 2
    out = [(g_word(x, n, rule), n - 4)]
    for tr in tracks:
        tw = shrink(x, n, tr)  # length n-2, aligned to cells 1..n-2
        out.append(((tw >> np.uint64(1)) & _mask(n - 4), n - 4))
    return out


def obs_centre(v, L, j, rule, tracks) -> np.ndarray:
    """Centre-cell observation bits at time j packed as a small integer."""
    code = np.zeros_like(v)
    for w, n in obs_words(v, L, j, rule, tracks):
        code = (code << np.uint64(1)) | ((w >> np.uint64(n // 2)) & np.uint64(1))
    return code


# --------------------------------------------------------------------------
# Exact decider.


def _alive(n_nodes, src, dst, forward: bool) -> np.ndarray:
    """Greatest set of nodes with an infinite forward (or backward) path."""
    alive = np.zeros(n_nodes, dtype=bool)
    alive[src] = True
    alive[dst] = True
    a, b = (src, dst) if forward else (dst, src)
    while True:
        ok = alive[a] & alive[b]
        deg = np.bincount(a[ok], minlength=n_nodes)
        new = alive & (deg > 0)
        if new.sum() == alive.sum():
            return new
        alive = new


@dataclass
class Graph:
    W: int
    nodes: np.ndarray            # sorted raw node ids
    src: np.ndarray              # compressed ids
    dst: np.ndarray
    fwd: np.ndarray              # bool per compressed node
    bwd: np.ndarray

    def cid(self, raw: np.ndarray) -> np.ndarray:
        """Compressed id, or -1 if the raw node is absent."""
        i = np.searchsorted(self.nodes, raw)
        i = np.minimum(i, len(self.nodes) - 1)
        return np.where(self.nodes[i] == raw, i, -1)


@dataclass
class Verdict:
    rule: int
    tracks: tuple
    k: int
    t: int
    status: str                  # 'law' | 'counterexample' | 'too_large'
    defect: tuple | None = None  # (u, u') raw (W+2)-windows
    edges: int = 0
    graph: Graph | None = field(default=None, repr=False)


def _pair_graph(hist: np.ndarray, W: int):
    order = np.argsort(hist, kind="stable")
    h = hist[order]
    cuts = np.flatnonzero(np.diff(h)) + 1
    groups = np.split(order.astype(np.uint64), cuts)
    total = sum(len(g) ** 2 for g in groups)
    if total > EDGE_CAP:
        return None, total
    half = np.uint64(W - 1)
    m = _mask(W - 1)
    src_parts, dst_parts = [], []
    for g in groups:
        a = np.repeat(g, len(g))
        b = np.tile(g, len(g))
        src_parts.append(((a >> np.uint64(1)) << half) | (b >> np.uint64(1)))
        dst_parts.append(((a & m) << half) | (b & m))
    src = np.concatenate(src_parts)
    dst = np.concatenate(dst_parts)
    nodes = np.unique(np.concatenate([src, dst]))
    s = np.searchsorted(nodes, src)
    d = np.searchsorted(nodes, dst)
    n = len(nodes)
    g = Graph(W, nodes, s, d, _alive(n, s, d, True), _alive(n, s, d, False))
    return g, total


def decide(rule: int, tracks=(), k: int = 1, t: int = 0) -> Verdict:
    tracks = tuple(tracks)
    W = 2 * (t + k) + 3
    L = W + 2
    v = np.arange(1 << W, dtype=np.uint64)
    nb = 1 + len(tracks)
    hist = np.zeros_like(v)
    for j in range(t, t + k):
        hist = (hist << np.uint64(nb)) | obs_centre(v, W, j, rule, tracks)
    graph, total = _pair_graph(hist, W)
    if graph is None:
        return Verdict(rule, tracks, k, t, "too_large", edges=total)
    u = np.arange(1 << L, dtype=np.uint64)
    hb = np.uint64(nb * k)
    wm = _mask(W)
    sig = ((hist[((u >> np.uint64(2)) & wm).astype(np.int64)] << (hb * np.uint64(2)))
           | (hist[((u >> np.uint64(1)) & wm).astype(np.int64)] << hb)
           | hist[(u & wm).astype(np.int64)])
    nxt = obs_centre(u, L, t + k, rule, tracks)
    order = np.lexsort((nxt, sig))
    s_sorted, n_sorted = sig[order], nxt[order]
    cuts = np.flatnonzero(np.diff(s_sorted)) + 1
    half = np.uint64(W - 1)
    m = _mask(W - 1)
    for grp, nx in zip(np.split(order.astype(np.uint64), cuts), np.split(n_sorted, cuts)):
        if len(grp) < 2 or nx[0] == nx[-1]:
            continue
        for lo in range(0, len(grp), 1024):          # bounded memory per block
            ga, xa = grp[lo:lo + 1024], nx[lo:lo + 1024]
            a = np.repeat(ga, len(grp)); b = np.tile(grp, len(ga))
            keep = np.repeat(xa, len(nx)) != np.tile(nx, len(xa))
            a, b = a[keep], b[keep]
            st = graph.cid(((a >> np.uint64(3)) << half) | (b >> np.uint64(3)))
            en = graph.cid(((a & m) << half) | (b & m))
            ok = (st >= 0) & (en >= 0)
            ok[ok] &= graph.bwd[st[ok]] & graph.fwd[en[ok]]
            if ok.any():
                i = int(np.flatnonzero(ok)[0])
                return Verdict(rule, tracks, k, t, "counterexample",
                               (int(a[i]), int(b[i])), total, graph)
    return Verdict(rule, tracks, k, t, "law", None, total, graph)


# --------------------------------------------------------------------------
# Independent tuple implementation used for certification.


class TupleCA:
    """Plain-tuple finite-window arithmetic, sharing no code with the decider."""

    def __init__(self, rule: int):
        self.rule = rule

    def step(self, w, table=None):
        tb = self.rule if table is None else table
        return tuple((tb >> (4 * w[i] + 2 * w[i + 1] + w[i + 2])) & 1
                     for i in range(len(w) - 2))

    def groovy(self, w):
        e = self.step(w)
        ee = self.step(e)
        d = tuple(x ^ y for x, y in zip(w[1:-1], e))
        ed = self.step(d)
        return tuple(a ^ b ^ c for a, b, c in zip(e[1:-1], ee, ed))

    def observe(self, w, j, tracks):
        """List of aligned observation words at time j (G first)."""
        for _ in range(j):
            w = self.step(w)
        out = [self.groovy(w)]
        for tr in tracks:
            out.append(self.step(w, tr)[1:-1])
        return out


def witness(v: Verdict, reps: int = 0) -> dict:
    """Eventually periodic counterexample pair from a counterexample verdict."""
    g = v.graph
    W = g.W
    L = W + 2
    m = (1 << (W - 1)) - 1
    u, u2 = v.defect
    order = np.argsort(g.src, kind="stable")
    s_sorted, d_by_src = g.src[order], g.dst[order]
    order_b = np.argsort(g.dst, kind="stable")
    d_sorted, s_by_dst = g.dst[order_b], g.src[order_b]

    def nbrs(x, forward):
        if forward:
            lo, hi = np.searchsorted(s_sorted, x), np.searchsorted(s_sorted, x, "right")
            cand = d_by_src[lo:hi]
            return [int(c) for c in cand if g.fwd[c]]
        lo, hi = np.searchsorted(d_sorted, x), np.searchsorted(d_sorted, x, "right")
        cand = s_by_dst[lo:hi]
        return [int(c) for c in cand if g.bwd[c]]

    def walk(x, forward):
        seen, path = {}, []
        while x not in seen:
            seen[x] = len(path)
            path.append(x)
            x = min(nbrs(x, forward))
        i = seen[x]
        return path[:i], path[i:]

    start = int(g.cid(np.array([((u >> 3) << (W - 1)) | (u2 >> 3)], dtype=np.uint64))[0])
    end = int(g.cid(np.array([((u & m) << (W - 1)) | (u2 & m)], dtype=np.uint64))[0])
    pre_b, cyc_b = walk(start, False)
    post_f, cyc_f = walk(end, True)

    def raw(c):
        x = int(g.nodes[c])
        return x >> (W - 1), x & m

    def spell(seq_raw):
        a0, b0 = seq_raw[0]
        s1 = [(a0 >> (W - 2 - i)) & 1 for i in range(W - 1)]
        s2 = [(b0 >> (W - 2 - i)) & 1 for i in range(W - 1)]
        for a, b in seq_raw[1:]:
            s1.append(a & 1); s2.append(b & 1)
        return s1, s2

    left = [raw(c) for c in cyc_b[::-1]]
    right = [raw(c) for c in cyc_f]
    lp, rp = len(left), len(right)
    reps = reps or max(4, -(-(4 * W) // min(lp, rp)))
    # Forward node chains that end exactly at `start` and begin exactly at
    # `end` (either may itself lie on its tail cycle).
    left_part = left * reps + [raw(c) for c in pre_b[::-1]]
    right_part = [raw(c) for c in post_f] + right * reps
    seg = [(((u >> (L - (W - 1) - o)) & m), ((u2 >> (L - (W - 1) - o)) & m)) for o in range(4)]
    assert left_part[-1] == seg[0] and right_part[0] == seg[-1]
    seq = left_part[:-1] + seg + right_part[1:]
    s1, s2 = spell(seq)
    centre = len(left_part) - 1 + (L - 1) // 2
    return {"S": "".join(map(str, s1)), "S_prime": "".join(map(str, s2)),
            "left_period": lp, "right_period": rp,
            "tail_reps": reps, "defect_cell": centre}


def verify_witness(rule, tracks, k, t, wit) -> dict:
    """Verify an explicitly defined bi-infinite pair, including both tail seams.

    A word s of length n means s[i] for 0 <= i < n, s[i % lp] to its
    left, and s[n-rp + (i-n) % rp] to its right. Periods need not be minimal.
    ``tail_reps`` is optional construction provenance, not a coverage claim.

    With r = t+k+2, padding by 2*r+max(lp,rp) includes every body/seam
    neighbourhood and a complete period strictly inside each tail, after
    trimming the radius-r causal margin. Translation invariance therefore
    extends the history equality to every integer site. The next observation
    must differ at the declared source coordinate ``defect_cell``.
    Malformed certificates return verified=False and an error.
    """
    def invalid(reason):
        return {"verified": False, "error": reason}

    try:
        tracks = tuple(tracks)
    except TypeError:
        return invalid("tracks must be an iterable of ECA truth tables")
    if any(type(v) is not int or not 0 <= v <= 255 for v in (rule, *tracks)):
        return invalid("rule and tracks must be integers from 0 to 255")
    if type(k) is not int or k < 1 or type(t) is not int or t < 0:
        return invalid("k must be positive and t nonnegative integers")
    if not isinstance(wit, dict):
        return invalid("witness must be an object")
    a, b = wit.get("S"), wit.get("S_prime")
    if any(not isinstance(s, str) or not s or set(s) - {"0", "1"} for s in (a, b)):
        return invalid("source words must be nonempty binary strings")
    if len(a) != len(b):
        return invalid("source words must have equal lengths")
    n = len(a)
    lp, rp = wit.get("left_period"), wit.get("right_period")
    if any(type(p) is not int or not 1 <= p <= n for p in (lp, rp)):
        return invalid("tail periods must be positive integers no longer than the words")
    defect = wit.get("defect_cell")
    if type(defect) is not int or not 0 <= defect < n:
        return invalid("defect_cell must index the recorded source words")
    if "tail_reps" in wit and (type(wit["tail_reps"]) is not int or wit["tail_reps"] < 1):
        return invalid("tail_reps, if supplied, must be a positive integer")
    radius = t + k + 2
    pad = 2 * radius + max(lp, rp)

    def extend(s):
        return tuple(int(s[i % lp] if i < 0 else
                         s[n-rp + (i-n) % rp] if i >= n else s[i])
                     for i in range(-pad, n + pad))

    a, b = extend(a), extend(b)
    ca = TupleCA(rule)
    history_equal = all(ca.observe(a, j, tracks) == ca.observe(b, j, tracks)
                        for j in range(t, t + k))
    diffs = []
    for idx, (wa, wb) in enumerate(zip(ca.observe(a, t+k, tracks), ca.observe(b, t+k, tracks))):
        offset = radius - pad
        diffs.extend((idx, i + offset) for i, (x, y) in enumerate(zip(wa, wb)) if x != y)
    at_defect = any(i == defect for _, i in diffs)
    return {"history_equal_on_full_line": history_equal,
            "next_differs_at": diffs[:6], "declared_defect_differs": at_defect,
            "verified": history_equal and at_defect}


def certify_law(rule, tracks, k, t, r_max=6, max_bits=21) -> dict:
    """Smallest radius R with a consistent table (history window -> next centre).

    Exhausts every source window of radius m = max(R+t+k+1, t+k+2), which is
    the table's complete causal support, so a consistent table is an exact
    local law on E^t of the full line.
    """
    tracks = tuple(tracks)
    for R in range(0, r_max + 1):
        mrad = max(R + t + k + 1, t + k + 2)
        L = 2 * mrad + 1
        if L > max_bits:
            return {"status": "unverified_radius_budget", "radius_tried_up_to": R - 1}
        v = np.arange(1 << L, dtype=np.uint64)
        cols = []
        for j in range(t, t + k):
            for w, n in obs_words(v, L, j, rule, tracks):
                c = n // 2
                cols.append((w >> np.uint64(c - R)) & _mask(2 * R + 1))
        key = np.stack(cols, axis=1)
        val = obs_centre(v, L, t + k, rule, tracks)
        uniq, inv = np.unique(key, axis=0, return_inverse=True)
        inv = inv.ravel()
        first = np.full(len(uniq), -1, dtype=np.int64)
        first[inv[::-1]] = val[::-1].astype(np.int64)
        if np.all(first[inv] == val.astype(np.int64)):
            return {"status": "certified", "radius": R, "source_windows": int(1 << L),
                    "realized_patterns": int(len(uniq))}
    return {"status": "unverified_radius_budget", "radius_tried_up_to": r_max}


def ring_collision(rule, tracks, k, t, n) -> bool:
    """Brute force on the ring of n cells (cell 0 leftmost, cyclic)."""
    ca = TupleCA(rule)
    tracks = tuple(tracks)
    seen = {}

    def cyc_step(s, tb):
        return tuple((tb >> (4 * s[i - 1] + 2 * s[i] + s[(i + 1) % n])) & 1 for i in range(n))

    def obs(s):
        e = cyc_step(s, rule)
        ee = cyc_step(e, rule)
        d = tuple(x ^ y for x, y in zip(s, e))
        ed = cyc_step(d, rule)
        g = tuple(a ^ b ^ c for a, b, c in zip(e, ee, ed))
        return (g,) + tuple(cyc_step(s, tr) for tr in tracks)

    for val in range(1 << n):
        s = tuple((val >> (n - 1 - i)) & 1 for i in range(n))
        for _ in range(t):
            s = cyc_step(s, rule)
        h = []
        for _ in range(k):
            h.append(obs(s)); s = cyc_step(s, rule)
        key, nx = tuple(h), obs(s)
        if seen.setdefault(key, nx) != nx:
            return True
    return False
