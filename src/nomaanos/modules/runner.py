"""
Runner module for NomaanOS
Provides:
 - list_modules(): list available module filenames (without .py)
 - run(name): import src.nomaanos.modules.<name> and call its main()
"""
import os
import importlib

MODULE_DIR = "src/nomaanos/modules"

def list_modules():
    """Return list of module names without .py extension."""
    if not os.path.exists(MODULE_DIR):
        return []
    files = []
    for f in os.listdir(MODULE_DIR):
        # only python files, ignore __init__ and runner itself
        if not f.endswith(".py"):
            continue
        if f in ("__init__.py", "runner.py"):
            continue
        name = f[:-3]
        files.append(name)
    return sorted(files)

def run(name):
    """Import module and call its main() function. Return message or result."""
    if name not in list_modules():
        return f"Module '{name}' not found."

    mod_path = f"src.nomaanos.modules.{name}"
    try:
        mod = importlib.import_module(mod_path)
    except Exception as e:
        return f"Failed to import {mod_path}: {e}"

    if not hasattr(mod, "main"):
        return f"Module '{name}' has no main() function."

    try:
        result = mod.main()
    except Exception as e:
        return f"Error running module '{name}': {e}"

    return result
