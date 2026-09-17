#!/usr/bin/env python3
"""Exact finite observer/coarse-graining audit for the HighLife <-> ECA54 bridge.

Post-hoc algebraic diagnostic, not part of the frozen primary classifier protocol.
It records the chain-rule decomposition of the unstandardized selective-surprisal
gap under the many-to-one width-1 outer-totalistic observation map.
"""
from __future__ import annotations
import argparse, json, math, pathlib, sys
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run as core


def cross_entropy(p: np.ndarray, q: np.ndarray) -> float:
    mask = p > 0
    if np.any(q[mask] <= 0):
        return math.inf
    return float(np.sum(p[mask] * (-np.log2(q[mask]))))


def kl_bits(p: np.ndarray, q: np.ndarray) -> float:
    mask = p > 0
    if np.any(q[mask] <= 0):
        return math.inf
    return float(np.sum(p[mask] * np.log2(p[mask] / q[mask])))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    rule = 54
    width = 521
    burn = 256
    score = 256

    q_fine = core.reference_eca(rule)
    phi = np.array([core.highlife_outer_symbol_from_eca_symbol(z) for z in range(8)], dtype=np.int64)
    q_coarse = np.zeros(18, dtype=float)
    for z, prob in enumerate(q_fine):
        q_coarse[phi[z]] += prob

    rng = np.random.default_rng(core.stable_seed('width1-representation-audit'))
    state = rng.integers(0, 2, size=width, dtype=np.uint8)
    for _ in range(burn):
        state = core.eca_step(state, rule)
    idx = np.arange(width, dtype=int)
    symbols = []
    for _ in range(score):
        symbols.append(core.eca_symbols(state, idx))
        state = core.eca_step(state, rule)
    z = np.concatenate(symbols)
    p_fine = np.bincount(z, minlength=8).astype(float)
    p_fine /= p_fine.sum()
    p_coarse = np.zeros(18, dtype=float)
    for zz, prob in enumerate(p_fine):
        p_coarse[phi[zz]] += prob

    delta_fine = cross_entropy(p_fine, q_fine) - cross_entropy(q_fine, q_fine)
    delta_coarse = cross_entropy(p_coarse, q_coarse) - cross_entropy(q_coarse, q_coarse)

    cond_surprisal = np.zeros(8, dtype=float)
    for zz in range(8):
        yy = phi[zz]
        if q_fine[zz] > 0:
            cond_surprisal[zz] = -math.log2(q_fine[zz] / q_coarse[yy])
    delta_within_fiber = float(np.sum(p_fine * cond_surprisal) - np.sum(q_fine * cond_surprisal))

    kl_fine = kl_bits(p_fine, q_fine)
    kl_coarse = kl_bits(p_coarse, q_coarse)
    kl_conditional = kl_fine - kl_coarse

    out = {
        'status': 'post-hoc exact algebra + finite Rule54 trajectory audit',
        'map': {str(z): int(phi[z]) for z in range(8)},
        'reference_fine': q_fine.tolist(),
        'reference_coarse': q_coarse.tolist(),
        'trajectory_fine': p_fine.tolist(),
        'trajectory_coarse': p_coarse.tolist(),
        'selective_surprisal_gap_bits': {
            'fine': delta_fine,
            'coarse_visible': delta_coarse,
            'within_fiber_residual': delta_within_fiber,
            'reconstructed_fine': delta_coarse + delta_within_fiber,
            'absolute_chain_error': abs(delta_fine - delta_coarse - delta_within_fiber),
        },
        'kl_bits': {
            'fine': kl_fine,
            'coarse': kl_coarse,
            'conditional_residual': kl_conditional,
        },
        'theorem': (
            'For any deterministic coarse-graining phi and reference Q, '
            'Delta_Q(P)=E_P[-log Q]-E_Q[-log Q] decomposes as the same gap '
            'on the pushforward observer plus the difference in conditional '
            'reference surprisal inside phi-fibers. Standardized R* is not '
            'additive because each observer uses a different reference SD. '
            'KL obeys the usual nonnegative chain rule.'
        ),
        'interpretation': (
            'On this Rule54/HighLife width-1 map the coarse observer merges '
            'left-right reflected neighborhoods. The selective-surprisal gap '
            'is exactly recoverable as coarse-visible plus within-fiber '
            'selection. Here KL happens to be unchanged because the trajectory '
            'uses the merged fibers in the same conditional proportions as the reference.'
        ),
    }
    path = pathlib.Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + '\n')
    print(path)

if __name__ == '__main__':
    main()
