"""Independent review primitives; import does not evaluate any CA or fit models.

Authored from the frozen protocol, before reviewing primary implementation.
Fresh CA evaluation is prohibited until the author's prediction seal is committed.
"""
import itertools
import math
import numpy as np


def family(n):
    return (n % 2 == 0, n % 3 == 0)


def design(widths):
    pairs = [(n, m) for n, m in itertools.combinations(widths, 2) if family(n) != family(m)]
    strata = [tuple(sorted((family(n), family(m)))) for n, m in pairs]
    assert len(set(strata)) == 6
    weights = np.array([1 / (6 * strata.count(s)) for s in strata])
    return pairs, weights


def valuation(n, p):
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count


def features(n, m, model):
    c, g = (n + m) / 42, (m - n) / 21
    out = [c, g, c*c, g*g, c*g]
    arithmetic = [(int(n % 2 == 0)+int(m % 2 == 0))/2,
                  (int(n % 3 == 0)+int(m % 3 == 0))/2,
                  (valuation(n, 2)+valuation(m, 2))/8,
                  abs(valuation(n, 2)-valuation(m, 2))/4,
                  (valuation(n, 3)+valuation(m, 3))/4,
                  abs(valuation(n, 3)-valuation(m, 3))/2]
    if model >= 1:
        out.extend(arithmetic)
    if model >= 2:
        out.extend(a*b for i, a in enumerate(arithmetic) for b in arithmetic[i:])
    return [1.] + out


def fit(pairs, weights, targets, model):
    """Augmented weighted least squares, SVD; never normal equations."""
    matrix = np.array([features(n, m, model) for n, m in pairs])
    ridge = np.eye(matrix.shape[1]) * .1
    ridge[0, 0] = 0.
    augmented = np.vstack([matrix * np.sqrt(weights[:, None]), ridge])
    rhs = np.concatenate([np.asarray(targets) * np.sqrt(weights), np.zeros(matrix.shape[1])])
    return np.linalg.lstsq(augmented, rhs, rcond=None)[0]


def scalar_successor(rule, width):
    result = np.empty(1 << width, dtype=np.uint32)
    mask = (1 << width)-1
    active = [k for k in range(8) if (rule >> k) & 1]
    for state in range(1 << width):
        left = ((state << 1) & mask) | (state >> (width-1))
        right = (state >> 1) | ((state & 1) << (width-1))
        output = 0
        for k in active:
            output |= (left if k & 4 else left ^ mask) & (state if k & 2 else state ^ mask) & (right if k & 1 else right ^ mask)
        result[state] = output
    return result


def graph(nxt):
    """Independent path walking with local visitation indices, no indegree peeling."""
    count = len(nxt)
    basin = np.full(count, -1, dtype=np.int32)
    period = np.zeros(count, dtype=np.uint32)
    depth = np.zeros(count, dtype=np.uint32)
    for start in range(count):
        if basin[start] >= 0:
            continue
        path, seen = [], {}
        current = start
        while basin[current] < 0 and current not in seen:
            seen[current] = len(path)
            path.append(current)
            current = int(nxt[current])
        if current in seen:
            cycle_at = seen[current]
            cycle = path[cycle_at:]
            basin[cycle] = min(cycle)
            period[cycle] = len(cycle)
            path = path[:cycle_at]
        for node in reversed(path):
            target = int(nxt[node])
            basin[node] = basin[target]
            period[node] = period[target]
            depth[node] = depth[target]+1
    return dict(basin=basin.astype(np.uint32), cycle_length=period, transient_depth=depth)


def entropy(labels):
    ordered = np.sort(labels)
    boundaries = np.flatnonzero(ordered[1:] != ordered[:-1])+1
    counts = np.diff(np.concatenate(([0], boundaries, [len(labels)])))
    total = len(labels)
    return math.fsum(-int(c)/total * math.log2(int(c)/total) for c in counts)


def relation(a, b, width):
    ha, hb = entropy(a), entropy(b)
    # Fixed source-space width packs labels; no data-dependent label encoding.
    hab = entropy((a.astype(np.uint64) << width) | b.astype(np.uint64))
    vi = max(0., min(float(width), 2*hab-ha-hb))
    return dict(h_a=ha, h_b=hb, h_joint=hab, vi=vi, vi_per_bit=vi/width)


def rank90(width, horizon):
    mask = (1 << width)-1
    pivots = {}
    for i in range(width):
        column = 1 << i
        for _ in range(horizon):
            column = (((column << 1) & mask) | (column >> (width-1))) ^ ((column >> 1) | ((column & 1) << (width-1)))
        while column:
            pivot = column.bit_length()-1
            if pivot in pivots:
                column ^= pivots[pivot]
            else:
                pivots[pivot] = column
                break
    return len(pivots)
