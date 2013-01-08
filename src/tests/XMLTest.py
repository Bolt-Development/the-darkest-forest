from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from ResourceLoader import *
    from XMLParser import *
    from XMLLoader import *

    XMLLoader().print_resources()

    badguy_resource = XMLLoader().load_resource_by_name_and_type("Enemy", "SuperScaryBadGuy")

    #badguy_config = badguy_resource.load()


