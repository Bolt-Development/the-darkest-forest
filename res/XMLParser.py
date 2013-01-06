import xml.etree.ElementTree as ET

class XMLParser(object):

    def get_root_element(self, filepath):
        pass
    def parse(self, filepath, type_name):
        """
        parse(filepath, type_name)
        filepath = path of .xml file
        type_name = name of the enemy, item, etc that you will be extracting
        Return:
        -> Will return a dictionary containing the attributes contained within the element root_name
        """
        tree = ET.parse(filepath)
        root = tree.getroot()
        print root.tag

if __name__ == '__main__':
    from ResourceLoader import *

    xml_resource = ResourceLoader().load_resource_by_name_and_type('enemies', 'other')

    XMLParser().parse(xml_resource.path, "SuperBadGuy")