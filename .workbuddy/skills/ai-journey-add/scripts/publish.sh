#!/usr/bin/env bash
# publish.sh — regenerate index.html, commit, and push an ai-learning-journey update
# in one call. Push uses the cached Windows Credential Manager token (gh is broken
# in the sandbox), injected via a one-shot insteadOf so it never lands in .git/config.
#
# Usage:  bash publish.sh <repo-path> "<commit message>"
# Requires: git, and a python interpreter (override with $PYTHON).

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

echo "==> extracting cached GCM credential (token not persisted)"
TOKEN=$(printf 'protocol=https\nhost=github.com\n' | git -c credential.helper=manager credential fill 2>/dev/null | sed -n 's/^password=//p')
if [ -z "$TOKEN" ]; then
  echo "ERROR: could not retrieve credential from Git Credential Manager."
  echo "       Fix on host PC: gh auth login, or ensure a github.com credential exists."
  exit 1
fi

echo "==> pushing via insteadOf rewrite"
git -c "url.https://70asunflower:$TOKEN@github.com/.insteadOf=https://github.com/" \
  push origin "$(git branch --show-current)" 2>&1 | tail -12

echo "==> remote URL (must be clean, no token):"
git remote -v
echo "==> DONE"
