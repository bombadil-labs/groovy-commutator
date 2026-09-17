#!/usr/bin/env python3
"""Cross-dimensional selective-persistence × spreading probe.

Frozen protocol:
  docs/research/protocols/2026-09-17-cross-dimensional-class4.md

No 2D threshold fitting is performed. The script emits per-rule/per-condition
R*, M*, S*, and perturbation-spreading summaries plus the exact HighLife
width-1 -> ECA 54 mapping control.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

PROTOCOL_ID = "cross-dimensional-class4-20260917-v1"


@dataclass(frozen=True)
class LifeRule:
    name: str
    births: tuple[int, ...]
    survives: tuple[int, ...]
    role: str

    @property
    def rulestring(self) -> str:
        return "B" + "".join(map(str, self.births)) + "/S" + "".join(map(str, self.survives))


LIFE_RULES = [
    LifeRule("life", (3,), (2, 3), "complex-exemplar"),
    LifeRule("highlife", (3, 6), (2, 3), "complex-exemplar"),
    LifeRule("day-night", (3, 6, 7, 8), (3, 4, 6, 7, 8), "complex-exemplar"),
    LifeRule("b35s236", (3, 5), (2, 3, 6), "explosive-adversary"),
    LifeRule("all-dead", (), (), "simple-control"),
    LifeRule("identity", (), tuple(range(9)), "simple-control"),
    LifeRule("complement", tuple(range(9)), (), "simple-control"),
    LifeRule("all-live", tuple(range(9)), tuple(range(9)), "simple-control"),
]

ECA_RULES = [
    (54, "prior-core"),
    (110, "prior-core"),
    (5, "persistence-control"),
    (62, "persistence-control"),
    (122, "spreading-control"),
    (126, "spreading-control"),
]


def stable_seed(*parts: object) -> int:
    text = "|".join(map(str, (PROTOCOL_ID,) + parts)).encode()
    return int.from_bytes(hashlib.sha256(text).digest()[:8], "little") & 0x7FFF_FFFF_FFFF_FFFF


def eca_step(state: np.ndarray, rule: int) -> np.ndarray:
    left = np.roll(state, 1)
    right = np.roll(state, -1)
    idx = (left << 2) | (state << 1) | right
    return ((rule >> idx) & 1).astype(np.uint8)


def life_step(state: np.ndarray, rule: LifeRule) -> np.ndarray:
    # Sum all eight Moore offsets separately. On a width-1 cylinder the
    # repeated wrapped positions therefore count with multiplicity, matching
    # standard torus/cylinder semantics and the HighLife->Rule54 control.
    count = np.zeros_like(state, dtype=np.uint8)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            count += np.roll(np.roll(state, dy, axis=0), dx, axis=1)
    b = np.zeros(9, dtype=np.uint8)
    s = np.zeros(9, dtype=np.uint8)
    if rule.births:
        b[list(rule.births)] = 1
    if rule.survives:
        s[list(rule.survives)] = 1
    return np.where(state != 0, s[count], b[count]).astype(np.uint8)


def eca_symbols(state: np.ndarray, indices: np.ndarray) -> np.ndarray:
    left = state[(indices - 1) % len(state)]
    center = state[indices]
    right = state[(indices + 1) % len(state)]
    return ((left << 2) | (center << 1) | right).astype(np.uint8)


def life_symbols(state: np.ndarray, ys: np.ndarray, xs: np.ndarray) -> np.ndarray:
    count = np.zeros(len(xs), dtype=np.uint8)
    h, w = state.shape
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            count += state[(ys + dy) % h, (xs + dx) % w]
    center = state[ys, xs]
    return (center * 9 + count).astype(np.uint8)


def reference_eca(rule: int) -> np.ndarray:
    counts = np.zeros(8, dtype=np.int64)
    for word in range(32):
        bits = np.array([(word >> (4 - i)) & 1 for i in range(5)], dtype=np.uint8)
        out = []
        for i in (1, 2, 3):
            idx = int((bits[i - 1] << 2) | (bits[i] << 1) | bits[i + 1])
            out.append((rule >> idx) & 1)
        z = (out[0] << 2) | (out[1] << 1) | out[2]
        counts[z] += 1
    return counts / counts.sum()


def life_patch_successor_symbols(patches: np.ndarray, rule: LifeRule) -> np.ndarray:
    # patches: [batch,5,5]. Evolve the central 3x3 one tick, then encode
    # the rule-input symbol at its center as (center, neighbor_count).
    n = patches.shape[0]
    succ = np.empty((n, 3, 3), dtype=np.uint8)
    b = np.zeros(9, dtype=np.uint8)
    s = np.zeros(9, dtype=np.uint8)
    if rule.births:
        b[list(rule.births)] = 1
    if rule.survives:
        s[list(rule.survives)] = 1
    for oy, py in enumerate((1, 2, 3)):
        for ox, px in enumerate((1, 2, 3)):
            cnt = np.zeros(n, dtype=np.uint8)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    cnt += patches[:, py + dy, px + dx]
            center = patches[:, py, px]
            succ[:, oy, ox] = np.where(center != 0, s[cnt], b[cnt])
    center = succ[:, 1, 1]
    ncount = succ.reshape(n, 9).sum(axis=1) - center
    return (center * 9 + ncount).astype(np.uint8)


def reference_life(rule: LifeRule, samples: int, seed: int, batch: int = 10_000) -> np.ndarray:
    rng = np.random.default_rng(seed)
    counts = np.zeros(18, dtype=np.int64)
    remaining = samples
    while remaining:
        k = min(batch, remaining)
        patches = rng.integers(0, 2, size=(k, 5, 5), dtype=np.uint8)
        z = life_patch_successor_symbols(patches, rule)
        counts += np.bincount(z, minlength=18)
        remaining -= k
    return counts / counts.sum()


def reference_surprisal(p: np.ndarray) -> tuple[np.ndarray, float, float]:
    q = np.full_like(p, np.inf, dtype=float)
    mask = p > 0
    q[mask] = -np.log2(p[mask])
    mu = float(np.sum(p[mask] * q[mask]))
    var = float(np.sum(p[mask] * (q[mask] - mu) ** 2))
    return q, mu, math.sqrt(max(var, 0.0))


def bernoulli_tables(current: np.ndarray, history: np.ndarray, target: np.ndarray):
    # Jeffreys smoothing.
    base_num = np.full(2, 0.5, dtype=float)
    base_den = np.full(2, 1.0, dtype=float)
    hist_num = np.full(256, 0.5, dtype=float)
    hist_den = np.full(256, 1.0, dtype=float)
    np.add.at(base_num, current, target)
    np.add.at(base_den, current, 1)
    np.add.at(hist_num, history, target)
    np.add.at(hist_den, history, 1)
    return base_num / base_den, hist_num / hist_den


def logloss_bits(prob: np.ndarray, target: np.ndarray) -> float:
    p = np.clip(prob, 1e-12, 1 - 1e-12)
    return float(np.mean(-(target * np.log2(p) + (1 - target) * np.log2(1 - p))))


def predictive_gain(train_events: list[dict], test_events: list[dict]) -> tuple[float, float, float, int, int]:
    tr_c = np.concatenate([e["current"] for e in train_events])
    tr_h = np.concatenate([e["history"] for e in train_events])
    tr_y = np.concatenate([e["target"] for e in train_events])
    te_c = np.concatenate([e["current"] for e in test_events])
    te_h = np.concatenate([e["history"] for e in test_events])
    te_y = np.concatenate([e["target"] for e in test_events])
    bp, hp = bernoulli_tables(tr_c, tr_h, tr_y)
    base = logloss_bits(bp[te_c], te_y)
    hist = logloss_bits(hp[te_h], te_y)
    return base - hist, base, hist, len(tr_y), len(te_y)


def sample_events_eca(rule: int, width: int, density: float, burn: int, score: int,
                      seeds: int, sites: int) -> list[dict]:
    out = []
    for rep in range(seeds):
        rng = np.random.default_rng(stable_seed("eca-events", rule, density, rep))
        state = (rng.random(width) < density).astype(np.uint8)
        for _ in range(burn):
            state = eca_step(state, rule)
        idx = np.sort(rng.choice(width, size=min(sites, width), replace=False))
        hist = np.zeros(len(idx), dtype=np.uint8)
        for _ in range(7):
            hist = ((hist << 1) | state[idx]) & 0xFF
            state = eca_step(state, rule)
        currents, histories, targets, symbols = [], [], [], []
        for _ in range(score):
            cur = state[idx].copy()
            hist = ((hist << 1) | cur) & 0xFF
            sym = eca_symbols(state, idx)
            nxt = eca_step(state, rule)
            currents.append(cur)
            histories.append(hist.copy())
            targets.append(nxt[idx].copy())
            symbols.append(sym)
            state = nxt
        out.append({
            "current": np.concatenate(currents),
            "history": np.concatenate(histories),
            "target": np.concatenate(targets),
            "symbol": np.concatenate(symbols),
        })
    return out


def sample_events_life(rule: LifeRule, size: int, density: float, burn: int, score: int,
                       seeds: int, sites: int) -> list[dict]:
    out = []
    for rep in range(seeds):
        rng = np.random.default_rng(stable_seed("life-events", rule.name, density, rep))
        state = (rng.random((size, size)) < density).astype(np.uint8)
        for _ in range(burn):
            state = life_step(state, rule)
        total = size * size
        flat = np.sort(rng.choice(total, size=min(sites, total), replace=False))
        ys, xs = flat // size, flat % size
        hist = np.zeros(len(flat), dtype=np.uint8)
        for _ in range(7):
            hist = ((hist << 1) | state[ys, xs]) & 0xFF
            state = life_step(state, rule)
        currents, histories, targets, symbols = [], [], [], []
        for _ in range(score):
            cur = state[ys, xs].copy()
            hist = ((hist << 1) | cur) & 0xFF
            sym = life_symbols(state, ys, xs)
            nxt = life_step(state, rule)
            currents.append(cur)
            histories.append(hist.copy())
            targets.append(nxt[ys, xs].copy())
            symbols.append(sym)
            state = nxt
        out.append({
            "current": np.concatenate(currents),
            "history": np.concatenate(histories),
            "target": np.concatenate(targets),
            "symbol": np.concatenate(symbols),
        })
    return out


def selective_r(events: list[dict], p_ref: np.ndarray) -> tuple[float, float, float, list[int]]:
    q, mu, sd = reference_surprisal(p_ref)
    z = np.concatenate([e["symbol"] for e in events])
    missing = sorted(set(map(int, z[p_ref[z] == 0])))
    if missing:
        return math.nan, mu, sd, missing
    traj = float(np.mean(q[z]))
    r = (traj - mu) / max(sd, 1e-12)
    return r, mu, sd, missing


def diameter_1d(diff: np.ndarray, origin: int) -> int:
    idx = np.flatnonzero(diff)
    if not len(idx):
        return 0
    n = len(diff)
    off = ((idx - origin + n // 2) % n) - n // 2
    return int(off.max() - off.min() + 1)


def diameter_2d(diff: np.ndarray, oy: int, ox: int) -> int:
    ys, xs = np.nonzero(diff)
    if not len(xs):
        return 0
    h, w = diff.shape
    dy = ((ys - oy + h // 2) % h) - h // 2
    dx = ((xs - ox + w // 2) % w) - w // 2
    return int(max(dy.max() - dy.min(), dx.max() - dx.min()) + 1)


def spreading_eca(rule: int, width: int, density: float, burn: int, t1: int, t2: int,
                  base_seeds: int, origins: int) -> dict:
    d1s, d2s = [], []
    extinct = 0
    for rep in range(base_seeds):
        rng = np.random.default_rng(stable_seed("eca-spread", rule, density, rep))
        base = (rng.random(width) < density).astype(np.uint8)
        for _ in range(burn):
            base = eca_step(base, rule)
        chosen = rng.choice(width, size=origins, replace=False)
        for origin in chosen:
            a = base.copy(); b = base.copy(); b[origin] ^= 1
            d1 = d2 = None
            for t in range(1, t2 + 1):
                a = eca_step(a, rule); b = eca_step(b, rule)
                if t == t1:
                    d1 = diameter_1d(a ^ b, int(origin))
                if t == t2:
                    d2 = diameter_1d(a ^ b, int(origin))
            assert d1 is not None and d2 is not None
            d1s.append(d1); d2s.append(d2)
            extinct += int(d2 == 0)
    return spread_summary(d1s, d2s, extinct)


def spreading_life(rule: LifeRule, size: int, density: float, burn: int, t1: int, t2: int,
                   base_seeds: int, origins: int) -> dict:
    d1s, d2s = [], []
    extinct = 0
    total = size * size
    for rep in range(base_seeds):
        rng = np.random.default_rng(stable_seed("life-spread", rule.name, density, rep))
        base = (rng.random((size, size)) < density).astype(np.uint8)
        for _ in range(burn):
            base = life_step(base, rule)
        chosen = rng.choice(total, size=origins, replace=False)
        for flat in chosen:
            oy, ox = divmod(int(flat), size)
            a = base.copy(); b = base.copy(); b[oy, ox] ^= 1
            d1 = d2 = None
            for t in range(1, t2 + 1):
                a = life_step(a, rule); b = life_step(b, rule)
                if t == t1:
                    d1 = diameter_2d(a ^ b, oy, ox)
                if t == t2:
                    d2 = diameter_2d(a ^ b, oy, ox)
            assert d1 is not None and d2 is not None
            d1s.append(d1); d2s.append(d2)
            extinct += int(d2 == 0)
    return spread_summary(d1s, d2s, extinct)


def spread_summary(d1s: Sequence[int], d2s: Sequence[int], extinct: int) -> dict:
    m1 = float(np.mean(d1s)); m2 = float(np.mean(d2s))
    alpha = None
    if m1 == 0 and m2 == 0:
        alpha = 0.0
    elif m1 > 0 and m2 > 0:
        alpha = float(math.log2(m2 / m1))
    return {
        "mean_d1": m1,
        "mean_d2": m2,
        "median_d1": float(np.median(d1s)),
        "median_d2": float(np.median(d2s)),
        "min_d1": int(min(d1s)), "max_d1": int(max(d1s)),
        "min_d2": int(min(d2s)), "max_d2": int(max(d2s)),
        "alpha_star": alpha,
        "extinction_fraction_t2": extinct / len(d2s),
        "trials": len(d2s),
    }


def highlife_outer_symbol_from_eca_symbol(code: int) -> int:
    """Push an ECA neighborhood through the width-1 HighLife observer.

    A one-row Moore cylinder counts left and right three times each and the
    center twice among the eight neighbors.
    """
    l, c, r = (code >> 2) & 1, (code >> 1) & 1, code & 1
    ncount = 3 * l + 2 * c + 3 * r
    return c * 9 + ncount


def width1_representation_audit(rule: int = 54, width: int = 521, burn: int = 256,
                                score: int = 256) -> dict:
    """Exact/finite audit of observer dependence on the Rule54↔HighLife line."""
    # Exact reference pushforward from uniform 5-bit line predecessors.
    p_eca = reference_eca(rule)
    p_outer = np.zeros(18, dtype=float)
    symbol_map = {}
    for z in range(8):
        oz = highlife_outer_symbol_from_eca_symbol(z)
        symbol_map[f"{z:03b}"] = {"eca_code": z, "outer_code": oz,
                                  "center": (z >> 1) & 1,
                                  "neighbor_count_with_multiplicity": oz % 9}
        p_outer[oz] += p_eca[z]

    q_e, mu_e, sd_e = reference_surprisal(p_eca)
    q_o, mu_o, sd_o = reference_surprisal(p_outer)

    rng = np.random.default_rng(stable_seed("width1-representation-audit"))
    state = rng.integers(0, 2, size=width, dtype=np.uint8)
    for _ in range(burn):
        state = eca_step(state, rule)
    idx = np.arange(width, dtype=int)
    vals_e, vals_o = [], []
    for _ in range(score):
        z = eca_symbols(state, idx)
        oz = np.fromiter((highlife_outer_symbol_from_eca_symbol(int(v)) for v in z),
                         dtype=np.uint8, count=len(z))
        vals_e.append(z); vals_o.append(oz)
        state = eca_step(state, rule)
    ze = np.concatenate(vals_e); zo = np.concatenate(vals_o)
    re = float((np.mean(q_e[ze]) - mu_e) / max(sd_e, 1e-12))
    ro = float((np.mean(q_o[zo]) - mu_o) / max(sd_o, 1e-12))

    return {
        "symbol_map": symbol_map,
        "map_is_injective": len(set(v["outer_code"] for v in symbol_map.values())) == 8,
        "eca_reference": p_eca.tolist(),
        "outer_reference_pushforward": p_outer.tolist(),
        "R_star_same_bit_history_eca_observer": re,
        "R_star_same_bit_history_outer_observer": ro,
        "R_star_equal": bool(abs(re - ro) < 1e-12),
        "M_star_invariance_reason": "identical bit histories and targets imply identical fitted/evaluated M*",
        "alpha_star_invariance_reason": "identical XOR bit fields along the one-row cylinder imply identical longitudinal support diameters",
        "interpretation": "M* and longitudinal spreading are exact under the state conjugacy; R* is observer/reference dependent under the many-to-one outer-totalistic symbol map.",
    }


def highlife_width1_control(ticks: int = 256, width: int = 521) -> dict:
    high = next(r for r in LIFE_RULES if r.name == "highlife")
    rows = []
    derived = 0
    for code in range(8):
        l, c, r = (code >> 2) & 1, (code >> 1) & 1, code & 1
        state = np.array([[l, c, r]], dtype=np.uint8)
        nxt = life_step(state, high)
        bit = int(nxt[0, 1])
        derived |= bit << code
        rows.append({"neighborhood": f"{l}{c}{r}", "output": bit})
    rng = np.random.default_rng(stable_seed("highlife-width1-control"))
    one = rng.integers(0, 2, size=width, dtype=np.uint8)
    two = one[None, :].copy()
    mismatch_tick = None
    for t in range(ticks + 1):
        if not np.array_equal(one, two[0]):
            mismatch_tick = t
            break
        one = eca_step(one, 54)
        two = life_step(two, high)
    return {
        "derived_eca_rule": derived,
        "expected_eca_rule": 54,
        "truth_table": rows,
        "ticks_checked": ticks,
        "width": width,
        "byte_identical": mismatch_tick is None,
        "first_mismatch_tick": mismatch_tick,
    }


def evaluate_eca(rule: int, role: str, density: float, cfg: dict) -> dict:
    t0 = time.time()
    events = sample_events_eca(rule, cfg["width1d"], density, cfg["burn"], cfg["score"],
                               cfg["event_seeds"], cfg["sites"])
    p = reference_eca(rule)
    rstar, ref_mu, ref_sd, missing = selective_r(events, p)
    mstar, base_ll, hist_ll, ntrain, ntest = predictive_gain(events[:4], events[4:6])
    spread = spreading_eca(rule, cfg["width1d"], density, cfg["burn"], cfg["t1"], cfg["t2"],
                           cfg["spread_seeds"], cfg["origins"])
    return {
        "dimension": 1, "name": f"eca-{rule}", "rule": rule, "role": role,
        "condition_density": density,
        "R_star": rstar, "M_star": mstar,
        "S_star": max(0.0, rstar) * max(0.0, mstar) if math.isfinite(rstar) else None,
        "reference_surprisal_mean": ref_mu, "reference_surprisal_sd": ref_sd,
        "unsupported_trajectory_symbols": missing,
        "baseline_logloss_bits": base_ll, "history_logloss_bits": hist_ll,
        "train_events": ntrain, "test_events": ntest,
        **spread, "wall_seconds": time.time() - t0,
    }


def evaluate_life(rule: LifeRule, density: float, cfg: dict) -> dict:
    t0 = time.time()
    # Reference doubling schedule is automatic and outcome-blind except for the
    # predeclared unsupported-symbol stopping condition.
    ref_n = cfg["reference_samples"]
    events = sample_events_life(rule, cfg["size2d"], density, cfg["burn"], cfg["score"],
                                cfg["event_seeds"], cfg["sites"])
    while True:
        p = reference_life(rule, ref_n, stable_seed("life-reference", rule.name, ref_n))
        rstar, ref_mu, ref_sd, missing = selective_r(events, p)
        if not missing or ref_n >= cfg["reference_max"]:
            break
        ref_n *= 2
    mstar, base_ll, hist_ll, ntrain, ntest = predictive_gain(events[:4], events[4:6])
    spread = spreading_life(rule, cfg["size2d"], density, cfg["burn"], cfg["t1"], cfg["t2"],
                            cfg["spread_seeds"], cfg["origins"])
    return {
        "dimension": 2, "name": rule.name, "rulestring": rule.rulestring, "role": rule.role,
        "condition_density": density,
        "R_star": rstar, "M_star": mstar,
        "S_star": max(0.0, rstar) * max(0.0, mstar) if math.isfinite(rstar) else None,
        "reference_samples": ref_n,
        "reference_surprisal_mean": ref_mu, "reference_surprisal_sd": ref_sd,
        "unsupported_trajectory_symbols": missing,
        "baseline_logloss_bits": base_ll, "history_logloss_bits": hist_ll,
        "train_events": ntrain, "test_events": ntest,
        **spread, "wall_seconds": time.time() - t0,
    }


def configs(mode: str) -> dict:
    if mode == "full":
        return dict(width1d=521, size2d=263, burn=512, score=256, event_seeds=6,
                    sites=64, t1=64, t2=128, spread_seeds=4, origins=8,
                    reference_samples=100_000, reference_max=800_000,
                    densities=[0.5, 0.3, 0.7])
    if mode == "pilot":
        # Explicitly non-primary: same formulas, smaller uniform budget for fast
        # end-to-end verification and directional debugging only.
        return dict(width1d=263, size2d=131, burn=128, score=96, event_seeds=6,
                    sites=24, t1=24, t2=48, spread_seeds=2, origins=4,
                    reference_samples=20_000, reference_max=160_000,
                    densities=[0.5])
    if mode == "smoke":
        return dict(width1d=131, size2d=67, burn=32, score=24, event_seeds=6,
                    sites=8, t1=8, t2=16, spread_seeds=1, origins=2,
                    reference_samples=2_000, reference_max=16_000,
                    densities=[0.5])
    raise ValueError(mode)


def write_csv(rows: list[dict], path: Path):
    keys = []
    seen = set()
    for row in rows:
        for k in row:
            if k not in seen:
                seen.add(k); keys.append(k)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            rr = {k: (json.dumps(v, sort_keys=True) if isinstance(v, (list, dict)) else v) for k, v in r.items()}
            w.writerow(rr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["smoke", "pilot", "full", "mapping"], default="smoke")
    ap.add_argument("--output-dir", default="results/cross_dimensional_class4_20260917")
    args = ap.parse_args()
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    mapping = highlife_width1_control()
    mapping["representation_audit"] = width1_representation_audit()
    (outdir / "mapping_control.json").write_text(json.dumps(mapping, indent=2, sort_keys=True) + "\n")
    if not mapping["byte_identical"] or mapping["derived_eca_rule"] != 54:
        raise SystemExit("HighLife width-1 mapping control failed; stopping before phenotype evaluation")
    if args.mode == "mapping":
        print(json.dumps(mapping, indent=2))
        return

    cfg = configs(args.mode)
    rows = []
    for density in cfg["densities"]:
        for rule, role in ECA_RULES:
            row = evaluate_eca(rule, role, density, cfg)
            rows.append(row)
            print(f"done {row['name']} d={density}: S*={row['S_star']:.4g} alpha*={row['alpha_star']}", flush=True)
        for rule in LIFE_RULES:
            row = evaluate_life(rule, density, cfg)
            rows.append(row)
            print(f"done {row['name']} d={density}: S*={row['S_star']:.4g} alpha*={row['alpha_star']}", flush=True)

    payload = {
        "protocol_id": PROTOCOL_ID,
        "mode": args.mode,
        "scientific_status": "primary" if args.mode == "full" else "non-primary implementation/pilot",
        "config": cfg,
        "mapping_control": mapping,
        "rows": rows,
    }
    jpath = outdir / f"crossdim_{args.mode}.json"
    cpath = outdir / f"crossdim_{args.mode}.csv"
    jpath.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")
    write_csv(rows, cpath)
    print(jpath)
    print(cpath)


if __name__ == "__main__":
    main()
