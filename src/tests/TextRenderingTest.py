from TestingUtils import *
import random

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from models.Engine import *
    from ResourceLoader import *

    from models.TextModels import *
    from views.TextViews import *

    fonts = ResourceLoader().load_resources_by_type('font')
    font = fonts[random.randint(0, len(fonts) - 1)]

    def on_init(event, **kwargs):
        engine = kwargs['emitter']
        print engine

        text = TextModel(font)
        view = TextView(text)
    
    
    engine = Engine()
    engine.set_caption('Text Rendering Testing')
    engine.on('init', on_init, memory=True)
    engine.start()
