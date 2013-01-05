try:
    from .common.Timer import *
except:
    from common.Timer import *
    
try:
    from .common.Guard import *
except:
    from common.Guard import *

class AnimationController(object):
    def __init__(self, model):
        self.model = model
        self.timer = Timer()
    
    def start(self):
        try:
            emitter = AnimationController.animation_timer
        except:
            print 'Animation Controller -- No Instance of Timer Running in Class'
            print 'Please run AnimationController.init()'
            emitter = None
            
        if emitter is not None:
            self.timer.start(emitter, interval = self.model.interval)
            self.timer.on('tick', self.next)
        
        
    def stop(self):
        self.timer.stop()
        
    def resume(self):
        self.timer.resume()
        
    def next(self):
        print "next frame now"
        self.model.next_frame()
        
    @classmethod
    def init(cls, emitter, message_type='tick'):
        if not guarded(lambda:cls.animation_timer):
            cls.animation_timer = Timer()
            cls.animation_timer.start(emitter, message_type=message_type)
        return cls.animation_timer
        