"""Exact seven-bit rule-order certificate. Freeze: research protocol of same date."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from groovy.ca import apply_rule


PREFIXES = (204, 30, 90, 54, 0)
B, C = 54, 110
SOURCE_PATHS = (
    "docs/research/protocols/2026-09-25-order-image-gate.md",
    "experiments/order_image_gate_20260925/run.py",
    "src/groovy/ca.py",
)


def scalar_step(bits: tuple[int, ...], rule: int) -> tuple[int, ...]:
    """Produce an inner word, decreasing length by two, from Wolfram LUT."""
    return tuple((rule >> (4*bits[i-1] + 2*bits[i] + bits[i+1])) & 1
                 for i in range(1, len(bits)-1))


def word(number: int, width: int) -> tuple[int, ...]:
    """Bit zero is the leftmost spatial position."""
    return tuple((number >> i) & 1 for i in range(width))


def value(bits: tuple[int, ...]) -> int:
    return sum(bit << i for i, bit in enumerate(bits))


def scalar_outputs(patch: int, prefix: int) -> tuple[int, int, int]:
    middle = scalar_step(word(patch, 7), prefix)
    first = scalar_step(scalar_step(middle, B), C)[0]
    second = scalar_step(scalar_step(middle, C), B)[0]
    return first, second, value(middle)


def scalar_pair_defect(middle: int) -> int:
    bits = word(middle, 5)
    return scalar_step(scalar_step(bits, B), C)[0] ^ scalar_step(scalar_step(bits, C), B)[0]


def ring_outputs(patch: int, prefix: int, outside: int) -> tuple[int, int]:
    ring = np.full(11, outside, dtype=np.uint8)
    for i, bit in enumerate(word(patch, 7)):
        ring[i+2] = bit
    answers = []
    for second, third in ((B, C), (C, B)):
        evolved = ring.copy()
        for rule in (prefix, second, third):
            evolved = apply_rule(evolved, rule)
        answers.append(int(evolved[5]))
    return tuple(answers)


def bitstring(values: list[int]) -> str:
    """Character at offset p is the value for seven-bit patch p."""
    return ''.join(str(v) for v in values)


def run() -> dict:
    k_table = [scalar_pair_defect(u) for u in range(32)]
    rows = []
    for prefix in PREFIXES:
        left, right, differences = [], [], []
        image = set()
        for patch in range(128):
            first, second, intermediate = scalar_outputs(patch, prefix)
            for exterior in (0, 1):
                if (first, second) != ring_outputs(patch, prefix, exterior):
                    raise AssertionError((patch, prefix, exterior, "independent ring check"))
            if first ^ second != k_table[intermediate]:
                raise AssertionError((patch, prefix, "order image identity"))
            left.append(first)
            right.append(second)
            differences.append(first ^ second)
            image.add(intermediate)
        witness = next((p for p, bit in enumerate(differences) if bit), None)
        rows.append({
            "prefix_rule": prefix,
            "first_schedule": [prefix, B, C],
            "second_schedule": [prefix, C, B],
            "first_output_bits": bitstring(left),
            "second_output_bits": bitstring(right),
            "difference_bits": bitstring(differences),
            "difference_patch_count": sum(differences),
            "image_middle5_words": sorted(image),
            "positive_k_middle5_words_in_image": sorted(u for u in image if k_table[u]),
            "first_witness": None if witness is None else {
                "patch_number": witness,
                "bits_left_to_right": ''.join(map(str, word(witness, 7))),
                "first_center_bit": left[witness],
                "second_center_bit": right[witness],
                "intermediate_middle5_word": scalar_outputs(witness, prefix)[2],
            },
        })
    root = Path(__file__).resolve().parents[2]
    return {
        "scope": "all binary configurations on the full 1D line; exact radius-three local maps",
        "encoding": "character at index p in each 128-bit string is center output for patch p, bit 0 leftmost",
        "protocol": SOURCE_PATHS[0],
        "source_hashes": {path: hashlib.sha256((root / path).read_bytes()).hexdigest()
                          for path in SOURCE_PATHS},
        "pair_defect_middle5_bits": bitstring(k_table),
        "pair_defect_positive_middle5_words": [u for u, bit in enumerate(k_table) if bit],
        "rows": rows,
        "verification": "scalar shrink LUT versus vectorized 11-ring with exterior 0 and 1, all patches/outputs",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(), indent=2) + "\n")
