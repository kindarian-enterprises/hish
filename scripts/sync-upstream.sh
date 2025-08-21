#!/usr/bin/env bash
set -euo pipefail

: "${MAIN_BRANCH:=main}"
: "${WORK_BRANCH:=my-team-customization}"

echo "Getting updates from main repository..."

echo "Switching to ${MAIN_BRANCH}..."
git checkout "${MAIN_BRANCH}"

echo "Fetching latest updates..."
git fetch origin

echo "Merging origin/${MAIN_BRANCH} into ${MAIN_BRANCH}..."
git merge "origin/${MAIN_BRANCH}"

echo "Switching back to ${WORK_BRANCH}..."
git checkout "${WORK_BRANCH}"

echo "Merging updates into ${WORK_BRANCH}..."
git merge "${MAIN_BRANCH}"

echo "Done. Updates merged into your working branch."
echo "Resolve conflicts if prompted, then commit."
