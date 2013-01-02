import pygame

class AudioModel(object):
    def __init__(self, resource):
        self.resource = resource
        self.__sound = None

    def _get_sound(self):
        if self.__sound is not None:
            return self.__sound
        
        self.__sound = self.resource.load()
        self.length = self.__sound.get_length()
        self.buffer = self.__sound.get_buffer()
        
        return self.__sound

        
    sound = property(_get_sound)
        
class AudioChannelModel(object):
    def __init__(self):
        self.channel = self.next_channel

    def next_channel(self):
        return pygame.mixer.Channel(next_channel.current)
        next_channel.current += 1
    next_channel.current = 0
