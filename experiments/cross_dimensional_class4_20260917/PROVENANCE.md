# Cross-dimensional Class-IV research unit — provenance

Repository target: `bombadil-labs/groovy-commutator`  
Base observed on 2026-09-17: `main` at `4ff191cb46bd9e0a9b349487aa3875486932ac9d`.

## Authorization and review status

The repository normally requires independent Gate-1 review before implementation/evaluation. No independent collaborator was available in this chat. Myk explicitly authorized proceeding on 2026-09-17 with “make it so!”, invoking the documented no-review-at-freeze exception. Both protocol files record that exception. Independent final review is still required before merge to `main`.

The GitHub connector available in this chat had read access but branch creation returned HTTP 403 `Resource not accessible by integration`. No repository write or PR was therefore made from this session. Work was performed in a local artifact tree and is packaged for explicit push.

## Actual local chronology

This chronology is the scientific chronology; later Git import commits must not be described as pre-evaluation review evidence.

1. Recovered prior Jev protocol/results and the selective-persistence result from Project/Library artifacts.
2. Frozen `docs/research/protocols/2026-09-17-cross-dimensional-class4.md` before implementing the new 2D harness. Frozen SHA-256: `99685559b9dfa2f8e0bfecdfcf64f8c4acf26e4b7a1ef62bf6fc8423c2cd35f1`.
3. Implemented `experiments/cross_dimensional_class4_20260917/run.py`.
4. Ran exact HighLife width-1 → ECA-54 mapping control, smoke/pilot diagnostics, then the frozen full primary/stress panel without threshold retuning.
5. Wrote `docs/research/2026-09-17-cross-dimensional-class4.md` from the frozen results.
6. Derived and exhaustively checked the periodic-strip local-rule restriction: height 1 forgets 12 Life-like rule bits; height 2 is injective on the full 18-bit Life-like rulespace.
7. Frozen `docs/research/protocols/2026-09-17-strip-spectrum.md` before implementing/evaluating the strip-spectrum dynamics. Frozen SHA-256: `f990d54e12a3407cba485a820708e7c78397f0194ca489781be78676a89fe1e1`.
8. Implemented `strip_spectrum.py` and ran primary density 0.5; saved `strip_spectrum_primary.json` before stress evaluation.
9. Ran frozen density 0.3/0.7 stress phase; saved `strip_spectrum_stress.json`.
10. Wrote `docs/research/2026-09-17-strip-spectrum.md`.
11. Added a post-hoc algebraic observer-chain-rule audit (`observer_chain_rule.py/json`). This is explicitly not part of the frozen classifier protocol.
12. Frozen `docs/research/protocols/2026-09-17-jev-codebook-ablation.md` and added `JEV_RUN3_CODEBOOK_ABLATION.md` as the next external Jev acquisition protocol/instruction sheet. No Run-3 Jev responses were generated in this session.

## Scientific status

- Exact/local: HighLife width-1 mapping to Rule 54; Life-like height-1 quotient enumeration; height-2 injectivity; coarse-observer surprisal chain identity.
- Computational exploratory: starred 1D/2D phenotype panel and strip spectra.
- Unrun: Jev Run 3 matched operational-codebook ablation.
- Pending: independent review of protocols, implementations, canonical result bytes, interpretation, and prior-art/novelty boundary before merge to `main`.

## Verification

All Python files compile with `python -m py_compile`. `MANIFEST.sha256` hashes every packaged non-cache artifact. Expensive research evaluations were run locally and were not placed in automatic GitHub Actions.
