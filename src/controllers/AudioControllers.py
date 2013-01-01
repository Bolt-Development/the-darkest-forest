from models.AudioModels import *

class AudioController(object):
    """Controls two channels of audio"""
    def __init__(self, model):
        self.model = model
    def play(self):
        self.model.sound.play()

class AudioChannelController(object):
    def __init__(self, model):
        self.model = model

    def next_channel(self):
        return pygame.mixer.Channel(next_channel.current)
        next_channel.current += 1
    next_channel.current = 0
    

    def play(self, filename):
        # play the sound





if __name__ == '__main__':
    pass
