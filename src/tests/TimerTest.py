from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()

    from models.Engine import *
    from common.Timer import *

    def on_tick():
        print 'tick'
    
    def init_audio(event, **kwargs):
        timer = Timer()
        timer.on('tick', on_tick)
        timer.start(engine, 2000, 10000, interval=1000)
        
    engine = Engine()
    engine.on("init", init_audio, memory=True)
    engine.start()
