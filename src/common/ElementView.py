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
        
        self._id = ElementView.next_id
        ElementView.next_id += 1
        
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
        
        self.ignore_model_size = self.fixed_height = False
        
        self.mouse_over = False
        self.mouse_down_on = False
        self._last_known_mouse = None
        
        self._visible = True
        self.z_order = 0
        
        
        self._stage = False
        self.on_stage = False
        
        self.draggable = False
        self.dragging = False
        self.drag_x = True
        self.drag_y = True
        self.drag_outside_parent = True
        
        
    def is_point_inside(self, x, y):
        _x, _y = self._x, self._y
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
        if self._model is not None and not self.ignore_model_size:
            self._width = self._model.width * self._scale_x
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
    
    def _on_child_changed(self, event, **kwargs):
        self._size_dirty = True
        self._scale_dirty = True
        self.on_child_changed(event, **kwargs)
        self.emit('changed')
    
    def on_child_changed(self, event, **kwargs):    # for overriding
        pass
    
    def make_dirty(self):
        self._size_dirty = True
        self._scale_dirty = True
        self.emit('changed')
    
    def on_child_moved(self):
        self._size_dirty = True
    
    def on_child_added(self, child):
        self._size_dirty = True
        child.on('changed', self._on_child_changed)
        child.on('moved', self.on_child_moved)
        # TODO :: consider listening for moved events
        self.emit('child_added', child = child)
    
    def on_child_removed(self, child):
        self._size_dirty = True
        
        # this will force the old content to be removed from the surface
        self._surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        child.remove('changed', self._on_child_changed)
        child.remove('moved', self.on_child_moved)
        self.emit('child_removed', child = child)
    
    def on_parent_changed(self, parent, old_parent):
        if old_parent is not None:
            old_parent.remove('render', self.on_render)
            old_parent.remove('moved', self.on_parent_moved)
            old_parent.remove('mouse_motion', self.on_mouse_moved_in_parent)
            old_parent.remove('mouse_clicked', self.on_mouse_clicked_in_parent)
            old_parent.remove('start_mouse_dragging', self.on_start_mouse_dragging_in_parent)
            old_parent.remove('stopped_mouse_dragging', self.on_stop_mouse_dragging_in_parent)
            old_parent.remove('added_to_stage', self.on_added_to_stage)
            old_parent.remove('removed_from_stage', self.on_removed_from_stage)
            old_parent.remove('visible', self.on_parent_visible)
            old_parent.remove('hidden', self.on_parent_hidden)
            
            if self.on_stage:
                self.on_removed_from_stage()
                self.on_stage = False
            
        if parent is not None:
            parent.on('render', self.on_render)
            parent.on('moved', self.on_parent_moved)
            parent.on('mouse_motion', self.on_mouse_moved_in_parent)
            parent.on('mouse_clicked', self.on_mouse_clicked_in_parent)
            parent.on('start_mouse_dragging', self.on_start_mouse_dragging_in_parent)
            parent.on('stopped_mouse_dragging', self.on_stop_mouse_dragging_in_parent)
            parent.on('added_to_stage', self.on_added_to_stage)
            parent.on('removed_from_stage', self.on_removed_from_stage)
            parent.on('visible', self.on_parent_visible)
            parent.on('hidden', self.on_parent_hidden)
            
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
        
    def on_parent_hidden(self, event, **kwargs):
        self.visible = False
        
    def on_parent_visible(self, event, **kwargs):
        self.visible = True
        
    def to_local_position(self, position):
        gx, gy = position
        
        parent = self.parent
        while parent is not None:
            gx -= parent.x
            gy -= parent.y
            
            parent = parent.parent
            
        gx -= self.x
        gy -= self.y
            
        return gx, gy
    
    def on_start_mouse_dragging_in_parent(self, event, **kwargs):
        _x, _y = self.to_local_position(kwargs['position'])
         
        if _x >= 0 and _x <= self.width and _y >= 0 and _y <= self.height:
            if any(self.map(lambda x: x.on_start_mouse_dragging_in_parent(event, **kwargs), False)):
                self.dragging = False
            elif self.draggable:
                self.dragging = True
                self.emit('started_mouse_dragging')
        return self.dragging
            
    def on_stop_mouse_dragging_in_parent(self, event, **kwargs):
        if self.draggable:
            self.dragging = False
        self.emit('stopped_mouse_dragging')
            
    def on_mouse_moved_in_parent(self, event, **kwargs):
        if not self.visible:
            return
        
        if self.dragging:
            dx, dy = kwargs['delta']
            nx, ny = self.x, self.y
            if self.drag_x:
                nx += dx
            if self.drag_y:
                ny += dy
                
                
            if not self.drag_outside_parent and self.parent is not None:
                if nx < 0:
                    nx = 0
                if ny < 0:
                    ny = 0
                if nx + self.width > self.parent.width:
                    nx = self.parent.width - self.width
                if ny + self.height > self.parent.height:
                    ny = self.parent.height - self.height
                        
            self.x = nx
            self.y = ny
            self.emit('mouse_dragging')
        
        x, y = kwargs['position']
        
        _x, _y = self.to_local_position(kwargs['position'])
            
        if _x >= 0 and _x <= self.width and _y >= 0 and _y <= self.height:
            if self.mouse_over:
                self.emit('mouse_motion', **kwargs)
            else:
                self.mouse_over = True
                self.emit('mouse_entered')
                self.on_mouse_entered(event, **kwargs)
        else:
            if self.mouse_over:
                self.mouse_over = False
                self.emit("mouse_exited")
                self.on_mouse_exited(event, **kwargs)
        self._last_known_mouse = (x, y)
            
    def on_mouse_entered(self, event, **kwargs):
        pass
    
    def on_mouse_exited(self, event, **kwargs):
        pass
    
    def on_mouse_clicked_in_parent(self, event, **kwargs):
        if not self.visible:
            return
        
        down_x, down_y = self.to_local_position(kwargs['down_target'])
        up_x, up_y = self.to_local_position(kwargs['up_target'])
        
        down_in = down_x >= 0 and down_x <= self.width and down_y >= 0 and down_y <= self.height
        up_in = up_x >= 0 and up_x <= self.width and up_y >= 0 and up_y <= self.height
        
        if down_in and up_in:
            kwargs['target'] = self
            self.propagate(event, **kwargs)
            
            self.on_mouse_clicked(event, **kwargs)
            
    def on_mouse_clicked(self, event, **kwargs):
        pass
            
    def on_render(self, event, **kwargs):
        surface = kwargs['surface']
        
        if not self.visible:
            return
        
        
        self.pre_render(surface)
        if self._surface is not None:
            if self._surface.get_width() != self.width or self._surface.get_height() != self.height:
                # consider a copy of the old (too small) surface
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
    
    def center(self, other):
        self.x = other.width * 0.5 - self.width * 0.5
        self.y = other.height * 0.5 - self.height * 0.5
        
    def _get_visible(self):
        return self._visible
    def _set_visible(self, value):
        if value != self._visible:
            if value:
                self.emit('visible')
            else:
                self.emit('hidden')
            self._visible = value
    visible = property(_get_visible, _set_visible)
    
    def _get_model(self):
        return self._model
    def _set_model(self, model):
        self._model = model
        self.make_dirty()
    model = property(_get_model, _set_model)
    
    def _get_id(self):
        return self._id
    id = property(_get_id)
ElementView.next_id = 0
    