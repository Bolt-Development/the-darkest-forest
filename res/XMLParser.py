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



        for element in root:
            if element.tag == name:
                for child in element:
                    for type in types:
                        if child.tag == type:
                            print child.tag
                        else:
                            setattr(model, child.tag, child.text)

        return model

if __name__ == '__main__':
    pass