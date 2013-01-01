from models.AudioModels import *

class AudioController(object):
    """Will eventually deal with 1 channel of audio, instead of just 1 audio file."""
    def __init__(self, model):
        self.model = model
    def play(self, event, **kwargs):
        self.model.sound.play()



if __name__ == '__main__':
    pass