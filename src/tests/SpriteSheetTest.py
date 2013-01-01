from TestingUtils import *

class SpriteSheetView(object):
    def __init__(self, model):
        self.model = model

        self.x, self.y = 0, 0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.rotation = 0

    def on_render(self, event, **kwargs):
        surface = kwargs['surface']

        width = self.model.surface.get_width() * self.scale_x
        height = self.model.surface.get_height() * self.scale_y

        pygame.Surface.blit(surface,
                            self.model.surface,
                            [self.x, self.y, width, height])

        
if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()
    
    from models.Engine import *
    from models.ImageModels import *

    from ResourceLoader import *

    def on_init(event, **kwargs):
        engine = kwargs['emitter']
        resource = ResourceLoader().load_resource_by_name_and_type('pixelland', 'image')
        model = SpriteSheetModel(resource)
        view = SpriteSheetView(model)
        
        engine.on('render', view.on_render)

    
    engine = Engine()
    engine.set_caption('Sprite Sheet Testing')
    engine.on('init', on_init, memory=True)
    engine.start()
