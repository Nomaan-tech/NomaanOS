"""Robust runner: prefer main(); then try run() with no args; then run(name)."""
from importlib import import_module
import inspect, os, pkgutil

PKG = "nomaanos.modules"

def list_modules():
    out = []
    try:
        pkg = import_module(PKG)
        p = os.path.dirname(pkg.__file__)
        for f in sorted(os.listdir(p)):
            if f.endswith(".py") and not f.startswith("__") and f != "runner.py":
                out.append(f[:-3])
    except Exception:
        try:
            for finder, name, ispkg in pkgutil.iter_modules(import_module("nomaanos").__path__):
                # names may include modules not in modules package; filter later if needed
                pass
        except Exception:
            pass
    return out

def _import_module_by_name(name):
    if not name:
        return None
    candidates = [
        f"{PKG}.{name}",
        f"nomaanos.{name}",
        name,
    ]
    last = None
    for c in candidates:
        try:
            return import_module(c)
        except Exception as e:
            last = e
    # final attempt (relative)
    try:
        return import_module(f"nomaanos.modules.{name}")
    except Exception as e:
        raise ImportError(f"Could not import module {name}: {last}") from last

def _call_entrypoint(mod, name):
    """Call main()/run() in a tolerant order."""
    if mod is None:
        raise RuntimeError("No module to call")

    # prefer main()
    if hasattr(mod, "main") and callable(getattr(mod, "main")):
        main_fn = getattr(mod, "main")
        try:
            sig = inspect.signature(main_fn)
            if len(sig.parameters) == 0:
                return main_fn()
            else:
                return main_fn(name)
        except Exception:
            # last-resort call
            return main_fn()

    # then try run() - first try no-arg, then try single-arg
    if hasattr(mod, "run") and callable(getattr(mod, "run")):
        run_fn = getattr(mod, "run")
        # try no-arg first (safe)
        try:
            return run_fn()
        except TypeError:
            # then try with name
            try:
                return run_fn(name)
            except Exception:
                # re-raise last error
                raise

    # module itself callable?
    if callable(mod):
        try:
            return mod()
        except TypeError:
            return mod(name)

    raise RuntimeError(f"No callable entrypoint found in module {mod!r}")

def run(name):
    if not name:
        raise ValueError("module name required, e.g. 'nomaanos run sysinfo'")
    mod = _import_module_by_name(name)
    return _call_entrypoint(mod, name)
