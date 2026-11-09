# Handoff

**Updated 2026-11-09.** Read [the direction page](START_HERE.md) first. This
page says only what state the repository is in and how to check it. The
previous handoff, a 475-line chronological log, is
[archived verbatim](archive/next-task-2026-10-08.md).

## State

- `main` contains every completed unit through 2026-10-08, plus the July
  attractor unit recovered from an unpushed branch. Nothing is in flight.
- The October work was reviewed and integrated on 2026-11-09:
  [review and integration record](2026-11-09-october-integration-review.md).
- No pull request is open. Every older remote branch was audited; what each
  held, and whether anything in it is absent from `main`, is in
  [the branch disposition](archive/branch-disposition-2026-11-09.md).
- No empirical unit is queued. The direction page lists three candidates and
  the condition each parked line needs.

## Check the repository

```
python scripts/check_result_integrity.py
python -m pytest -q tests
npm ci --prefix site
npm run test:research --prefix site
npm run build --prefix site
```

Three things to know before trusting a failure:

- **Line endings.** The integrity check hashes file bytes. `.gitattributes`
  now requests LF for text files, so a fresh clone passes on Windows. An older
  Windows checkout made with `core.autocrlf=true` reports dozens of false
  hash failures until its files are re-checked-out (`git rm --cached -r . &&
  git reset --hard`, on a clean tree).
- **Unix-only module.** Some hashed runners import `resource`. The test suite
  supplies a stand-in on Windows through `tests/conftest.py`; running such a
  runner directly on Windows still fails, and the runners must not be edited,
  because their bytes are part of recorded results.
- **Prolog.** One relational-search test needs the pinned `swipl-wasm` Node
  package: `npm ci --prefix experiments/relational_search_20260923`.

Expensive runs stay outside automatic CI; see `AGENTS.md`.

## If you are about to start something

1. Write the four-question decision argument from the direction page.
2. Open one `gather/<unit>` branch **based on `main`**, with a draft pull
   request. Do not stack it on another unmerged branch.
3. When the unit ends, add its account to [the findings](FINDINGS.md), update
   its knowledge entries, and change at most one row of the direction page.
4. Say who reviewed it and at which revision, or say `Reviewed by: none`.

## Corrections outstanding

None known. If a witness or a reproducing check contradicts a bounded claim,
correct the claim visibly and preserve the original result bytes and the
failed prediction.
