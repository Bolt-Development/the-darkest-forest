from TestingUtils import *

        
if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()
    
    from models.Engine import *
    from models.TextModels import *

    from ResourceLoader import *

    def on_init(event, **kwargs):
        engine = kwargs['emitter']
        fonts = ResourceLoader().load_resources_by_type('font')
        print fonts

    
    engine = Engine()
    engine.set_caption('Sprite Sheet Testing')
    engine.on('init', on_init, memory=True)
    engine.start()
