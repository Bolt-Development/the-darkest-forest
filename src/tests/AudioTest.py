from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()

    from models.Engine import *
    from models.AudioModels import *
    from controllers.AudioControllers import *

    def on_event(event, **kwargs):
        print event, kwargs

    def init_audio(event, **kwargs):
        audio = AudioController()
        engine.on("w_down", audio.play)

    engine = Engine()
    engine.on("init", init_audio, memory=True)
    engine.on('tick', on_event)
    engine.on('render', on_event)
    engine.start()

