"""Read one preserved rule; construct its native physical index on first use."""
import argparse
import base64
import json
from pathlib import Path
import tarfile

import numpy as np

import sequential_lift_6d_pilot as core
from uniform_jet6_cache import NativeLaw, PhysicalKeys, frozen, unpacked


class CachedRule:
    def __init__(self, record):
        assert record["format"] == "grid-referenced-physical-partial-rule-v1"
        self.record = record
        self.grid = frozen(unpacked(record["grid_bits_big"], record["grid_shape"]))
        self.k = record["forced_root_count"]
        raw = base64.b64decode(record["representative_flat_indices_u32le"], validate=True)
        assert len(raw) == 4*self.k
        self.representatives = np.frombuffer(raw, dtype="<u4")
        assert len(set(self.representatives.tolist())) == self.k
        assert int(self.representatives.max()) < self.grid.size
        self.derivative = unpacked(record["forced_derivative_bits_big"], (self.k,))
        self.decoder = unpacked(record["forced_decoder_bits_big"], (self.k,))
        self._law = None

    @property
    def law(self):
        if self._law is None:
            keyer = PhysicalKeys(tuple(self.record["radii_array_order"]))
            keys = keyer.keys(self.grid)
            ids = keys.ravel()[self.representatives]
            assert len(np.unique(ids)) == self.k
            assert np.array_equal(np.unique(keys), np.sort(ids)), "Representatives must cover the exact physical domain"
            derivative = np.zeros(int(keys.max())+1, dtype=np.uint8)
            decoder = np.zeros_like(derivative)
            derivative[ids], decoder[ids] = self.derivative, self.decoder
            self._law = NativeLaw(keyer, derivative, decoder)
        return self._law

    def step(self, grid):
        """Native phase-free local rule, with identity/no-flip off forced domain."""
        return self.law.step_grid(grid)

    def decoder_grid(self, grid):
        return core.lookup(self.law.decoder, self.law.keyer.keys(grid))

    def recover(self, grid):
        decoded = self.decoder_grid(grid)
        parent = decoded[:, 0]
        assert np.array_equal(decoded, np.broadcast_to(parent[:, None], decoded.shape))
        return parent


def read_member(archive_path, name):
    """Stream to the requested member without constructing other rules."""
    with tarfile.open(archive_path, "r|gz") as archive:
        for member in archive:
            if member.name == name:
                assert member.isfile()
                return CachedRule(json.loads(archive.extractfile(member).read()))
    raise KeyError(name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("member", help="For example w7/rule110/d4.json")
    args = parser.parse_args()
    cache = read_member(args.archive, args.member)
    print(json.dumps({"rule": cache.record["rule"], "dimension": cache.record["dimension"],
                      "width": cache.record["width"], "forced_keys": cache.k,
                      "grid_shape": list(cache.grid.shape), "native_index_built": cache._law is not None}))
