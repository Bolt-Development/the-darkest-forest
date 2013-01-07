from PubSub import *
from ParentChild import *


class ElementModel(PubSub, ParentChild):
    def __init__(self):
        PubSub.__init__(self)
        ParentChild.__init__(self)
        
        self._x = self._y = self._width = self._height = 0
        self._inner_width = self._inner_height = 0
        self._vx = self._vy = self._ax = self._ay = 0
        self._size_dirty = False
        
        
    def on_child_added(self, child):
        self._size_dirty = True
    
    def on_child_removed(self, child):
        self._self_dirty = True
    
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
        