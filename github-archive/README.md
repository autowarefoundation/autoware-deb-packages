# autoware-deb-packages — GitHub metadata archive

Snapshot of the GitHub-side metadata for `autowarefoundation/autoware-deb-packages`, exported 2026-08-06 before the repository was rewritten to remove Git LFS.

The git history itself is **not** here — it lives in the repository. This directory only preserves the things a delete-and-recreate would destroy.

## Browsable

| File | Contents |
|---|---|
| `ISSUES.md` | 45 issues, with bodies and all comments inline |
| `PULLS.md` | 125 pull requests, with bodies, reviews and comments inline |

## Raw JSON (full fidelity)

| File | Contents |
|---|---|
| `issues.json` | 170 entries — all issues *and* PR stubs, as the API returns them |
| `pulls.json` | 125 pull requests, full detail (branches, merge state, timestamps) |
| `issue_comments.json` | 123 issue/PR comments |
| `review_comments.json` | 5 inline code-review comments |
| `reviews.ndjson` | 8 PR reviews, one JSON object per PR |
| `labels.json` | 34 labels with colours and descriptions |
| `milestones.json` | 0 milestones (none existed) |
| `repo_metadata.json` | Description, topics, settings, counts at export time |

JSON files are arrays-of-pages as produced by `gh api --paginate --slurp`. `build_index.py` flattens them; re-run it to regenerate the Markdown.

## What is deliberately not preserved

- **Git LFS objects** — ~9.01 GB across 3,673 pointers. Judged disposable: they were CI-produced `.deb`/`.ddeb` build artifacts of an unused repository.
- **Stars and watchers** (2 stars) — cannot be transferred.
- **Issue/PR numbering on GitHub** — after recreation, `#159`, `#162`, `#166` and the other references appearing in commit messages will no longer resolve. The bodies behind those numbers are in `ISSUES.md` / `PULLS.md`.
- **Forks** — `jspricke/autoware-deb-packages` and `isamu-takagi/autoware-deb-packages` are outside this repository's control and retain the pre-rewrite history.
