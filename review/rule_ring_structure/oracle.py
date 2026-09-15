"""Independent reviewer oracle, written from the frozen protocol before source review.

No evaluation runs at import. Confirmation widths must not be evaluated before
the author's discovery-selection seal. This is review code, not the author code.
"""
from collections import Counter, deque
import math


HORIZONS = (1, 2, 4, 8, 16, 32)


def successor(rule, width):
    result = []
    for state in range(1 << width):
        output = 0
        for x in range(width):
            left = (state >> ((x - 1) % width)) & 1
            center = (state >> x) & 1
            right = (state >> ((x + 1) % width)) & 1
            value = (rule >> (4 * left + 2 * center + right)) & 1
            output |= value << x
        result.append(output)
    return result


def graph_partitions(nxt):
    """Peel trees by indegree, walk remaining cycles, then restore trees."""
    indegree = [0] * len(nxt)
    for target in nxt:
        indegree[target] += 1
    queue = deque(i for i, count in enumerate(indegree) if count == 0)
    peeled = []
    while queue:
        state = queue.popleft()
        peeled.append(state)
        target = nxt[state]
        indegree[target] -= 1
        if indegree[target] == 0:
            queue.append(target)
    basin = [-1] * len(nxt)
    length = [-1] * len(nxt)
    distance = [-1] * len(nxt)
    for start in range(len(nxt)):
        if indegree[start] == 0 or basin[start] != -1:
            continue
        cycle = [start]
        state = nxt[start]
        while state != start:
            cycle.append(state)
            state = nxt[state]
        label = min(cycle)
        for state in cycle:
            basin[state] = label
            length[state] = len(cycle)
            distance[state] = 0
    for state in reversed(peeled):
        target = nxt[state]
        basin[state] = basin[target]
        length[state] = length[target]
        distance[state] = distance[target] + 1
    assert all(b >= 0 and c >= 1 and d >= 0 for b, c, d in zip(basin, length, distance))
    return basin, length, distance


def partitions(rule, width):
    nxt = successor(rule, width)
    current = list(range(len(nxt)))
    labels = {}
    for tick in range(1, max(HORIZONS) + 1):
        current = [nxt[state] for state in current]
        if tick in HORIZONS:
            labels[f'future_{tick}'] = current.copy()
    labels['basin'], labels['cycle_length'], labels['transient_distance'] = graph_partitions(nxt)
    return nxt, labels


def canonical_partition(labels):
    mapping = {}
    return [mapping.setdefault(int(label), len(mapping)) for label in labels]


def entropy_counts(counts):
    total = sum(counts)
    return math.fsum(-count / total * math.log2(count / total) for count in counts)


def relation(left, right):
    a = entropy_counts(Counter(left).values())
    b = entropy_counts(Counter(right).values())
    joint = entropy_counts(Counter(zip(left, right)).values())
    return a, b, joint, 2 * joint - a - b


def gf2_rank(rows):
    basis = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                row ^= basis[pivot]
            else:
                basis[pivot] = row
                break
    return len(basis)


def rule90_rank(width, horizon):
    """Independent bit-polynomial column construction, no state enumeration."""
    mask = (1 << width) - 1
    columns = []
    for site in range(width):
        column = 1 << site
        for _ in range(horizon):
            left = ((column << 1) & mask) | (column >> (width - 1))
            right = (column >> 1) | ((column & 1) << (width - 1))
            column = left ^ right
        columns.append(column)
    return gf2_rank(columns)
