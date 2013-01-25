from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from common.Scene import *
    from common.Stage import *
    from common.Transitions import *

    
    from common.gui.Layouts import *
    from common.gui.Buttons import *
    from common.gui.Sliders import *
    from models.ImageModels import *
    from models.TextModels import *
    from views.ImageView import *
    from views.TextViews import *
    from ResourceLoader import *

    loader = ResourceLoader()
    
    chk_image = loader.load_resource_by_name_and_type('check', 'image')
    x_image = loader.load_resource_by_name_and_type('x', 'image')

    chk_view = ImageView(ImageModel(chk_image))
    x_view = ImageView(ImageModel(x_image))

    font = loader.load_resources_by_type('font')[0]

    stage = Stage()

    scene = Scene('Toggle and Slider Test')
    scene.width = stage.width
    scene.height = stage.height

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

    hbox = HBox()
    slider = HSlider(toggle.width)

    sound_level_label = TextView(TextModel(font, 'Sound Level', 14))

    hbox.add_child(sound_level_label)
    hbox.add_child(slider)

    hbox.x = 38
    hbox.y = toggle.y + toggle.height + 15

    slider.y = hbox.height * 0.5 - slider.height * 0.5
    
    container.add_child(hbox)

    scene.add_child(container)

    stage.start(scene)
