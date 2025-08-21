#!/usr/bin/env bash
set -euo pipefail

: "${UPSTREAM_REMOTE:=upstream}"
: "${UPSTREAM_BRANCH:=main}"
: "${WORK_BRANCH:=main}"

echo "Fetching ${UPSTREAM_REMOTE}..."
git fetch "${UPSTREAM_REMOTE}"

echo "Switching to ${WORK_BRANCH}..."
git checkout "${WORK_BRANCH}"

echo "Merging ${UPSTREAM_REMOTE}/${UPSTREAM_BRANCH} into ${WORK_BRANCH}..."
git merge "${UPSTREAM_REMOTE}/${UPSTREAM_BRANCH}"

echo "Done. Resolve conflicts if prompted, then commit."
