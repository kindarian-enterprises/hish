# Branching & Update Policy

## Roles
- **upstream (remote)**: canonical repo.
- **main (local)**: your working branch with local tweaks.

## Normal update flow (plain Git)
```bash
git fetch upstream
git checkout main
git merge upstream/main
# resolve conflicts, then git commit
```

We recommend **merge** (not rebase) to preserve a clear history of upstream vs local changes.
Advanced users may rebase; it's optional.

## Local overrides

* Keep machine/user-specific files in ignored paths (see `.gitignore`).
* To share specific changes, move them out of ignored paths and commit on a feature branch, then open a PR.
