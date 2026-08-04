#!/usr/bin/env bash
# publish.sh — regenerate index.html, commit, and push an ai-learning-journey update
# in one call. Push uses the gh CLI as the git credential helper (logged in & valid
# in the WorkBuddy sandbox since 2026-07-23); falls back to the openssl backend on
# the intermittent schannel TLS failure. The token never lands in .git/config.
#
# Usage:  bash publish.sh <repo-path> "<commit message>"
# Requires: git, gh (logged in), and a python interpreter (override with $PYTHON).

set -euo pipefail

REPO="${1:-$(git rev-parse --show-toplevel 2>/dev/null)}"
if [ -z "$REPO" ]; then
  REPO="D:/Project/workspace/my_github/ai-learning-journey"
fi
MSG="${2:-chore: update learning journey content}"
PY="${PYTHON:-$(command -v python3 || command -v python || echo python)}"

cd "$REPO" || { echo "ERROR: cannot cd into $REPO"; exit 1; }

echo "==> repo: $(pwd)"
echo "==> branch: $(git branch --show-current)"
echo "==> python: $PY"

echo "==> regenerating index.html"
"$PY" scripts/generate_index.py 2>&1 | tail -4 || echo "WARN: generator reported issues (continuing)"

echo "==> git status (pre-add)"
git status --short

echo "==> staging all changes"
git add -A

echo "==> commit"
git -c user.name="70asunflower" -c user.email="1982043113@qq.com" \
  commit -m "$MSG" 2>&1 | tail -6 || echo "NOTE: nothing to commit"

echo "==> pushing via gh credential helper"
GH_PUSH() {
  git -c credential.helper="!gh auth git-credential" \
    push origin "$(git branch --show-current)" 2>&1 | tail -12
}
if ! GH_PUSH; then
  echo "==> gh-helper push failed; retrying with openssl backend (schannel workaround)"
  git -c http.sslBackend=openssl -c credential.helper="!gh auth git-credential" \
    push origin "$(git branch --show-current)" 2>&1 | tail -12 \
    || { echo "ERROR: push failed on both attempts"; exit 1; }
fi

echo "==> remote URL (must be clean, no token):"
git remote -v
echo "==> DONE"
