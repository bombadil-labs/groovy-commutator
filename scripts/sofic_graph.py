from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict, deque


class ResourceCeiling(RuntimeError):
    def __init__(self, kind, limit, observed=None):
        self.kind = kind
        self.limit = limit
        self.observed = observed
        suffix = f" ({observed})" if observed is not None else ""
        super().__init__(f"{kind} ceiling {limit} exceeded{suffix}")


@dataclass(frozen=True)
class Graph:
    n_states: int
    edges: tuple[tuple[int, int, int], ...]

    @property
    def n_edges(self):
        return len(self.edges)


def normalize_graph(n_states, edges):
    edges = tuple(sorted(set((int(a), int(label), int(b)) for a, label, b in edges)))
    used = set()
    for a, _, b in edges:
        used.add(a)
        used.add(b)
    if not used:
        return Graph(0, ())
    remap = {state: i for i, state in enumerate(sorted(used))}
    return Graph(len(remap), tuple((remap[a], label, remap[b]) for a, label, b in edges))


def trim_biinfinite(graph):
    n = graph.n_states
    if n == 0:
        return graph
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    selfloop = [False] * n
    for a, _, b in graph.edges:
        adj[a].append(b)
        radj[b].append(a)
        if a == b:
            selfloop[a] = True

    seen = [False] * n
    order = []
    for root in range(n):
        if seen[root]:
            continue
        seen[root] = True
        stack = [(root, 0)]
        while stack:
            v, i = stack[-1]
            if i < len(adj[v]):
                w = adj[v][i]
                stack[-1] = (v, i + 1)
                if not seen[w]:
                    seen[w] = True
                    stack.append((w, 0))
            else:
                order.append(v)
                stack.pop()

    component = [-1] * n
    components = []
    for root in reversed(order):
        if component[root] >= 0:
            continue
        cid = len(components)
        current = []
        stack = [root]
        component[root] = cid
        while stack:
            v = stack.pop()
            current.append(v)
            for w in radj[v]:
                if component[w] < 0:
                    component[w] = cid
                    stack.append(w)
        components.append(current)

    cyclic = set()
    for comp in components:
        if len(comp) > 1 or any(selfloop[v] for v in comp):
            cyclic.update(comp)
    if not cyclic:
        return Graph(0, ())

    def reach(starts, adjacency):
        reached = set(starts)
        queue = list(starts)
        for v in queue:
            for w in adjacency[v]:
                if w not in reached:
                    reached.add(w)
                    queue.append(w)
        return reached

    keep = reach(cyclic, adj) & reach(cyclic, radj)
    return normalize_graph(n, ((a, label, b) for a, label, b in graph.edges if a in keep and b in keep))


def transition_sets(graph):
    temp = [defaultdict(set) for _ in range(graph.n_states)]
    for a, label, b in graph.edges:
        temp[a][label].add(b)
    return [{label: tuple(sorted(dest)) for label, dest in row.items()} for row in temp]


def language_inclusion(graph_a, graph_b, max_pairs=2_000_000, return_word=True):
    graph_a = trim_biinfinite(graph_a)
    graph_b = trim_biinfinite(graph_b)
    if graph_a.n_states == 0:
        return True, None, 1
    ta = transition_sets(graph_a)
    tb = transition_sets(graph_b)
    start = (frozenset(range(graph_a.n_states)), frozenset(range(graph_b.n_states)))
    queue = deque([start])
    seen = {start}
    parent = {start: None}
    parent_label = {}
    while queue:
        sa, sb = queue.popleft()
        labels = set()
        for state in sa:
            labels.update(ta[state].keys())
        for label in sorted(labels):
            na = frozenset(v for state in sa for v in ta[state].get(label, ()))
            nb = frozenset(v for state in sb for v in tb[state].get(label, ()))
            if na and not nb:
                if not return_word:
                    return False, None, len(seen)
                word = [label]
                current = (sa, sb)
                while parent[current] is not None:
                    word.append(parent_label[current])
                    current = parent[current]
                word.reverse()
                return False, word, len(seen)
            nxt = (na, nb)
            if nxt not in seen:
                if len(seen) >= max_pairs:
                    raise ResourceCeiling("inclusion-subset-pairs", max_pairs, len(seen))
                seen.add(nxt)
                parent[nxt] = (sa, sb)
                parent_label[nxt] = label
                queue.append(nxt)
    return True, None, len(seen)


def compress_block_language(
    graph,
    max_subset_states=500_000,
    max_states=200_000,
    max_edges=2_000_000,
    max_pretrim_edges=5_000_000,
    max_image_pair_states=None,  # shared limit bundle compatibility; enforced only by image_compressed
):
    graph = trim_biinfinite(graph)
    if graph.n_states == 0:
        return graph, {"subset_states": 0, "pretrim_states": 0, "pretrim_edges": 0}
    transitions = transition_sets(graph)
    initial = frozenset(range(graph.n_states))
    subsets = [initial]
    ids = {initial: 0}
    edges = []
    q = 0
    while q < len(subsets):
        subset = subsets[q]
        labels = set()
        for state in subset:
            labels.update(transitions[state].keys())
        for label in sorted(labels):
            target = frozenset(v for state in subset for v in transitions[state].get(label, ()))
            if not target:
                continue
            tid = ids.get(target)
            if tid is None:
                if len(subsets) >= max_subset_states:
                    raise ResourceCeiling("determinization-subset-states", max_subset_states, len(subsets))
                tid = len(subsets)
                ids[target] = tid
                subsets.append(target)
            edges.append((q, label, tid))
            if len(edges) > max_pretrim_edges:
                raise ResourceCeiling("determinization-pretrim-edges", max_pretrim_edges, len(edges))
        q += 1
    raw = normalize_graph(len(subsets), edges)
    result = trim_biinfinite(raw)
    if result.n_states > max_states:
        raise ResourceCeiling("compressed-graph-states", max_states, result.n_states)
    if result.n_edges > max_edges:
        raise ResourceCeiling("compressed-graph-edges", max_edges, result.n_edges)
    return result, {"subset_states": len(subsets), "pretrim_states": raw.n_states, "pretrim_edges": raw.n_edges}


def disjoint_union(graphs):
    edges = []
    offset = 0
    for graph in graphs:
        for a, label, b in graph.edges:
            edges.append((a + offset, label, b + offset))
        offset += graph.n_states
    return trim_biinfinite(normalize_graph(offset, edges))


def initial_one_seed_graph(diagonal, seed):
    edges = []
    for symbol in diagonal:
        edges.append((0, symbol, 0))
        edges.append((1, symbol, 1))
    edges.append((0, seed, 1))
    return trim_biinfinite(normalize_graph(2, edges))


def raw_image_graph(graph, paired_rule):
    graph = trim_biinfinite(graph)
    source_edges = list(graph.edges)
    incoming = [[] for _ in range(graph.n_states)]
    outgoing = [[] for _ in range(graph.n_states)]
    for i, (a, _, b) in enumerate(source_edges):
        outgoing[a].append(i)
        incoming[b].append(i)
    pairs = []
    pair_id = {}
    for middle in range(graph.n_states):
        for e0 in incoming[middle]:
            for e1 in outgoing[middle]:
                pair_id[(e0, e1)] = len(pairs)
                pairs.append((e0, e1))
    edges = []
    for sid, (e0, e1) in enumerate(pairs):
        for e2 in outgoing[source_edges[e1][2]]:
            label = int(paired_rule[4096 * source_edges[e0][1] + 64 * source_edges[e1][1] + source_edges[e2][1]])
            edges.append((sid, label, pair_id[(e1, e2)]))
    return trim_biinfinite(normalize_graph(len(pairs), edges))


def image_compressed(graph, paired_rule, **limits):
    graph = trim_biinfinite(graph)
    source_edges = list(graph.edges)
    incoming = [[] for _ in range(graph.n_states)]
    outgoing = [[] for _ in range(graph.n_states)]
    for i, (a, _, b) in enumerate(source_edges):
        outgoing[a].append(i)
        incoming[b].append(i)

    pairs = []
    pair_id = {}
    for middle in range(graph.n_states):
        for e0 in incoming[middle]:
            for e1 in outgoing[middle]:
                pair_id[(e0, e1)] = len(pairs)
                pairs.append((e0, e1))
    max_pairs = limits.get("max_image_pair_states", 1_000_000)
    if len(pairs) > max_pairs:
        raise ResourceCeiling("image-pair-states", max_pairs, len(pairs))
    if not pairs:
        return Graph(0, ()), {"image_pair_states": 0, "subset_states": 0, "pretrim_states": 0, "pretrim_edges": 0}

    max_subset = limits.get("max_subset_states", 500_000)
    max_states = limits.get("max_states", 200_000)
    max_edges = limits.get("max_edges", 2_000_000)
    max_pretrim_edges = limits.get("max_pretrim_edges", 5_000_000)
    initial = frozenset(range(len(pairs)))
    subsets = [initial]
    ids = {initial: 0}
    edges = []
    q = 0
    transition_visits = 0
    while q < len(subsets):
        subset = subsets[q]
        by_label = defaultdict(set)
        for sid in subset:
            e0, e1 = pairs[sid]
            for e2 in outgoing[source_edges[e1][2]]:
                label = int(paired_rule[4096 * source_edges[e0][1] + 64 * source_edges[e1][1] + source_edges[e2][1]])
                by_label[label].add(pair_id[(e1, e2)])
                transition_visits += 1
        for label, target_set in sorted(by_label.items()):
            target = frozenset(target_set)
            tid = ids.get(target)
            if tid is None:
                if len(subsets) >= max_subset:
                    raise ResourceCeiling("determinization-subset-states", max_subset, len(subsets))
                tid = len(subsets)
                ids[target] = tid
                subsets.append(target)
            edges.append((q, label, tid))
            if len(edges) > max_pretrim_edges:
                raise ResourceCeiling("determinization-pretrim-edges", max_pretrim_edges, len(edges))
        q += 1

    raw = normalize_graph(len(subsets), edges)
    result = trim_biinfinite(raw)
    if result.n_states > max_states:
        raise ResourceCeiling("compressed-graph-states", max_states, result.n_states)
    if result.n_edges > max_edges:
        raise ResourceCeiling("compressed-graph-edges", max_edges, result.n_edges)
    return result, {
        "image_pair_states": len(pairs),
        "subset_states": len(subsets),
        "pretrim_states": raw.n_states,
        "pretrim_edges": raw.n_edges,
        "transition_visits": transition_visits,
    }
