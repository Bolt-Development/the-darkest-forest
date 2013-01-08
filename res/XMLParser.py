import xml.etree.ElementTree as ET

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
            element = ET.Element(tag=child.tag, attrib=child.attrib)
            result.append(element)

        return result

if __name__ == '__main__':
    pass