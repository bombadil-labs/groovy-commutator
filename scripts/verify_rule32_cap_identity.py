#!/usr/bin/env python3
"""Post-census compact-cap audit, not a preregistered candidate selection.

Rule32 was selected after inspecting nonconstant depth-one caps. This file
checks the proposed identity using direct seven-bit shrinking windows.
It does not execute the subsequently frozen physical/edit experiment.
"""
import hashlib
import itertools
import json


def f(row):
    return tuple(l & (1-c) & r for l, c, r in zip(row, row[1:], row[2:]))


def a(j, row):
    if j == 0:
        return row[1] ^ f(row)[0]
    left = a(j-1, f(row))
    right = f(tuple(a(j-1, row[i:i+len(row)-2]) for i in range(3)))[0]
    return left ^ right


def audit():
    realized, outputs = set(), []
    for row in itertools.product((0, 1), repeat=7):
        top = tuple(a(1, row[i:i+5]) for i in range(3))
        cap = top[0] & top[2]
        assert a(2, row) == cap
        assert a(1, f(row)) == (top[0] & top[1] & top[2])
        assert (f(top)[0] ^ cap) == (top[0] & top[1] & top[2])
        realized.add(sum(bit << (2-i) for i, bit in enumerate(top)))
        outputs.append(cap)
    assert set(outputs) == {0, 1}
    return {"selection": "post-census, compact nonconstant spatial cap",
            "rule": 32, "h": 1, "R": 1, "source_windows": 128,
            "identity_assertions": 384,
            "cap": "A_2(S)[x] = A_1(S)[x-1] AND A_1(S)[x+1]",
            "top_update": "A_1(F_32(S)) = F_128(A_1(S))",
            "eca_cap": 160, "top_eca": 128,
            "realized_top_neighborhoods": sorted(realized),
            "cap_outputs_sha256": hashlib.sha256(bytes(outputs)).hexdigest(),
            "physical_edit_experiment_executed": False}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
