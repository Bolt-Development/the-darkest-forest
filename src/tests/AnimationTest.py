from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from models.Engine import *
    from models.AnimationModels import *
    from models.ImageModels import *
    from controllers.AnimationControllers import *
    from views.AnimationViews import *
    from ResourceLoader import *
    from common.Timer import *
    def init_animation():
        spritesheet_resource = ResourceLoader().load_resource_by_name_and_type('pixelland', 'image')
        animation_model = AnimationModel(spritesheet_resource, (10,10))
        animation_controller = AnimationController(animation_model)
        animation_view = AnimationView()
        timer = Timer()
        timer.on("tick", animation_controller.next)
        timer.start(engine, 0, "infinite", 1000)
        engine.on("render", animation_view.on_render)

    engine = Engine()
    engine.on("init", init_animation, memory=True)

    engine.start()