from PubSub import *
from ParentChild import *
import pygame

class ElementView(PubSub, ParentChild):
    """ Handles common tasks such as mouse on, over, out in. """
    def __init__(self, model = None, controller = None):
        PubSub.__init__(self)
        ParentChild.__init__(self)
        
        self._model = model
        self._controller = controller
        
        self._x = self._y = 0
        self._gx = self._gy = 0
        self._scale_x = self._scale_y = 1.0
        self._rotation = 0
        
        self._scale_dirty = False
        
        if model is not None:
            self._width = model.width 
            self._height = model.height
        else:
            self._width = self._height = 0
            
        self._surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
        self._inner_width = self._inner_height = 0
        
        self.border_size = 1
        self.border_color = (255, 255, 255)
        self.show_border = False
        
        self.background_color = (0, 0, 255)
        self.show_background = False
        
        self._size_dirty = False
        self._global_dirty = False
        
        self.mouse_over = False
        self.mouse_down_on = False
        self._last_known_mouse = None
        
        self.visible = True
        self.z_order = 0
        
    def is_point_inside(self, x, y, use_global_position=False):
        _x, _y = self._x, self._y
        if use_global_position:
            _x, _y = self.global_x, self.global_y
        return x >= _x and x <= _x+ self.width and y >= _y and y <= _y + self.height
    
    def _get_x(self):
        return self._x
    
    def _get_y(self):
        return self._y
    
    def _set_x(self, value):
        self._x = value
        self._global_dirty = True
        self.emit('moved')
        
    def _set_y(self, value):
        self._y = value
        self._global_dirty = True
        self.emit('moved')
        
    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    
    def _calculate_size(self):
        self._width = self._model.width * self._scale_x
        self._height = self._model.height * self._scale_y
    
    def _get_scale_x(self):
        if self._scale_dirty:
            self._calculate_size()
        return self._scale_x
    
    def _set_scale_x(self, value):
        self._scale_x = value
        self.emit('changed')
        self._scale_dirty = True
        
    scale_x = property(_get_scale_x, _set_scale_x)
    
    def _get_scale_y(self):
        if self._scale_dirty:
            self._calculate_size()
        return self._scale_y
    
    def _set_scale_y(self, value):
        self._scale_y = value
        self.emit('changed')
        self._scale_dirty = True
        
    scale_y = property(_get_scale_y, _set_scale_y)
    
    def _get_global_position(self):
        self._gx = self.x
        self._gy = self.y
            
        parent = self.parent
        while parent is not None:
            self._gx += parent.x
            self._gy += parent.y
            parent = parent.parent
        self._global_dirty = False
        
    def _get_global_x(self):
        if self._global_dirty:
            self._get_global_position()
        return self._gx
    global_x = property(_get_global_x)
            
    def _get_global_y(self):
        if self._global_dirty:
            self._get_global_position()
        return self._gy
    global_y = property(_get_global_y)
                             
    def _get_inner_size(self):
        max_width = 0
        max_height = 0
        
        for child in self.children:
            max_width = max(child.width, max_width)
            max_height = max(child.height, max_height)
            
            
        self._inner_width = max_width
        self._inner_height = max_height
        
        self._size_dirty = False
    
    def _get_width(self):
        if self._size_dirty:
            self._get_inner_size()
        return max(self._width, self._inner_width) # * scale?
    
    def _set_width(self, value):
        self._width = value
        self._size_dirty = True
        
    width = property(_get_width, _set_width)
        
    def _get_height(self):
        if self._size_dirty:
            self._get_inner_size()
        return max(self._height, self._inner_height)
    
    def _set_height(self, value):
        self._height = value
        self._size_dirty = True
    height = property(_get_height, _set_height)
    
    def on_child_added(self, child):
        self._size_dirty = True
        self.emit('child_added', child = child)
    
    def on_child_removed(self, child):
        self._size_dirty = True
        self.emit('child_removed', child = child)
    
    def on_parent_changed(self, parent, old_parent):
        if old_parent is not None:
            old_parent.remove('render', self.on_render)
            old_parent.remove('moved', self.on_parent_moved)
            old_parent.remove('mouse_motion', self.on_mouse_moved_in_parent)
            
        if parent is not None:
            parent.on('render', self.on_render)
            parent.on('moved', self.on_parent_moved)
            parent.on('mouse_motion', self.on_mouse_moved_in_parent)
            parent.on('mouse_clicked', self.on_mouse_clicked_in_parent)
        
    def on_parent_moved(self, event, **kwargs):
        self._global_dirty = True
            
    def on_mouse_moved_in_parent(self, event, **kwargs):
        x, y = kwargs['position']
        
        _x, _y = x, y   # remove this later (used during testing)
        if self.parent is not None:
            _x = x - self.parent.x
            _y = y - self.parent.y
            
        if self.is_point_inside(_x, _y):
            if self.mouse_over:
                self.emit('mouse_motion', **kwargs)
            else:
                self.mouse_over = True
                self.emit('mouse_entered')
        else:
            if self.mouse_over:
                self.mouse_over = False
                self.emit("mouse_exited")
        self._last_known_mouse = (x, y)
                
    def on_mouse_clicked_in_parent(self, event, **kwargs):
        down_x, down_y = kwargs['down_target']
        up_x, up_y = kwargs['up_target']
        
        if self.is_point_inside(down_x, down_y, True) and self.is_point_inside(up_x, up_y, True):
            self.emit('mouse_clicked', **kwargs)
                
    def on_render(self, event, **kwargs):
        surface = kwargs['surface']
                
        self.pre_render(surface)
        if self._surface is not None:
            if self._surface.get_width() != self.width or self._surface.get_height() != self.height:
                # consider a copy of the old (too small) surface
                self._surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            if self.show_border:
                self._surface.fill(self.border_color, (0, 0, self.width, self.height))
                
            if self.show_background:
                self._surface.fill(self.background_color, (self.border_size, 
                                                           self.border_size, 
                                                           self.width - self.border_size * 2, 
                                                           self.height - self.border_size * 2))
                
        self.emit('render', surface = self._surface)
        if self.visible and self.width > 0 and self.height > 0:
            self.render(surface)
        
    def render(self, surface):
        blitter = pygame.Surface.blit
        blitter(surface, self._surface, (self.x, self.y, self.width, self.height))
    
    def pre_render(self, surface):
        pass
    