try:
    from .common.ElementView import *
except:
    from common.ElementView import *
    
class SliderBullet(ElementView):
    def __init__(self, slider, initial_color=(127, 127, 127), mouse_over_color=(127, 126, 149)):
        ElementView.__init__(self)
        
        self.draggable = True
        self.drag_outside_parent = False
        self.show_background = True
        self.background_color = initial_color
        self.mouse_over_color = mouse_over_color
        self.initial_color = initial_color
        
        self.slider = slider
    
class HSlider(ElementView):
    def __init__(self, width, height=15, current=0.5):
        ElementView.__init__(self)
        
        self.width = width
        self.height = height
        self.show_background = True
        self.background_color = (238, 233, 233)
        
        self.init_bullet()
        self.add_child(self.bullet)
        
        self._current = 0
        self.current = current
        
    def on_mouse_clicked(self, event, **kwargs):
        position = self.to_local_position(kwargs['up_target'])
        print position[0]
        print position[0] / self.width
        
    def init_bullet(self):
        self.bullet = SliderBullet(self)
        self.drag_y = False
        self.bullet.height = self.height
        self.bullet.width = self.width * 0.15
        
        self.bullet.on('moved', self.on_bullet_moved)
        
    def on_bullet_moved(self, event, **kwargs):
        self._current = self.bullet.x / (self.width - self.bullet.width)
        self.emit('changed')
        
    def _get_current(self):
        return self._current
    
    def _set_current(self, value):
        self._current = value
        self.emit('changed')
        self.position_bullet()
    current = property(_get_current, _set_current)
    
    def position_bullet(self):
        x = self.current * self.width
        self.bullet.x = x - self.bullet.width * 0.5
        self.bullet.y = self.y