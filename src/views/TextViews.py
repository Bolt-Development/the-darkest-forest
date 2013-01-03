from .common.PubSub import *

from .models.TextModels import *

import pygame

class TextView(PubSub):
    def __init__(self, model):
        PubSub.__init__(self)
        
        self._model = model
        
        self._model.on('change', self.on_change)
        
        self._rotation = 0
        self._x = self._y = 0
        self._scale_x = self._scale_y = 1.0
        self._width = self._height = 0
        self._surface = None
        
        self._mouse_over = False
        self._last_known_mouse = None
        
        self.dirty = True
        
    def on_change(self, even, **kwargs):
        self.dirty = True
        
    def init(self):
        self.init_size()
        self.init_surface()
        self.emit('init')
        
    def scale(self, x, y):
        self._scale_x = x
        self._scale_y = y
        
        self.dirty = True
        
    def rotate(self, angle):
        self._rotation = angle
        
        self.dirty = True
        
    def init_size(self):
        self._width = self._model.width * self._scale_x
        self._height = self._model.height * self._scale_y
        
        
    def init_surface(self):
        font = self._model.font
        text = self._model.text
        color = self._model.color
        
        scalar = pygame.transform.scale
        rot = pygame.transform.rotate
        
        self._surface = font.render(text, True, color)
        self._surface = scalar(self._surface, (self._width, self._height))
        self._surface = rot(self._surface, self._rotation)
        
        # a change of size might bring you under the mouse
        # even if the mouse isn't moving
        self.handle_mouse_position()
        self.dirty = False
        
    def on_render(self, event, **kwargs):
        if self.dirty: 
            self.init()
        
        surface = kwargs['surface']
        blitter = pygame.Surface.blit
        
        blitter(surface, self._surface, (self._x, self._y, self._width, self._height))
        
    def on_mouse_motion(self, event, **kwargs):
        position = kwargs['position']
        self._last_known_mouse = position
        self.handle_mouse_position()
        
    def handle_mouse_position(self):
        if self._last_known_mouse is None:
            return
        
        x, y = self._last_known_mouse
        if x > self._x and x < (self._x + self._width) and  y > self._y and y < (self._y + self._height):
            if not self._mouse_over:
                self._mouse_over = True
                self.emit('mouse_enter')
            self.emit('mouse_over')
        else:
            if self._mouse_over:
                self._mouse_over = False
                self.emit('mouse_exit')
                
    def _get_x(self):
        return self._x
    def _set_x(self, value):
        self._x = value
        self.dirty = True
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        return self._y
    def _set_y(self, value):
        self._y = value
        self.dirty = True
    y = property(_get_y, _set_y)
    
    def _get_width(self):
        if self.dirty:
            self.init()
            
        return self._width
    
    def _get_height(self):
        if self.dirty:
            self.init()
            
        return self._height
    
    width = property(_get_width)
    height = property(_get_height)
        
class ParagraphView(PubSub):
    def __init__(self, model, width = 300):
        PubSub.__init__(self)
        
        self._model = model
        
        self._model.on('change', self.change_model)
        
        self._width = width
        self._x = self._y = self._height = 0
        self._offset_x = self._offset_y = 3
        self.dirty = True
        
    def change_model(self):
        self.make_dirty()
        
    def make_dirty(self):
        self.dirty = True
    
    def clean_up(self):
        txt = self._model.text
        
        x, y = 0, 0
        for line in txt.split('\n'):
            for word in line.split():
                if len(word.strip()) == 0:
                    continue
                
                child = TextView(TextModel(self._model.resource, word, self._model.height))
                child.on('change', self.make_dirty)
                
                x += child.width + self._offset_x
                if x > self._width:
                    y += self._model.size + self._offset_y
                    x = 0
                    
                child.x = x - child.width
                child.y = y
                
                self.on('render', child.on_render)
                self.on('mouse_motion', child.on_mouse_motion)
                
                self.emit('word_added', word = word, view = child, rect = (x, y, child.width, child.height))
            y += self._model.size + self._offset_y
            x = 0
                
        self._height = y + self._model.height + self._offset_y
        self._surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        self.dirty = False
    
    def on_render(self, event, **kwargs):
        if self.dirty:
            self.clean_up()
        
        self._surface.fill((0, 0, 0, 255), (self._x, self._y, self._width, self._height))
        self.emit('render', surface = self._surface)
            
        surface = kwargs['surface']
        blitter = pygame.Surface.blit
        
        blitter(surface, self._surface, (self._x, self._y, self._width, self._height))
        
    def on_mouse_motion(self, event, **kwargs):
        x, y = kwargs['position']
        if x > self._x and x < self._x + self._width and y > self._y and y < self._y + self._height:
            local = x - self._x, y - self._y
            self.emit('mouse_motion', position = local)