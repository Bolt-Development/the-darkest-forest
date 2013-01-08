from PubSub import *
import pygame

class ElementView(PubSub, ParentChild):
    """ Handles common tasks such as mouse on, over, out in. """
    def __init__(self, model, controller = None):
        PubSub.__init__(self)
        ParentChild.__init__(self)
        
        self._model = model
        self._controller = controller
        
        self._x = self._y = 0
        self._gx = self._gy = 0
        self._scale_x = self._scale_y = 1.0
        self._scale_dirty = False
        
        self._width = model.width 
        self._height = model.height
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
        self.emit('moved')
        
    def _set_y(self, value):
        self._y = value
        self.emit('moved')
        
    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    
    def _calculate_size(self):
        self._width = self.model.width * self._scale_x
        self._height = self.model.height * self._scale_y
        self._surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
    
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
        self._inner_width = 0
        self._inner_height = 0
        for child in self.children:
            self._inner_width += child.width
            self._inner_height += child.height
        self._size_dirty = False
    
    def _get_width(self):
        if self._size_dirty:
            self._get_inner_size()
        return max(self._width, self._inner_width)
    
    def _set_width(self, value):
        self._width = value
        
    width = property(_get_Width, _set_width)
        
    def _get_height(self):
        if not self._size_dirty:
            self._get_inner_size()
        return max(self._height, self._inner_height)
    
    def _set_height(self, value):
        self._height = value
        
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
        parent.on('render', self.on_render)
        parent.on('moved', self.on_parent_moved)
        parent.on('mouse_motion', self.on_mouse_moved_in_parent)
        
    def on_parent_moved(self, event, **kwargs):
        self._global_dirty = True
            
    def on_mouse_moved_in_parent(self, event, **kwargs):
        x, y = kwargs['position']
        if self.is_point_inside(x, y):
            if self.mouse_over:
                self.emit('mouse_motion')
            else:
                self.mouse_over = True
                self.emit('mouse_entered')
        else:
            if self.mouse_over:
                self.mouse_over = False
                self.emit("mouse_exited")
                
    def on_mouse_clicked_in_parent(self, event, **kwargs):
        down_x, down_y = kwargs['down_target']
        up_x, up_y = kwargs['up_target']
        
        if self.is_point_inside(down_x, down_y, True) and self.is_point_inside(up_x, up_y, True):
            self.emit('mouse_clicked', kwargs)
                
    def on_render(self, event, **kwargs):
        surface = kwargs['surface']
        
        # render
        
        self.emit('render', surface = self.surface)
    