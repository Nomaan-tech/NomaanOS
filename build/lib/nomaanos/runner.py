import os
import importlib

MODULE_DIR = "src/nomaanos/modules"

def list_modules():
    if not os.path.exists(MODULE_DIR):
        return []
    return [f.replace(".py", "") for f in os.listdir(MODULE_DIR)
            if f.endswith(".py") and f not in ["__init__.py"]]

def run_module(name):
    if name not in list_modules():
        return f"Module '{name}' not found."

    mod = importlib.import_module(f"src.nomaanos.modules.{name}")

    if not hasattr(mod, "main"):
        return f"Module '{name}' has no main() function."

    return mod.main()
