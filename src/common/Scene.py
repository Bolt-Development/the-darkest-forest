from PubSub import *
import pygame

class Scene(PubSub):
    def __init__(self, width, height, x = 0, y = 0):
        PubSub.__init__(self)
        
        self.width = width
        self.height = height
        self.x, self.y = x, y
        
        self.initialized = False
        
    def init(self):    
        self.active = False
        
        self.last_time_entered = None
        self.last_time_exited = None
        
        self.last = None
        self.next = None
        
        self.initialized = True
        self.emit('init', emitter = self)
        
    def enter(self, last):
        self.last = last
        
        

class Transition(PubSub):
    def __init__(self):
        self.model = model
        
    def enter(self, last):
        if self.last == last:
            
    
