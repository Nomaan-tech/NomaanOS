#!/bin/sh
set -eu

echo "=== which nomaanos ==="
which nomaanos || echo "(not found)"

echo
echo "=== show installed script (if exists) ==="
if command -v nomaanos >/dev/null 2>&1; then
  echo "Path: $(command -v nomaanos)"
  echo "---- head of this file ----"
  head -n 80 "$(command -v nomaanos)" || true
  echo "---- end head ----"
fi

try_cmd() {
  echo
  echo ">>> RUN: $*"
  outfile=$(mktemp)
  errfile=$(mktemp)
  set +e
  "$@" >"$outfile" 2>"$errfile"
  rc=$?
  set -e
  echo "EXIT CODE: $rc"
  echo "--- STDOUT ---"
  sed -n '1,200p' "$outfile" || true
  echo "--- STDERR ---"
  sed -n '1,200p' "$errfile" || true
  echo "-------------"
  rm -f "$outfile" "$errfile"
}

# Try multiple invocations (these have been relevant in your logs)
try_cmd nomaanos sysinfo || true
try_cmd nomaanos info || true
try_cmd nomaanos run sysinfo || true
try_cmd python3 -m nomaanos sysinfo || true
try_cmd python3 -c "import nomaanos; print(getattr(nomaanos, '__file__', 'module-file-not-found'))" || true

echo
echo "DEBUG DONE"
