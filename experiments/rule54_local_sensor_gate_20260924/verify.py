"""Independent scalar Rule-54 sensors and exact local-action replay."""

from collections import defaultdict
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
N = 34


def evolve(x):
    y = 0
    for i in range(N):
        a = (x >> ((i - 1) % N)) & 1
        b = (x >> i) & 1
        c = (x >> ((i + 1) % N)) & 1
        y |= ((54 >> (4*a + 2*b + c)) & 1) << i
    return y


def local_word(x, i):
    return sum(((x >> ((i + j - 2) % N)) & 1) << j for j in range(5))


def local_g_formula(word):
    # Independent local causal cone, with offsets -2..2.
    s = [(word >> k) & 1 for k in range(5)]
    def rule(a, b, c):
        return (54 >> (4*a + 2*b + c)) & 1
    e = [rule(s[k-1], s[k], s[k+1]) for k in range(1, 4)]
    ee = rule(*e)
    d = [s[k] ^ e[k-1] for k in range(1, 4)]
    ed = rule(*d)
    return e[1] ^ ee ^ ed


def action(state, kind, flag, lookup):
    e = evolve(state)
    d = state ^ e
    g = e ^ evolve(e) ^ evolve(d)
    fired = []
    for i in range(N):
        if kind == "raw":
            yes = local_word(state, i) == flag
        elif kind == "compiled_g":
            yes = lookup[local_word(state, i)] == flag
        else:
            yes = (({"e": e, "d": d, "g": g}[kind] >> i) & 1) == flag
        if yes:
            fired.append(i)
    return fired[0] if len(fired) == 1 else -1


def stats(rows, kind, flag, lookup):
    successes = unique = rescues = harms = 0
    rescue_witness = harm_witness = None
    for row in rows:
        chosen = -1 if kind == "none" else action(row["at_decision"], kind, flag, lookup)
        wins = row["winning_actions"]
        now, passive = chosen in wins, -1 in wins
        successes += now
        unique += chosen != -1
        if now and not passive:
            rescues += 1
            rescue_witness = rescue_witness or [row["rotation"], row["injury"], chosen]
        if passive and not now:
            harms += 1
            harm_witness = harm_witness or [row["rotation"], row["injury"], chosen]
    return {"score": successes, "unique": unique, "rescues": rescues,
            "harms": harms, "rescue_witness": rescue_witness,
            "harm_witness": harm_witness}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text())
    assert result["schema"] == "rule54-local-sensor-gate-v1"
    source_file = ROOT / result["source"]
    assert hashlib.sha256(source_file.read_bytes()).hexdigest() == result["source_sha256"]
    for path, digest in result["source_hashes"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    source = json.loads(source_file.read_text())
    rows = source["trials"]
    assert len(rows) == result["trials"] == N*N
    lookup = [local_g_formula(p) for p in range(32)]
    assert sum(bit << p for p, bit in enumerate(lookup)) == result["g_local_truth_table"]
    for row in rows:
        x = row["at_decision"]
        e = evolve(x)
        g = e ^ evolve(e) ^ evolve(x ^ e)
        assert all(lookup[local_word(x, i)] == ((g >> i) & 1) for i in range(N))
    assert stats(rows, "none", None, lookup) == result["fixed"]
    assert result["full_state_ceiling"] == source["full_state_successes"]
    choices = {"g": range(2), "e": range(2), "d": range(2),
               "raw": range(32), "compiled_g": range(2)}
    for kind, predicates in choices.items():
        saved = result["families"][kind]
        for p in predicates:
            assert stats(rows, kind, p, lookup) == saved["menu"][str(p)]
        candidates = [(None, result["fixed"]), *[(p, saved["menu"][str(p)]) for p in predicates]]
        best = max(candidates, key=lambda t: (t[1]["score"], t[0] is None, -(t[0] or 0)))
        assert saved["best_predicate"] == best[0] and saved["best"] == best[1]
    assert all(result["families"]["g"]["menu"][str(p)] == result["families"]["compiled_g"]["menu"][str(p)] for p in range(2))
    best = lambda kind: result["families"][kind]["best"]["score"]
    assert result["predictions"]["P1_g_exceeds_fixed"] == ("supported" if best("g") > 340 else "failed")
    assert result["predictions"]["P2_cheap_simple_matches_g"] == ("supported" if max(best(k) for k in ("e", "d", "raw")) >= best("g") else "failed")
    assert result["predictions"]["P3_compiled_g_matches"] == "supported"
    print("Independent scalar sensors, local G truth table and all policy outcomes verified")


if __name__ == "__main__":
    main()
