class ParentChild(object):
    def __init__(self, parent=None):
        self._parent = parent
        self._children = []
        
        if parent is not None:
            self.parent.add_child(self)
    
    def add_child(self, *children):
        for child in children:
            if child == self or child in self._children:
                continue
            
            self._children.append(child)
            if child._parent is not None and child._parent != self:
                child._parent.remove_child(child)
                
            child._parent = self
            self.on_child_added(child)
            
    def remove_child(self, *children):
        for child in children:
            if child == self:
                continue
            
            if child in self.children:
                self._children.remove(child)
                if child._parent == self:
                    child._parent = None
                self.on_child_removed(child)
                
    def clear_children(self):
        copy = [x for x in self._children]
        [self.remove_child(x) for x in copy]
            
    def _get_children(self):
        return self._children
    children = property(_get_children)
    
    def _get_parent(self):
        return self._parent
    def _set_parent(self, parent):
        old_parent = self._parent
        if parent == self or parent == self._parent:
            return
        
        self._parent = parent
        
        if old_parent is not None:
            old_parent.remove_child(self)
        
    parent = property(_get_parent, _set_parent)
    
    def on_child_added(self, child):
        pass
    
    def on_child_removed(self, child):
        pass
    
    def on_parent_changed(self, parent, old_parent):
        pass
    
if __name__ == '__main__':
    node = ParentChild()
    node2 = ParentChild()

    node3 = ParentChild(node2)
    node2.add_child(node)
    node.add_child(node3)
    
    print node.children, len(node.children)
    print node2.children, len(node2.children)
    print node3.children, len(node3.children)
