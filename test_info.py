#!/usr/bin/env python3
import subprocess, json, sys, shlex

candidates = [
    ["nomaanos", "sysinfo"],
    ["nomaanos", "run", "sysinfo"],
    ["nomaanos", "info"],
    ["python3", "-m", "nomaanos", "sysinfo"],
    ["python3", "-m", "nomaanos", "info"],
]

def try_call(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=6)
        s = out.decode().strip()
        return s
    except Exception as e:
        return None

for cmd in candidates:
    s = try_call(cmd)
    print("TRY:", " ".join(shlex.quote(c) for c in cmd), "=>", "len(stdout)=", len(s) if s is not None else "ERR")
    if not s:
        continue
    # quick sanity: must start with '{' or '['
    s_stripped = s.lstrip()
    if not s_stripped:
        print("  empty output, skipping")
        continue
    if s_stripped[0] not in ('{','['):
        print("  not JSON (first char):", repr(s_stripped[:60]))
        continue
    try:
        data = json.loads(s)
    except Exception as e:
        print("  json.loads failed:", e)
        print("  raw:", s[:800])
        continue
    print("  JSON parsed OK. Keys:", list(data.keys()) if isinstance(data, dict) else "list")
    # validate required fields
    if isinstance(data, dict) and "project" in data and "time" in data:
        print("TEST PASSED: project/time found:", data.get("project"), data.get("time"))
        sys.exit(0)
    else:
        print("  missing project/time ->", list(data.keys()) if isinstance(data, dict) else "non-dict")
print("NO VALID JSON RESULT FOUND FROM CANDIDATES")
sys.exit(2)
