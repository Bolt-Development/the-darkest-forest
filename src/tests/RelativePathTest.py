from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()

    print sys.path
    # create a deep module
    from common.math.Collision import *

    
    collision = Collision()
