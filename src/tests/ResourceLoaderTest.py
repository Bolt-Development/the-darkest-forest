from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from ResourceLoader import *

    loader = ResourceLoader()
    loader.load_resource('bomb')
