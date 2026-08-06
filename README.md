# autoware-deb-packages

See the readme in the release branch.

- [jammy-humble-main](https://github.com/autowarefoundation/autoware-deb-packages/blob/jammy-humble-main/README.md)

## Archive

This repository is no longer maintained.

In August 2026 the history was rewritten. The rewrite deleted every Debian package from every branch. It also deleted all Git LFS configuration and all Git LFS objects. These packages were build artifacts of a CI workflow. The repository size decreased from about 11 GB to about 1.4 MB.

The rewrite changed every commit SHA. Old links to a commit do not resolve.

The GitHub issues and pull requests were exported before the rewrite. The repository was then deleted and created again, so the original numbers do not resolve. A commit message that references `#159`, `#162`, or `#166` points to content that is now in the files below.

| File | Contents |
|---|---|
| [`github-archive/ISSUES.md`](github-archive/ISSUES.md) | 45 issues, with bodies and comments |
| [`github-archive/PULLS.md`](github-archive/PULLS.md) | 125 pull requests, with bodies, reviews and comments |
| [`github-archive/PLAN.md`](github-archive/PLAN.md) | The size analysis and the rewrite procedure |
| [`github-archive/README.md`](github-archive/README.md) | A description of every file in the archive |

The archive also holds the raw JSON from the GitHub API. Use [`github-archive/build_index.py`](github-archive/build_index.py) to build the two Markdown files again from that JSON.
