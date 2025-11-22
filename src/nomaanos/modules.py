# compatibility wrapper so imports like "from src.nomaanos import modules" work
from .modules import runner as _runner

def list_modules():
    return _runner.list_modules()

def run(name):
    return _runner.run(name)
