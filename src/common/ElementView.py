from PubSub import *
from ParentChild import *

from Stage import * # for isinstance

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
        
        self.fixed_width = self.fixed_height = False
        
        self.mouse_over = False
        self.mouse_down_on = False
        self._last_known_mouse = None
        
        self.visible = True
        self.z_order = 0
        
        
        self._stage = False
        self.on_stage = False
        
        
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
        if self._model is not None:
            if not self.fixed_width:
                self._width = self._model.width * self._scale_x
            if not self.fixed_height:
                self._height = self._model.height * self._scale_y
            
        self._scale_dirty = False
    
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
            max_width = max(child.x + child.width, max_width)
            max_height = max(child.y + child.height, max_height)
            
        self._inner_width = max_width
        self._inner_height = max_height
        
        self._size_dirty = False
    
    def _get_width(self):
        if self._scale_dirty:
            self._calculate_size()
        if self._size_dirty:
            self._get_inner_size()
        return max(self._width, self._inner_width) # * scale?
    
    def _set_width(self, value):
        self._width = value
        self.emit('changed')
        self._size_dirty = True
        
    width = property(_get_width, _set_width)
        
    def _get_height(self):
        if self._scale_dirty:
            self._calculate_size()
        if self._size_dirty:
            self._get_inner_size()
        return max(self._height, self._inner_height)
    
    def _set_height(self, value):
        self._height = value
        self.emit('changed')
        self._size_dirty = True
    height = property(_get_height, _set_height)
    
    def on_child_changed(self, event, **kwargs):
        self.make_dirty()
    
    def make_dirty(self):
        self._size_dirty = True
        self._scale_dirty = True
        self.emit('changed')
    
    def on_child_added(self, child):
        self._size_dirty = True
        child.on('changed', self.on_child_changed)
        # TODO :: consider listening for moved events
        self.emit('child_added', child = child)
    
    def on_child_removed(self, child):
        self._size_dirty = True
        child.remove('changed', self.on_child_changed)
        self.emit('child_removed', child = child)
    
    def on_parent_changed(self, parent, old_parent):
        if old_parent is not None:
            old_parent.remove('render', self.on_render)
            old_parent.remove('moved', self.on_parent_moved)
            old_parent.remove('mouse_motion', self.on_mouse_moved_in_parent)
            old_parent.remove('mouse_clicked', self.on_mouse_clicked_in_parent)
            old_parent.remove('added_to_stage', self.on_added_to_stage)
            old_parent.remove('removed_from_stage', self.on_removed_from_stage)
            
            if self.on_stage:
                self.on_removed_from_stage()
                self.on_stage = False
            
        if parent is not None:
            parent.on('render', self.on_render)
            parent.on('moved', self.on_parent_moved)
            parent.on('mouse_motion', self.on_mouse_moved_in_parent)
            parent.on('mouse_clicked', self.on_mouse_clicked_in_parent)
            parent.on('added_to_stage', self.on_added_to_stage)
            parent.on('removed_from_stage', self.on_removed_from_stage)
            
            up = parent
            while up is not None:
                if isinstance(up, Stage):
                    if not self.on_stage:
                        self._stage = up
                        self.on_added_to_stage()
                        self.on_stage = True
                up = up.parent
                
    def on_added_to_stage(self):
        self.emit('added_to_stage')
        
    def on_removed_from_stage(self):
        self.emit('removed_from_stage')
        
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
            kwargs['target'] = self
            self.propagate(event, **kwargs)
            
    def on_render(self, event, **kwargs):
        surface = kwargs['surface']
        
        if not self.visible:
            return
        
        self.pre_render(surface)
        if self._surface is not None:
            if self._surface.get_width() != self.width or self._surface.get_height() != self.height:
                # consider a copy of the old (too small) surface
                print self, self.width, self.height, self._inner_height
                self._surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            mod = 0
            if self.show_border:
                draw_line = pygame.draw.line
                
                bw = self.width - self.border_size
                bh = self.height - self.border_size
                draw_line(self._surface, self.border_color, (0, 0), (bw, 0), self.border_size)
                draw_line(self._surface, self.border_color, (bw, 0), (bw, bh), self.border_size)
                draw_line(self._surface, self.border_color, (bw, bh), (0, bh), self.border_size)
                draw_line(self._surface, self.border_color, (0, 0), (0, bh), self.border_size)
                mod = self.border_size
                
            if self.show_background:
                color = self.background_color
                    
                self._surface.fill(color, (self.border_size, 
                                           self.border_size, 
                                           self.width - mod * 2, 
                                           self.height - mod * 2))
                
        self.emit('render', surface = self._surface)
        if self.visible and self.width > 0 and self.height > 0:
            self.render(surface)
        
    def render(self, surface):
        blitter = pygame.Surface.blit
        blitter(surface, self._surface, (self.x, self.y, self.width, self.height))
    
    def pre_render(self, surface):
        pass
    