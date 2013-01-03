from TestingUtils import *

        
if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()
    
    from models.Engine import *
    from models.TextModels import *

    from views.TextViews import *

    from ResourceLoader import *

    long_string = \
        """
            Jack Spicer: How many times can I say "my bad"? 

            Omi: I soon realized that the only way to return to the future was to wait. 
            [Clay, Kimiko and Jack's jaws drop] 
            Kimiko: You waited for a thousand years? 
            Omi: Exactly. 
            Kimiko: But you don't have wrinkles or liver spots, or... 
            Jack Spicer: Or that old people smell. 
            [Kimiko smacks him] 
            Jack Spicer: OW!
        """

    def on_init(event, **kwargs):
        engine = kwargs['emitter']
        
        fonts = ResourceLoader().load_resources_by_type('font')

        import random
        font = fonts[random.randint(0, len(fonts) - 1)]
        model = TextModel(font, text=long_string)
        view = ParagraphView(model)

        engine.on('render', view.on_render)
        engine.on('mouse_motion', view.on_mouse_motion)

    
    engine = Engine()
    engine.set_caption('Sprite Sheet Testing')
    engine.on('init', on_init, memory=True)
    engine.start()
