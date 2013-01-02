from PubSub import *
import pygame

class SceneModel(PubSub):
    def __init__(self):
        PubSub.__init__(self)
        
    def init(self):    
        self.active = False
        
        self.last_time_entered = None
        self.last_time_exited = None
        
        self.last = None
        self.next = None
        

class SceneController(object):
    def __init__(self, model):
        self.model = model
        
    def enter(self, last):
        if self.last == last:
            
    
