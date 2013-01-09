from PubSub import *
from ParentChild import *

try:
    from .models.Engine import *
except:
    from models.Engine import *
    
from Stage import *
import pygame

class Scene(PubSub, ParentChild):
    def __init__(self, name, parent=None):
        PubSub.__init__(self)
        ParentChild.__init__(self)
        
        self.name = name
        self._width = self._height = self._x = self._y = 0
        
        self._surface = False
        self._stage = False
        
        self.on_stage = False
        
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
        self.last = last
        self.emit('entered', last = last)
        
    def exit(self, next):
        self.next = next
        self.emit('exited', next = next)
        
    def _get_surface(self):
        if self._surface:
            return self._surface
        
        self._surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        return self._surface
    surface = property(_get_surface)
    
    def _get_stage(self):
        return self._stage or None
    
    def _set_stage(self, stage):
        if self._stage:
            self.on_removed_from_stage()
            
        self._stage = stage
        self.on_added_to_stage()
    stage = property(_get_stage, _set_stage)
    
    def on_added_to_stage(self):
        self.emit('added_to_stage', stage = self.stage)
        for child in self.children:
            child.on_added_to_stage()
        self.on_stage = True
        
    def on_removed_from_stage(self):
        self.emit('removed_from_stage', stage = self.stage)
        
    def on_child_added(self, child):
        self.emit('child_added', child = child)
    
    def on_child_removed(self):
        self.emit('child_removed', child = child)
    
    def on_parent_changed(self, parent, old_parent):
        if isinstance(parent, Stage):
            self.stage = parent
            self.emit('added_to_stage')
        