if __name__ == '__main__':
    import sys
    import os
    
    up_one_folder = os.sep.join(sys.path[0].split('\\')[:-1])

    if up_one_folder.endswith('src') and not up_one_folder in sys.path:
        sys.path.insert(0, up_one_folder)

    from common.math.Collision import *

    print sys.path

    
    collision = Collision()
