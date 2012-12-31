from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    
    from models.Engine import *
    from models.space.Grid import *
    from models.space.Tile import *

    grid = None

    def on_init(event, **kwargs):
        print 'here'

    def on_render(event, **kwargs):
        print 'render'

    
    engine = Engine()
    engine.set_caption('Grid Testing')
    engine.on('init', on_init, memory=True)
    engine.on('render', on_render)
    engine.start()
