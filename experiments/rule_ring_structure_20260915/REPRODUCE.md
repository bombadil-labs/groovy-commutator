# Reproducing the whole-state ring study

This unit follows `docs/research/protocols/rule-ring-structure-20260915.md`.
Gate 1 approved revision `db2be505e4120259b649bf03967facd6b882a809`:
https://github.com/bombadil-labs/groovy-commutator/pull/264#issuecomment-5687700172

Run outside GitHub Actions, with Python 3.11+ and NumPy 2.3.5. Use one BLAS
thread so thread stacks do not consume the 2-GiB address-space ceiling.

```bash
OPENBLAS_NUM_THREADS=1 python scripts/rule_ring_structure.py discovery
# Preserve/commit discovery-selection.json and discovery-result.json;
# create confirmation-seal.json with their SHA256 and the selection commit.
OPENBLAS_NUM_THREADS=1 python scripts/rule_ring_structure.py confirmation
```

Each stage has a 600-second alarm, a 2-GiB address-space limit and a checked
resident-memory budget. The script records execution status even on an error.
It refuses to overwrite previously evaluated NPZ cases or completed results.
Replay in a separate checkout with a fresh study output directory, retaining
the implementation freeze and appropriate seal. Do not delete archival results
to make room for a replay.

`partitions/` stores the complete successor and nine label arrays per case.
Stage case lists reference their exact hashes. Evidence rows retain all four
source references, both partition relations, and their comparison. Response
tables average absolute changes across the fixed 28 rule pairs. Associations
and the discovery selection are saved separately; confirmation never refits
the selection. All ring-pair rows, including mixed discovery/confirmation
pairs, remain available in the final evidence table.

The independent review and final result distinguish software checks, known
controls, descriptive associations and unresolved class specificity. No
automatic research rerun belongs in CI; its tier checks only pinned bytes.
