from PubSub import *
from Timer import *

import random

class Transition(PubSub):
    def __init__(self, current, next):
        PubSub.__init__(self)
        self.current = current
        self.next = next
        
        self.timer = Timer()
        self.timer.on('tick', self.on_timer)
        self.timer.on('finished', self.on_timer_finished)
        self.timer.on('started', self.on_timer_started)
        
        self.parent_temp = None
        
    def start(self, delay=0, duration='infinite', interval=0, repeats='infinite', message_type='tick'):
        if self.current.parent == None or self.current == self.next:
            return
        
        if self.current.transitioning or self.next.transitioning:
            print 'stopping'
            return
        
        self.emitter = self.current._stage
        self.timer.start(self.emitter, delay, duration, interval, repeats, message_type)
        
    def on_timer_started(self):
        self.current.transitioning = True
        self.next.transitioning = True
        self.next.transition_target = [self.current.x, self.current.y, self.next.width, self.next.height]
        
        self.on_start()
        
        self.emit('started')
        self.parent_temp = self.next.parent
        self.current.parent.add_child(self.next)
        
        if self.current.parent.on_stage:
            self.next.enter(self.current)
        
    def on_start(self):
        pass
    def on_timer(self):
        pass
    def on_stop(self):
        pass
    
    def on_timer_finished(self, event, **kwargs):
        self.emit('finished', event = event, args = kwargs)
        self.current.parent.remove_child(self.current)
        self.current.transitioning = False
        self.next.transitioning = False
        self.next.transition_target = None
        
        if self.parent_temp is not None:
            self.parent_temp.add_child(self.current)
        self.current.exit(self.next)
        self.on_stop()
        
class ScrollTransition(Transition):
    def __init__(self, current, next, direction_x='random', direction_y=0, speed_x=12, speed_y=12):
        Transition.__init__(self, current, next)
        
        self.direction_x = self.get_direction(direction_x)
        self.direction_y = self.get_direction(direction_y)
        
        self.speed_x =  max(2, speed_x)
        self.speed_y = max(2, speed_y)
        
        if self.direction_x == 0:
            self.speed_x = 0
            
        if self.direction_y == 0:
            self.speed_y = 0
            
        self.instant = False
        if self.speed_x == 0 and self.speed_y == 0:
            self.instant = True
        
    def get_direction(self, value):
        if value is None:
            return 0
        elif value == 'random':
            decider = random.random()
            if decider < 0.5:
                return -1
            else:
                return 1
        elif value < -1:
            return -1
        elif value > 1:
            return 1
        else:
            return value
        
    def on_start(self):
        self.position()
        
    def position(self):
        self.target_x, self.target_y = self.current.x, self.current.y
        
        if self.direction_x == 0:
            self.next.x = self.current.x
        elif self.direction_x < 0:
            self.next.x = self.current.x + self.current.width
        else:
            self.next.x = self.current.x - self.next.width
            
        if self.direction_y == 0:
            self.next.y = self.current.y
        elif self.direction_y < 0:
            self.next.y = self.current.y + self.current.height
        else:
            self.next.y = self.current.y - self.next.height
            
        
    def on_timer(self):
        if self.next.x == self.target_x and self.next.y == self.target_y:
            self.timer.stop('finished')
        else:
            x_dist = (self.speed_x * self.direction_x)
            y_dist = (self.speed_y * self.direction_y)
            
            self.next.x += x_dist
            self.next.y += y_dist
            
            self.current.x += x_dist
            self.current.y += y_dist
            
            
            min_x = max_x = 0
            if self.next.x > self.target_x:
                min_x = self.target_x
                max_x = self.next.x
            else:
                min_x = self.next.x
                max_x = self.target_x
                
            if max_x - min_x <= self.speed_x:
                self.next.x = self.target_x
                
                
            min_y = max_y = 0
            if self.next.y > self.target_y:
                min_y = self.target_y
                max_y = self.next.y
            else:
                min_y = self.next.y
                max_y = self.target_y
                
            if max_y - min_y <= self.speed_y:
                self.next.y = self.target_y
            
            