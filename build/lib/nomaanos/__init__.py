# package initializer - expose main() to entrypoints
try:
    from .core import main  # if your main lives in core.py
except Exception:
    # fallback - many repos define main() in __init__ or other module
    try:
        from .nomaan import main
    except Exception:
        # last fallback: import runner wrapper if provided
        try:
            from .runner import main
        except Exception:
            # If above fail, do nothing; installed CLI script will import actual main.
            pass
__all__ = ["main"]
