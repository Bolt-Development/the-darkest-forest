try:
    from .models.Engine import *
except:
    from models.Engine import *
from ParentChild import *

class Stage(Engine, ParentChild):
    def __init__(self, width=1600, height=900):
        Engine.__init__(self, width, height)
        ParentChild.__init__(self)
        
        self._do_once = True
        self.last_mouse_down_target = None
        self.dragging = False
        self.on_stage = True    # views climbing up their ancestors need this
        
    def start(self, scene, start_paused = False):
        self.first_child = scene
        Engine.start(self, start_paused)
        # nothing after here gets called until engine.stop has been called!
    
    def init(self):
        Engine.init(self)
        self.add_child(self.first_child)
    
    def on_child_removed(self, scene):
        print 'removed scene', scene.name
    
    def on_child_added(self, scene):
        if self._do_once:
            scene.enter(None)
            self._do_once = False   # call enter on the start arguement
        print 'scene added to stage', scene.name

    def emit(self, message_type, **kwargs):
        """ 
            Overrides default behavior, and unless the current scene 
            traps a message_type, will echo the emit through the current scene. 
        """
        
        kwargs['stage'] = self
        
        if message_type == 'mouse_down':
            self.last_mouse_down_target = kwargs['position']
            self.last_mouse_down_time = pygame.time.get_ticks()
        elif message_type == 'mouse_up':
            if not self.dragging:
                self.emit('mouse_clicked', down_target=self.last_mouse_down_target, up_target=kwargs['position'])
            else:
                self.dragging = False
                self.emit('stop_mouse_dragging', **kwargs)
                
            self.last_mouse_down_target = None
            return
        elif message_type == 'mouse_motion':
            if self.dragging: 
                self.emit('mouse_dragged')
            elif not self.dragging:
                if self.last_mouse_down_target is not None:
                    now = pygame.time.get_ticks()
                    position = kwargs['position']
                    delta = kwargs['delta']
                    
                    same_place = [position[x] - delta[x] == self.last_mouse_down_target[x] for x in xrange(len(position))]
                    
                    if now - self.last_mouse_down_time > 25 and all(same_place):
                        self.dragging = True
                        self.emit('start_mouse_dragging', **kwargs)
        elif message_type == 'render' or message_type == 'tick':
            Engine.emit(self, message_type, **kwargs)
            return
        
        for child in self.children:
            if child.transitioning:
                continue
            kwargs['scene'] = child
            child.emit(message_type, **kwargs)
            
    def point_over_element(self, elem, x, y):
        return x >= elem.x and x <= elem.x + elem.width and y >= elem.y and y <= elem.y + elem.height
    
    
    # x and y are not settable
    def _get_x(self):
        return 0
    
    def _get_y(self):
        return 0
    
    x = property(_get_x)
    y = property(_get_y)
            