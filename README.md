# Groovy Commutator

An operator-commutator framework for cellular automata — generalized from
a single rule's self-commutator to the relationship *between* pairs of
rules. Origin: https://liet-codes.github.io/wet-math/commutator.html

## Research and the public site

The site's **Research** section is the ongoing working record. Each entry has
a plain-language summary, evidence status, methods, limitations, and links to
the code and data. Main pages remain curated explanations; the Research index
keeps a separate list of ideas to explain next.

Within Research, the **Knowledge base** tracks individual concepts, findings,
questions, theories, and experiments. Typed links record support,
contradiction, tests, and dependencies, with reasons and research provenance.
Entries show backlinks and indirect dependents. See the
[knowledge authoring guide](docs/knowledge/README.md).

To add a note or promote an insight, follow
[the research authoring guide](docs/research/README.md). Write the note in
`docs/research/` and register it in `site/content/research.json`; the normal
site build creates its page and updates the index automatically.

### First research checkpoint

[Observed history and coarse-grained prediction](docs/research/2026-09-07-history-repairability.md)
continues **Analysis of Collusion Wiki**: recovered Rule 90/110 notes, reproduced
broad sweeps, exact algebra checks, and new independent-seed history curves.
The simple Class-IV identification failed; repair depends on the observation.
This checkpoint also corrects the old affine converse: nonlinear Rules 4 and
200 have zero commutator. Start with the research note for methods and limits.

## Layout

- `src/groovy/` — the actual library. Start with `operators.py`'s
  docstring, then `ca.py`, `metrics.py`, `classify.py`. Newer extensions,
  each with the math in its module docstring: `secondorder.py`
  (reversible memory, incl. the generalized-μ reversibility result),
  `metaevolution.py` (rules-birthing-rules), `prehoc.py` (4-input rules,
  the collapse theorem, coupled layers), `nonuniform.py` (per-cell rule
  fields, the second collapse theorem, state-gated rule transport),
  `ca2d.py` (Life-like 2D engine) — see `NOTES.md` sections 6–8.
- `scripts/` — runnable sweep/precompute scripts (`run_full_sweep.py`,
  `precompute_image_ratios.py`, `aggregate_sweep.py`) that write to
  `results/`, plus one `experiment_*.py` per data-backed claim on the
  site's questions page — each writes a small JSON to `site/src/data/`.
  Use these instead of `classify.sweep` for anything beyond pilot scale.
- `notebooks/01_exploration.ipynb` — narrated walkthrough: the affine
  theorem, the four single-rule regimes, the five pair regimes, the drain
  mechanism, the pilot sweep.
- `NOTES.md` — citations, the QM correspondence, and the open interpretive
  thread.
- `CLAUDE.md` — orientation + established results + open task, for picking
  this up in an agentic coding session.
- `results/` — sweep outputs: `sweep_full.parquet` (raw), 
  `sweep_full_classified.parquet` (regime-labeled, joined with image_ratio),
  `sweep_summary.csv`, `image_ratios.csv`.
- `docs/research/` — canonical research notes, archived conversation material,
  and the authoring/promotion guide. Published notes are selected by
  `site/content/research.json`; archived notes stay available as evidence.
- `site/` — source for the GitHub Pages site (React + Vite): main pages —
  home, concepts (cellular automata, boolean calculus incl. the `I`/Euler-
  integration reading of evolution, the State&rarr;State shape, each
  instrument, all with live in-browser demos), questions (named questions
  answered by embedded, confidence-labeled data — including ones still
  open), The Walk (a guided narrative with live demos), and explorer
  (a card-based tool for composing the instruments yourself, 1D or 2D) —
  plus static Research pages generated from Markdown.
  `site/src/lib/groovy-engine.js` is the client-side
  reimplementation of `src/groovy/*.py` — keep them in sync. Dev server:
  `npm run dev --prefix site`; build: `npm run build --prefix site`
  (outputs to `public/`).
- `public/` — **generated** by the `site/` build, gitignored, deployed to
  GitHub Pages by `.github/workflows/pages.yml`. Don't edit directly. The
  handful of static figures the pages embed (e.g. the full 256×256 regime
  heatmap) live in `site/public/assets/img/` and are produced by
  `scripts/build_findings_assets.py`.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
pip install -r requirements.txt   # adds matplotlib + jupyter for the notebook
jupyter notebook notebooks/01_exploration.ipynb
```

## Quick taste

```python
from groovy import G, divergence_trajectory, divergence_stats
import numpy as np

rng = np.random.default_rng(0)
S = rng.integers(0, 2, size=64).astype("uint8")

G(S, 90)    # all zeros -- rule 90 is affine with no bias, D and E commute
G(S, 165)   # all ones  -- affine with bias, constant nonzero commutator

field = divergence_trajectory(S, 110, 54, steps=150)
divergence_stats(field)   # structured, persistent disagreement -- not noise, not drain
```

## Status
Full 256-rule, 32,640-pair exhaustive sweep complete (5 seeds/pair) — see
`results/` and `CLAUDE.md`. The public site (`site/`) has been redesigned
into four pages including a new interactive Explorer, per
`DESIGN_BRIEF.md` / `INTERACTIVE_EXPLORER_SPEC.md`. Current open threads:
validating the provisional regime-classification thresholds against the
real compressibility distribution, extending `groovy-engine.js`'s 2D CA
support back into `src/groovy/` (see that file's own module docstring),
and the new instruments (absential view, second-order memory,
meta-evolution) described in `NOTES.md` section 6.
