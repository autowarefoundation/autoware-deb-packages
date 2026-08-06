# autoware-deb-packages: delete Git LFS and archive the repository

Analysis date: 2026-08-06.
Repository: `autowarefoundation/autoware-deb-packages`.

This document has two parts. Part A to Part D give the analysis. Part E gives the
step-by-step plan.

---

## A. What the repository contains

The repository holds Debian packages that a GitHub Actions workflow built. These
packages are build artifacts. The repository has 151 commits and 22 branches.

The repository stores the packages in two different ways. The `jammy-humble*`
branches store the packages as normal git blobs. The `release/*` branches store
the packages as Git LFS pointers.

### Total size

| Item | Value |
|---|---|
| Git pack size after a clone | 1.81 GiB |
| Objects in the pack | 15426 |
| Git LFS payload on GitHub | 9.01 GB |
| Git LFS pointer files | 3673 |
| Total size | about 11 GB |

### Where the git data is

A clone downloads all branches. Almost all of the data comes from six branches.

| Scope | Objects | Size |
|---|---|---|
| All branches | 15426 | 1.81 GiB |
| `origin/main` and all of its history | 218 | 0.07 MB |
| All branches that are not `jammy-humble*` | 571 | 0.10 MB |
| Only the `jammy-humble*` branches | 14856 | 1860 MB |

### Which file types use the space

| Extension | Files | Size on disk |
|---|---|---|
| `.ddeb` | 2032 | 1711 MB |
| `.deb` | 2544 | 99 MB |
| `.build` | 5088 | 45 MB |
| All other types | about 5300 | 4 MB |

The debug symbol packages (`.ddeb`) are 92 percent of the git data. The largest
single file is 52 MB.

### Git LFS configuration

The full history contains one `.gitattributes` blob. This blob has two lines:

```
*.deb filter=lfs diff=lfs merge=lfs -text
*.ddeb filter=lfs diff=lfs merge=lfs -text
```

Both lines configure Git LFS. Therefore, deletion of this one file deletes all
Git LFS configuration from the repository.

### GitHub metadata

| Item | Count |
|---|---|
| Issues | 45 |
| Pull requests | 125 |
| Comments | 123 |
| Reviews | 8 |
| Labels | 34 |
| Milestones | 0 |
| Releases | 0 |
| Forks | 2 |
| Stars | 2 |

---

## B. Errors in the first plan

The first plan had five steps:

1. Clone the repository without the Git LFS files.
2. Delete the repository.
3. Create the repository again.
4. Push the history back.
5. Disable GitHub Actions.

The plan is correct in one point. GitHub gives no self-service method to delete
single Git LFS objects. Deletion of the repository is the only method.

The plan has four errors.

### Error 1. The push fails

`git-lfs 3.4.1` is installed on this machine. The pre-push hook looks for the
3673 Git LFS objects. The local clone does not contain these objects. Therefore
the push stops with an error.

### Error 2. The new repository keeps its Git LFS configuration

The clone contains the Git LFS pointer files and the `.gitattributes` file. A
push sends both to the new repository. The result is a repository with 3673
broken pointers. The Git LFS storage becomes empty, but the repository still
declares Git LFS.

### Error 3. GitHub Actions starts a new build

The workflow `generate-deb-packages-aws.yaml` runs on a push to `main`. The
workflow writes packages to the `jammy-humble-main` branch. Therefore the new
repository fills itself with packages again.

### Error 4. The token cannot delete a repository

The token has four scopes: `gist`, `read:org`, `repo`, and `workflow`. The scope
`delete_repo` is absent.

### One more inconsistency

The first plan destroys 9.01 GB of Debian packages in Git LFS. The same plan
keeps 1.86 GB of Debian packages in normal git blobs. Both groups are the same
kind of build artifact.

---

## C. The solution

Delete all package files from the history first. Then delete the repository and
create it again.

`git filter-repo` deletes these paths from all 22 branches:

- `*.deb`
- `*.ddeb`
- `*.build`
- `*.buildinfo`
- `*.changes`
- `.gitattributes`

### Result of the rewrite

| Item | Before | After |
|---|---|---|
| Pack size | 1.81 GiB | 1.36 MiB |
| Objects | 15426 | 670 |
| Commits | 151 | 151 |
| Branches | 22 | 22 |
| `.deb` and `.ddeb` blobs | 4576 | 0 |
| `.gitattributes` files | 1 | 0 |

The option `--prune-empty never` keeps all 151 commits. Every commit message and
every commit date stays in the history.

The files that stay are the source material: `sources.repos`, `colcon-*.yml`, the
workflow files, the `Packages` and `Release` index files, the keyring, and the
README files.

CAUTION: Make a backup of the original clone before the rewrite. The rewrite
changes every commit SHA. The `main` branch moves from `beebdd5` to `9ac0d19`.
All links to a commit in this repository become invalid.

The `main` branch also changes because its own history contained the
`.gitattributes` file. Commit `b88f487` deleted that file later.

---

## D. Work that is already complete

Two directories on the local machine hold the results.

**`/home/mfc/projects/autoware-deb-packages-archive/`** holds the GitHub
metadata:

- `ISSUES.md` and `PULLS.md` — all 170 entries with bodies and comments
- `issues.json`, `pulls.json`, `issue_comments.json`, `review_comments.json`,
  `reviews.ndjson`, `labels.json`, `milestones.json`, `repo_metadata.json`
- `build_index.py` — the script that builds the two Markdown files
- `README.md` — a description of each file

**`/home/mfc/projects/autoware-deb-packages-clean.git/`** holds the clean git
history. Its size is 1.36 MiB.

The original clone at `/home/mfc/projects/autoware-deb-packages/` is not
changed. This clone is the backup.

---

## E. The plan

### Step 1. Not necessary

The account owner deletes the repository in the web browser. Therefore the token
does not need the `delete_repo` scope.

### Step 2. Make sure that the archive is complete

Read `ISSUES.md` and `PULLS.md`. Make sure that the two files contain the correct
content. After Step 3, GitHub does not hold this data.

### Step 3. Delete the repository in the web browser

CAUTION: Complete Step 2 before this step. This step deletes 45 issues, 125 pull
requests, and 9.01 GB of Git LFS objects. You cannot undo this step.

1. Open the settings page of the repository:
   `https://github.com/autowarefoundation/autoware-deb-packages/settings`
2. Move to the section "Danger Zone" at the end of the page.
3. Select "Delete this repository".
4. Type the name `autowarefoundation/autoware-deb-packages` in the dialog.
5. Select the button that confirms the deletion.

Note: GitHub shows a warning about the 2 forks. The forks stay on GitHub after
the deletion.

Note: You can also create the repository again in the web browser. Then Step 4
is not necessary. The order of Step 5 and Step 6 stays the same.

CAUTION: Do not push before Step 5 disables GitHub Actions. A push to `main`
starts a new package build.

### Step 4. Create the repository again

```
gh repo create autowarefoundation/autoware-deb-packages --public
```

Note: The account `xmfcx` is an admin of the organization. The organization
permits public repositories. Therefore this step succeeds.

### Step 5. Disable GitHub Actions

CAUTION: Run this step before the push in Step 6. If GitHub Actions is active,
the push starts a new package build.

```
gh api -X PUT \
  repos/autowarefoundation/autoware-deb-packages/actions/permissions \
  -F enabled=false
```

### Step 6. Push the clean history

```
git -C /home/mfc/projects/autoware-deb-packages-clean.git push --mirror \
  https://github.com/autowarefoundation/autoware-deb-packages.git
```

The push sends 1.36 MiB. It completes in a few seconds.

### Step 7. Restore the repository configuration

```
gh api -X PATCH repos/autowarefoundation/autoware-deb-packages \
  -f default_branch=main -F has_wiki=false -F has_projects=false
```

### Step 8. Restore the 34 labels

```
cd /home/mfc/projects/autoware-deb-packages-archive
jq -r '.[]|.[]|[.name,.color,.description//""]|@tsv' labels.json |
while IFS=$'\t' read -r name color desc; do
  gh label create "$name" -R autowarefoundation/autoware-deb-packages \
    -c "$color" -d "$desc" --force
done
```

### Step 9. Examine the new repository

Open the repository in a browser. Make sure that all 22 branches are present.
Make sure that the repository size is about 1.4 MiB.

### Step 10. Archive the repository

CAUTION: Complete all other steps before this step. An archived repository is
read-only. You cannot push to it and you cannot change its configuration.

```
gh repo archive autowarefoundation/autoware-deb-packages --yes
```

Note: An archived repository does not run GitHub Actions. Step 5 and Step 10
both stop the workflows.

### Step 11. Make sure that the Git LFS storage decreased

Open the billing page of the organization. Make sure that the Git LFS storage
decreased by about 9 GB.

If the storage did not decrease, write to GitHub Support. The two forks can keep
the objects alive.

---

## F. Risks

### The two forks

The repository has two forks:

| Fork | Size | Last push |
|---|---|---|
| `jspricke/autoware-deb-packages` | 31581 KB | 2023-01-30 |
| `isamu-takagi/autoware-deb-packages` | 1 KB | 2023-04-03 |

Deletion of the parent repository does not delete a fork. GitHub makes one fork
the new parent of the network. Therefore the old history can stay in a fork that
this organization does not control.

The effect on the Git LFS bill is not certain. Step 11 tests this effect.

### An alternative method

A force-push of the clean history to the current repository keeps the issue
numbers and the pull request numbers. This method does not delete the Git LFS
objects. GitHub never deletes an unreferenced Git LFS object. The organization
pays for the 9.01 GB until GitHub Support deletes the objects.

---

## G. Data that this plan does not preserve

- **The 9.01 GB of Debian packages in Git LFS.** These files are build artifacts
  of an unused repository.
- **The GitHub numbers of the issues and the pull requests.** Commit messages in
  this repository contain `#159`, `#162`, and `#166`. These references become
  invalid. The text behind each number is in `ISSUES.md` and `PULLS.md`.
- **The 2 stars and the watchers.** GitHub cannot transfer them.
- **All commit SHA values.** Every permanent link to a commit becomes invalid.
