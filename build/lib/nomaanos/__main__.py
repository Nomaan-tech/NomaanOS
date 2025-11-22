# small compatibility __main__ so `python -m nomaanos` works
# it calls package-level main() and exits with its return code.
from . import main as _main
if __name__ == "__main__":
    raise SystemExit(_main())
