from PubSub import *
import pygame

class ElementView(PubSub, ParentChild):
    """ Handles common tasks such as mouse on, over, out in. """
    def __init__(self, model, controller = None):
        PubSub.__init__(self)
        ParentChild.__init__(self)
                             
    def on_child_added(self, child):
        pass
    
    def on_child_removed(self, child):
        pass
    
    def on_parent_changed(self, parent, old_parent):
        pass
    