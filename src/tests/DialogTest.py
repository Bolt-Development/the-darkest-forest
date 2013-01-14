from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from common.Scene import *
    from common.Stage import *
    from common.Transitions import *

    
    from common.gui.Buttons import *
    from common.gui.Dialogs import *
    from models.TextModels import *
    from views.TextViews import *
    from ResourceLoader import *
    
    fonts = ResourceLoader().load_resources_by_type('font')

    import random
    font = fonts[random.randint(0, len(fonts) - 1)]

    def on_init(event, **kwargs):
        dialog = Dialog(TextModel(font, 'Make a choice, please. The choice ' +
                                        'you make is not as important as ' +
                                        'making the choice.\n\nIt is better to ' +
                                        'do something and be afraid, than to ' +
                                        'live with the fear of doing it.', 24), 625, 'okay', 'cancel')
        
        choose = ChooseDialog(TextModel(font, 'Choose your difficulty', 24), 'easy', 'medium', 'hard')

        def on_okay(event, **kwargs):
            scene.add_child(choose)

        def on_changed(event, **kwargs):
            dialog.center(scene)
        dialog.on('changed', on_changed)
        dialog.on('okay', on_okay)

        scene.add_child(dialog)
    
    stage = Stage()
    
    scene = Scene("Dialog Scene")
    scene.width = stage.width
    scene.height = stage.height
    scene.fill_color=(132, 134, 0)
    scene.on('init', on_init)

    stage.start(scene)
    
    

