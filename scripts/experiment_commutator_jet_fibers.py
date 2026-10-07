#!/usr/bin/env python3
"""Exact residual-fiber analysis for full-entropy commutator-jet factors.

Constructs the equal-label source pair de Bruijn graph, prunes to bi-infinite
support, classifies recurrent ambiguity, computes directional synchronization,
and checks bounded local inversion.

Protocol:
  docs/research/protocols/commutator-jet-fibers-20261007.md

Only NumPy is required.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict, deque
from pathlib import Path

import numpy as np

OUT = Path("results/commutator_jet_fibers_20261007.json")

FACTORS = (
    ("110_control_GQ", 110, 2, False),
    ("110_primary_GQR", 110, 3, True),
    ("62_control_GQRA4", 62, 4, False),
    ("62_primary_GQRA4A5", 62, 5, True),
)


def step_line(a: np.ndarray, rule: int) -> np.ndarray:
    left = np.concatenate(([0], a[:-1]))
    right = np.concatenate((a[1:], [0]))
    idx = (left << 2) | (a << 1) | right
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    return lut[idx]


def local_level_truth(rule: int, level: int) -> np.ndarray:
    radius = level + 1
    width = 2 * radius + 1
    out = np.zeros(1 << width, dtype=np.uint8)
    pad = level + 4
    for word in range(1 << width):
        core = np.array([(word >> i) & 1 for i in range(width)], dtype=np.uint8)
        source = np.pad(core, (pad, pad))
        rows = [source]
        for _ in range(level + 2):
            rows.append(step_line(rows[-1], rule))
        temporal = [rows[t] ^ rows[t + 1] for t in range(len(rows) - 1)]
        levels = [temporal]
        for _ in range(level):
            prev = levels[-1]
            levels.append([
                prev[t + 1] ^ step_line(prev[t], rule)
                for t in range(len(prev) - 1)
            ])
        out[word] = levels[level][0][pad + radius]
    return out


def pack_symbol(word, max_radius, levels, truths):
    symbol = 0
    for output_pos, level in enumerate(levels):
        radius = level + 1
        subword = 0
        bit_pos = 0
        for source_pos in range(max_radius - radius, max_radius + radius + 1):
            subword |= ((word >> source_pos) & 1) << bit_pos
            bit_pos += 1
        symbol |= int(truths[level][subword]) << output_pos
    return symbol


def source_edges(rule, end_level):
    levels = tuple(range(1, end_level + 1))
    radius = end_level + 1
    state_bits = 2 * radius
    nstates = 1 << state_bits
    truths = {level: local_level_truth(rule, level) for level in levels}

    src, dst, labels = [], [], []
    for state in range(nstates):
        for new_bit in (0, 1):
            word = state | (new_bit << state_bits)
            label = pack_symbol(word, radius, levels, truths)
            next_state = (state >> 1) | (new_bit << (state_bits - 1))
            src.append(state)
            dst.append(next_state)
            labels.append(label)

    return (
        np.asarray(src, dtype=np.int32),
        np.asarray(dst, dtype=np.int32),
        np.asarray(labels, dtype=np.int16),
        nstates,
        radius,
        truths,
    )


def pair_edges(src, dst, labels, nstates):
    pair_src, pair_dst = [], []
    for label in np.unique(labels):
        indices = np.flatnonzero(labels == label)
        a = np.repeat(indices, len(indices))
        b = np.tile(indices, len(indices))
        pair_src.append(src[a].astype(np.int64) * nstates + src[b])
        pair_dst.append(dst[a].astype(np.int64) * nstates + dst[b])
    return np.concatenate(pair_src), np.concatenate(pair_dst)


def alive_nodes(nnodes, src, dst, forward=True):
    alive = np.ones(nnodes, dtype=bool)
    a, b = (src, dst) if forward else (dst, src)
    while True:
        ok = alive[a] & alive[b]
        degree = np.bincount(a[ok], minlength=nnodes)
        new = alive & (degree > 0)
        if int(new.sum()) == int(alive.sum()):
            return new
        alive = new


def adjacency_lists(nnodes, src, dst):
    adj = [[] for _ in range(nnodes)]
    radj = [[] for _ in range(nnodes)]
    for s, d in zip(src.tolist(), dst.tolist()):
        adj[s].append(d)
        radj[d].append(s)
    return adj, radj


def strongly_connected(adj, radj):
    n = len(adj)
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
    comps = []
    for root in reversed(order):
        if component[root] >= 0:
            continue
        cid = len(comps)
        members = []
        component[root] = cid
        stack = [root]
        while stack:
            v = stack.pop()
            members.append(v)
            for w in radj[v]:
                if component[w] < 0:
                    component[w] = cid
                    stack.append(w)
        comps.append(members)
    return np.asarray(component, dtype=np.int32), comps


def component_perron(members, src, dst):
    pos = {v: i for i, v in enumerate(members)}
    es, ed = [], []
    for s, d in zip(src.tolist(), dst.tolist()):
        if s in pos and d in pos:
            es.append(pos[s])
            ed.append(pos[d])

    n = len(members)
    if n == 1 and not any(s == 0 and d == 0 for s, d in zip(es, ed)):
        return 0.0

    indeg = np.bincount(ed, minlength=n)
    outdeg = np.bincount(es, minlength=n)
    if np.all(indeg == 1) and np.all(outdeg == 1):
        return 1.0
    if np.all(indeg == 2) and np.all(outdeg == 2):
        return 2.0

    es = np.asarray(es, dtype=np.int32)
    ed = np.asarray(ed, dtype=np.int32)
    v = np.ones(n, dtype=np.float64)
    v /= v.max()
    estimate = None
    for _ in range(20000):
        w = v + np.bincount(ed, weights=v[es], minlength=n)
        scale = float(w.max())
        if scale == 0:
            return 0.0
        w /= scale
        if estimate is not None and np.max(np.abs(w - v)) < 1e-14:
            v = w
            break
        v = w
        estimate = scale

    av = np.bincount(ed, weights=v[es], minlength=n)
    denom = float(np.dot(v, v))
    return float(np.dot(v, av) / denom)


def cycle_descriptor(members, adj, raw_u, raw_v, source_bits):
    internal = set(members)
    next_map = {}
    for v in members:
        inside = [d for d in adj[v] if d in internal]
        if len(inside) != 1:
            return None
        next_map[v] = inside[0]

    start = min(members)
    sequence = []
    current = start
    while current not in sequence:
        sequence.append(current)
        current = next_map[current]

    xb, yb = [], []
    for state in sequence:
        dest = next_map[state]
        xb.append((int(raw_u[dest]) >> (source_bits - 1)) & 1)
        yb.append((int(raw_v[dest]) >> (source_bits - 1)) & 1)

    reps = []
    for shift in range(len(xb)):
        xr = xb[shift:] + xb[:shift]
        yr = yb[shift:] + yb[:shift]
        key = "".join(map(str, xr)) + "|" + "".join(map(str, yr))
        reps.append((key, xr, yr))
    _, xr, yr = min(reps, key=lambda row: row[0])
    xor = [a ^ b for a, b in zip(xr, yr)]
    return {
        "period": len(sequence),
        "x_period": "".join(map(str, xr)),
        "y_period": "".join(map(str, yr)),
        "xor_period": "".join(map(str, xor)),
    }


def shortest_interfaces(adj, component, recurrent_ids, names, raw_u, raw_v, source_bits):
    out = []
    n = len(adj)
    for source_component in recurrent_ids:
        starts = np.flatnonzero(component == source_component).tolist()
        pred = [-2] * n
        queue = deque()
        for state in starts:
            pred[state] = -1
            queue.append(state)

        found = {}
        while queue:
            state = queue.popleft()
            target_component = int(component[state])
            if (
                target_component in recurrent_ids
                and target_component != source_component
                and target_component not in found
            ):
                found[target_component] = state
            for dest in adj[state]:
                if pred[dest] == -2:
                    pred[dest] = state
                    queue.append(dest)

        for target_component, end in found.items():
            path = []
            state = end
            while state != -1:
                path.append(state)
                state = pred[state]
            path.reverse()

            i = 0
            while i + 1 < len(path) and component[path[i + 1]] == source_component:
                i += 1
            j = len(path) - 1
            while j - 1 >= 0 and component[path[j - 1]] == target_component:
                j -= 1
            path = path[i:j + 1]

            x0 = int(raw_u[path[0]])
            y0 = int(raw_v[path[0]])
            xs = [(x0 >> b) & 1 for b in range(source_bits)]
            ys = [(y0 >> b) & 1 for b in range(source_bits)]
            for node in path[1:]:
                xs.append((int(raw_u[node]) >> (source_bits - 1)) & 1)
                ys.append((int(raw_v[node]) >> (source_bits - 1)) & 1)

            out.append({
                "from": names[source_component],
                "to": names[target_component],
                "edges": len(path) - 1,
                "x_word": "".join(map(str, xs)),
                "y_word": "".join(map(str, ys)),
                "xor_word": "".join(str(a ^ b) for a, b in zip(xs, ys)),
            })

    return sorted(out, key=lambda row: (row["from"], row["to"]))


def directional_sync(src, dst, labels, nstates, reverse=False):
    if reverse:
        src, dst = dst, src

    transitions = [defaultdict(set) for _ in range(nstates)]
    alphabet = sorted(set(labels.tolist()))
    for s, d, label in zip(src.tolist(), dst.tolist(), labels.tolist()):
        transitions[s][label].add(d)

    start = frozenset(range(nstates))
    subsets = [start]
    index = {start: 0}
    words = [()]
    queue = deque([start])
    best_size = nstates
    best_index = 0

    while queue:
        subset = queue.popleft()
        i = index[subset]
        if len(subset) < best_size:
            best_size = len(subset)
            best_index = i
        for label in alphabet:
            dest = set()
            for state in subset:
                dest.update(transitions[state].get(label, ()))
            if not dest:
                continue
            frozen = frozenset(dest)
            if frozen not in index:
                index[frozen] = len(subsets)
                subsets.append(frozen)
                words.append(words[i] + (label,))
                queue.append(frozen)

    return {
        "determinized_states": len(subsets),
        "minimum_compatible_contexts": best_size,
        "median_compatible_contexts": float(np.median([len(s) for s in subsets])),
        "minimum_word_length": len(words[best_index]),
        "witness_jet_word": list(words[best_index]),
        "compatible_source_contexts": sorted(subsets[best_index]),
    }


def local_inverse(rule, end_level, truths, radius):
    source_radius = end_level + 1
    width = 2 * (radius + source_radius) + 1
    count = 1 << width
    words = np.arange(count, dtype=np.uint64)
    key = np.zeros(count, dtype=np.uint64)
    center = radius + source_radius
    bit_pos = 0

    for output_offset in range(-radius, radius + 1):
        for level in range(1, end_level + 1):
            r = level + 1
            start = center + output_offset - r
            window = 2 * r + 1
            mask = (1 << window) - 1
            sub = ((words >> np.uint64(start)) & np.uint64(mask)).astype(np.int64)
            key |= truths[level][sub].astype(np.uint64) << np.uint64(bit_pos)
            bit_pos += 1

    source_bit = ((words >> np.uint64(center)) & 1).astype(np.uint8)
    order = np.argsort(key, kind="stable")
    sorted_key = key[order]
    sorted_bit = source_bit[order]
    changes = np.empty(count, dtype=bool)
    changes[0] = True
    changes[1:] = sorted_key[1:] != sorted_key[:-1]
    starts = np.flatnonzero(changes)
    ends = np.r_[starts[1:], count]

    for a, b in zip(starts, ends):
        values = sorted_bit[a:b]
        if values.min() != values.max():
            states = order[a:b]
            x = int(states[np.flatnonzero(values == 0)[0]])
            y = int(states[np.flatnonzero(values == 1)[0]])
            return {
                "radius": radius,
                "pass": False,
                "source_width": width,
                "realized_jet_windows": len(starts),
                "witness": {
                    "word_x": int(words[x]),
                    "word_y": int(words[y]),
                    "shared_jet_key": int(sorted_key[a]),
                },
            }

    return {
        "radius": radius,
        "pass": True,
        "source_width": width,
        "realized_jet_windows": len(starts),
        "witness": None,
    }


def analyze_factor(name, rule, end_level, primary):
    src0, dst0, labels, nstates, source_radius, truths = source_edges(rule, end_level)
    pair_src0, pair_dst0 = pair_edges(src0, dst0, labels, nstates)

    raw_vertices = np.unique(np.concatenate([pair_src0, pair_dst0]))
    src = np.searchsorted(raw_vertices, pair_src0)
    dst = np.searchsorted(raw_vertices, pair_dst0)
    nvertices = len(raw_vertices)

    bi = alive_nodes(nvertices, src, dst, True) & alive_nodes(
        nvertices, src, dst, False
    )
    edge_mask = bi[src] & bi[dst]
    kept_vertices = np.flatnonzero(bi)
    remap = np.full(nvertices, -1, dtype=np.int32)
    remap[kept_vertices] = np.arange(len(kept_vertices), dtype=np.int32)

    es = remap[src[edge_mask]]
    ed = remap[dst[edge_mask]]
    raw = raw_vertices[kept_vertices]
    raw_u = raw // nstates
    raw_v = raw % nstates
    diagonal = raw_u == raw_v

    adj, radj = adjacency_lists(len(kept_vertices), es, ed)
    component, components = strongly_connected(adj, radj)

    recurrent_ids = []
    for cid, members in enumerate(components):
        cyclic = len(members) > 1 or any(v in adj[v] for v in members)
        if cyclic:
            recurrent_ids.append(cid)

    records = []
    names = {}
    used_names = set()
    for cid in recurrent_ids:
        members = components[cid]
        internal_edges = [
            (s, d)
            for s, d in zip(es.tolist(), ed.tolist())
            if component[s] == cid and component[d] == cid
        ]
        indeg = np.bincount(
            [d for _, d in internal_edges], minlength=len(kept_vertices)
        )[members]
        outdeg = np.bincount(
            [s for s, _ in internal_edges], minlength=len(kept_vertices)
        )[members]
        simple = bool(np.all(indeg == 1) and np.all(outdeg == 1))
        non_diag = int((~diagonal[members]).sum())
        diag_count = int(diagonal[members].sum())

        cycle = None
        if simple and non_diag:
            cycle = cycle_descriptor(
                members, adj, raw_u, raw_v, 2 * source_radius
            )

        if non_diag == 0:
            base_name = "diag"
        elif cycle:
            base_name = cycle["x_period"] + "|" + cycle["y_period"]
        else:
            base_name = "mixed"

        assigned = base_name
        suffix = 2
        while assigned in used_names:
            assigned = f"{base_name}#{suffix}"
            suffix += 1
        used_names.add(assigned)
        names[cid] = assigned

        rho = component_perron(members, es, ed)
        rec = {
            "name": assigned,
            "size": len(members),
            "edges": len(internal_edges),
            "diagonal_vertices": diag_count,
            "non_diagonal_vertices": non_diag,
            "simple_cycle": simple,
            "spectral_radius": rho,
            "entropy_bits_per_site": math.log2(rho) if rho > 0 else None,
        }
        if cycle:
            rec.update(cycle)
        records.append(rec)

    pair_rho = max(r["spectral_radius"] for r in records)
    pair_entropy = math.log2(pair_rho)

    interfaces = shortest_interfaces(
        adj, component, recurrent_ids, names, raw_u, raw_v, 2 * source_radius
    )

    direction = {
        "forward": directional_sync(src0, dst0, labels, nstates, False),
        "reverse": directional_sync(src0, dst0, labels, nstates, True),
    }

    inverse = []
    if primary:
        for radius in range(5):
            rec = local_inverse(rule, end_level, truths, radius)
            inverse.append(rec)
            if rec["pass"]:
                break

    return {
        "rule": rule,
        "prefix_levels": list(range(1, end_level + 1)),
        "prefix_names": ["G", "Q", "R", "A4", "A5"][:end_level],
        "primary": primary,
        "source_radius": source_radius,
        "source_contexts": nstates,
        "realized_alphabet": len(np.unique(labels)),
        "pair_graph_total_vertices": nvertices,
        "pair_graph_total_edges": len(src),
        "biinfinite_vertices": int(bi.sum()),
        "biinfinite_edges": int(edge_mask.sum()),
        "biinfinite_non_diagonal_vertices": int((~diagonal).sum()),
        "biinfinite_transient_non_diagonal_vertices": int(
            (~diagonal).sum()
            - sum(
                r["non_diagonal_vertices"] for r in records
            )
        ),
        "pair_graph_perron": pair_rho,
        "pair_graph_entropy_bits_per_site": pair_entropy,
        "relative_pair_entropy_above_source": pair_entropy - 1.0,
        "recurrent_components": sorted(records, key=lambda r: r["name"]),
        "interfaces": interfaces,
        "directional_synchronization": direction,
        "local_inverse": inverse,
    }


def main():
    factors = {}
    for name, rule, end_level, primary in FACTORS:
        factors[name] = analyze_factor(name, rule, end_level, primary)

    result = {
        "schema": "commutator-jet-fibers-v1",
        "date": "2026-10-07",
        "protocol": (
            "docs/research/protocols/"
            "commutator-jet-fibers-20261007.md"
        ),
        "factors": factors,
        "summary": {
            "110_control_relative_pair_entropy":
                factors["110_control_GQ"]["relative_pair_entropy_above_source"],
            "110_primary_relative_pair_entropy":
                factors["110_primary_GQR"]["relative_pair_entropy_above_source"],
            "62_control_relative_pair_entropy":
                factors["62_control_GQRA4"]["relative_pair_entropy_above_source"],
            "62_primary_relative_pair_entropy":
                factors["62_primary_GQRA4A5"]["relative_pair_entropy_above_source"],
            "110_primary_non_diagonal_recurrent_components": sum(
                1 for r in factors["110_primary_GQR"]["recurrent_components"]
                if r["non_diagonal_vertices"]
            ),
            "62_primary_non_diagonal_recurrent_components": sum(
                1 for r in factors["62_primary_GQRA4A5"]["recurrent_components"]
                if r["non_diagonal_vertices"]
            ),
            "110_primary_all_non_diagonal_recurrent_are_cycles": all(
                r["simple_cycle"]
                for r in factors["110_primary_GQR"]["recurrent_components"]
                if r["non_diagonal_vertices"]
            ),
            "62_primary_all_non_diagonal_recurrent_are_cycles": all(
                r["simple_cycle"]
                for r in factors["62_primary_GQRA4A5"]["recurrent_components"]
                if r["non_diagonal_vertices"]
            ),
        },
    }
    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
