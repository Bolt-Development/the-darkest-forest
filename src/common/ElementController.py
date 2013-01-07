import math

class ElementController(object):
    def __init__(self, emitter, model=None):
        self._emitter = emitter
        self._model = model
        
        self._behaviors = []
        self._emitter.on('tick', self.on_update)
        
    def on_update(self, event, **kwargs):
        forces = self.calculate_forces()
        self.apply_force(forces.x, forces.y)
        self.calculate_velocity()
        
        self._model.x += self._model._vx
        self._model.y += self._model._vy
        
        self._model._ax = self._model._ay = 0
        
    def calculate_forces(self):
        force = 0
        
        if self._model is not None:
            for behavior in self._behaviors:
                result = behavior.apply(self.model)
                if result is not None:
                    force += result
                    
        return force
                    
    def apply_force(self, x, y):
        # This may eventually be taken over by pymunk
        self._model._ax += x
        self._model._ay += y
        
        magn = math.sqrt(self._model._ax * self._model._ax + self._model._ay * self._model._ay)
        if magn > self._model._max_force:
            self._model._ax = (self._model._ax / magn) * self._model._max_force
            self._model._ax = (self._model._ax / magn) * self._model._max_force
            self._model._force = self._model._max_force
        else:
            self._model._force = magn
            
        return self._max_force - self._force
    
    def calculate_velocity(self):
        self._model._vx += self._model._ax - (self._model._friction_x * self._model._vx)
        self._model._vy += self._model._ay - (self._model._friction_y * self._model._vy)
        
        magn = math.sqrt(self._model._vx * self._model._vx + self._model._vy * self._model._vy)
        if magn > self._model._max_speed:
            self._model._vx = (self._model._vx / magn) * self._model._max_speed
            self._model._vy = (self._model._vy / magn) * self._model._max_speed
            self._model._speed = self._model._max_speed
        elif magn <= 0.0001:
            self._model._vx = self._model._vy = 0
            self._model._ax = self._model._ay = 0
            
        if magn > 0.0001:
            self._model._hx = self._model._vx / magn
            self._model._hy = self._model._vy / magn
    
    
    def _get_model(self):
        return model
    
    def _set_model(self, model):
        self._model = model
        # TODO this may need additional steps
        
    def _get_emitter(self):
        return self._emitter
    
    model = property(_get_model, _set_model)
    emitter = property(_get_emitter)