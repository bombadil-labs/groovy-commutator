# Audit correction: Research033 symbol-round expectations — 2026-09-09

**Status:** frozen after corrected full census run `34381601120` and before rerunning the independent audit.

The first audit correctly exposed `int16` overflow in the primary generated-symbol closure. After widening paired-symbol indices to `np.intp`, the complete census reproduces all scientific classifications exactly:

- 5,360 Research032 residual cases;
- 0 generated-symbol certificates;
- 5,132 generated-edge certificates;
- 228 cases remaining after edge closure.

Only the frozen generated-symbol **round counts** for the first two audit cases change.

Use these corrected expectations:

- Rule 1 / target `01001100` / pair `0-2`: 48 symbols in **5** rounds; 153 edges in 3 rounds; edge-safe.
- Rule 5 / target `01001100` / pair `0-2`: 64 symbols in **5** rounds; 230 edges in 4 rounds; edge-unsafe.

All Rule-122 and Rule-161 sentinel expectations in the original audit protocol remain unchanged.

The independent audit must now pass all 14 cases under these corrected frozen values. Do not change any case, target, edge expectation, or safety classification after the audit runs.
