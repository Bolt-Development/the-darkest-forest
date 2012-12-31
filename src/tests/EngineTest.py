if __name__ == '__main__':
    import sys
    import os

    sys.path.insert(0, os.path.normpath(os.path.join(os.getcwd(), "..")))

    from models.Engine import *

    def on_event(event, **kwargs):
        print event, kwargs
    
    
    engine = Engine()
    engine.set_caption('Engine Debug Testing')
    engine.on('tick', on_event)
    engine.on('render', on_event)
    engine.start()
