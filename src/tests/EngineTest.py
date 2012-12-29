if __name__ == '__main__':
    import sys
    import os
    
    up_one_folder = os.sep.join(sys.path[0].split('\\')[:-1])
    
    if up_one_folder.endswith('src') and not up_one_folder in sys.path:
        sys.path.insert(0, up_one_folder)

    from models.Engine import *

    def on_event(event, **kwargs):
        print event, kwargs
    
    
    engine = Engine()
    engine.set_caption('Engine Debug Testing')
    engine.on('tick', on_event)
    engine.on('render', on_event)
    engine.start()
