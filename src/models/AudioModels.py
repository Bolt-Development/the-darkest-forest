import pygame
class AudioModel(object):
    def __init__(self, resource):
        assert(resource.type == 'audio')
        
        self.resource = resource
        self.sound = pygame.mixer.Sound(self.resource.filepath)