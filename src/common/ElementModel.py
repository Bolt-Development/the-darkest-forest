from PubSub import *
from ParentChild import *


class ElementModel(PubSub, ParentChild):
    def __init__(self):
        PubSub.__init__(self)
        ParentChild.__init__(self)
        
        self._x = self._y = self._width = self._height = 0
        self._dx = self._dy = self._old_x, = self._old_y = 0
        self._inner_width = self._inner_height = 0
        self._vx = self._vy = self._ax = self._ay = 0
        self._size_dirty = self._move_dirty = False
        
        self._move_validator = None
        
    def load(self, resource):
        pass    # TODO
    
    def on_child_added(self, child):
        self._size_dirty = True
        self.emit('change')
    
    def on_child_removed(self, child):
        self._self_dirty = True
        self.emit('change')
    
    def on_parent_changed(self, parent, old_parent):
        pass    # TODO check for instance of Stage, call on_added_to_stage for self and children
    
    def _get_width(self):
        if not self._size_dirty:
            return self._width + self._inner_width
        
        self._inner_width = 0
        for child in self.children:
            self._inner_width += child.width
        return self._width + self._inner_width
    
    def _set_width(self, value):
        self._width = value
        
    width = property(_get_Width, _set_width)
        
    def _get_height(self):
        if not self._size_dirty:
            return self._height + self._inner_height
        
        self._inner_height = 0
        for child in self.children:
            self._inner_height += child.height
        return self._height + self._inner_height
    
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
    