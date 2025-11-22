"""
Safe package initializer for nomaanos.
Expose a callable `main()` at package level and a `run(name)` helper.
"""
import importlib

def _call_from_candidates(candidates, name="main"):
    """Try candidate modules in order; return first callable found (function)"""
    for cand in candidates:
        try:
            m = importlib.import_module(f"nomaanos.{cand}")
        except Exception:
            continue
        # prefer a function named `main`
        if hasattr(m, "main") and callable(getattr(m, "main")):
            return getattr(m, "main")
        # fallback to run()
        if hasattr(m, "run") and callable(getattr(m, "run")):
            return getattr(m, "run")
        # if module itself is callable (rare) return a wrapper
        if callable(m):
            return m
    return None

def main(*args, **kwargs):
    """
    Package-level main() callable. Tries common candidate modules and calls them.
    This is what python -m nomaanos and console script will call.
    """
    candidates = ("main", "core", "runner")
    fn = _call_from_candidates(candidates)
    if fn is None:
        raise RuntimeError("no main() available in nomaanos package")
    # call function; if it accepts args, pass them; otherwise call without
    try:
        return fn(*args, **kwargs)
    except TypeError:
        return fn()

def run(name=None):
    """Run a named submodule: delegate to nomaanos.runner.run if present."""
    try:
        runner = importlib.import_module("nomaanos.runner")
        if hasattr(runner, "run") and callable(runner.run):
            return runner.run(name)
    except Exception:
        pass
    # fallback: try to import nomaanos.modules.<name> and call its main/run
    if not name:
        raise ValueError("no module name provided to run()")
    try:
        mod = importlib.import_module(f"nomaanos.modules.{name}")
    except Exception as e:
        return {"error": f"cannot import module {name}: {e}"}
    if hasattr(mod, "main") and callable(mod.main):
        try:
            return mod.main()
        except Exception as e:
            return {"error": f"calling main() failed: {e}"}
    if hasattr(mod, "run") and callable(mod.run):
        try:
            return mod.run()
        except Exception as e:
            return {"error": f"calling run() failed: {e}"}
    return {"error": "no callable entrypoint in module"}
