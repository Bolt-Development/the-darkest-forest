from PubSub import *
import pygame

class ElementView(PubSub, ParentChild):
    """ Handles common tasks such as mouse on, over, out in. """
    def __init__(self, model, controller = None):
        PubSub.__init__(self)
        ParentChild.__init__(self)
        
        self.x = self.x = 0
        self.scale_x = self.scale_y = 1.0
        self._width = self._height = self._inner_width = self._inner_height = 0
        
    def is_point_inside(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height
                             
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
    
    def on_child_added(self, child):
        pass
    
    def on_child_removed(self, child):
        pass
    
    def on_parent_changed(self, parent, old_parent):
        pass
    