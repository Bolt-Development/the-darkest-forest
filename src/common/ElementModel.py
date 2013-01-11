from PubSub import *
from ParentChild import *


class ElementModel(PubSub, ParentChild):
    def __init__(self):
        PubSub.__init__(self)
        ParentChild.__init__(self)
        
        self._x = self._y = self._width = self._height = 0
        self._dx = self._dy = self._old_x, = self._old_y = 0
        self._speed = self._max_force = self._max_speed = 100
        self._force = self._friction_x = self._friction_y = 0
        
        # rotation target
        self._rtx = self._rty = 0
        
        self._inner_width = self._inner_height = self._rotation = 0
        self._vx = self._vy = self._ax = self._ay = self._hx = self._hy = 0
        self._size_dirty = self._move_dirty = False
        
        self._move_validator = None
        
    def load(self, resource):
        pass    # TODO
    
    def on_child_added(self, child):
        self._size_dirty = True
        self.emit('changed')
    
    def on_child_removed(self, child):
        self._self_dirty = True
        self.emit('changed')
    
    def on_parent_changed(self, parent, old_parent):
        pass    # TODO check for instance of Stage, call on_added_to_stage for self and children
    
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
    
    def _get_bounding_radius(self):
        return [self.x, self.y, self.width, self.height]
    bounding_radius = property(_get_bounding_radius)
    
    def _handle_move(self):
        next_x, next_y = self._x + self._dx, self._y + self._dy
        
        if self._move_validator is not None:
            if self._move_validator(self._x, self._y, next_x, next_y, self._dx, self._dy):
                self._move_to(next_x, next_y)
        else:
            self._move_to(next_x, next_y)
            
    def _move_to(self, x, y):
        if self._x == x and self._y == y:
            return
        
        # assume move has been validated
        old_x, old_y = self._x, self._y
        self._x = x
        self._y = y
        self.emit('moved', x = x, y = y, old_x = old_x, old_y = old_y, delta_x = self._dx, delta_y - self._dy)
        
    def _get_x(self):
        if not self._move_dirty:
            return self._x
        
        self._handle_move()
        return self._x
    
    def _set_x(self, value):
        self._old_x = self._x
        self._dx = value - old_x
        
        self._move_dirty = True
    x = property(_get_x, _set_x)
    
    def _get_y(self):
        if not self._move_dirty:
            return self._y
        
        self._handle_move()
        return self._y
    
    def _set_y(self, value):
        self._old_y = self._y
        self._dy = value - old_y
        
        self._move_dirty = True
    y = property(_get_y, _set_y)
    