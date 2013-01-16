try:
    from .common.PubSub import *
except:
    from common.PubSub import *
    
class Attribute(PubSub):
    def __init__(self, name, value=0):
        PubSub.__init__(self)
        
        self._name = name
        self._base = value
        self._reduced_amount = self._bonus_amount = 0
        
    def _get_name(self):
        return self._name
    name = property(_get_name)
    
    def _get_current(self):
        return self._base - self._reduced_amount + self._bonus_amount
    def _set_current(self, value):
        old = self._base
        self._base = value
        
        self.emit('changed', old = old, new = self._base)
    current = property(_get_current, _set_current)
    
    def _get_bonus(self):
        return self._bonus_amount
    def _set_bonus(self, value):
        old = self._bonus_amount
        self._bonus_amount = value
        self.emit('bonus_changed', old = old, new = self._bonus_amount)
    bonus = property(_get_bonus, _set_bonus)
    
    def _get_reduced(self):
        return self._reduced_amount
    def _set_reduced(self, value):
        old = self._reduced_amount
        self._reduced_amount = value
        self.emit('reduced_changed', old = old, new = self._reduced_amount)
    reduced = property(_get_reduced, _set_reduced)
    
class AttributeModel(PubSub):
    def __init__(self):
        PubSub.__init__(self)
        
        self.attributes = []
    