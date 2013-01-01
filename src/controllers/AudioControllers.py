from models.AudioModels import *

class AudioController(object):
    """Controls two channels of audio"""
    def __init__(self):
        channel_1 = pygame.mixer.Channel(0)
        channel_2 = pygame.mixer.Channel(1)
        self.channels = [channel_1, channel_2]
        self.queue = []
        self.loaded_files = {}

    def play(self, filename):
        if filename not in self.loaded_files:
            model = AudioModel(filename)
            self.loaded_files[filename] = model
        self.loaded_files[filename].sound.play()



if __name__ == '__main__':
    pass