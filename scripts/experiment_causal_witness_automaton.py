"""Research032: exact symbolic causal-witness search with reduced 8-ary MDDs."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from experiment_causal_witness_horizon import macro_rule, TARGETS, pkey, FULL_CLASS  # noqa:E402

A = 8
PAIR_LIST = [(a, b) for a in range(A) for b in range(a + 1, A)]
PROTOCOL = "docs/research/protocols/causal-witness-automaton-20260909.md"


class NodeBudgetExceeded(RuntimeError):
    pass


class MDD:
    """Reduced ordered 8-valued decision diagram with terminals 0..7."""

    def __init__(self, nvars: int, node_budget: int):
        self.nvars = nvars
        self.node_budget = node_budget
        self.unique: dict[tuple[int, tuple[int, ...]], int] = {}
        self.data: dict[int, tuple[int, tuple[int, ...]]] = {}
        self.apply_cache: dict[tuple[int, int, int], int] = {}
        self.restrict_cache: dict[tuple[int, int, int], int] = {}
        self.pair_cache: dict[tuple[int, int], int] = {}
        self.apply_states_total = 0

    @property
    def node_count(self) -> int:
        return len(self.unique)

    def mk(self, var: int, children) -> int:
        children = tuple(int(x) for x in children)
        if all(x == children[0] for x in children):
            return children[0]
        key = (var, children)
        got = self.unique.get(key)
        if got is not None:
            return got
        if len(self.unique) >= self.node_budget:
            raise NodeBudgetExceeded(f"MDD node ceiling {self.node_budget} exceeded")
        node = A + len(self.unique)
        self.unique[key] = node
        self.data[node] = key
        return node

    def variable(self, var: int) -> int:
        return self.mk(var, range(A))

    def var_index(self, node: int) -> int:
        return self.nvars if node < A else self.data[node][0]

    def children(self, node: int):
        return None if node < A else self.data[node][1]

    def apply3(self, g, x: int, y: int, z: int) -> int:
        key = (x, y, z)
        got = self.apply_cache.get(key)
        if got is not None:
            return got
        if x < A and y < A and z < A:
            out = int(g[64 * x + 8 * y + z])
        else:
            var = min(self.var_index(x), self.var_index(y), self.var_index(z))
            cx = self.children(x) if self.var_index(x) == var else (x,) * A
            cy = self.children(y) if self.var_index(y) == var else (y,) * A
            cz = self.children(z) if self.var_index(z) == var else (z,) * A
            out = self.mk(var, [self.apply3(g, cx[i], cy[i], cz[i]) for i in range(A)])
        self.apply_cache[key] = out
        return out

    def restrict(self, node: int, var: int, value: int) -> int:
        key = (node, var, value)
        got = self.restrict_cache.get(key)
        if got is not None:
            return got
        if node < A:
            out = node
        else:
            nvar, children = self.data[node]
            if nvar == var:
                out = self.restrict(children[value], var, value)
            elif nvar > var:
                out = node
            else:
                out = self.mk(nvar, [self.restrict(c, var, value) for c in children])
        self.restrict_cache[key] = out
        return out

    def output_pair_mask(self, x: int, y: int) -> int:
        """64-bit mask of output leaf pairs reachable under shared assignments."""
        key = (x, y)
        got = self.pair_cache.get(key)
        if got is not None:
            return got
        if x < A and y < A:
            out = 1 << (A * x + y)
        else:
            var = min(self.var_index(x), self.var_index(y))
            cx = self.children(x) if self.var_index(x) == var else (x,) * A
            cy = self.children(y) if self.var_index(y) == var else (y,) * A
            out = 0
            for value in range(A):
                out |= self.output_pair_mask(cx[value], cy[value])
        self.pair_cache[key] = out
        return out

    def find_assignment(self, x: int, y: int, target: tuple[int, ...]):
        """Return (assignment, leaf_x, leaf_y) witnessing target difference, or None."""
        memo = {}

        def rec(a: int, b: int):
            key = (a, b)
            if key in memo:
                return memo[key]
            if a < A and b < A:
                ans = ({}, a, b) if target[a] != target[b] else None
                memo[key] = ans
                return ans
            var = min(self.var_index(a), self.var_index(b))
            ca = self.children(a) if self.var_index(a) == var else (a,) * A
            cb = self.children(b) if self.var_index(b) == var else (b,) * A
            for value in range(A):
                ans = rec(ca[value], cb[value])
                if ans is not None:
                    assignment, u, v = ans
                    assignment = dict(assignment)
                    assignment[var] = value
                    out = (assignment, u, v)
                    memo[key] = out
                    return out
            memo[key] = None
            return None

        return rec(x, y)


def canonical_targets_mask_for_output_pairs() -> list[int]:
    result = [0] * (A * A)
    for u in range(A):
        for v in range(A):
            bits = 0
            for tid, target in enumerate(TARGETS):
                if target[u] != target[v]:
                    bits |= 1 << tid
            result[A * u + v] = bits
    return result


OUTPUT_PAIR_TARGET_MASK = canonical_targets_mask_for_output_pairs()


def target_mask_from_output_pair_mask(pair_mask: int) -> int:
    out = 0
    mask = pair_mask
    while mask:
        lsb = mask & -mask
        idx = lsb.bit_length() - 1
        out |= OUTPUT_PAIR_TARGET_MASK[idx]
        mask ^= lsb
    return out


def build_local_function(rule: int, horizon: int, node_budget: int):
    started = time.perf_counter()
    g = macro_rule(rule)
    mdd = MDD(2 * horizon + 1, node_budget)
    row = [mdd.variable(i) for i in range(2 * horizon + 1)]
    for _ in range(horizon):
        mdd.apply_cache.clear()
        row = [mdd.apply3(g, row[i], row[i + 1], row[i + 2]) for i in range(len(row) - 2)]
        mdd.apply_states_total += len(mdd.apply_cache)
    return mdd, row[0], g, time.perf_counter() - started


def evaluate_word(g, word: list[int], horizon: int) -> int:
    row = list(word)
    for _ in range(horizon):
        row = [int(g[64 * row[i] + 8 * row[i + 1] + row[i + 2]]) for i in range(len(row) - 2)]
    assert len(row) == 1
    return row[0]


def horizon_masks(rule: int, horizon: int, node_budget: int):
    mdd, root, g, build_seconds = build_local_function(rule, horizon, node_budget)
    build_node_count = mdd.node_count
    masks = []
    query_started = time.perf_counter()
    for a, b in PAIR_LIST:
        target_mask = 0
        for axis in range(2 * horizon + 1):
            ra = mdd.restrict(root, axis, a)
            rb = mdd.restrict(root, axis, b)
            target_mask |= target_mask_from_output_pair_mask(mdd.output_pair_mask(ra, rb))
        masks.append(target_mask)
    query_seconds = time.perf_counter() - query_started
    return {
        "masks": masks,
        "mdd": mdd,
        "root": root,
        "g": g,
        "build_seconds": build_seconds,
        "query_seconds": query_seconds,
        "build_node_count": build_node_count,
        "query_node_count": mdd.node_count,
        "apply_states": mdd.apply_states_total,
        "pair_states": len(mdd.pair_cache),
    }


def extract_witness(rule: int, horizon: int, pair: tuple[int, int], tid: int, node_budget: int):
    result = horizon_masks(rule, horizon, node_budget)
    mdd, root, g = result["mdd"], result["root"], result["g"]
    a, b = pair
    target = TARGETS[tid]
    for axis in range(2 * horizon + 1):
        ra = mdd.restrict(root, axis, a)
        rb = mdd.restrict(root, axis, b)
        ans = mdd.find_assignment(ra, rb, target)
        if ans is None:
            continue
        assignment, u, v = ans
        word_a = [0] * (2 * horizon + 1)
        word_b = [0] * (2 * horizon + 1)
        for var, value in assignment.items():
            word_a[var] = value
            word_b[var] = value
        word_a[axis] = a
        word_b[axis] = b
        check_u = evaluate_word(g, word_a, horizon)
        check_v = evaluate_word(g, word_b, horizon)
        assert check_u == u and check_v == v and target[u] != target[v]
        return {
            "rule": rule,
            "horizon": horizon,
            "target": pkey(target),
            "target_id": tid,
            "pair": f"{a}-{b}",
            "axis": axis,
            "word_a": word_a,
            "word_b": word_b,
            "macro_output_a": u,
            "macro_output_b": v,
            "target_a": target[u],
            "target_b": target[v],
        }
    raise AssertionError((rule, horizon, pair, tid, "mask said witness but extraction failed"))


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scan_rule(rule: int, hmax: int, node_budget: int):
    cumulative = [0] * len(PAIR_LIST)
    records = []
    events = []
    censored = None
    for horizon in range(hmax + 1):
        unresolved_before = len(PAIR_LIST) * len(TARGETS) - sum(x.bit_count() for x in cumulative)
        if unresolved_before == 0:
            break
        try:
            result = horizon_masks(rule, horizon, node_budget)
        except NodeBudgetExceeded as exc:
            censored = {"horizon": horizon, "reason": str(exc), "node_budget": node_budget}
            break
        fresh_count = 0
        new_specs = []
        for pidx, mask in enumerate(result["masks"]):
            fresh = mask & ~cumulative[pidx]
            fresh_count += fresh.bit_count()
            while fresh:
                lsb = fresh & -fresh
                tid = lsb.bit_length() - 1
                if horizon >= 3:
                    new_specs.append((pidx, tid))
                fresh ^= lsb
            cumulative[pidx] |= mask
        unresolved_after = len(PAIR_LIST) * len(TARGETS) - sum(x.bit_count() for x in cumulative)
        records.append({
            "horizon": horizon,
            "build_node_count": result["build_node_count"],
            "query_node_count": result["query_node_count"],
            "build_seconds": result["build_seconds"],
            "query_seconds": result["query_seconds"],
            "apply_states": result["apply_states"],
            "pair_states": result["pair_states"],
            "new_births": fresh_count,
            "unresolved_after": unresolved_after,
        })
        for pidx, tid in new_specs:
            event = {"horizon": horizon, "pair": f"{PAIR_LIST[pidx][0]}-{PAIR_LIST[pidx][1]}", "target": pkey(TARGETS[tid]), "target_id": tid}
            if horizon >= 4:
                event["witness"] = extract_witness(rule, horizon, PAIR_LIST[pidx], tid, node_budget)
            events.append(event)
    return {
        "rule": rule,
        "wclass": FULL_CLASS[rule],
        "horizons": records,
        "events_h3_plus": events,
        "unresolved_final": len(PAIR_LIST) * len(TARGETS) - sum(x.bit_count() for x in cumulative),
        "censored": censored,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule-start", type=int, default=0)
    ap.add_argument("--rule-end", type=int, default=256)
    ap.add_argument("--hmax", type=int, default=5)
    ap.add_argument("--node-budget", type=int, default=5_000_000)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if not (0 <= args.rule_start < args.rule_end <= 256):
        raise SystemExit("bad rule range")
    rows = [scan_rule(rule, args.hmax, args.node_budget) for rule in range(args.rule_start, args.rule_end)]
    protocol_path = ROOT / PROTOCOL
    out = {
        "experiment": "causal-witness-automaton",
        "schema": 1,
        "rule_start": args.rule_start,
        "rule_end": args.rule_end,
        "hmax": args.hmax,
        "node_budget": args.node_budget,
        "source_hashes": {
            "scripts/experiment_causal_witness_automaton.py": file_hash(Path(__file__)),
            PROTOCOL: file_hash(protocol_path),
        },
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    counts = {}
    for h in range(args.hmax + 1):
        counts[str(h)] = sum(e["horizon"] == h for r in rows for e in r["events_h3_plus"])
    print(json.dumps({
        "rules": len(rows),
        "hmax": args.hmax,
        "events_h3_plus": counts,
        "censored_rules": [r["rule"] for r in rows if r["censored"]],
        "unresolved_final": sum(r["unresolved_final"] for r in rows),
    }, indent=2))


if __name__ == "__main__":
    main()
