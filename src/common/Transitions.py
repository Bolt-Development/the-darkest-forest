from PubSub import *
from Timer import *

class Transition(PubSub):
    def __init__(self, current, next):
        self.current = current
        self.next = next
        
        self.timer = Timer()
        self.timer.on('tick', self.on_timer)
        self.timer.on('finished', self.on_timer_finished)
        
    def start(self, update_emitter, delay=0, duration='infinite', interval=0, repeats='infinite', message_type='tick'):
        self.emitter = update_emitter
        self.timer.start(update_emitter, delay, duration, interval, repeats, message_type)
        self.on_start()
        
    def on_start(self):
        pass
    def on_timer(self):
        pass
    def on_stop(self):
        pass
    
    def on_timer_finished(self, event, **kwargs):
        self.emit('finished', event = event, args = kwargs)
        self.on_stop()
        
class ScrollTransition(Transition):
    def __init__(self, current, next):
        Transition.__init__(self, current, next)
        
        self.speed = 1
        
    def on_start(self):
        self.position()
        self.emitter.add_child(self.next)
        
    def position(self):
        self.target_x, self.target_y = self.current.x, self.current.y
        
        self.next.x = self.current.x + self.current.width
        self.next.y = self.current.y
        
    def on_timer(self):
        if self.next.x == self.target_x and self.next.y == self.target_y:
            print 'stopping'
            self.timer.stop()
        else:
            self.next.x -= self.speed
            
            self.current.x -= self.speed
            self.current.y
            
    def on_stop(self):
        self.emitter.remove_child(self.current)
            
            
            
            