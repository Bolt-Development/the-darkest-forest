from models.AudioModels import *

class AudioController(object):
    """Controls two channels of audio"""
    def __init__(self, model):
        self.model = model
    def play(self):
        self.model.sound.play()
    def stop(self):
        self.model.sound.stop()
    def fade(self, time):
        self.model.sound.fadeout(time)

class AudioChannelController(object):
    def __init__(self, model):
        self.model = model

    def play(self, model, loops=0, maxtime=0, fade_ms=0):
        self.model.channel.play(model.sound, loops, maxtime, fade_ms)







if __name__ == '__main__':
    pass
