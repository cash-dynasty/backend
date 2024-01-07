import os
import sys


def inject_source_path():
    """Injects the source path to sys.path."""
    sys.path.append(os.getcwd())
    sys.path.append("./app")
