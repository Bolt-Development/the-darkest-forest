from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from models.Engine import *
    from models.AudioModels import *
    from controllers.AudioControllers import *
    from ResourceLoader import *

    resource = ResourceLoader().load_resource_by_name_and_type('bomb', 'audio')

    def init_audio(event, **kwargs):
        audio = AudioController(AudioModel(resource))
        engine.on("w_down", audio.play)
        
    engine = Engine()
    engine.on("init", init_audio, memory=True)
    engine.start()
