from pathlib import Path

path = Path('scripts/verify_predictive_assembly_support.py')
text = path.read_text()

old = '''def independent_raw_certificate(classes: Sequence[TupleClass], optimum: int, n_atoms: int) -> dict:
    k = optimum.bit_count()
    below = reference_exists_at_most(classes, k - 1, n_atoms) if k else None
    if below is not None:
        raise AssertionError(("reference found smaller support", support_tuple(below), k))
    at = reference_exists_at_most(classes, k, n_atoms)
    if at is None:
        raise AssertionError("reference solver failed to find support at primary optimum")
    return {
        "no_support_at_most_k_minus_1": True,
        "support_at_k_found": list(support_tuple(at)),
        "reference_optimum": k,
    }
'''

new = '''def target_count_lower_bound(classes: Sequence[TupleClass]) -> tuple[int, int]:
    """Independent information lower bound from the tuple decision table.

    A support of s binary atoms has at most 2**s projected keys. Prediction
    sufficiency forbids two distinct target classes from sharing a projected key,
    so s >= ceil(log2(number of target classes)). This uses only the explicit
    tuple table, not the packed cutting-plane constraint family.
    """
    target_count = len({row.target for row in classes})
    lower = 0 if target_count <= 1 else (target_count - 1).bit_length()
    return lower, target_count


def tuple_difference_mask(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    out = 0
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            out |= 1 << i
    return out


def disjoint_witness_packing(classes: Sequence[TupleClass], optimum: int) -> tuple[int, ...] | None:
    """Try to certify |optimum| by pairwise-disjoint cross-target differences.

    Minimality of a sufficient support S implies that, for each atom i in S,
    removing i exposes at least one cross-target collision. We enumerate the
    exact tuple-table collisions under S\\{i}; every resulting difference meets
    S exactly in i. A backtracking matching then asks for one witness per support
    atom whose full difference sets are pairwise disjoint. If found, these k
    actual decision-table differences are a machine-checkable lower bound k for
    every hitting set. Failure to find such a packing is not treated as evidence;
    the canonical evaluation stops without a result instead of falling back to
    the previously unbounded iterative-deepening search.
    """
    support_atoms = support_tuple(optimum)
    if not support_atoms:
        return ()
    support_mask = optimum
    candidates: dict[int, tuple[int, ...]] = {}
    for atom in support_atoms:
        selected = tuple(i for i in support_atoms if i != atom)
        groups: dict[tuple[int, ...], list[TupleClass]] = {}
        for row in classes:
            proj = tuple(row.key[i] for i in selected)
            groups.setdefault(proj, []).append(row)
        diffs: set[int] = set()
        bit = 1 << atom
        for rows in groups.values():
            if len(rows) < 2:
                continue
            for i, left in enumerate(rows):
                for right in rows[i + 1:]:
                    if left.target == right.target:
                        continue
                    diff = tuple_difference_mask(left.key, right.key)
                    if not (diff & bit):
                        raise AssertionError("full optimum would conflict after removing one atom")
                    if diff & (support_mask ^ bit):
                        raise AssertionError("projection group disagrees on another optimum atom")
                    diffs.add(diff)
        minimal = minimize_constraints(diffs)
        if not minimal:
            raise AssertionError(("minimum support atom has no tuple-table necessity witness", atom))
        candidates[atom] = minimal

    order = sorted(support_atoms, key=lambda atom: (len(candidates[atom]), atom))

    def rec(pos: int, used: int, chosen: tuple[int, ...]) -> tuple[int, ...] | None:
        if pos == len(order):
            return chosen
        atom = order[pos]
        for diff in candidates[atom]:
            if diff & used:
                continue
            found = rec(pos + 1, used | diff, (*chosen, diff))
            if found is not None:
                return found
        return None

    packed = rec(0, 0, ())
    if packed is None:
        return None
    if len(packed) != len(support_atoms):
        raise AssertionError("disjoint witness packing cardinality mismatch")
    used = 0
    for diff in packed:
        if not diff or (diff & used):
            raise AssertionError("invalid disjoint witness packing")
        used |= diff
    return packed


def independent_raw_certificate(classes: Sequence[TupleClass], optimum: int, n_atoms: int) -> dict:
    """Machine-check an exact lower bound without exponential tuple DFS."""
    del n_atoms
    k = optimum.bit_count()
    lower, target_count = target_count_lower_bound(classes)
    if lower == k:
        return {
            "method": "target_class_count_binary_projection_bound",
            "target_class_count": target_count,
            "lower_bound": lower,
            "reference_optimum": k,
        }
    if lower > k:
        raise AssertionError(("independent counting lower bound exceeds primary optimum", lower, k))

    packing = disjoint_witness_packing(classes, optimum)
    if packing is not None and len(packing) == k:
        return {
            "method": "pairwise_disjoint_difference_witness_packing",
            "target_class_count": target_count,
            "counting_lower_bound": lower,
            "lower_bound": len(packing),
            "difference_witness_masks": list(packing),
            "reference_optimum": k,
        }
    raise RuntimeError(
        f"independent exact lower-bound certificate did not reach primary optimum k={k}; "
        f"target-count bound={lower}, disjoint packing="
        f"{None if packing is None else len(packing)}. No canonical result written."
    )
'''
if text.count(old) != 1:
    raise SystemExit(f'expected one independent_raw_certificate preimage, found {text.count(old)}')
text = text.replace(old, new)

old_param = '"independent_certificate": "direct decision-table iterative-deepening search",'
new_param = '"independent_certificate": "machine-checked tuple-table lower bound: target-class count, with disjoint-difference packing fallback",'
if text.count(old_param) != 1:
    raise SystemExit('independent_certificate parameter preimage mismatch')
text = text.replace(old_param, new_param)

old_self = '''    cert = independent_raw_certificate(tuples, optimum, 4)
    assert cert["reference_optimum"] == 2
    assert constraints

    accepted = json.loads(PREV_RESULT.read_text())
'''
new_self = '''    cert = independent_raw_certificate(tuples, optimum, 4)
    assert cert["reference_optimum"] == 2
    assert cert["method"] == "target_class_count_binary_projection_bound"
    assert constraints

    parity_packed = tuple(PackedClass(key, (key & 1) ^ ((key >> 1) & 1), key) for key in range(4))
    parity_optimum, _ = cutting_plane_optimum(parity_packed)
    assert parity_optimum.bit_count() == 2
    parity_tuples = tuple(
        TupleClass(tuple((key >> i) & 1 for i in range(2)), (row.target,), key)
        for key, row in enumerate(parity_packed)
    )
    parity_cert = independent_raw_certificate(parity_tuples, parity_optimum, 2)
    assert parity_cert["reference_optimum"] == 2
    assert parity_cert["method"] == "pairwise_disjoint_difference_witness_packing"
    assert len(parity_cert["difference_witness_masks"]) == 2

    accepted = json.loads(PREV_RESULT.read_text())
'''
if text.count(old_self) != 1:
    raise SystemExit('self-test preimage mismatch')
text = text.replace(old_self, new_self)
path.write_text(text)
