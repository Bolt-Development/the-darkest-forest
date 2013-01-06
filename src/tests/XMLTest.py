from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from ResourceLoader import *
    from XMLParser import *

    xml_resource = ResourceLoader().load_resource_by_name_and_type('enemies', 'enemy')

    attributes = XMLParser().parse(xml_resource, "SuperScaryGuy")
    print "hp:", attributes["hp"]
    print "damage:", attributes["damage"]
