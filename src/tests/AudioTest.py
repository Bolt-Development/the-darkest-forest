from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from models.Engine import *
    from models.AudioModels import *
    from controllers.AudioControllers import *
    from ResourceLoader import *

    resource = ResourceLoader().load_resource_by_name_and_type('bomb', 'audio')
    music_resources = ResourceLoader().load_resources_by_type('music')
    
    def init_audio(event, **kwargs):
        model = AudioModel(resource)
        music_model = AudioModel(music_resources[0])
        
        audio = AudioController(model)
        music = MusicController(music_model)
        engine.on("w_down", audio.play)
        engine.on("q_down", lambda:music.play(loops=3))
        
    engine = Engine()
    engine.on("init", init_audio, memory=True)
    engine.start()
