import os
import sys

def add_source_folder():
    add_to_path(os.path.normpath(os.path.join(os.getcwd(), "..")))

def add_to_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

def add_resource_folder():
    add_to_path(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..//..', 'res')))