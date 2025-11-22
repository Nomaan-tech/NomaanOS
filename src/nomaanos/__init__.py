"""
Compatibility shim for nomaanos package.
Exports:
 - main() callable (if available in repo)
 - run(name)         flexible wrapper handling runner.run with 0 or 1 args
 - info()            tries common providers
 - get_runner_module() for introspection
"""
import importlib
import inspect
import sys

__all__ = ["main", "run", "info", "get_runner_module"]

def _try_import(name):
    """Try common import variants and return module or None."""
    candidates = [
        f"nomaanos.{name}",
        name,
        f"src.nomaanos.{name}",
        f"src.{name}",
    ]
    for c in candidates:
        try:
            return importlib.import_module(c)
        except Exception:
            continue
    return None

# pick main-like module (main/core/runner)
_main_mod = _try_import("main") or _try_import("core") or _try_import("runner")
_runner_mod = _try_import("runner") or _main_mod

# expose callable main (prefer module.main() if present)
def _get_main_callable():
    if _main_mod is None:
        return None
    # if module defines a function named main, use it
    if hasattr(_main_mod, "main") and callable(getattr(_main_mod, "main")):
        return getattr(_main_mod, "main")
    # if module itself is callable (rare), return as-is
    if callable(_main_mod):
        return _main_mod
    # fallback: if runner module defines run, wrap it as main default
    if hasattr(_main_mod, "run") and callable(getattr(_main_mod, "run")):
        run_fn = getattr(_main_mod, "run")
        # create wrapper that accepts no args when called as main()
        def main_wrapper():
            # if run expects one arg, call with default module name or empty
            try:
                sig = inspect.signature(run_fn)
                if len(sig.parameters) == 0:
                    return run_fn()
                else:
                    return run_fn("")  # pass empty name
            except Exception:
                return run_fn()
        return main_wrapper
    return None

main = _get_main_callable()

# If still None, provide helpful stub (avoid TypeError)
def _main_stub(*a, **kw):
    return {"error": "no callable main() available in nomaanos package", "args": (a, kw)}
if main is None:
    main = _main_stub

def run(name):
    """
    Flexible run(name) that delegates to runner.run.
    If runner.run expects 0 args, it will be called without args.
    If it expects 1 arg, it will be called with `name`.
    If no runner found, raise helpful error.
    """
    if _runner_mod is None:
        raise RuntimeError("no runner module found (expected nomaanos.runner or main/core)")

    if hasattr(_runner_mod, "run") and callable(getattr(_runner_mod, "run")):
        run_fn = getattr(_runner_mod, "run")
        try:
            sig = inspect.signature(run_fn)
            if len(sig.parameters) == 0:
                return run_fn()
            else:
                return run_fn(name)
        except Exception:
            # last resort: try both ways
            try:
                return run_fn(name)
            except TypeError:
                return run_fn()
    # fallback if module itself is callable
    if callable(_runner_mod):
        try:
            return _runner_mod(name)
        except TypeError:
            return _runner_mod()
    raise RuntimeError("runner has no callable run")

def info():
    # try common info providers
    for candidate in ("info", "sysinfo", "get_info"):
        m = _try_import(candidate)
        if m is not None and hasattr(m, candidate) and callable(getattr(m, candidate)):
            try:
                return getattr(m, candidate)()
            except Exception as e:
                return {"error": f"info() raised: {e}"}
    # try main/core module for info()
    for mod in (_main_mod, _runner_mod):
        if mod is not None and hasattr(mod, "info") and callable(getattr(mod, "info")):
            try:
                return getattr(mod, "info")()
            except Exception as e:
                return {"error": f"info() raised: {e}"}
    return {"project": "nomaanos", "note": "no info() provider found"}

def get_runner_module():
    return _runner_mod

# Keep module-level import nice for CLI script that does: from nomaanos import main
