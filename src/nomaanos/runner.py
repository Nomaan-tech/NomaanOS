"""
Minimal runner module for nomaanos.
Provides:
 - list_modules() -> list of available module names
 - run(name=None) -> if name is None return info, else run named module
 - info() -> returns dict with basic info (printed as JSON by caller)
"""
import json, time, platform

def list_modules():
    # discover modules under the package that are importable
    try:
        import pkgutil, importlib
        pkg = importlib.import_module("nomaanos")
        pkgpath = getattr(pkg, "__path__", [])
        names = []
        for finder, name, ispkg in pkgutil.iter_modules(pkgpath):
            if name.startswith("_"):
                continue
            # only top-level modules representing commands
            names.append(name)
        return sorted(names)
    except Exception:
        # fallback: hardcode common ones if discovery fails
        return ["hello", "sysinfo"]

def info():
    return {
        "project": "NomaanOS",
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user": "unknown",
        "python": platform.python_version(),
        "platform": platform.platform(),
    }

def run(name=None):
    """
    If name is None -> return info() dict
    If name is provided -> try to import nomaanos.modules.<name> and call its main()/run()
    """
    if not name:
        return info()
    # allow submodule name like "sysinfo" to be run
    modname = f"nomaanos.modules.{name}"
    try:
        mod = __import__(modname, fromlist=["*"])
    except Exception as e:
        return {"error": f"cannot import module {name}: {e}"}
    # prefer main()
    if hasattr(mod, "main") and callable(getattr(mod, "main")):
        try:
            return mod.main()
        except TypeError:
            # try calling without args
            try:
                return mod.main()
            except Exception as ee:
                return {"error": f"calling main() failed: {ee}"}
    if hasattr(mod, "run") and callable(getattr(mod, "run")):
        try:
            return mod.run()
        except Exception as ee:
            return {"error": f"calling run() failed: {ee}"}
    # if module is itself callable (rare)
    if callable(mod):
        try:
            return mod()
        except Exception as ee:
            return {"error": f"calling module failed: {ee}"}
    return {"error": "no callable entrypoint in module"}
