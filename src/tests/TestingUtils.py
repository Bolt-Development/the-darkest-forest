import os
import sys

def add_source_folder():
    sys.path.insert(0, os.path.normpath(os.path.join(os.getcwd(), "..")))
