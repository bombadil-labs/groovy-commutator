# Publication provenance: representation and causal retention

On 2026-09-22 the refreshed Bombadil connector restored access. PR [#282](https://github.com/bombadil-labs/groovy-commutator/pull/282) imports the five local commits in order. The connector creates new commit objects: dates of remote publication are not dates of protocol freezing or evaluation. Original SHA references in frozen documents and canonical reports are retained; use this table to locate their published counterparts. This records the author's local chronology, not independent preregistration or review.

| Original local commit | Published commit |
| --- | --- |
| `5b54f39c15b09ea3de54b184a138caf7a9b4f5b4` | `15307177a392ba30ba4f78b0d6f358e8f6bbe355` |
| `0e5d0e28f67270cb9734b6070d11d60a52ba6cf2` | `ae3e0affe2eae61762c2b4aa48563477c4b2f2a8` |
| `bc7741b3f29e81e5d703f80e47a46dd0d93aec74` | `f9addddb5658bbf6e587be1593c66055ce5867f7` |
| `d41b427e96324d7ce9b4296dc651230419a6c7a2` | `22d1c42ec29bfff48c0113f15c4a9c6689c7b832` |
| `3ab8604ac617f888ca706bdd73470f881f3aca1f` | `09ac216e4aaf4479eb2bd2d70bb54515de2a874e` |

The complete imported head tree was compared with local head `3ab8604ac617f888ca706bdd73470f881f3aca1f` using `git diff HEAD FETCH_HEAD`: no differences, including file modes. All original canonical bytes are preserved. Subsequent publication edits only update handoff documentation and this record. The original git bundle was also delivered in the session handoff archive.

Integration uses Myk's explicit solo authorization. CI and self-review do not constitute independent scientific review. Check PR #282 for the authoritative merge status.
