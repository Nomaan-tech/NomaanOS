#!/usr/bin/env python3
# Robust NomaanOS CLI — imports runner module via importlib to avoid collisions

import sys
import importlib

# prefer core/helpers from your package
try:
    from src.nomaanos.core import info, hello
    from src.nomaanos import config
except Exception:
    # graceful fallback if running from different CWD in Termux/proot
    # don't fail here — we'll surface import errors later
    info = lambda: {"error": "core not available"}
    hello = lambda name="Nomaan": f"Hello, {name}!"
    class _FakeConfig:
        def load(self): return {}
        def save(self, cfg): return True
    config = _FakeConfig()

RUNNER_MODULE_PATH = "src.nomaanos.modules.runner"

def _get_runner():
    """Import runner module dynamically and return it (or None)."""
    try:
        mod = importlib.import_module(RUNNER_MODULE_PATH)
        return mod
    except Exception as e:
        print(f"[ERROR] cannot import runner module ({RUNNER_MODULE_PATH}): {e}")
        return None

def cmd_info():
    try:
        print(info())
    except Exception as e:
        print("[ERROR] info():", e)

def cmd_hello(args):
    name = args[0] if args else "Nomaan"
    try:
        print(hello(name))
    except Exception as e:
        print("[ERROR] hello():", e)

def cmd_config():
    try:
        print("NomaanOS Config:", config.load())
    except Exception as e:
        print("[ERROR] config.load():", e)

def cmd_set(args):
    if len(args) < 2:
        print("Usage: nomaan set <key> <value>")
        return
    key = args[0]
    value = args[1]
    # Simple auto-typing
    if isinstance(value, str):
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.isdigit():
            try:
                value = int(value)
            except Exception:
                pass
    try:
        cfg = config.load()
    except Exception:
        cfg = {}
    cfg[key] = value
    try:
        config.save(cfg)
    except Exception as e:
        print("[WARN] config.save() failed:", e)
    print("Updated:", cfg)

def cmd_modules():
    runner = _get_runner()
    if not runner:
        return
    # prefer runner.list_modules() if available
    if hasattr(runner, "list_modules"):
        try:
            print("Available modules:", runner.list_modules())
            return
        except Exception as e:
            print("[ERROR] runner.list_modules():", e)
    # fallback: try modules package wrapper
    try:
        mod_pkg = importlib.import_module("src.nomaanos.modules")
        if hasattr(mod_pkg, "list_modules"):
            print("Available modules:", mod_pkg.list_modules())
            return
    except Exception:
        pass
    print("[INFO] No modules found or runner missing list_modules().")

def cmd_run(args):
    if not args:
        print("Usage: nomaan run <module>")
        return
    name = args[0]
    runner = _get_runner()
    if not runner:
        return
    if not hasattr(runner, "run"):
        print("[ERROR] runner missing run()")
        return
    try:
        result = runner.run(name)
        if result is not None:
            print(result)
    except Exception as e:
        print(f"[ERROR] running module '{name}':", e)

def main():
    if len(sys.argv) == 1:
        print("NomaanOS CLI: try 'info', 'hello <name>', 'config', 'set <k> <v>', 'modules', 'run <module>'")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "info":
        cmd_info()
    elif cmd == "hello":
        cmd_hello(args)
    elif cmd == "config":
        cmd_config()
    elif cmd == "set":
        cmd_set(args)
    elif cmd == "modules":
        cmd_modules()
    elif cmd == "run":
        cmd_run(args)
    else:
        print("Unknown command:", cmd)

if __name__ == "__main__":
    main()
