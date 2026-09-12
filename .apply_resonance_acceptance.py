from pathlib import Path

note_path = Path('docs/research/2026-09-12-dimensional-resonance-response.md')
note = note_path.read_text()
old = '**Authored by:** OpenAI GPT-5.6 Sol. **Reviewed by:** pending independent Gate 2 on gathering PR #173.'
new = '**Authored by:** OpenAI GPT-5.6 Sol. **Reviewed by:** Claude Code / Fable 5.1, 2026-09-12, Gate 2 on exact final head `da9c1d6a035ad33b6bd14c12488010fb20b8dba8` ([review](https://github.com/bombadil-labs/groovy-commutator/pull/173#issuecomment-5648727318)); reviewer-merged in PR #173 as `ec0c2918cd221ac4eab0ea98e9db3b3c9ecfe33b`.'
if note.count(old) != 1:
    raise SystemExit(f'note provenance preimage count={note.count(old)}')
note_path.write_text(note.replace(old, new, 1))

checkpoint_path = Path('docs/research/checkpoints/dimensional-lift.md')
checkpoint = checkpoint_path.read_text()
old_heading = '## Checkpoint 2026-09-12: transformed-homologue mutual-transparency bet fails on primary ring seven; Gate 2 pending'
new_heading = '## Checkpoint 2026-09-12: transformed-homologue mutual-transparency bet fails on primary ring seven; accepted'
if checkpoint.count(old_heading) != 1:
    raise SystemExit(f'checkpoint heading preimage count={checkpoint.count(old_heading)}')
checkpoint = checkpoint.replace(old_heading, new_heading, 1)
old_review = '- **Review state:** evaluation, reporting, latest-main reconciliation and this current-account update are complete on the gathering lineage. Exact-head independent Claude/Fable Gate 2 and reviewer merge remain required before acceptance on `main`.'
new_review = '- **Review state:** Claude/Fable independently reviewed exact final gathering head `da9c1d6a035ad33b6bd14c12488010fb20b8dba8`, reran the frozen verifier off GitHub Actions in about 23.5 seconds with byte-identical canonical JSON, signed Gate 2, and reviewer-merged PR #173 into `main` as `ec0c2918cd221ac4eab0ea98e9db3b3c9ecfe33b`. This unit is accepted.'
if checkpoint.count(old_review) != 1:
    raise SystemExit(f'checkpoint review preimage count={checkpoint.count(old_review)}')
checkpoint_path.write_text(checkpoint.replace(old_review, new_review, 1))
