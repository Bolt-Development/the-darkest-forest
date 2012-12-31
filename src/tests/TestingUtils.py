import os
import sys

def add_source_folder():
    path = os.path.normpath(os.path.join(os.getcwd(), ".."))

    if path not in sys.path:
        sys.path.insert(0, path)
