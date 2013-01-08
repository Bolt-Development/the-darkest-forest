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
        
        self.border_size = 1
        self.border_color = (255, 255, 255)
        self.show_border = False
        
        self.background_color = (0, 0, 255)
        self.show_background = False
        
        self._size_dirty = False
        
    def is_point_inside(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height
                             
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
        pass
    