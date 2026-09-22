"""Physical geometry, exact marker certificate, and explicit completion checks."""
from copy import deepcopy
import json
from pathlib import Path
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
from groovy.separator_lift import history_table, step  # noqa: E402
from groovy_four_row_separator import verify_graph  # noqa: E402
from groovy_three_row_geometry import scalar_rows  # noqa: E402


@pytest.fixture(scope="module")
def table():
    return history_table()


@pytest.mark.parametrize("source", ["00010011110", "00111110001", "00000000000"])
@pytest.mark.parametrize("phase", range(4))
def test_actual_plane_advance_in_every_vertical_phase(source, phase, table):
    rows = scalar_rows(source)
    before = np.array([list(map(int, row)) for row in rows[:3] + ["1" * len(source)]])
    after = np.array([list(map(int, row)) for row in rows[1:] + ["1" * len(source)]])
    # Includes a horizontal translation and the period-11 former obstruction.
    before = np.roll(before, shift=(-phase, 2), axis=(0, 1))
    after = np.roll(after, shift=(-phase, 2), axis=(0, 1))
    assert np.array_equal(step(before, table), after)


def test_explicit_ambient_completion_is_total(table):
    assert not step(np.zeros((4, 11), dtype=np.uint8), table).any()
    # All four rows resemble markers, so this invalid neighborhood outputs zero.
    assert not step(np.ones((4, 11), dtype=np.uint8), table).any()
    with pytest.raises(ValueError):
        step(np.full((4, 11), 2), table)


def test_rank_certificate_cannot_hide_a_longer_run():
    record = json.loads((ROOT / "results/groovy_four_row_separator_20260922.json").read_text())
    assert verify_graph(record["image_graph"])
    damaged = deepcopy(record["image_graph"])
    ones = next(item for item in damaged["output_subgraphs"] if item["bit"] == 1)
    ones["rank"][1] = 0
    with pytest.raises(AssertionError):
        verify_graph(damaged)
