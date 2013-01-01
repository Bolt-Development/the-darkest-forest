import pygame
class AudioModel(object):
    def __init__(self, file):
        self.sound = pygame.mixer.Sound(file)