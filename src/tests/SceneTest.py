from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from common.Scene import *
    from common.Stage import *

    
    from common.gui.Buttons import *
    from models.TextModels import *
    from ResourceLoader import *
    
    fonts = ResourceLoader().load_resources_by_type('font')

    import random
    font = fonts[random.randint(0, len(fonts) - 1)]

    def print_event(event, **kwargs):
        print event

    def on_init(event, **kwargs):
        menu1.add_child(Button(TextModel(font, "Click Me", 24)))

    def on_render(event, **kwargs):
        print event, kwargs

    menu1 = Scene("Menu One")
    menu1.on('init', on_init)
   # menu1.on('render', on_render)
    
    stage = Stage()
    stage.start(menu1)
    
    

