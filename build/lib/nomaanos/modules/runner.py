"""
Robust runner: tries multiple import paths so both 'pip installed' and
'development workspace (src/...)' layouts work.
Provides list_modules() and run(name).
"""
import importlib
import os

MODULE_DIR = "src/nomaanos/modules"

def _try_import_module_candidates(name):
    """
    Try import candidates in order:
     - nomaanos.modules.<name>    (installed package)
     - src.nomaanos.modules.<name> (dev layout used earlier)
     - relative import .<name> from this package
    Return imported module or raise ImportError.
    """
    candidates = [
        f"nomaanos.modules.{name}",
        f"src.nomaanos.modules.{name}",
        f".{name}"
    ]
    last_err = None
    for cand in candidates:
        try:
            # if cand starts with dot, treat as package-relative
            if cand.startswith("."):
                mod = importlib.import_module(cand, __name__)
            else:
                mod = importlib.import_module(cand)
            return mod
        except Exception as e:
            last_err = e
            # continue to next candidate
            continue
    # nothing worked
    raise ImportError(f"Failed to import module {name}; last error: {last_err}") from last_err

def list_modules():
    """
    List available module filenames in dev layout if present,
    otherwise return empty list (runner can still be used).
    """
    files = []
    # prefer dev filesystem listing if exists
    try:
        base = os.path.join(os.getcwd(), "src", "nomaanos", "modules")
        if os.path.isdir(base):
            for f in sorted(os.listdir(base)):
                if f.endswith(".py") and f not in ("__init__.py", "runner.py"):
                    files.append(f.replace(".py", ""))
            return files
    except Exception:
        pass
    # fallback: return empty list (installed package can still run known modules)
    return []

def run(name):
    """
    Import the module by name (using flexible candidate list) and call its main()/run()/entrypoint.
    Accepts modules that define:
      - def main(): -> returns or prints
      - or def run(): -> returns or prints
    """
    mod = _try_import_module_candidates(name)
    # prefer main(), then run()
    for attr in ("main", "run"):
        if hasattr(mod, attr):
            fn = getattr(mod, attr)
            try:
                return fn()
            except TypeError:
                # if function expects args, call with name
                try:
                    return fn(name)
                except Exception as e:
                    raise
    raise AttributeError(f"Module '{name}' has no callable main() or run().")
