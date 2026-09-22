"""Fast regression tests for the Groovy-field closure decider and certificates."""
import sys
from pathlib import Path
import pytest

import numpy as np
sys.path[:0] = [str(Path(__file__).resolve().parents[1] / p) for p in ("src", "scripts")]
from groovy.groovy_field import (decide, witness, verify_witness,  # noqa: E402
                                 certify_law, ring_collision)


def verdict(rule, tracks, k, t=0):
    v = decide(rule, tracks, k, t)
    if v.status == "counterexample":
        assert verify_witness(rule, tracks, k, t, witness(v))["verified"]
    elif v.status == "law":
        assert certify_law(rule, tracks, k, t, r_max=8)["status"] == "certified"
    return v.status


@pytest.mark.parametrize("rule,tracks,k,t,expected", [
    (32, (), 1, 0, "law"),            # G_32 E_32 = E_128 G_32 (known)
    (90, (), 1, 0, "law"),            # G_90 = 0
    (110, (), 1, 0, "counterexample"),  # PR #293
    (110, (), 3, 0, "counterexample"),  # line-only memory-3 failure
    (110, (), 2, 1, "counterexample"),  # burn-in does not rescue memory 2
    (110, (128,), 1, 0, "counterexample"),
    (110, (128,), 2, 0, "law"),       # G + run-of-three-ones marker
    (110, (1,), 3, 0, "counterexample"),  # run-of-zeros marker misses phase
    (110, (204,), 1, 0, "law"),       # retaining the source always closes
    (30, (), 3, 0, "law"),            # Rule 30's G is third-order autonomous
    (145, (), 3, 0, "law"),           # output complement of 110 closes
    (110, (90,), 3, 0, "law"),        # l xor r repairs 110 at memory 3
    (54, (57,), 3, 0, "law"),         # lossy nonlinear universal track
])
def test_known_verdicts(rule, tracks, k, t, expected):
    assert verdict(rule, tracks, k, t) == expected


def test_rule54_is_fifth_order_by_decider():
    assert decide(54, (), 4, 0).status == "counterexample"
    assert decide(54, (), 5, 0).status == "law"


def test_memory3_110_has_no_collision_on_rings_up_to_10():
    # The all-ring SCC proof is replayed by verify_groovy_field_audit.py.
    assert not any(ring_collision(110, (), 3, 0, n) for n in range(1, 11))


def test_ring_collision_implies_decider_counterexample():
    for rule in (18, 54, 110, 150, 106):
        for k in (1, 2):
            if any(ring_collision(rule, (), k, 0, n) for n in range(1, 8)):
                assert decide(rule, (), k, 0).status == "counterexample"


def test_periodic_seams_are_part_of_the_certificate():
    # This crop has equal G on its complete interior, but extending the
    # declared constant tails makes G differ at coordinates 6 and 7.
    w = {"S": "0101001", "S_prime": "0000110", "left_period": 1,
         "right_period": 1, "tail_reps": 4, "defect_cell": 3}
    result = verify_witness(10, (), 1, 0, w)
    assert not result["history_equal_on_full_line"]
    assert not result["verified"]


@pytest.mark.parametrize("change", [
    {"S": "0201001", "S_prime": "1200011"},
    {"S_prime": "0"}, {"S": ""}, {"left_period": 999},
    {"right_period": 0}, {"left_period": True}, {"right_period": 1.5},
    {"tail_reps": -7}, {"defect_cell": 1000000}, {"defect_cell": -1},
])
def test_malformed_witnesses_are_rejected(change):
    w = {"S": "0101001", "S_prime": "0000110", "left_period": 1,
         "right_period": 1, "tail_reps": 4, "defect_cell": 3, **change}
    assert not verify_witness(10, (), 1, 0, w)["verified"]


def test_missing_extension_metadata_is_rejected():
    assert not verify_witness(2, (), 1, 0, {"S": "0010001", "S_prime": "1010011"})["verified"]


def test_declared_defect_must_actually_differ():
    w = witness(decide(110, (), 1, 0))
    assert verify_witness(110, (), 1, 0, w)["verified"]
    w["defect_cell"] = 0  # deep in the common-observation periodic tail
    result = verify_witness(110, (), 1, 0, w)
    assert result["history_equal_on_full_line"]
    assert not result["declared_defect_differs"]
    assert not result["verified"]


def test_future_records_retain_witnesses_and_budget_status(monkeypatch):
    import groovy_field_suite as suite
    rec = suite.entry(suite.certified(110, (), 1, 0))
    assert verify_witness(rec["rule"], rec["tracks"], rec["k"], rec["t"], rec["witness"])["verified"]
    assert rec["verification"]["history_equal_on_full_line"]
    monkeypatch.setattr(suite, "certify_law", lambda *a, **kw:
                        {"status": "unverified_radius_budget", "radius_tried_up_to": 0})
    rec = suite.entry(suite.certified(32, (), 1, 0))
    assert rec["verdict"] == "?" and rec["status"] == "law"
    assert rec["certificate"]["status"] == "unverified_radius_budget"


def test_output_guard_preserves_existing_bytes(tmp_path):
    from groovy_field_suite import output_path, write_record
    path = tmp_path / "census.json"
    path.write_text("preserved\n")
    with pytest.raises(FileExistsError):
        output_path(tmp_path, "census.json")
    with pytest.raises(FileExistsError):
        write_record(path, {"replacement": True})
    assert path.read_text() == "preserved\n"


def test_valid_history_dynamics_do_not_define_native_g_off_image():
    from verify_groovy_field_audit import boundary_examples
    boundaries = boundary_examples()
    a, b = boundaries["complement_split"]
    assert a["gradient"] == b["gradient"] and a["G"] != b["G"]
    assert boundaries["native_G_boundary"]["D_B_Z"] == ["000", "000", "010", "111"]
    assert boundaries["native_G_boundary"]["B_D_B_Z_undefined"]
