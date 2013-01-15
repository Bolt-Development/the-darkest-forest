try:
    from .common.ElementView import *
except:
    from common.ElementView import *

class HBox(ElementView):
    def __init__(self):
        ElementView.__init__(self)
        
        self._offset = 10
        self.starting_x = self._offset
        self.starting_y = 0
        
    def position_elements(self):
        x, y = self.starting_x, self.starting_y
        
        max_width = max_height = 0
        for child in self.children:
            x, y = self.position_child(child, x, y)
            max_width = max(max_width, child.width)
            max_height = max(max_height, child.height)
        self._inner_width = x + max_width
        self._inner_height = y + max_height
        self.emit('changed')
            
    def position_child(self, child, x, y):
        child.x = x
        child.y = y
        
        return x + child.width + self._offset, y
        
    def on_child_changed(self, event, **kwargs):
        self.position_elements()
        
    def on_child_added(self, child):
        ElementView.on_child_added(self, child)
        self.position_elements()
    
    def on_child_removed(self, child):
        ElementView.on_child_removed.on_child_removed(self, child)
        self.position_elements()
        
class VBox(HBox):
    def __init__(self):
        HBox.__init__(self)
        
        self.starting_x = 0
        self.starting_y = self._offset
        
    def position_child(self, child, x, y):
        child.x = x
        child.y = y
        
        return x, y + child.height + self._offset

