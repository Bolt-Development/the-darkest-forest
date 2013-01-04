from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from models.Engine import *
    from models.AnimationModels import *
    from controllers.AnimationControllers import *
    from views.AnimationViews import *
    from ResourceLoader import *

    spritesheet_resource = ResourceLoader().load_resource_by_name_and_type('pixelland', 'image')
    animation_model = AnimationModel
    animation_controller = AnimationController(animation_model)
    animation_view = AnimationView()

    engine = Engine()
    engine.on("render", animation_view.on_render)
    engine.start()