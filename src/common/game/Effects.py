try:
    from .common.PubSub import *
except:
    from common.PubSub import *
    
class Effect(PubSub):
    def __init__(self):
        PubSub.__init__(self)
        
        
    def apply(self, entity, target=None):
        if target is None:
            target = entity
            
        self.on_apply(entity, target)
        
    def remove(self, entity, target=None):
        if target is None:
            target = entity
            
        self.on_remove(entity, target)
        
    def on_apply(self, entity, target):
        pass    # to override
    
    def on_remove(self, entity, target):
        pass    # override this method