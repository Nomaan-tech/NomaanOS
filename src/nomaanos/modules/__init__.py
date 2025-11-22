# nomaanos.modules - compatibility wrapper
# Exposes list_modules() and run(name) for CLI and installs.
import importlib, os

__all__ = ["list_modules", "run"]

MODULE_DIR = os.path.dirname(__file__)

def _module_files():
    try:
        for f in os.listdir(MODULE_DIR):
            if not f.endswith(".py"):
                continue
            if f in ("__init__.py","runner.py"):
                continue
            yield f[:-3]
    except Exception:
        return []

def list_modules():
    """Return sorted list of candidate module names (filenames without .py)."""
    try:
        return sorted(_module_files())
    except Exception:
        return []

def _import_runner():
    # Try installed absolute path first (nomaanos.modules.runner)
    try:
        return importlib.import_module("nomaanos.modules.runner")
    except Exception:
        # fallback relative import (dev environment)
        try:
            return importlib.import_module(".runner", __package__)
        except Exception:
            return None

def run(name):
    """Run module by name. Delegates to runner if available, else tries to import module directly."""
    runner = _import_runner()
    if runner is not None and hasattr(runner, "run"):
        try:
            return runner.run(name)
        except Exception as e:
            return f"runner.run failed: {e}"
    # fallback: import module directly
    modname = f"nomaanos.modules.{name}"
    try:
        mod = importlib.import_module(modname)
    except Exception as e:
        return f"Failed to import {modname}: {e}"
    # Prefer main() then run()
    if hasattr(mod, "main"):
        try:
            return mod.main()
        except TypeError:
            # maybe main expects an argument
            try:
                return mod.main(name)
            except Exception as e:
                return f"module {name} main() failed: {e}"
        except Exception as e:
            return f"module {name} main() error: {e}"
    if hasattr(mod, "run"):
        try:
            return mod.run(name)
        except Exception as e:
            return f"module {name} run() error: {e}"
    return f"Module {name} has no callable main() or run()"
