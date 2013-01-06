import xml.etree.ElementTree as ET

class XMLParser(object):

    def get_type_element(self, root_element):
        # Test
        return "enemy"
    def parse(self, resource, name):
        """
        parse(filepath, type_name)
        filepath = path of .xml file
        name = name of the enemy, item, etc that you will be extracting
        Return:
        -> Will return a dictionary containing the attributes contained within the element root_name
        """
        result_dict = {}

        tree = ET.parse(resource.path)
        root = tree.getroot()
        for child in root.findall(resource.type):
            if child.get("name") == name:
                for attribute in child:
                    result_dict[attribute.tag] = attribute.text

        return result_dict

if __name__ == '__main__':
    from ResourceLoader import *

    xml_resource = ResourceLoader().load_resource_by_name_and_type('enemies', 'enemy')

    attributes = XMLParser().parse(xml_resource, "SuperScaryGuy")
    print "hp:", attributes["hp"]
    print "damage:", attributes["damage"]