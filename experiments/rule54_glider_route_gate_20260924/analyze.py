"""Post-evaluation diagnostic: when do the rescued trials rejoin the clean route?"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

import verify  # Independent scalar Rule-54 truth-table implementation.


def analyze(result: Path) -> dict:
    record = json.loads(result.read_text(encoding="utf-8"))
    clean_by_time = [
        {verify.shifted(state, shift) for shift in range(verify.N)}
        for state in record["clean_route"]
    ]
    first_rejoin = Counter()
    relative_injury_sites = Counter()
    same_address = 0
    rescued = 0
    known_injury_site_successes = sum(
        trial["injury"] in trial["winning_actions"] for trial in record["trials"]
    )
    for trial in record["trials"]:
        actions = trial["winning_actions"]
        if -1 in actions or not actions:
            continue
        rescued += 1
        relative_injury_sites[str((trial["injury"] - trial["rotation"]) % verify.N)] += 1
        assert len(actions) == 1, "multiple winning actions need separate reporting"
        site = actions[0]
        same_address += site == trial["injury"]
        before = trial["at_decision"]
        after = list(verify.decode(verify.evolve(before)))
        after[site] = verify.decode(before)[site]
        state = verify.encode("".join(after))
        first = 3 if state in clean_by_time[3] else None
        for tick in range(4, 9):
            state = verify.evolve(state)
            if first is None and state in clean_by_time[tick]:
                first = tick
        first_rejoin[str(first)] += 1
    assert rescued == record["rescued_from_passive_failure"]
    return {
        "schema": "rule54-glider-route-posthoc-v1",
        "status": "post_evaluation_diagnostic_not_frozen_prediction",
        "canonical_result_sha256": hashlib.sha256(result.read_bytes()).hexdigest(),
        "rescued_trials": rescued,
        "winning_hold_at_original_injury_site": same_address,
        "hold_known_injury_site_successes": known_injury_site_successes,
        "known_injury_site_is_exogenous_oracle": True,
        "first_clean_route_rejoin_time": dict(sorted(first_rejoin.items())),
        "rescued_relative_injury_sites": dict(sorted(relative_injury_sites.items())),
    }


if __name__ == "__main__":
    source, target = map(Path, sys.argv[1:3])
    report = analyze(source)
    with target.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(report, sort_keys=True))
