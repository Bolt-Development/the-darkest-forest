from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()

    from models.Engine import *is
    from models.AudioModels import *
    from controllers.AudioControllers import *

    def init_audio():
        pygame.mixer.init()
        audio = AudioController(AudioModel("bomb.ogg"))
        engine.on("w_down", audio.play())
    engine = Engine()
    engine.on("init", init_audio())
    while pygame.mixer.get_busy():
        pass
