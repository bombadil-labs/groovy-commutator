"""Independent dense-tensor audit for frozen Research034 width-3 cases."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np

B = 64
D = tuple(9 * a for a in range(8))
CASES = [
    (5, '01001100', (0,2), 230, 1162, 3, 16, True, 'mechanism'),
    (122, '00100000', (1,4), 3528, 138795, 8, 64, False, 'sentinel'),
    (122, '00100000', (1,5), 3523, 138676, 8, 64, False, 'sentinel'),
    (122, '00100000', (3,6), 3520, 138591, 8, 64, False, 'sentinel'),
    (122, '00100000', (3,7), 3520, 138626, 8, 64, False, 'sentinel'),
    (122, '00100000', (4,5), 3523, 138676, 8, 64, False, 'sentinel'),
    (122, '00100000', (6,7), 3520, 138626, 8, 64, False, 'sentinel'),
    (161, '00000100', (0,1), 3520, 138626, 8, 64, False, 'sentinel'),
    (161, '00000100', (0,4), 3520, 138626, 8, 64, False, 'sentinel'),
    (161, '00000100', (1,4), 3520, 138591, 8, 64, False, 'sentinel'),
    (161, '00000100', (2,3), 3523, 138676, 8, 64, False, 'sentinel'),
    (161, '00000100', (2,6), 3523, 138676, 8, 64, False, 'sentinel'),
    (161, '00000100', (3,6), 3528, 138795, 8, 64, False, 'sentinel'),
]


def bits3(x):
    return ((x >> 0) & 1, (x >> 1) & 1, (x >> 2) & 1)


def macro_table(rule):
    lut = tuple((rule >> i) & 1 for i in range(8))
    g = np.empty((8, 8, 8), dtype=np.uint8)
    for l in range(8):
        for c in range(8):
            for r in range(8):
                row = list(bits3(l) + bits3(c) + bits3(r))
                for _ in range(3):
                    row = [lut[4 * row[i] + 2 * row[i+1] + row[i+2]] for i in range(len(row) - 2)]
                g[l, c, r] = row[0] | (row[1] << 1) | (row[2] << 2)
    return g


def paired_tensor(rule):
    g = macro_table(rule)
    ph = np.empty((B, B, B), dtype=np.uint8)
    for x in range(B):
        xa, xb = divmod(x, 8)
        for y in range(B):
            ya, yb = divmod(y, 8)
            for z in range(B):
                za, zb = divmod(z, 8)
                ph[x, y, z] = 8 * int(g[xa, ya, za]) + int(g[xb, yb, zb])
    return ph


def initial_tensor(seed):
    W = np.zeros((B, B, B), dtype=bool)
    for a in D:
        for b in D:
            for c in D:
                W[a,b,c] = True
    for b in D:
        for c in D:
            W[seed,b,c] = True
    for a in D:
        for c in D:
            W[a,seed,c] = True
    for a in D:
        for b in D:
            W[a,b,seed] = True
    assert int(W.sum()) == 704
    return W


def output_sets(ph, W):
    pre = [[None] * B for _ in range(B)]
    post = [[None] * B for _ in range(B)]
    for b in range(B):
        for c in range(B):
            av = np.flatnonzero(W[:, b, c])
            pre[b][c] = np.unique(ph[av, b, c]).astype(np.intp) if len(av) else np.empty(0, dtype=np.intp)
            ev = np.flatnonzero(W[b, c, :])
            post[b][c] = np.unique(ph[b, c, ev]).astype(np.intp) if len(ev) else np.empty(0, dtype=np.intp)
    return pre, post


def dense_step(ph, W):
    pre, post = output_sets(ph, W)
    N = W.copy()
    for b in range(B):
        for c in range(B):
            q0 = pre[b][c]
            ds = np.flatnonzero(W[b, c, :])
            if not len(q0) or not len(ds):
                continue
            q1s = ph[b, c, ds].astype(np.intp)
            for q1 in np.unique(q1s):
                chosen = ds[q1s == q1]
                parts = [post[c][int(d)] for d in chosen if len(post[c][int(d)])]
                if not parts:
                    continue
                q2 = np.unique(np.concatenate(parts))
                N[np.ix_(q0, np.asarray([q1], dtype=np.intp), q2)] = True
    return N


def dense_closure(ph, seed):
    W = initial_tensor(seed)
    rounds = 0
    while True:
        N = dense_step(ph, W)
        rounds += 1
        if np.array_equal(N, W):
            return W, rounds
        W = N


def verify_fixed_point(ph, W):
    N = dense_step(ph, W)
    return bool(np.array_equal(N, W))


def edge_closure(ph, seed):
    e = {(x, y) for x in D for y in D}
    e.update((x, seed) for x in D)
    e.update((seed, x) for x in D)
    rounds = 0
    while True:
        old = set(e)
        pred = {i: set() for i in range(B)}
        succ = {i: set() for i in range(B)}
        for x, y in old:
            succ[x].add(y)
            pred[y].add(x)
        add = set()
        for p1, p2 in old:
            left = {int(ph[p0, p1, p2]) for p0 in pred[p1]}
            right = {int(ph[p1, p2, p3]) for p3 in succ[p2]}
            add.update((u, v) for u in left for v in right)
        e |= add
        rounds += 1
        if e == old:
            return e, rounds


def vertices_tensor(W):
    coords = np.argwhere(W)
    if not len(coords):
        return set()
    return set(map(int, np.unique(coords)))


def visible(sym, target):
    a, b = divmod(sym, 8)
    return target[a] != target[b]


def run_case(index):
    rule, target, pair, expected_edge_count, expected_words, expected_rounds, expected_vertices, expected_safe, kind = CASES[index]
    seed = 8 * pair[0] + pair[1]
    ph = paired_tensor(rule)
    edges, edge_rounds = edge_closure(ph, seed)
    W, rounds = dense_closure(ph, seed)
    verts = vertices_tensor(W)
    safe = not any(visible(v, target) for v in verts)
    edge_vertices = {v for edge in edges for v in edge}
    fixed = verify_fixed_point(ph, W)
    hierarchy = verts.issubset(edge_vertices)
    out = {
        'index': index,
        'rule': rule,
        'target': target,
        'pair': f'{pair[0]}-{pair[1]}',
        'kind': kind,
        'initial_words': 704,
        'edge_count': len(edges),
        'edge_rounds': edge_rounds,
        'word_count': int(W.sum()),
        'rounds': rounds,
        'vertex_count': len(verts),
        'safe': safe,
        'fixed_point_verified': fixed,
        'width3_vertices_subset_of_edge_vertices': hierarchy,
        'expected': {
            'edge_count': expected_edge_count,
            'word_count': expected_words,
            'rounds': expected_rounds,
            'vertex_count': expected_vertices,
            'safe': expected_safe,
        },
    }
    out['passes'] = (
        out['edge_count'] == expected_edge_count
        and out['word_count'] == expected_words
        and out['rounds'] == expected_rounds
        and out['vertex_count'] == expected_vertices
        and out['safe'] == expected_safe
        and fixed
        and hierarchy
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--case-index', type=int, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if not (0 <= args.case_index < len(CASES)):
        raise SystemExit('bad case index')
    out = run_case(args.case_index)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))
    if not out['passes']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
