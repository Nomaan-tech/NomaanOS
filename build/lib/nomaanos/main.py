import sys
from nomaanos.core import info, hello
from nomaanos.config import load, save
from nomaanos.modules import run as run_module, list_modules

def main():
    if len(sys.argv) == 1:
        print("NomaanOS CLI: try 'info', 'hello <name>', 'config', 'get <key>', 'set <key> <value>', 'modules', or 'run <module>'")
        return

    cmd = sys.argv[1]

    if cmd == "info":
        print(info())

    elif cmd == "hello":
        name = sys.argv[2] if len(sys.argv) > 2 else "Nomaan"
        print(hello(name))

    elif cmd == "modules":
        print("Available modules:", list_modules())

    elif cmd == "run":
        if len(sys.argv) < 3:
            print("Usage: nomaanos run <module>")
            return
        module = sys.argv[2]
        print(run_module(module))

    else:
        print("Unknown command:", cmd)

if __name__ == "__main__":
    main()
