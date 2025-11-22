#!/usr/bin/env python3
"""
NomaanOS core — tiny starter module.
Run: python src/nomaanos/core.py
"""

from datetime import datetime
import platform
import os

def info():
    return {
        "project": "NomaanOS",
        "time": datetime.utcnow().isoformat() + "Z",
        "user": os.getenv("USER", "unknown"),
        "python": platform.python_version(),
        "platform": platform.platform()
    }

def hello(name="Nomaan"):
    return f"Hello, {name}! Welcome to NomaanOS. ({info()['time']})"

if __name__ == "__main__":
    print(hello())
    print("System info:", info())
