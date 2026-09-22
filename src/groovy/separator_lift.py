"""A binary 2D realization of Rule 30's ordered three-G-history law.

Valid planes repeat (G_0, G_1, G_2, 1) vertically, including every phase.
The local stencil is x=-6..6, y=-2..1. Four consecutive ones identify the
separator because no Rule-30 G field contains 1111. Invalid marker patterns
and unknown history keys produce zero, making the ambient rule total.

The marked history table is generated once from its complete 21-bit source
cone. This setup cost and its sparse table storage are not free computation.
"""
from __future__ import annotations

from functools import lru_cache
import hashlib

import numpy as np

from .groovy_field import g_word, shrink

SOURCE_BITS = 21
WIDTH = 13
MASK = np.uint64((1 << WIDTH) - 1)


def source_history_words(source):
    """Packed 13-cell G_0..G_2 windows and center G_0..G_3 outputs."""
    rows, centers = [], []
    n, current = SOURCE_BITS, source
    for j in range(4):
        g = g_word(current, n, 30)
        width = n - 4
        centers.append(((g >> np.uint64(width // 2)) & 1).astype(np.uint8))
        if j < 3:
            rows.append((g >> np.uint64((width - WIDTH) // 2)) & MASK)
            current = shrink(current, n, 30)
            n -= 2
    return rows, centers


def pack_rows(rows):
    key = np.zeros_like(rows[0], dtype=np.uint64)
    for row in rows:
        key = (key << np.uint64(WIDTH)) | row
    return key


def sorted_table(keys, values):
    """Return forced rows, or original indices of an output conflict."""
    order = np.argsort(keys, kind="stable")
    k, v = keys[order], values[order]
    same = k[1:] == k[:-1]
    conflicts = np.flatnonzero(same & (v[1:] != v[:-1]))
    if len(conflicts):
        i = conflicts[0]
        return None, None, [int(order[i]), int(order[i + 1])]
    first = np.r_[True, ~same]
    return k[first], v[first], None


def table_digest(keys, values):
    return hashlib.sha256(keys.astype("<u8").tobytes() + values.astype(np.uint8).tobytes()).hexdigest()


@lru_cache(maxsize=1)
def history_table():
    source = np.arange(1 << SOURCE_BITS, dtype=np.uint64)
    rows, centers = source_history_words(source)
    keys, values, conflict = sorted_table(pack_rows(rows), centers[3])
    if conflict is not None:
        raise ValueError(f"marked history-law conflict: {conflict}")
    keys.flags.writeable = False
    values.flags.writeable = False
    return keys, values


def marker_roles(rows):
    """Detect 1111 at x=-1..2 in each of the four vertical rows."""
    flags = np.stack([((row >> np.uint64(4)) & np.uint64(15)) == 15 for row in rows])
    unique = flags.sum(axis=0) == 1
    # Array row j has y-offset j-2; the separator's phase is 3.
    roles = (5 - flags.argmax(axis=0)) % 4
    return roles, unique


def local_step(rows, table=None):
    """Total uniform rule on batches of four packed 13-bit neighborhood rows.

    rows are ordered by y=-2,-1,0,+1; bit 12 is x=-6, bit 0 is x=+6.
    No temporal role is provided by the caller. The return is one output bit
    for each batch entry; history-table lookup uses a default-zero completion.
    """
    if len(rows) != 4 or any(np.asarray(r).shape != np.asarray(rows[0]).shape for r in rows):
        raise ValueError("four equally shaped neighborhood rows are required")
    rows = [np.asarray(row, dtype=np.uint64) for row in rows]
    if any(np.any(row > MASK) for row in rows):
        raise ValueError("neighborhood rows must contain exactly 13 binary positions")
    keys, values = history_table() if table is None else table
    role, unique = marker_roles(rows)
    out = np.zeros_like(rows[0], dtype=np.uint8)
    copy = unique & (role < 2)
    out[copy] = ((rows[3][copy] >> np.uint64(6)) & 1).astype(np.uint8)
    out[unique & (role == 3)] = 1
    newest = np.flatnonzero(unique & (role == 2))
    if len(newest):
        lookup = pack_rows([row[newest] for row in rows[:3]])
        index = np.searchsorted(keys, lookup)
        safe = np.minimum(index, len(keys) - 1)
        present = (index < len(keys)) & (keys[safe] == lookup)
        out[newest[present]] = values[safe[present]]
    return out


def step(plane, table=None):
    """Apply the same binary rule everywhere on a periodic finite 2D plane."""
    plane = np.asarray(plane)
    if plane.ndim != 2 or 0 in plane.shape or np.any((plane != 0) & (plane != 1)):
        raise ValueError("a nonempty 2D binary plane is required")
    table = history_table() if table is None else table
    packed = []
    for dy in (-2, -1, 0, 1):
        row = np.zeros(plane.shape, dtype=np.uint64)
        for dx in range(-6, 7):
            bit = np.roll(plane, shift=(-dy, -dx), axis=(0, 1))
            row = (row << np.uint64(1)) | bit.astype(np.uint64)
        packed.append(row.ravel())
    return local_step(packed, table).reshape(plane.shape)
