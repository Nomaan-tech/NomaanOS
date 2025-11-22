# modules package API wrapper — export run(name) and list_modules()
# This lazy-loads the real runner so installed + dev imports both work.
import importlib

__all__ = ["run", "list_modules"]

_runner = None
def _get_runner():
    global _runner
    if _runner is None:
        # try absolute package path first (for installed package)
        try:
            _runner = importlib.import_module("nomaanos.modules.runner")
        except Exception:
            # fallback to relative import (for dev environment)
            _runner = importlib.import_module(".runner", __name__)
    return _runner

def list_modules():
    """Return list of modules (delegates to runner.list_modules)."""
    return _get_runner().list_modules()

def run(name):
    """Run a module by name (delegates to runner.run)."""
    return _get_runner().run(name)
