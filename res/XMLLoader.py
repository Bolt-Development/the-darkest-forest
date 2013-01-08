import os
import fnmatch

from XMLParser import *
from models.XMLModel import *

def get_files(path):

    path = path + "/xml"
    result = []
    for path, dirs, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file.lower(), r'*.'+"xml"):
                result.append(os.path.join(path, file))
    return result


class XMLLoader(object):
    def __init__(self):
        self.resource_path = os.path.dirname(os.path.realpath(__file__))
        self.xml_resources = []
        for resource_path in get_files(self.resource_path):
            self.xml_resources.append(XMLParser().extract(resource_path))

    def load_resources_by_type(self, type):
        print type

    def load_resource_by_name_and_type(self, name, type):
        print name, type

class XMLResource(object):
    def __init__(self, file):
        assert file.endswith(".xml"), "This ain't no XML buddy"

        self.filepath = file

        self.type = XMLParser().get_typename(self.filepath)

    def load(self):
        return XMLModel()


