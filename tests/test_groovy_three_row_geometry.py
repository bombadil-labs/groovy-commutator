"""Certificate semantics and the single-trajectory equivariance obstruction."""
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from groovy_three_row_geometry import RECORD, verify_certificate  # noqa: E402


def certificate():
    return json.loads(RECORD.read_text())["search"]["certificate"]


def test_scalar_replay_proves_full_plane_collision():
    assert verify_certificate(certificate())["verified"]


def test_one_trajectory_has_false_period_three_return():
    cert = certificate()
    first, second = cert["examples"]
    s = tuple(map(int, first["source"]))
    evolved = "".join(str(s[(i - 1) % len(s)] ^ (s[i] | s[(i + 1) % len(s)]))
                      for i in range(len(s)))
    assert evolved == second["source"]
    assert first["g_rows"][1:] == second["g_rows"][:3]
    a, b, c, a_again = first["g_rows"]
    b_prime = second["g_rows"][3]
    assert a == a_again
    assert b != b_prime
    # L(ES)=R L(S), but L(E^2 S) != R L(ES).
    assert [b, c, a] == second["g_rows"][:3]
    assert [c, a, b] != second["g_rows"][1:]


@pytest.mark.parametrize("mutation", ["phase", "row", "defect", "target"])
def test_certificate_corruption_is_rejected(mutation):
    cert = deepcopy(certificate())
    if mutation == "phase":
        cert["examples"][0]["phase"] = 0
    elif mutation == "row":
        cert["examples"][0]["g_rows"][0] = "0" * cert["horizontal_period"]
    elif mutation == "defect":
        cert["defect_xy"] = [0, 0]
    elif mutation == "target":
        cert["output_rows"][1] = cert["output_rows"][0][:]
    with pytest.raises(ValueError):
        verify_certificate(cert)
