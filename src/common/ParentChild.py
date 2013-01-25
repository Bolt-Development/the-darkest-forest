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
            
            old_parent = child._parent
            if old_parent is not None and old_parent != self:
                old_parent._children.remove(child)
                old_parent.on_child_removed(child)
                
            
            child._parent = self
            self._children.append(child)
            self.on_child_added(child)
            
            child.on_parent_changed(self, old_parent)
            
    def remove_child(self, *children):
        for child in children:
            if child in self._children:
                self._children.remove(child)
                
                child._parent = None
                child.on_parent_changed(None, self)
                
                self.on_child_removed(child)
                
    def clear_children(self):
        copy = [x for x in self._children]
        [self.remove_child(x) for x in copy]
            
    def _get_children(self):
        return self._children
    children = property(_get_children)
    
    def _get_parent(self):
        return self._parent
    parent = property(_get_parent)
    
    def on_child_added(self, child):
        pass
    
    def on_child_removed(self, child):
        pass
    
    def on_parent_changed(self, parent, old_parent):
        pass
    
    def map(self, fun, append_self = True):
        result = []
        
        for child in self.children:
            result += child.map(fun)
            
        if append_self:
            result.append(fun(self))
        return result
        
        
if __name__ == '__main__':
    node = ParentChild()
    node2 = ParentChild()

    node3 = ParentChild(node2)
    node2.add_child(node)
    node.add_child(node3)
    
    print node.children, len(node.children)
    print node2.children, len(node2.children)
    print node3.children, len(node3.children)
