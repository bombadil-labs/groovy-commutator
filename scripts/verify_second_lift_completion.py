#!/usr/bin/env python3
"""Bounded second-lift completion comparison (frozen protocol 2026-09-10).

This implementation is intentionally self-contained. The primary path uses
truth-table lookup on chunked NumPy arrays. The independent path uses literal
Boolean formulas for F32/F128/F160 and separately reconstructs every feature /
target pair. Primary evaluation is only run by the default command; the
``--controls-only`` mode is safe to use before the implementation commit is
pinned because it executes only the frozen theorem/ordering controls.

Frozen matrix:
  completions H128, H160
  domains inherited B=E(full binary shift), ambient GF(2)^2 full shift
  coordinates K, O
  h=0,1,2; R=0,1,2

Pair symbols are 2*U+V. Source bits and pair symbols are enumerated MSB-first.
Feature keys are site-major x=-R..R, then row j=0..h, U before V, packed MSB
first into uint32. Target symbols are 2*U+V.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import pathlib
import shutil
import subprocess

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "results/second_lift_completion_20260911.json"
TABLE_DIR = ROOT / "results/second_lift_completion_tables_20260911"
PROTOCOL = ROOT / "docs/research/protocols/second-lift-completion-comparison-20260910.md"
CHUNK = 65_536
COMPLETIONS = (128, 160)
DOMAINS = ("inherited", "ambient")
KINDS = ("K", "O")
DEPTHS = (0, 1, 2)
RADII = (0, 1, 2)
MASK_TO_TARGET = np.full(16, 255, dtype=np.uint8)
MASK_TO_TARGET[[1, 2, 4, 8]] = [0, 1, 2, 3]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def truth(rule: int) -> np.ndarray:
    return np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)


TRUTH = {r: truth(r) for r in (32, 128, 160)}


def eca_primary(bits: np.ndarray, rule: int) -> np.ndarray:
    """Shrinking ECA update, primary path."""
    if bits.shape[1] < 3:
        raise ValueError("need width >= 3")
    code = 4 * bits[:, :-2] + 2 * bits[:, 1:-1] + bits[:, 2:]
    return TRUTH[rule][code]


def eca_reference(bits: np.ndarray, rule: int) -> np.ndarray:
    """Independent shrinking update using literal Boolean formulas."""
    l, c, r = bits[:, :-2], bits[:, 1:-1], bits[:, 2:]
    if rule == 32:
        return l & (1 ^ c) & r
    if rule == 128:
        return l & c & r
    if rule == 160:
        return l & r
    raise ValueError(rule)


def H_primary(pair: tuple[np.ndarray, np.ndarray], top: int) -> tuple[np.ndarray, np.ndarray]:
    u, v = pair
    return eca_primary(u, 32) ^ v[:, 1:-1], eca_primary(v, top)


def H_reference(pair: tuple[np.ndarray, np.ndarray], top: int) -> tuple[np.ndarray, np.ndarray]:
    u, v = pair
    return eca_reference(u, 32) ^ v[:, 1:-1], eca_reference(v, top)


def crop_pair(pair: tuple[np.ndarray, np.ndarray], margin: int) -> tuple[np.ndarray, np.ndarray]:
    if margin == 0:
        return pair
    return pair[0][:, margin:-margin], pair[1][:, margin:-margin]


def xor_pair(a: tuple[np.ndarray, np.ndarray], b: tuple[np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    if a[0].shape != b[0].shape or a[1].shape != b[1].shape:
        raise AssertionError((a[0].shape, b[0].shape))
    return a[0] ^ b[0], a[1] ^ b[1]


def A_recursive(pair: tuple[np.ndarray, np.ndarray], top: int, j: int, ref: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """A_j = A_{j-1} H XOR H A_{j-1}; radius j+1."""
    Hf = H_reference if ref else H_primary
    if j == 0:
        hp = Hf(pair, top)
        return xor_pair(crop_pair(pair, 1), hp)
    left = A_recursive(Hf(pair, top), top, j - 1, ref=ref)
    right = Hf(A_recursive(pair, top, j - 1, ref=ref), top)
    return xor_pair(left, right)


def O_coord(pair: tuple[np.ndarray, np.ndarray], top: int, j: int, ref: bool = False) -> tuple[np.ndarray, np.ndarray]:
    Hf = H_reference if ref else H_primary
    cur = pair
    for _ in range(j):
        cur = Hf(cur, top)
    return A_recursive(cur, top, 0, ref=ref)


def coords(pair: tuple[np.ndarray, np.ndarray], top: int, kind: str, h_plus_target: int, ref: bool = False):
    fn = A_recursive if kind == "K" else O_coord
    return [fn(pair, top, j, ref=ref) for j in range(h_plus_target + 1)]


def decode_binary_words(start: int, stop: int, width: int) -> np.ndarray:
    vals = np.arange(start, stop, dtype=np.uint64)
    shifts = np.arange(width - 1, -1, -1, dtype=np.uint64)
    return ((vals[:, None] >> shifts) & 1).astype(np.uint8)


def decode_pair_words(start: int, stop: int, width: int) -> tuple[np.ndarray, np.ndarray]:
    vals = np.arange(start, stop, dtype=np.uint64)
    shifts = 2 * np.arange(width - 1, -1, -1, dtype=np.uint64)
    symbols = ((vals[:, None] >> shifts) & 3).astype(np.uint8)
    return symbols >> 1, symbols & 1


def encode_first_image(source: np.ndarray, ref: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """E(S)=(D(S),G(S)) aligned on centers with two source sites of halo."""
    step = eca_reference if ref else eca_primary
    fs = step(source, 32)
    d = source[:, 1:-1] ^ fs
    d_fs = fs[:, 1:-1] ^ step(fs, 32)
    f_d = step(d, 32)
    g = d_fs ^ f_d
    return d[:, 1:-1], g


def radius_for(h: int, R: int) -> int:
    return max(R + h + 1, h + 2)


def input_size(domain: str, rho: int) -> tuple[int, int]:
    if domain == "inherited":
        r = rho + 2
        return 2 * r + 1, 1 << (2 * r + 1)
    return 2 * rho + 1, 1 << (2 * (2 * rho + 1))


def extract_feature_target(
    pair: tuple[np.ndarray, np.ndarray], top: int, kind: str, h: int, R: int, ref: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    cs = coords(pair, top, kind, h + 1, ref=ref)
    n = pair[0].shape[0]
    key = np.zeros(n, dtype=np.uint32)
    for x in range(-R, R + 1):
        for j in range(h + 1):
            u, v = cs[j]
            c = u.shape[1] // 2
            key = (key << 1) | u[:, c + x].astype(np.uint32)
            key = (key << 1) | v[:, c + x].astype(np.uint32)
    tu, tv = cs[h + 1]
    c = tu.shape[1] // 2
    target = (2 * tu[:, c] + tv[:, c]).astype(np.uint8)
    return key, target


def case_chunk(start: int, stop: int, domain: str, rho: int, top: int, kind: str, h: int, R: int, ref: bool = False):
    width, _ = input_size(domain, rho)
    if domain == "inherited":
        source = decode_binary_words(start, stop, width)
        pair = encode_first_image(source, ref=ref)
    else:
        pair = decode_pair_words(start, stop, width)
    return extract_feature_target(pair, top, kind, h, R, ref=ref)


def canonical_records(unique_keys: np.ndarray, masks: np.ndarray) -> bytes:
    """4 little-endian key bytes followed by one target-membership byte."""
    rec = np.empty(len(unique_keys), dtype=[("key", "<u4"), ("mask", "u1")])
    rec["key"] = unique_keys
    rec["mask"] = masks
    assert rec.dtype.itemsize == 5
    return rec.tobytes()


def relation_from_arrays(keys: np.ndarray, targets: np.ndarray, preimages: np.ndarray):
    order = np.argsort(keys, kind="stable")
    ks = keys[order]
    ts = targets[order]
    ps = preimages[order]
    starts = np.r_[0, np.flatnonzero(ks[1:] != ks[:-1]) + 1]
    uniq = ks[starts]
    bit_targets = (np.uint8(1) << ts).astype(np.uint8)
    masks = np.bitwise_or.reduceat(bit_targets, starts)
    conflict_ix = np.flatnonzero((masks & (masks - 1)) != 0)
    witness = None
    if len(conflict_ix):
        gi = int(conflict_ix[0])
        lo = int(starts[gi])
        hi = int(starts[gi + 1]) if gi + 1 < len(starts) else len(ks)
        mask = int(masks[gi])
        vals = [t for t in range(4) if mask & (1 << t)]
        t0, t1 = vals[:2]
        p0 = int(ps[lo + int(np.flatnonzero(ts[lo:hi] == t0)[0])])
        p1 = int(ps[lo + int(np.flatnonzero(ts[lo:hi] == t1)[0])])
        witness = {"key": int(uniq[gi]), "targets": [t0, t1], "preimages": [p0, p1]}
    return uniq.astype(np.uint32), masks.astype(np.uint8), witness


def verify_complete_law_for_pass(top: int, domain: str, kind: str, h: int, R: int, uniq: np.ndarray, masks: np.ndarray) -> int:
    """Independent all-window replay of the complete tuple law for a passing cap."""
    rho = radius_for(h, R)
    _, total = input_size(domain, rho)
    checked = 0
    for start in range(0, total, CHUNK):
        stop = min(total, start + CHUNK)
        width, _ = input_size(domain, rho)
        if domain == "inherited":
            source = decode_binary_words(start, stop, width)
            pair = encode_first_image(source, ref=True)
        else:
            pair = decode_pair_words(start, stop, width)
        rows = coords(pair, top, kind, h, ref=True)
        key, _ = extract_feature_target(pair, top, kind, h, R, ref=True)
        loc = np.searchsorted(uniq, key)
        forced_masks = masks[loc]
        assert np.all((forced_masks & (forced_masks - 1)) == 0)
        forced = MASK_TO_TARGET[forced_masks]
        fu, fv = (forced >> 1) & 1, forced & 1

        hp = H_reference(pair, top)
        direct = coords(hp, top, kind, h, ref=True)
        direct_center = []
        for row in direct:
            c = row[0].shape[1] // 2
            direct_center.append((row[0][:, c], row[1][:, c]))

        predicted = []
        if kind == "K":
            for j in range(h + 1):
                hj = H_reference(rows[j], top)
                c = hj[0].shape[1] // 2
                hu, hv = hj[0][:, c], hj[1][:, c]
                if j < h:
                    nxt = rows[j + 1]
                    c2 = nxt[0].shape[1] // 2
                    gu, gv = nxt[0][:, c2], nxt[1][:, c2]
                else:
                    gu, gv = fu, fv
                predicted.append((hu ^ gu, hv ^ gv))
        else:
            for j in range(h + 1):
                if j < h:
                    nxt = rows[j + 1]
                    c2 = nxt[0].shape[1] // 2
                    predicted.append((nxt[0][:, c2], nxt[1][:, c2]))
                else:
                    predicted.append((fu, fv))
        for (pu, pv), (du, dv) in zip(predicted, direct_center):
            if not np.array_equal(pu, du) or not np.array_equal(pv, dv):
                bad = int(np.flatnonzero((pu != du) | (pv != dv))[0])
                raise AssertionError(("complete-law", top, domain, kind, h, R, start + bad))
        checked += stop - start
    return checked


def evaluate_case(top: int, domain: str, kind: str, h: int, R: int, write_table: bool = True) -> dict:
    rho = radius_for(h, R)
    width, total = input_size(domain, rho)
    keys = np.empty(total, dtype=np.uint32)
    targets = np.empty(total, dtype=np.uint8)
    digest_primary = hashlib.sha256()
    digest_reference = hashlib.sha256()

    for start in range(0, total, CHUNK):
        stop = min(total, start + CHUNK)
        kp, tp = case_chunk(start, stop, domain, rho, top, kind, h, R, ref=False)
        kr, tr = case_chunk(start, stop, domain, rho, top, kind, h, R, ref=True)
        if not np.array_equal(kp, kr) or not np.array_equal(tp, tr):
            bad = int(np.flatnonzero((kp != kr) | (tp != tr))[0])
            raise AssertionError((top, domain, kind, h, R, start + bad, int(kp[bad]), int(kr[bad]), int(tp[bad]), int(tr[bad])))
        keys[start:stop] = kp
        targets[start:stop] = tp
        packed = np.empty(stop - start, dtype=[("k", "<u4"), ("t", "u1")])
        packed["k"] = kp
        packed["t"] = tp
        digest_primary.update(packed.tobytes())
        packed2 = np.empty(stop - start, dtype=[("k", "<u4"), ("t", "u1")])
        packed2["k"] = kr
        packed2["t"] = tr
        digest_reference.update(packed2.tobytes())

    pre = np.arange(total, dtype=np.uint32)
    uniq, masks, witness = relation_from_arrays(keys, targets, pre)
    records = canonical_records(uniq, masks)
    table_sha = sha_bytes(records)
    pass_case = witness is None

    if witness is not None:
        p0, p1 = witness["preimages"]
        k0, t0 = case_chunk(p0, p0 + 1, domain, rho, top, kind, h, R, ref=True)
        k1, t1 = case_chunk(p1, p1 + 1, domain, rho, top, kind, h, R, ref=True)
        assert int(k0[0]) == int(k1[0]) == witness["key"]
        assert sorted([int(t0[0]), int(t1[0])]) == witness["targets"]
        fb = 2 * (h + 1) * (2 * R + 1)
        witness["feature_patch_bits_msb"] = format(witness["key"], f"0{fb}b") if fb else ""
        witness["evaluation_convention"] = "inherited: binary source MSB-first; ambient: base-four pair symbols MSB-first; feature site-major x then row j then U,V"
        if domain == "inherited":
            witness["preimage_source_words_msb"] = [format(p, f"0{width}b") for p in (p0, p1)]
        else:
            def base4_word(p):
                return [int((p >> (2 * q)) & 3) for q in range(width - 1, -1, -1)]
            witness["preimage_pair_symbols_msb"] = [base4_word(p0), base4_word(p1)]
    else:
        loc = np.searchsorted(uniq, keys)
        forced_masks = masks[loc]
        assert np.all((forced_masks & (forced_masks - 1)) == 0)
        forced = MASK_TO_TARGET[forced_masks]
        assert np.array_equal(forced, targets)

    complete_law_windows = verify_complete_law_for_pass(top, domain, kind, h, R, uniq, masks) if pass_case else 0

    artifact = None
    if write_table:
        TABLE_DIR.mkdir(parents=True, exist_ok=True)
        name = f"H{top}_{domain}_{kind}_h{h}_R{R}.records.b64"
        payload = base64.b64encode(records) + b"\n"
        (TABLE_DIR / name).write_bytes(payload)
        artifact = {
            "path": str((TABLE_DIR / name).relative_to(ROOT)),
            "encoding": "base64 of canonical 5-byte records",
            "stored_bytes": len(payload),
        }

    return {
        "completion": top,
        "domain": domain,
        "kind": kind,
        "h": h,
        "R": R,
        "pair_radius": rho,
        "input_width": width,
        "input_words": total,
        "feature_bits": 2 * (h + 1) * (2 * R + 1),
        "target_bits": 2,
        "realized_keys": int(len(uniq)),
        "pass": bool(pass_case),
        "complete_law_radius_if_pass": (max(1, R) if kind == "K" else R) if pass_case else None,
        "complete_law_windows_independently_verified": int(complete_law_windows),
        "complete_law_if_pass": ({
            "K": "rows j<h: H(A_j) XOR A_(j+1); top: H(A_h) XOR cap(K_h patch)",
            "O": "rows j<h: shift to O_(j+1); top: cap(O_h patch)",
        }[kind] if pass_case else None),
        "feature_target_sha256": digest_primary.hexdigest(),
        "independent_feature_target_sha256": digest_reference.hexdigest(),
        "table_record_count": int(len(uniq)),
        "table_sha256": table_sha,
        "default_unrealized_target": 0,
        "table_artifact": artifact,
        "conflict": witness,
    }


def controls_only() -> dict:
    """Frozen controls only; no primary matrix results."""
    counts = {}
    src = decode_binary_words(0, 128, 7)
    ep = encode_first_image(src, ref=False)
    er = encode_first_image(src, ref=True)
    assert np.array_equal(ep[0], er[0]) and np.array_equal(ep[1], er[1])
    for top in COMPLETIONS:
        hp = H_primary(ep, top)
        hr = H_reference(er, top)
        assert np.array_equal(hp[0], hr[0]) and np.array_equal(hp[1], hr[1])
        fs = eca_primary(src, 32)
        ef = encode_first_image(fs, ref=False)
        assert hp[0].shape[1] == 1 == ef[0].shape[1]
        assert np.array_equal(hp[0], ef[0]) and np.array_equal(hp[1], ef[1])
    v = ep[1]
    codes = 4 * v[:, 0] + 2 * v[:, 1] + v[:, 2]
    assert not np.any(codes == 5)
    counts["first_image_source_windows"] = 128
    counts["forbidden_top101_hits"] = 0

    u, v = decode_pair_words(0, 4**2, 2)
    symbols = 2 * u + v
    expected = np.array([[a, b] for a in range(4) for b in range(4)], dtype=np.uint8)
    assert np.array_equal(symbols, expected)
    b = decode_binary_words(0, 8, 3)
    assert ["".join(map(str, row.tolist())) for row in b] == ["000", "001", "010", "011", "100", "101", "110", "111"]
    counts["ordering_pair_words_width2"] = 16
    counts["ordering_binary_words_width3"] = 8

    n = 8
    s = decode_binary_words(0, 1 << n, n)
    def ring_step(row, rule):
        t = TRUTH[rule]
        return t[4 * np.roll(row, 1, axis=1) + 2 * row + np.roll(row, -1, axis=1)]
    f = ring_step(s, 32)
    d = s ^ f
    g = (f ^ ring_step(f, 32)) ^ ring_step(d, 32)
    X = (d, g)
    def ring_H(X, top):
        return ring_step(X[0], 32) ^ X[1], ring_step(X[1], top)
    def ring_a0(X, top):
        hx = ring_H(X, top)
        return X[0] ^ hx[0], X[1] ^ hx[1]
    def ring_a1(X, top):
        hx = ring_H(X, top)
        a0hx = ring_a0(hx, top)
        a0x = ring_a0(X, top)
        ha0x = ring_H(a0x, top)
        return a0hx[0] ^ ha0x[0], a0hx[1] ^ ha0x[1]
    h128 = ring_H(X, 128)
    h160 = ring_H(X, 160)
    agree = np.all(h128[0] == h160[0], axis=1) & np.all(h128[1] == h160[1], axis=1)
    assert int(agree.sum()) == 256
    u0 = ring_a0(X, 128)
    v128 = ring_a1(X, 128)
    v160 = ring_a1(X, 160)
    hu128 = ring_H(u0, 128)
    hu160 = ring_H(u0, 160)
    pred = (v128[0] ^ hu128[0] ^ hu160[0], v128[1] ^ hu128[1] ^ hu160[1])
    ok = np.all(pred[0] == v160[0], axis=1) & np.all(pred[1] == v160[1], axis=1)
    assert int(ok.sum()) == 256
    diff = np.any(hu128[0] != hu160[0], axis=1) | np.any(hu128[1] != hu160[1], axis=1)
    hits = np.flatnonzero(diff)
    assert len(hits) == 40 and int(hits[0]) == 21
    distinct = len({(tuple(a.tolist()), tuple(b.tolist())) for a, b in zip(X[0], X[1])})
    assert distinct == 255
    counts.update({
        "n8_source_cases": 256,
        "n8_distinct_family_states": 255,
        "completion_difference_after_A0": 40,
        "first_completion_difference_source": 21,
        "depth1_recoding_ok": 256,
    })
    return counts


def finite_diagnostics() -> dict:
    """Section 8 diagnostics. Small periodic rings only, explicitly labeled."""
    out = {"inherited_n8": {}, "ambient_n4": {}}
    def ring_step(row, rule):
        t = TRUTH[rule]
        return t[4 * np.roll(row, 1, axis=1) + 2 * row + np.roll(row, -1, axis=1)]
    def ring_H(X, top):
        return ring_step(X[0], 32) ^ X[1], ring_step(X[1], top)
    def ring_A(X, top, j):
        if j == 0:
            hx = ring_H(X, top)
            return X[0] ^ hx[0], X[1] ^ hx[1]
        hx = ring_H(X, top)
        l = ring_A(hx, top, j - 1)
        a = ring_A(X, top, j - 1)
        r = ring_H(a, top)
        return l[0] ^ r[0], l[1] ^ r[1]
    def ring_O(X, top, j):
        cur = X
        for _ in range(j):
            cur = ring_H(cur, top)
        return ring_A(cur, top, 0)
    def pack_tuple(rows):
        parts = []
        for u, v in rows:
            parts.append(np.packbits(u, axis=1, bitorder="big"))
            parts.append(np.packbits(v, axis=1, bitorder="big"))
        return np.concatenate(parts, axis=1)
    def hist_from_keys(keys: np.ndarray):
        raw = [row.tobytes() for row in keys]
        c = {}
        for x in raw:
            c[x] = c.get(x, 0) + 1
        hist = {}
        for size in c.values():
            hist[size] = hist.get(size, 0) + 1
        return len(c), {str(k): v for k, v in sorted(hist.items())}
    s = decode_binary_words(0, 256, 8)
    f = ring_step(s, 32)
    d = s ^ f
    g = (f ^ ring_step(f, 32)) ^ ring_step(d, 32)
    X = (d, g)
    xkey = pack_tuple([X])
    _, first = np.unique(xkey, axis=0, return_index=True)
    first = np.sort(first)
    for top in COMPLETIONS:
        out["inherited_n8"][str(top)] = {}
        for h in DEPTHS:
            K = [ring_A(X, top, j) for j in range(h + 1)]
            O = [ring_O(X, top, j) for j in range(h + 1)]
            kd = pack_tuple(K)
            od = pack_tuple(O)
            ks, kh = hist_from_keys(kd)
            os, oh = hist_from_keys(od)
            kd_dist = kd[first]
            od_dist = od[first]
            ksd, khd = hist_from_keys(kd_dist)
            osd, ohd = hist_from_keys(od_dist)
            out["inherited_n8"][str(top)][str(h)] = {
                "source_weighted": {"K_image": ks, "K_fiber_hist": kh, "O_image": os, "O_fiber_hist": oh},
                "uniform_distinct_X": {"family_states": len(first), "K_image": ksd, "K_fiber_hist": khd, "O_image": osd, "O_fiber_hist": ohd},
                "K_O_same_partition": bool(np.array_equal((kd[:, None, :] == kd[None, :, :]).all(2), (od[:, None, :] == od[None, :, :]).all(2))),
            }
    u, v = decode_pair_words(0, 4**4, 4)
    X = (u, v)
    for top in COMPLETIONS:
        out["ambient_n4"][str(top)] = {}
        for h in DEPTHS:
            K = [ring_A(X, top, j) for j in range(h + 1)]
            O = [ring_O(X, top, j) for j in range(h + 1)]
            ki, kh = hist_from_keys(pack_tuple(K))
            oi, oh = hist_from_keys(pack_tuple(O))
            out["ambient_n4"][str(top)][str(h)] = {"states": 256, "K_image": ki, "K_fiber_hist": kh, "O_image": oi, "O_fiber_hist": oh}
    for h in DEPTHS:
        assert out["inherited_n8"]["128"][str(h)]["source_weighted"] == out["inherited_n8"]["160"][str(h)]["source_weighted"]
        assert out["inherited_n8"]["128"][str(h)]["uniform_distinct_X"] == out["inherited_n8"]["160"][str(h)]["uniform_distinct_X"]
    return out


def recoding_audits() -> dict:
    """Exhaustive local-domain triangular controls on B."""
    result = {"K_O": {}, "cross_completion": {}}

    def T_from_K_fields(krows, top):
        rows = [(a.copy(), b.copy()) for a, b in krows]
        outs = []
        for t in range(len(rows)):
            c = rows[0][0].shape[1] // 2
            outs.append((rows[0][0][:, c], rows[0][1][:, c]))
            if t + 1 == len(rows):
                break
            nxt = []
            for j in range(len(rows) - 1):
                hj = H_reference(rows[j], top)
                higher = crop_pair(rows[j + 1], 1) if rows[j + 1][0].shape[1] == rows[j][0].shape[1] else rows[j + 1]
                diff = higher[0].shape[1] - hj[0].shape[1]
                if diff:
                    assert diff % 2 == 0
                    higher = crop_pair(higher, diff // 2)
                nxt.append(xor_pair(hj, higher))
            rows = nxt
        return outs

    def inverse_T_from_O_fields(orows, top):
        current = [(a.copy(), b.copy()) for a, b in orows]
        k = []
        for j in range(len(orows)):
            c = current[0][0].shape[1] // 2
            k.append((current[0][0][:, c], current[0][1][:, c]))
            if len(current) == 1:
                break
            nxt = []
            for t in range(len(current) - 1):
                hcur = H_reference(current[t], top)
                future = current[t + 1]
                diff = future[0].shape[1] - hcur[0].shape[1]
                if diff:
                    assert diff % 2 == 0
                    future = crop_pair(future, diff // 2)
                nxt.append(xor_pair(future, hcur))
            current = nxt
        return k

    for top in COMPLETIONS:
        result["K_O"][str(top)] = {}
        for h in DEPTHS:
            sr = 2 * h + 3
            width = 2 * sr + 1
            total = 1 << width
            ok_forward = ok_inverse = 0
            for start in range(0, total, CHUNK):
                stop = min(total, start + CHUNK)
                src = decode_binary_words(start, stop, width)
                X = encode_first_image(src, ref=True)
                krows = [A_recursive(X, top, j, ref=True) for j in range(h + 1)]
                orows = [O_coord(X, top, j, ref=True) for j in range(h + 1)]
                pred_o = T_from_K_fields(krows, top)
                direct_o = []
                for row in orows:
                    c = row[0].shape[1] // 2
                    direct_o.append((row[0][:, c], row[1][:, c]))
                assert all(np.array_equal(a, c) and np.array_equal(b, d) for (a, b), (c, d) in zip(pred_o, direct_o))
                pred_k = inverse_T_from_O_fields(orows, top)
                direct_k = []
                for row in krows:
                    c = row[0].shape[1] // 2
                    direct_k.append((row[0][:, c], row[1][:, c]))
                assert all(np.array_equal(a, c) and np.array_equal(b, d) for (a, b), (c, d) in zip(pred_k, direct_k))
                ok_forward += stop - start
                ok_inverse += stop - start
            result["K_O"][str(top)][str(h)] = {"binary_source_radius": sr, "source_words": total, "forward_ok": ok_forward, "inverse_ok": ok_inverse}

    for h in DEPTHS:
        sr = 3 * h + 3
        width = 2 * sr + 1
        total = 1 << width
        ok_128_160 = ok_160_128 = 0
        for start in range(0, total, CHUNK):
            stop = min(total, start + CHUNK)
            src = decode_binary_words(start, stop, width)
            X = encode_first_image(src, ref=True)
            k128 = [A_recursive(X, 128, j, ref=True) for j in range(h + 1)]
            k160 = [A_recursive(X, 160, j, ref=True) for j in range(h + 1)]
            o128 = [O_coord(X, 128, j, ref=True) for j in range(h + 1)]
            o160 = [O_coord(X, 160, j, ref=True) for j in range(h + 1)]
            for a, b in zip(o128, o160):
                assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1])
            p160 = inverse_T_from_O_fields(o128, 160)
            p128 = inverse_T_from_O_fields(o160, 128)
            d160 = []
            d128 = []
            for row in k160:
                c = row[0].shape[1] // 2
                d160.append((row[0][:, c], row[1][:, c]))
            for row in k128:
                c = row[0].shape[1] // 2
                d128.append((row[0][:, c], row[1][:, c]))
            assert all(np.array_equal(a, c) and np.array_equal(b, d) for (a, b), (c, d) in zip(p160, d160))
            assert all(np.array_equal(a, c) and np.array_equal(b, d) for (a, b), (c, d) in zip(p128, d128))
            ok_128_160 += stop - start
            ok_160_128 += stop - start
        result["cross_completion"][str(h)] = {"binary_source_radius": sr, "source_words": total, "128_to_160_ok": ok_128_160, "160_to_128_ok": ok_160_128}
    return result


def git_last_change(path: pathlib.Path) -> str | None:
    env_key = "SECOND_LIFT_IMPLEMENTATION_COMMIT" if path.resolve() == pathlib.Path(__file__).resolve() else None
    if env_key and env_key in __import__("os").environ:
        return __import__("os").environ[env_key]
    try:
        rel = str(path.resolve().relative_to(ROOT.resolve()))
        return subprocess.check_output(["git", "-C", str(ROOT), "log", "-1", "--format=%H", "--", rel], text=True).strip() or None
    except Exception:
        return None


def run_full() -> dict:
    controls = controls_only()
    if TABLE_DIR.exists():
        shutil.rmtree(TABLE_DIR)
    cases = []
    for top in COMPLETIONS:
        for domain in DOMAINS:
            for kind in KINDS:
                for h in DEPTHS:
                    for R in RADII:
                        cases.append(evaluate_case(top, domain, kind, h, R, write_table=True))
    o_equal = {}
    for h in DEPTHS:
        for R in RADII:
            a = next(c for c in cases if (c["completion"], c["domain"], c["kind"], c["h"], c["R"]) == (128, "inherited", "O", h, R))
            b = next(c for c in cases if (c["completion"], c["domain"], c["kind"], c["h"], c["R"]) == (160, "inherited", "O", h, R))
            same = a["table_sha256"] == b["table_sha256"] and a["feature_target_sha256"] == b["feature_target_sha256"] and a["pass"] == b["pass"]
            assert same
            o_equal[f"h{h}_R{R}"] = True
    recoding = recoding_audits()
    diagnostics = finite_diagnostics()
    minima = []
    for top in COMPLETIONS:
        for domain in DOMAINS:
            for kind in KINDS:
                for h in DEPTHS:
                    passing = [c["R"] for c in cases if c["completion"] == top and c["domain"] == domain and c["kind"] == kind and c["h"] == h and c["pass"]]
                    minima.append({"completion": top, "domain": domain, "kind": kind, "h": h, "minimum_passing_R_through_2": min(passing) if passing else None})
    table_manifest = [{k: c[k] for k in ("completion", "domain", "kind", "h", "R", "table_record_count", "table_sha256", "default_unrealized_target", "table_artifact")} for c in cases]
    return {
        "schema": 1,
        "protocol": "second-lift-completion-comparison-20260910",
        "source_hashes": {"script": sha_file(pathlib.Path(__file__)), "protocol": sha_file(PROTOCOL)},
        "source_commits": {"implementation_commit": git_last_change(pathlib.Path(__file__)), "protocol_last_change_commit": git_last_change(PROTOCOL)},
        "implementation_corrections": [],
        "protocol_deviations": [{
            "stage": "pre-pin harness development",
            "description": "Before the implementation commit was pinned, the theorem-backed K↔O/cross-completion recoding audits and the Section 8 finite n=8/n=4 diagnostic helper were executed while validating the harness. No 72-case primary cap matrix or table artifact was run or inspected, no protocol choice or scientific logic was changed in response, and all of these controls/diagnostics are rerun canonically after the pinned implementation. This procedural deviation is retained rather than hidden.",
        }],
        "packing": "source/pair words MSB-first; pair symbol=2U+V; feature site-major x then row j then U,V; uint32 key; target pair 2U+V",
        "canonical_table_record": "4 little-endian key bytes + 1 target-membership-mask byte, sorted unsigned key; unseen key target defaults to symbol 0; artifact stores base64 of exact record bytes",
        "matrix": {"completions": list(COMPLETIONS), "domains": list(DOMAINS), "coordinates": list(KINDS), "h": list(DEPTHS), "R": list(RADII), "case_count": len(cases)},
        "controls": controls,
        "cases": cases,
        "minimum_passing_radius": minima,
        "inherited_O_literal_table_equality": o_equal,
        "recoding_audits": recoding,
        "recoding_cost_bounds": {
            "T_or_inverse_radius_at_depth_h": "<= h for radius-one H",
            "cross_completion_radius_each_direction": "<= 2h",
            "cross_completion_H_applications_each_direction": "h(h+1) whole-field applications of a two-component H/H'",
            "depth1_sharp_formula": "(u,v) -> (u, v XOR H(u) XOR H'(u)), radius <= 1",
            "transferred_complete_law_radius": "if one coordinate law has radius r, conservative conjugated bound <= r+4h",
            "status": "constructive upper bounds, not minimum radii or gate lower bounds",
        },
        "finite_diagnostics": diagnostics,
        "table_manifest": table_manifest,
        "resource_accounting": {"chunk_words": CHUNK, "declared_active_case_memory_limit_bytes": 2 * 1024**3, "case_timeout_seconds": 4 * 3600, "spatial_lattice": "Z unchanged", "alphabet": "GF(2)^2 input; K_h/O_h represented alphabet GF(2)^(2(h+1))", "note": "alphabet growth and correction depth are resources; no new spatial axis"},
        "summary": {"all_independent_digests_match": all(c["feature_target_sha256"] == c["independent_feature_target_sha256"] for c in cases), "case_count": len(cases), "passing_cases": sum(c["pass"] for c in cases), "conflicting_cases": sum(not c["pass"] for c in cases)},
    }


def write_result(data: dict):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls-only", action="store_true", help="run only frozen pre-evaluation controls")
    ap.add_argument("--stdout", action="store_true", help="print full result JSON instead of writing canonical file")
    ns = ap.parse_args(argv)
    if ns.controls_only:
        print(json.dumps({"controls": controls_only()}, indent=2, sort_keys=True))
        return 0
    data = run_full()
    if ns.stdout:
        print(json.dumps(data, indent=1, sort_keys=True))
    else:
        write_result(data)
        print(json.dumps(data["summary"], sort_keys=True))
        print("wrote", OUT.relative_to(ROOT), "and", TABLE_DIR.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
