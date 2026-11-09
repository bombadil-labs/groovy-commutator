#!/usr/bin/env python3
"""Render code-generated S,D,G,Q,R spacetime panels for Rules 110 and 62.

Scientific definitions:
  S_{t+1}=H(S_t)
  D_t=S_t xor S_{t+1}
  A_{k+1,t}=A_{k,t+1} xor H(A_{k,t})
with A0=D, A1=G, A2=Q, A3=R.

The default figure uses one central seed bit, width 321, 140 rows and fixed
zero exterior. The light cone stays away from the boundary.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def step_line(state: np.ndarray, rule: int) -> np.ndarray:
    state = np.asarray(state, dtype=np.uint8)
    left = np.concatenate(([0], state[:-1]))
    right = np.concatenate((state[1:], [0]))
    idx = (left << 2) | (state << 1) | right
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    return lut[idx]


def generate(rule: int, width: int = 321, steps: int = 140):
    source = np.zeros(width, dtype=np.uint8)
    source[width // 2] = 1

    s = [source]
    for _ in range(steps + 5):
        s.append(step_line(s[-1], rule))

    levels = [[s[t] ^ s[t + 1] for t in range(len(s) - 1)]]
    for _ in range(3):
        prev = levels[-1]
        levels.append([
            prev[t + 1] ^ step_line(prev[t], rule)
            for t in range(len(prev) - 1)
        ])

    return {
        "S": np.stack(s[:steps]),
        "D": np.stack(levels[0][:steps]),
        "G": np.stack(levels[1][:steps]),
        "Q": np.stack(levels[2][:steps]),
        "R": np.stack(levels[3][:steps]),
    }


def render(rule: int, output_dir: Path):
    fields = generate(rule)
    output_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output_dir / f"rule{rule}_SDGQR_fields.npz", **fields)

    # One independent plot per field; compose externally if desired.
    for label in ("S", "D", "G", "Q", "R"):
        fig = plt.figure(figsize=(5, 3.2), dpi=180)
        ax = fig.add_axes([0.02, 0.02, 0.96, 0.90])
        ax.imshow(fields[label], aspect="auto", interpolation="nearest")
        ax.set_title(f"Rule {rule}: {label}")
        ax.set_xticks([])
        ax.set_yticks([])
        fig.savefig(
            output_dir / f"rule{rule}_{label}.png",
            bbox_inches="tight",
            pad_inches=0.03,
        )
        plt.close(fig)


def main():
    out = Path("results/commutator_jet_20261007")
    for rule in (110, 62):
        render(rule, out)


if __name__ == "__main__":
    main()
