import pygame

class AudioModel(object):
    def __init__(self, resource):
        assert(resource.type == 'audio')
        
        self.resource = resource
        self.sound = pygame.mixer.Sound(self.resource.filepath)
        self.length = self.sound.get_length()
        self.buffer = self.sound.get_buffer()
        
class AudioChannelModel(object):
    def __init__(self):
        self.channel = self.next_channel

    def next_channel(self):
        return pygame.mixer.Channel(next_channel.current)
        next_channel.current += 1
    next_channel.current = 0
