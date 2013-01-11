from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from common.Scene import *
    from common.Stage import *
    from common.Transitions import *

    
    from common.gui.Buttons import *
    from models.TextModels import *
    from ResourceLoader import *
    
    fonts = ResourceLoader().load_resources_by_type('font')

    import random
    font = fonts[random.randint(0, len(fonts) - 1)]

    def print_event(event, **kwargs):
        print event

    def on_init(event, **kwargs):
        def on_click(event, **kwargs):
            if next_scene.parent == menu1:
                menu1.remove_child(next_scene)
                button.text = 'oops, click me again to bring it back!'
            else:
                menu1.add_child(next_scene)
                button.text = 'Click me'
                
            button.x = stage.width * 0.5 - button.width * 0.5
            button.y = stage.height * 0.5 - button.height * 0.5

        def on_scene_next(event, **kwargs):
            ScrollTransition(menu1, menu2).start(stage)
    
        button = Button(TextModel(font, "Click Me", 24))
        button.on('mouse_clicked', on_click)

        next_scene = Button(TextModel(font, 'Next Scene', 24))
        next_scene.on('mouse_clicked', on_scene_next)

        button.x = stage.width * 0.5 - button.width * 0.5
        button.y = stage.height * 0.5 - button.height * 0.5

        next_scene.x = stage.width * 0.5 - button.width * 0.5
        next_scene.y = button.y + button.height + 10
        
        menu1.add_child(button)
        menu1.add_child(next_scene)

    def on_init2(event, **kwargs):
        button2 = Button(TextModel(font, "Go Back To Main Menu", 24))
        menu2.add_child(button2)

    def on_render(event, **kwargs):
        print event, kwargs

    menu1 = Scene("Menu One")
    menu1.on('init', on_init)

    menu2 = Scene("Menu Two")
    menu2.on('init', on_init2)
    
    stage = Stage()
    stage.start(menu1)
    
    

