from PubSub import *
import pygame

class Timer(PubSub):
    def __init__(self):
        PubSub.__init__(self)
        self.running = False
        self.infinite = False
        self.infinite_repeats = False
        
    def start(self, update_emitter, delay=0, duration='infinite', interval=0, repeats='infinite', message_type='tick'):
        if self.running:
            return    # consider runtime error
        
        self.time_to_start = pygame.time.get_ticks() + delay
        
        self.infinite_repeats = repeats == 'infinite'
        self.infinite = duration == 'infinite'
            
        if not self.infinite:
            self.time_to_stop = self.time_to_start + duration
        else:
            self.time_to_stop = None
        
        self.delay = delay
        self.duration = duration
        
        self.interval = interval
        self.interval_time = 0
        
        self.repeats = repeats
        self.call_count = 0
        
        self.emitter = update_emitter
        self.message_type = message_type
        self.emitter.on(message_type, self.on_tick)
        
        self.running = True
        self.running_time = 0
        self.emit('started')
        
    def on_tick(self, event, **kwargs):
        if self.running:
            ticks = pygame.time.get_ticks()
            elapsed = kwargs['elapsed']
            
            self.running_time += elapsed
            self.interval_time += elapsed
            
            if (self.infinite or ticks < self.time_to_stop) and ticks > self.time_to_start:
                if self.interval_time >= self.interval:
                    self.interval_time = 0
                    if self.infinite_repeats or self.call_count < self.repeats:
                        self.emit('tick', elapsed = elapsed)
                        self.call_count += 1
                    else:
                        self.stop('finished')
            elif not self.infinite and ticks > self.time_to_stop:
                self.stop('finished')
                
    def stop(self, message_type='stopped'):
        self.emit(message_type)
        self.running = False
        self.time_last_stopped = pygame.time.get_ticks()
        
    def resume(self):
        if self.running:
            return
        
        self.emit('resumed')
        self.running = True
        self.time_to_stop += pygame.time.get_ticks() - self.time_last_stopped
                