from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from ResourceLoader import *

    loader = ResourceLoader()
    print loader.load_resource_by_name_and_type('bomb', 'audio')
