# Rule-110 G autonomy: chronology and review

Authored by: Codex (OpenAI), 2026-09-22.

- Base main: `5aee7bb9ac6c70eaa114a8ed5baf38ba6b10e8c1`; no open PR or issue
  overlapped the unit at selection.
- Frozen scientific protocol: commit `ad38b4937321501889b6b8a1caab4e4bfb54052e`,
  SHA-256 `1a4c16b696a9b8c3cff6b3abc4f4d70d02badf65976a9bf75a8ca7f30014651b`.
  Local commit `95d20917c8620a4ecec63546834f2966677feb5e` has identical protocol
  bytes; the remote commit was published through the Bombadil connector because
  direct git push lacked credentials. The working tree was then aligned to it.
- After protocol freeze, while independent review was pending, the author
  hand-derived a possible periodic collision with source words 001 and 011.
  This is pre-execution mathematical candidate selection, not an unseen
  prediction or a result of the later enumeration. It was disclosed to the
  reviewer before approval and to Myk before execution.
- Independent prospective review: Sol (gpt-5.6-sol), agent
  `/root/g_autonomy_review`, approved the frozen revision without blockers.
  [Signed review record](https://github.com/bombadil-labs/groovy-commutator/pull/293#issuecomment-5780787370).
  The reviewer performed no target implementation or evaluation. The protocol's
  provenance header was subsequently updated; scientific scope stayed fixed.
- Implementation is committed after Gate 1 and before the primary evaluation.
  The pinned implementation and execution time belong in `execution.json`.
  Final independent result review is pending, tracked on PR #293.

No old reset or solo-research waiver is used for this unit.
