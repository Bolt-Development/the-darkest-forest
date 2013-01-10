from ElementView import *

from Stage import *
import pygame

class Scene(ElementView):
    def __init__(self, name, parent=None):
        ElementView.__init__(self)
        
        self.name = name
        
        self.initialized = False
        self.transitioning = False
        
    def init(self):    
        self.active = False
        
        self.last_time_entered = None
        self.last_time_exited = None
        
        self.last = None
        self.next = None
        
        self.initialized = True
        self.emit('init', emitter = self)
        
    def enter(self, last):
        if not self.initialized:
            self.init()
            
        self.active = True
        self.last = last
        self.last_time_entered = pygame.time.get_ticks()
        self.emit('entered', last = last)
        
    def exit(self, next):
        self.active = False
        self.next = next
        self.last_time_exited = pygame.time.get_ticks()
        self.emit('exited', next = next, time_in_scene = self.last_time_exited - self.last_time_entered)