from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from common.Scene import *
    from common.Stage import *
    from common.Transitions import *

    
    from common.gui.Buttons import *
    from models.ImageModels import *
    from models.TextModels import *
    from views.ImageView import *
    from ResourceLoader import *

    loader = ResourceLoader()
    
    chk_image = loader.load_resource_by_name_and_type('check', 'image')
    x_image = loader.load_resource_by_name_and_type('x', 'image')

    chk_view = ImageView(ImageModel(chk_image))
    x_view = ImageView(ImageModel(x_image))

    font = loader.load_resources_by_type('font')[0]

    stage = Stage()

    scene = Scene('Toggle and Slider Test')

    container = Scene('Options Container')
    container.draggable = True
    container.show_background = True
    container.width = 300
    container.height = 500
    
    toggle = Toggle(TextModel(font, 'Sound', 24))
    toggle.active_image = chk_view
    toggle.inactive_image = x_view
    toggle.x = 30
    toggle.y = 12
    container.add_child(toggle)

    scene.add_child(container)

    stage.start(scene)
