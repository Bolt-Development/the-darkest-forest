from TestingUtils import *

class SpriteSheetView(object):
    def __init__(self, model):
        self.model = model

    def on_render(self, event, **kwargs):
        surface = kwargs['surface']

        
if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()
    
    from models.Engine import *
    from models.ImageModels import *

    from ResourceLoader import *

    def on_init(event, **kwargs):
        engine = kwargs['emitter']

        resource = ResourceLoader.load_resource_by_name_type('spritesheet', 'image')
        model = SpriteSheetModel(resource)
        view = SpriteSheetView(model)
        
        engine.on('render', view.on_render)

    
    engine = Engine()
    engine.set_caption('Sprite Sheet Testing')
    engine.on('init', on_init, memory=True)
    engine.start()
