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
                        if child.tag == 'loot':
                            loot_model = LootModel()
                            for item in child:
                                loot_model.add(item.text)
                            setattr(model, child.tag, loot_model)
                        elif child.tag == type:
                            #setattr(model, child.tag, self.parse_child(child, types))
                            pass
                        else:
                            setattr(model, child.tag, child.text)

        return model

class LootModel(object):
    def __init__(self, contents=None):
        if contents is not None:
            self.contents = contents
        else:
            self.contents = []
    def add(self, item):
        self.contents.append(item)

if __name__ == '__main__':
    pass