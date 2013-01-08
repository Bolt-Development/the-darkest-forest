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
        self.types = []
        for resource_path in get_files(self.resource_path):
            for element in XMLParser().extract(resource_path):
                self.xml_resources.append(XMLResource(element, resource_path))

            type = XMLParser().get_typename(resource_path)
            if type not in self.types:
                self.types.append(type)

    def load_resources_by_name(self, name):
        return [res for res in self.xml_resources if res.name == name]

    def load_resources_by_type(self, type):
        return [res for res in self.xml_resources if res.type == type]

    def load_resource_by_name_and_type(self, name, type):
        return [res for res in self.xml_resources if res.name == name and res.type == type][0]

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

        return XMLParser().parse(self.name, self.filepath, XMLLoader().types)


