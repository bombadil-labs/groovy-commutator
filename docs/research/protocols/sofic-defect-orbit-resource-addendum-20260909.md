# Resource addendum: exact sofic defect orbit — 2026-09-09

**Status:** frozen after bounded Rule-35/Rule-5 implementation controls and before evaluating any of the 170 Research034 survivors.

The primary protocol froze limits on compressed graph states/edges, determinization subset states, inclusion-product subset pairs, and CI wall-clock time. The exact implementation additionally materializes an intermediate higher-block NFA state universe and a pre-trim deterministic transition graph.

To prevent an unbounded implementation-specific allocation from becoming an implicit post-hoc stopping rule, freeze these operational exact ceilings before the primary survivor census:

- maximum composable input-edge-pair states in one image NFA: **1,000,000**;
- maximum transitions in one pre-trim determinization/compression graph: **5,000,000**.

These are censoring thresholds only. Crossing either threshold does not imply dynamical complexity, non-stabilization, permanence, or absence of a witness.

The scientific semantics are unchanged:

- exact labeled-graph image under the paired radius-1 CA;
- exact block-language determinization/compression;
- exact block-language inclusion;
- primary horizon remains 12;
- original frozen hypotheses remain unchanged.

The bounded implementation controls observed before this addendum are not part of the 170-case primary outcome:

- the Rule-35 known witness is reproduced first at macro-horizon 3;
- the Rule-5 permanent-safety control remains target-invisible through the bounded control horizon;
- raw higher-block image graphs and the compressed right-resolving presentations are bidirectionally block-language equivalent on those controls.
