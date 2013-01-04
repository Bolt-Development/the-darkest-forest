try:
    from .common.PubSub import *
except:
    from common.PubSub import *
try:
    from .models.TextModels import *
except:
    from models.TextModels import *


import pygame
import sys

class BaseTextView(PubSub):
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
        self._mouse_down = False
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
        self._surface = scalar(self._surface, [int(x) for x in (self._width, self._height)])
        self._surface = rot(self._surface, self._rotation)
        
        # a change of size might bring you under the mouse
        # even if the mouse isn't moving
        self.handle_mouse_position()
        self.dirty = False
        
    def on_render(self, event, **kwargs):
        if self.dirty: 
            self.init()
        
        surface = kwargs['surface']
        self.render(surface)
        
    def on_mouse_down(self, event, **kwargs):
        x, y = kwargs['position']
        if self._mouse_over:
            local = x - self._x, y - self._y
            self._mouse_down = True  # mouse went down inside me
            self.emit('mouse_down', button = kwargs['button'], position = local)
        else:
            self._mouse_down = False
            
    def on_mouse_up(self, event, **kwargs):
        x, y = kwargs['position']
        if self._mouse_over:
            if self._mouse_down: # mouse went down and came up inside me = click!
                local = x - self._x, y - self._y
                self.emit('mouse_up', position = local, button = kwargs['button'])
                self.emit('clicked', emitter = self, button = kwargs['button'], position = local)
                self._mouse_down = False
            
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
                self.emit('mouse_enter', emitter = self)
            self.emit('mouse_over', emitter = self)
            self.emit('mouse_motion', emitter = self, position = (x - self._x, y - self._y))
        else:
            if self._mouse_over:
                self._mouse_over = False
                self.emit('mouse_exit', emitter = self)
                
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
    
    def _get_text(self):
        return self._model.text
    def _set_text(self, text):
        self._model.text = text
    text = property(_get_text, _set_text)
    
    def _get_color(self):
        return self._model.color
    def _set_color(self, value):
        self._model.set_color(value)
    color = property(_get_color, _set_color)
    
    width = property(_get_width)
    height = property(_get_height)
        
class TextView(BaseTextView):
    def __init__(self, model):
        BaseTextView.__init__(self, model)
        
    def render(self, surface):
        blitter = pygame.Surface.blit
        
        blitter(surface, self._surface, (self._x, self._y, self._width, self._height))
        
        
class ParagraphView(BaseTextView):
    def __init__(self, model, width = 300):
        BaseTextView.__init__(self, model)
        self._min_width = sys.maxint
        self._width = width
        
        self._offset_x = self._offset_y = 3
        
    def init(self):
        txt = self._model.text
        
        self.clear_subs('render')
        self.clear_subs('mouse_motion')
        self.clear_subs('mouse_down')
        self.clear_subs('mouse_up')
        
        view = None
        x, y = self._offset_x, self._offset_y
        for line in txt.split('\n'):
            for word in line.split():
                if len(word.strip()) == 0:
                    continue
                
                view = TextView(TextModel(self._model.resource, word, self._model.height))
                view.on('change', self.on_change)
                
                next_x = x + view.width + (self._offset_x * 2.0)
                if next_x > self._width:
                    y += view.height+ self._offset_y
                    x = self._offset_x
                    
                view.x = x + self._offset_x
                view.y = y
                
                x += view.width + self._offset_x
                
                self._min_width = min(view.width, self._min_width)
                
                self.on('render', view.on_render)
                self.on('mouse_motion', view.on_mouse_motion)
                self.on('mouse_down', view.on_mouse_down)
                self.on('mouse_up', view.on_mouse_up)
                
                self.emit('word_added', word = word, view = view, rect = (x, y, view.width, view.height))
            if view is not None:
                y += view.height + self._offset_y
            x = self._offset_x
                
        self._width = max(self._width, self._min_width)
        self._height = y + self._offset_y
        self._surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        
        if self._last_known_mouse is not None:
            self.emit('mouse_motion', position = self._last_known_mouse)
        self.dirty = False
    
    def render(self, surface):
        if self.dirty:
            self.clean_up()
        
        self._surface.fill((0, 0, 255, 45), (0, 0, self._width, self._height))
        self.emit('render', surface = self._surface)
            
        blitter = pygame.Surface.blit
        
        blitter(surface, self._surface, (self._x, self._y, self._width, self._height))
        
    def _get_width(self):
        return self._width
    def _set_width(self, value):
        self._width = value
        if self._width < 0:
            self._width = 0
        self.dirty = True
    width = property(_get_width, _set_width)
    
    def _get_fontsize(self):
        return self._model.size
    def _set_size(self, value):
        self._model.load_font(self._model.resource, value)
    fontsize = property(_get_fontsize, _set_size)
            