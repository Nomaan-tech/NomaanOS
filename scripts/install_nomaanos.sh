#!/usr/bin/env sh
set -e

# 1) go to repo root (adjust if your repo path is different)
REPO=~/workspace/nomaanos
if [ ! -d "$REPO" ]; then
  echo "ERROR: repo not found at $REPO"
  exit 1
fi
cd "$REPO"

echo ">>> cleaning previous installs (safe)"
python3 -m pip uninstall -y nomaanos >/dev/null 2>&1 || true
rm -f /data/data/com.termux/files/usr/bin/nomaanos >/dev/null 2>&1 || true

echo ">>> ensuring pyproject/setup exists"
if [ ! -f "pyproject.toml" ] && [ ! -f "setup.py" ] && [ ! -f "setup.cfg" ]; then
  echo "WARNING: no pyproject.toml or setup.py in repo root. Aborting."
  exit 1
fi

echo ">>> installing editable (so workspace changes reflect immediately)"
python3 -m pip install --upgrade pip wheel setuptools >/dev/null
python3 -m pip install -e . || {
  echo "pip install failed"
  exit 1
}

echo ">>> Done. Quick smoke tests:"
echo " - nomaanos info:"
nomaanos info || echo "nomaanos info failed"
echo " - nomaanos modules:"
nomaanos modules || echo "nomaanos modules failed"
echo " - nomaanos run sysinfo:"
nomaanos run sysinfo || echo "nomaanos run sysinfo failed"

echo "INSTALLER: finished."
