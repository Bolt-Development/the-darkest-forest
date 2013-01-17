from Attibutes import *

try:
    from .common.PubSub import *
except:
    from common.PubSub import *
    
class Skill(Attribute):
    def __init__(self, name, value = 0):
        Attribute.__init__(self, name, value)
        
        self._effect = None
        
    def _get_effect(self):
        return self._effect
    def _set_effect(self, effect):
        old = self._effect
        self._effect = effect
        if old is None:
            self.emit('effect_added', emitter = self, effect = effect)
        else:
            self.emit('effect_changed', emitter = self, effect = effect, old = old)
            

class SkillModel(PubSub):
    def __init__(self):
        PubSub.__init__(self)
        
        self.skills = []
        
    def get_skill_by_name(self, name):
        return [skill for skill in self.skills if skill.name == name]
    
    def add_skill(self, skill):
        self.skills.append(skill)
        
        skill.on('changed', self.on_skill_changed)
        skill.on('bonus_changed', self.on_skill_changed)
        skill.on('reduced_changed', self.on_skill_changed)
        skill.on('effect_added', self.on_skill_changed)
        skill.on('effect_changed', self.on_skill_changed)
        
    def remove_skill(self, skill):
        if skill in self.skills:
            self.skills.remove(skill)
            
            skill.remove('changed', self.on_skill_changed)
            skill.remove('bonus_changed', self.on_skill_changed)
            skill.remove('reduced_changed', self.on_skill_changed)
            skill.remove('effect_added', self.on_skill_changed)
            skill.remove('effect_changed', self.on_skill_changed)
            
    def on_skill_change(self, event, **kwargs):
        skill = kwargs['emitter']
        self.emit(skill.name + '_' + event.message_type, **kwargs)