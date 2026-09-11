#!/usr/bin/env python3
"""One-shot reporting integration for the completed intervention-axis unit.

This script only updates prose/catalog metadata after the canonical result is
already fixed. It is removed after its one execution; its commit remains in
history as reporting provenance.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "docs/research/2026-09-09-dimensional-closure-program.md"
CHECKPOINT = ROOT / "docs/research/checkpoints/dimensional-lift.md"
PROGRAM_JSON = ROOT / "site/content/research-program.json"
KNOWLEDGE_JSON = ROOT / "site/content/knowledge.json"

RESULT22 = """22. **Finite width packs, while independent unbounded width defeats a fixed capacity budget.** Every fixed finite strip is sitewise column-packable into a one-dimensional product alphabet; for fixed target alphabet size `q` and longitudinal expansion `K`, an unconstrained strip family eventually violates `|A|^(wn) <= q^(Kn)`. The inherited Rule32 correction tower is analytically source-bounded by one bit of independent-state capacity per longitudinal site. In the bounded `n=6..12`, `h=0..4` diagnostic, its K/O and H128/H160 whole-field partitions are already saturated at `h=0`: deeper correction rows add no new whole-field distinctions on those tested finite families. This supplies a necessary anti-packing resource test, not a definition of spatial dimension.
"""
RESULT23 = """
23. **Separated transverse channels have unbounded constant-support intervention rank under the declared representation.** In the established Rule90 strip family, `m` separated channels provide `m` independent logical-bit actions of physical support two, preserved by the same fixed 2D law; copied width instead needs a `2m`-cell edit to remain in its copied subfamily at edit time. Even after a one-dimensional target is allowed arbitrarily much total storage, preserving all `2^m` endpoints of the source actions inside one fixed `K+2R`-site target window over alphabet size `q` requires `2^m <= q^(K+2R)`, so some local addressability resource must grow with `m`. The bounded `m=1..6`, rings 5/7 replay and touching-strip 17/64 control pass exactly. This is transverse intervention independence as an operational axis witness, not an intrinsic-dimension theorem.
"""
OLD_OPEN = """- The relationship between correction depth, spatial dimension, growing spatial radius and minimum causal representation dimension is not yet characterized. The completed second-lift comparison keeps the lattice one-dimensional while growing a product alphabet, and the transverse-freedom unit now shows that every fixed finite width column-packs and that the tested Rule32 correction tuples add no whole-field distinctions after `h=0` through depth four. A genuinely new spatial axis still needs a stronger uniform resource, topology, intervention, or symmetry criterion; a fixed code's ancestral rank may primarily reflect its layout.
"""
NEW_OPEN = """- The relationship between correction depth, spatial dimension, growing spatial radius and minimum causal representation dimension is not yet characterized. The completed second-lift comparison keeps the lattice one-dimensional while growing a product alphabet; finite-width packing separates nominal rows from independent state capacity; and the intervention-axis unit now adds a stronger operational witness: an unbounded translated family of constant-support, dynamically preserved interventions that cannot fit into one fixed one-dimensional endpoint window even when total target storage is unlimited. This still does not define intrinsic dimension: the common-window/action contract is representation-relative, non-spatial systems can realize similar resources, and a fixed code's ancestral rank may primarily reflect its layout.
"""
PROGRAM_APPEND = """

## Completed execution: uniform local intervention axis

The [frozen protocol](protocols/intervention-axis-20260911.md) and [result note](2026-09-11-intervention-axis.md) continue the transverse-freedom question from whole-state capacity to local action structure. The physical witness is the already-established family of aligned Rule90 strips separated by one background row under one fixed binary 2D law. For every finite channel count `m`, translated logical-bit flips give `m` commuting, image-preserving generators of support two and the accepted many-strip theorem preserves their independent Rule90 dynamics. Thus native local intervention rank is at least `m` at constant physical support.

The copied-width control uses the same layout but forces every strip to carry the same logical row. At edit time a nontrivial source-bit flip remains in that subfamily only if every channel is toggled, for support exactly `2m`; proper nonempty subsets leave the representation. The bounded verifier checks `m=1..6`, rings 5 and 7, zero/one/fixed-seeded bases, every action subset and two coarse updates. Every separated endpoint is valid and distinct, every generator has disjoint two-cell support, physical evolution matches independent literal Rule90, and every copied-width support/count control passes. The independently rebuilt touching-strip control reproduces 17/64 valid and 47/64 invalid local inputs, retaining the established `100/100` witness, so instantaneous addressability alone is not mistaken for dynamical closure.

The Gate-1 clarification makes the one-dimensional comparison genuinely distinct from the previous total-capacity theorem. The target may use arbitrarily many total sites as `m` grows. Only a common local endpoint window is fixed: alphabet size `q`, anchored core `K`, halo `R`. All `2^m` source action subsets at one logical coordinate must differ from the target base only inside those `K+2R` sites, so injectivity requires `2^m <= q^(K+2R)`. Every fixed finite `(q,K,R)` eventually fails. Therefore the separated strips force a **local intervention/addressability resource** to grow even after total one-dimensional storage is released. This is a useful operational axis witness under the declared representation contract; it is not a sufficient or representation-independent definition of spatial dimension, self-assembly, or endogenous control.
"""

CHECKPOINT_SECTION = """## Checkpoint 2026-09-11: uniform local intervention-axis unit completed; gate-2 pending

Read `docs/research/2026-09-11-intervention-axis.md`. This unit follows the accepted finite-width packing/transverse-freedom result by releasing total target storage and freezing only a common local intervention endpoint window.

- Gate 1: Claude/Fable approved integrated protocol `dc363745` with two binding clarifications before implementation: I3 allows arbitrarily much total 1D target storage while holding the common `(q,K,R)` endpoint window fixed, and copied-family image preservation is evaluated at edit time. Clarifications landed before the verifier; the gathering branch was reconciled with accepted `main`.
- Implementation `c8d6c1a` and permanent replay workflow `7f7eb64` were integrated at `77ae5a5` with no canonical result present. The first primary run then produced canonical result commit `eba1b0c`; integrity registration and one-shot cleanup followed; evaluation merged at `8bffdd5`.
- Analytic/inherited I1: for every finite `m`, the separated Rule90 strip actions witness native local intervention rank at least `m` at physical support budget two. This repackages the accepted many-strip/action theorem; the new finite replay is an implementation control, not its proof.
- Analytic I2: in copied width `D_m`, a nontrivial source-bit flip that stays in the copied family at edit time costs exactly `2m`; proper nonempty subsets of channel flips leave the subfamily. This is representation-relative and instantaneous.
- Analytic I3: even with unlimited total 1D target storage, if all channel-subset actions at one source coordinate must terminate inside one common `K+2R`-site target window over alphabet size `q`, injectivity requires `2^m <= q^(K+2R)`. Every fixed finite local endpoint budget eventually fails.
- Bounded I5 replay: `m=1..6`, rings 5/7, zero/one/fixed-seeded bases, every `2^m` action subset and two coarse updates all pass: exact endpoint counts, two-cell disjoint supports, and independent Rule90 evolution. I2 controls pass throughout.
- I4 control independently reproduces touching-strip `17/64` valid versus `47/64` invalid local inputs and the known `100/100` extra-cell witness. Addressability without autonomous closure is therefore excluded by the rank definition.
- Permanent source-hash and byte-for-byte replay CI is green on the evaluation sub-PR. No frozen choice changed after primary evaluation.
- Do not infer an intrinsic-dimension theorem, representation-independent lower bound, self-assembly, endogenous control, or that non-spatial registers cannot realize similar local action structure. The supplied background/action interface remains a resource.
- **Review state:** reporting is complete on the gathering branch after this reporting integration; external Claude/Fable Gate-2 review of the final exact head remains required before `main`.

"""


def patch_program() -> None:
    s = PROGRAM.read_text()
    if RESULT23.strip() not in s:
        if RESULT22 not in s:
            raise SystemExit("result 22 anchor missing")
        s = s.replace(RESULT22, RESULT22 + RESULT23, 1)
    if NEW_OPEN.strip() not in s:
        if OLD_OPEN not in s:
            raise SystemExit("open-question anchor missing")
        s = s.replace(OLD_OPEN, NEW_OPEN, 1)
    if "## Completed execution: uniform local intervention axis" not in s:
        s = s.rstrip() + PROGRAM_APPEND + "\n"
    PROGRAM.write_text(s)


def patch_checkpoint() -> None:
    s = CHECKPOINT.read_text()
    old_heading = "## Checkpoint 2026-09-11: finite-width packing and transverse-freedom unit completed; gate-2 pending"
    accepted_heading = "## Checkpoint 2026-09-11: finite-width packing and transverse-freedom unit completed and accepted"
    s = s.replace(old_heading, accepted_heading, 1)
    s = s.replace(
        "- **Review state:** reporting is complete on the gathering branch only after its reporting sub-PR merges. External Claude/Fable gate-2 review of the final gathering head remains required before `main`.",
        "- **Review state:** Claude/Fable accepted the final gathering head and merged PR #103 under the reviewer-merges rule; this unit is on `main`.",
        1,
    )
    if CHECKPOINT_SECTION.splitlines()[0] not in s:
        if accepted_heading not in s:
            raise SystemExit("checkpoint insertion anchor missing")
        s = s.replace(accepted_heading, CHECKPOINT_SECTION + accepted_heading, 1)
    CHECKPOINT.write_text(s)


def patch_program_json() -> None:
    data = json.loads(PROGRAM_JSON.read_text())
    if not isinstance(data, list):
        raise SystemExit("research-program.json is not a list")
    target = next((x for x in data if x.get("source") == "docs/research/2026-09-09-dimensional-closure-program.md"), None)
    if target is None:
        raise SystemExit("dimensional program registration not found")
    target["updated"] = "2026-09-11"
    target["summary"] = (
        "Transverse intervention independence now supplies an operational axis witness beyond state capacity: separated Rule90 channels have unbounded constant-support native intervention rank, while copied width does not; even with unlimited total 1D storage, a fixed alphabet and fixed common local endpoint window eventually cannot preserve all channel actions. This remains a representation-relative resource theorem, not an intrinsic-dimension criterion."
    )
    supports = target.setdefault("supports", [])
    if "intervention-axis" not in supports:
        supports.append("intervention-axis")
    PROGRAM_JSON.write_text(json.dumps(data, indent=2) + "\n")


def patch_knowledge_json() -> None:
    data = json.loads(KNOWLEDGE_JSON.read_text())
    if not isinstance(data, dict):
        raise SystemExit("knowledge.json top level is not an object")
    # Discover the entry list from the existing transverse-freedom record rather
    # than hard-coding the registry's container key.
    entry_key = None
    exemplar = None
    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and (
                    item.get("id") == "transverse-freedom-capacity"
                    or item.get("slug") == "transverse-freedom-capacity"
                    or item.get("source") == "docs/knowledge/transverse-freedom-capacity.md"
                ):
                    entry_key, exemplar = key, item
                    break
        if exemplar is not None:
            break
    if exemplar is None or entry_key is None:
        raise SystemExit("could not discover knowledge entry list")
    entries = data[entry_key]
    def ident(item):
        return item.get("id") or item.get("slug")
    if not any(isinstance(x, dict) and ident(x) == "transverse-intervention-independence" for x in entries):
        item = copy.deepcopy(exemplar)
        replacements = {
            "id": "transverse-intervention-independence",
            "slug": "transverse-intervention-independence",
            "title": "Transverse intervention independence survives release of total target storage",
            "label": "Transverse intervention independence",
            "source": "docs/knowledge/transverse-intervention-independence.md",
            "summary": "Separated Rule90 strips have native local intervention rank at least m with two-cell actions for every finite channel count m. A 1D target may use unlimited total storage, but if alphabet q and one common K+2R-site endpoint window are fixed, preserving all channel-subset endpoints requires 2^m <= q^(K+2R); copied width instead requires support 2m to remain copied at edit time.",
            "status": "exact",
            "updated": "2026-09-11",
            "date": "2026-09-11",
        }
        for k, v in replacements.items():
            if k in item or k in {"id", "title", "source", "summary"}:
                item[k] = v
        # Avoid inheriting entry-specific relationship summaries if present;
        # explicit graph edges are added below.
        for k in ("relationships", "backlinks", "reviewNotices"):
            item.pop(k, None)
        entries.append(item)

    # Discover the edge list from an existing depends_on edge and clone its
    # schema so provenance/rationale field names stay repository-native.
    edge_key = None
    edge_exemplar = None
    for key, value in data.items():
        if not isinstance(value, list):
            continue
        for edge in value:
            if isinstance(edge, dict) and (edge.get("type") == "depends_on" or edge.get("relation") == "depends_on"):
                edge_key, edge_exemplar = key, edge
                break
        if edge_exemplar is not None:
            break
    if edge_exemplar is None or edge_key is None:
        raise SystemExit("could not discover knowledge edge list")
    edges = data[edge_key]
    src_key = "source" if "source" in edge_exemplar else "from"
    dst_key = "target" if "target" in edge_exemplar else "to"
    type_key = "type" if "type" in edge_exemplar else "relation"
    exists = any(
        isinstance(e, dict)
        and e.get(src_key) == "transverse-intervention-independence"
        and e.get(dst_key) == "transverse-freedom-capacity"
        for e in edges
    )
    if not exists:
        edge = copy.deepcopy(edge_exemplar)
        edge[src_key] = "transverse-intervention-independence"
        edge[dst_key] = "transverse-freedom-capacity"
        edge[type_key] = "depends_on"
        if "rationale" in edge:
            edge["rationale"] = "The intervention-axis unit follows the finite-width/state-capacity result by releasing total target storage and fixing only local endpoint capacity."
        if "reason" in edge:
            edge["reason"] = "The intervention-axis unit follows the finite-width/state-capacity result by releasing total target storage and fixing only local endpoint capacity."
        if "provenance" in edge:
            edge["provenance"] = "docs/research/2026-09-11-intervention-axis.md"
        if "sourceNote" in edge:
            edge["sourceNote"] = "docs/research/2026-09-11-intervention-axis.md"
        edges.append(edge)
    KNOWLEDGE_JSON.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    patch_program()
    patch_checkpoint()
    patch_program_json()
    patch_knowledge_json()
    print("updated intervention-axis reporting registries")
