import xml.etree.ElementTree as ET
from models.XMLModel import *


class XMLParser(object):

    def get_typename(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        return root.attrib['typename']

    def extract(self, file):
        tree = ET.parse(file)
        root = tree.getroot()

        result = []
        for child in root:
            result.append(child.tag)

        return result

    def parse(self, name, file, types):
        model = XMLModel()

        tree = ET.parse(file)
        root = tree.getroot()
        for child in root:
            print child.tag, child.attrib

        return model

if __name__ == '__main__':
    pass