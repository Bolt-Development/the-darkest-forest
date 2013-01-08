try:
    from .models.Engine import *
except:
    from models.Engine import *
from ParentChild import *

class Stage(Engine, ParentChild):
    def __init__(self, width=854, height=480):
        Engine.__init__(self, width, height)
        ParentChild.__init__(self)
        
        self.last_mouse_down_target = None
        
    def start(self, scene, start_paused = False):
        self.add_child(scene)
        Engine.start(self, start_paused)
        # nothing after here gets called until engine.stop has been called!
    
    def on_child_removed(self, scene):
        print 'removed scene', scene.name
    
    def on_child_added(self, scene):
        if len(self.children) == 0:
            scene.enter(None)
        print 'scene added to stage', scene.name

    def emit(self, message_type, **kwargs):
        """ 
            Overrides default behavior, and unless the current scene 
            traps a message_type, will echo the emit through the current scene. 
        """
        
        kwargs['stage'] = self
        PubSub.emit(self, message_type, **kwargs)
        
        if message_type == 'mouse_down':
            self.last_mouse_down_target = kwargs['position']
        elif message_type == 'mouse_up':
            self.emit('mouse_clicked', down_target=self.last_mouse_down_target, up_target=kwargs['position'])
            self.last_mouse_down_target = None
        
        for child in self.children:
            kwargs['scene'] = child
            child.emit(message_type, **kwargs)
            
    def point_over_element(self, elem, x, y):
        return x >= elem.x and x <= elem.x + elem.width and y >= elem.y and y <= elem.y + elem.height
            