# Push instructions — `gather/cross-dimensional-class4`

The ChatGPT GitHub connector could read `bombadil-labs/groovy-commutator` but returned HTTP 403 when asked to create the gathering branch. This bundle is therefore an **overlay**, not evidence that the work was pushed.

## 1. Start from the pinned base or consciously rebase

```bash
git clone https://github.com/bombadil-labs/groovy-commutator.git
cd groovy-commutator
git fetch origin
# The research was frozen against this observed main SHA:
git checkout 4ff191cb46bd9e0a9b349487aa3875486932ac9d
# Or, if intentionally integrating onto newer main, checkout that and record the deviation.
git switch -c gather/cross-dimensional-class4
```

## 2. Overlay the bundle

Unzip/copy the bundle contents at the repository root, preserving paths. Do not copy the bundle's packaging ZIP into the repository.

Verify bytes:

```bash
sha256sum -c MANIFEST.sha256
python -m py_compile \
  experiments/cross_dimensional_class4_20260917/run.py \
  experiments/cross_dimensional_class4_20260917/strip_restriction.py \
  experiments/cross_dimensional_class4_20260917/strip_spectrum.py \
  experiments/cross_dimensional_class4_20260917/observer_chain_rule.py
```

## 3. Preserve artifact grouping in Git history

Because the scientific work had to be performed outside the repo after the connector write failure, these integration commits are **not** evidence that Gate-1 review preceded evaluation. `PROVENANCE.md` carries the real chronology.

Suggested integration commits:

```bash
# A — frozen protocol records / external Jev next-run instructions
git add \
  docs/research/protocols/2026-09-17-cross-dimensional-class4.md \
  docs/research/protocols/2026-09-17-strip-spectrum.md \
  docs/research/protocols/2026-09-17-jev-codebook-ablation.md \
  JEV_RUN3_CODEBOOK_ABLATION.md \
  PROVENANCE.md
git commit -m "Record cross-dimensional Class-IV protocols and provenance"

# B — implementation
git add experiments/cross_dimensional_class4_20260917
git commit -m "Add cross-dimensional and strip-spectrum harnesses"

# C — evidence / notes
git add \
  docs/research/2026-09-17-cross-dimensional-class4.md \
  docs/research/2026-09-17-strip-spectrum.md \
  results/cross_dimensional_class4_20260917 \
  MANIFEST.sha256 \
  PUSH_INSTRUCTIONS.md
git commit -m "Record cross-dimensional Class-IV and strip-spectrum results"
```

## 4. Repository integration work still required

Before the gathering PR is ready for independent review, integrate this unit with the repo's current research infrastructure:

- register the result notes in `site/content/research.json` or the current research shard;
- update the relevant Program/checkpoint and knowledge entries if the current repo head still uses them;
- register canonical result hashes/verifiers in `scripts/check_result_integrity.py` as appropriate;
- run the repo's cheap research/site checks (`npm run test:research --prefix site`, build if required);
- do **not** add the expensive full evaluations to automatic CI.

Those integration files were deliberately not fabricated from a stale snapshot in this bundle.

## 5. Open the gathering PR

```bash
git push -u origin gather/cross-dimensional-class4
gh pr create \
  --base main \
  --head gather/cross-dimensional-class4 \
  --draft \
  --title "Research: cross-dimensional Class-IV phenotype and strip restrictions" \
  --body-file PROVENANCE.md
```

The PR should explicitly say:

- Myk authorized the no-review-at-freeze exception on 2026-09-17;
- evaluation therefore preceded independent review;
- the exact results and exploratory results are separated in the notes;
- final independent Gate-2 review is required on the current head before merge.

## 6. Full local replay commands

Cross-dimensional panel:

```bash
python experiments/cross_dimensional_class4_20260917/run.py \
  --mode full \
  --output-dir results/cross_dimensional_class4_20260917
```

Exact strip restriction:

```bash
python experiments/cross_dimensional_class4_20260917/strip_restriction.py \
  --output results/cross_dimensional_class4_20260917/strip_restriction_exact.json
```

Strip primary and stress:

```bash
python experiments/cross_dimensional_class4_20260917/strip_spectrum.py \
  --phase primary \
  --output-dir results/cross_dimensional_class4_20260917

python experiments/cross_dimensional_class4_20260917/strip_spectrum.py \
  --phase stress \
  --output-dir results/cross_dimensional_class4_20260917
```

Observer-chain post-hoc audit:

```bash
python experiments/cross_dimensional_class4_20260917/observer_chain_rule.py \
  --output results/cross_dimensional_class4_20260917/observer_chain_rule.json
```
