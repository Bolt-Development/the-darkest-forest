from PubSub import *
from Timer import *

class Transition(PubSub):
    def __init__(self, current, next):
        self.current = current
        self.next = next
        
        self.timer = Timer()
        self.timer.on('tick', self.on_timer)
        self.timer.on('finished', self.on_timer_finished)
        
    def start(self, update_emitter, delay, duration, interval=0, repeats='infinite', message_type='tick'):
        self.timer.start(update_emitter, delay, duration, interval, repeats, message_type)
        
    def on_timer(self):
        pass
    
    def on_timer_finished(self, event, **kwargs):
        self.emit('finished', event = event, args = kwargs)
        