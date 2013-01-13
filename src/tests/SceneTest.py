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
            ScrollTransition(menu1, menu2).start()
            print 'click'
    
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
        def on_scene_back(event, **kwargs):
            ScrollTransition(menu2, menu2.last).start()

        def show_scene_one(event, **kwargs):
            ScrollTransition(inner_scene2, inner_scene).start()

        def show_scene_two(event, **kwargs):
            ScrollTransition(inner_scene, inner_scene2, None, 'random').start()
            
            
        button2 = Button(TextModel(font, "Go Back To Main Menu", 24))
        button2.on('mouse_clicked', on_scene_back)
        menu2.add_child(button2)

        inner_scene = Scene('Inner Scene 1')
        inner_scene.fill_color=(0, 0, 255)
        inner_scene.x = 300
        inner_scene.y = 150
        inner_scene.width = 200
        inner_scene.height = 150

        inner_scene2 = Scene('Inner Scene 2')
        inner_scene2.fill_color=(0, 255, 255)
        inner_scene2.width = inner_scene.width
        inner_scene2.height = inner_scene.height

        scene_1 = Button(TextModel(font, 'Show Scene One', 16))
        scene_2 = Button(TextModel(font, 'Show Scene Two', 16))

        scene_1.on('mouse_clicked', show_scene_one)
        scene_2.on('mouse_clicked', show_scene_two)

        scene_1.x = inner_scene.x - scene_1.width - 14
        scene_2.x = scene_1.x

        scene_1.y = inner_scene.y
        scene_2.y = scene_1.y + scene_1.height + 15

        inner_scene.add_child(Button(TextModel(font, 'Scene One', 18)))
        inner_scene2.add_child(Button(TextModel(font, 'Scene Two', 18)))
        
        menu2.add_child(inner_scene)
        menu2.add_child(scene_1)
        menu2.add_child(scene_2)

    def on_render(event, **kwargs):
        print event, kwargs

    
    stage = Stage()
    
    menu1 = Scene("Menu One")
    menu1.width = stage.width
    menu1.height = stage.height
    menu1.fill_color=(132, 134, 0)
    menu1.on('init', on_init)

    menu2 = Scene("Menu Two")
    menu2.width = stage.width
    menu2.height = stage.height
    menu2.fill_color=(132, 134, 127)
    menu2.on('init', on_init2)

    stage.start(menu1)
    
    

