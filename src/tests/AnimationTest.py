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
    
    def init_animation():
        animation_timer = AnimationController.init(engine)
        
        spritesheet_resource = ResourceLoader().load_resource_by_name_and_type('explosion', 'image')
        animation_model = AnimationModel(spritesheet_resource, (0, 0), (282, 238), 10)
        animation_controller = AnimationController(animation_model)
        animation_view = AnimationView(animation_model)
        
        animation_controller.start()

        engine.on("render", animation_view.on_render)

    engine = Engine()
    engine.on("init", init_animation, memory=True)

    engine.start()
