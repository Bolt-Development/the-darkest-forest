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

    def next_channel(self):
        channel = pygame.mixer.Channel(next_channel.current)
        AudioChannelController.current += 1
        return channel
    

    def play(self, model, loops=0, maxtime=0, fade_ms=0):
        self.channel.play(model.sound, loops, maxtime, fade_ms)

AudioChannelController.current = 0





if __name__ == '__main__':
    pass
