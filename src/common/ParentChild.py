class ParentChild(object):
    def __init__(self, parent=None):
        self._parent = parent
        self._children = []
        
        if parent is not None:
            self.parent.add_child(self)
            
    def add_child(self, *children):
        for child in children:
            if child == self:
                continue
            
            self.children.append(child)
            child.parent = self
            self.on_child_added(child)
            
    def remove_child(self, *children):
        for child in children:
            if child == self:
                continue
            
            if child in self.children:
                self.children.remove(child)
                child.parent = None
                self.on_child_removed(child)
            
    def _get_children(self):
        return self._children
    children = property(_get_children)
    
    def _get_parent(self):
        return self.parent
    def _set_parent(self, parent):
        if parent == self or parent in self.children:
            return
        
        if parent != self.parent:
            self.parent.remove_child(self)
        self.parent = parent
        if parent is not None:
            self.parent.add_child(self)
        self.on_parent_changed(parent)
    parent = property(_get_parent, _set_parent)
    
    def on_child_added(self, child):
        pass
    
    def on_child_removed(self):
        pass
    
    def on_parent_changed(self, parent):
        pass