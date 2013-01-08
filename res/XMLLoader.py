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
            for name in XMLParser().extract(resource_path):
                self.xml_resources.append(XMLResource(name, resource_path))



    def load_resources_by_type(self, type):
        print type

    def load_resource_by_name_and_type(self, name, type):
        print name, type

    def print_resources(self):
        for res in self.xml_resources:
            print [res.name, res.type]

class XMLResource(object):
    def __init__(self, name, file):
        assert file.endswith(".xml"), "This ain't no XML bro"

        self.name = name
        self.filepath = file
        self.type = XMLParser().get_typename(self.filepath)

    def load(self):
        pass


