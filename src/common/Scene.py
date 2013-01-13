from ElementView import *

from Stage import *
import pygame

class Scene(ElementView):
    def __init__(self, name, parent=None):
        ElementView.__init__(self)
        
        self.name = name
        
        self.initialized = False
        self._transitioning = False
        self._trans_rect = None
        self.transition_target = None
        self.active = False
        
        self.fill_color = (0, 0, 0, 0)
        
    def init(self):
        self.last_time_entered = None
        self.last_time_exited = None
        
        self.last = None
        self.next = None
        
        self.initialized = True
        self.emit('init', emitter = self)
        
    def pre_render(self, surface):
        if not self.initialized:
            self.enter(None)
        self._surface.fill(self.fill_color, [0, 0, self.width, self.height])

        
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

    def render(self, surface):
        blitter = pygame.Surface.blit
        if self.transitioning:
            rect = self._trans_rect
            if self.transition_target is not None:
                rect = self.transition_target
            
            if rect[0] > self.x:
                x = rect[0]
                w = self.width + self.x - rect[0]
            else:
                x = self.x
                w = (rect[0] + rect[2]) - x
                    
            if rect[1] > self.y:
                y = rect[1]
                h = self.height - (rect[1] - self.y)
            else:
                y = self.y
                h = (rect[1] + rect[3]) - y
                
            my_surface = self._surface.subsurface((x - self.x, y - self.y, w, h))
            blitter(surface, my_surface, (x, y, w, h))
        else:
            ElementView.render(self, surface)
            
    def _get_transitioning(self):
        return self._transitioning
    
    def _set_transitioning(self, value):
        if value != self._transitioning:
            self._transitioning = value
            if value:
                self._trans_rect = [self.x, self.y, self.width, self.height]
            self.emit('transitioning')
    transitioning = property(_get_transitioning, _set_transitioning)