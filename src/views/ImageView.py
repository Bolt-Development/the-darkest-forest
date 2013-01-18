try:
    from .common.ElementView import *
except:
    from common.ElementView import *
    
class ImageView(ElementView):
    def __init__(self, model):
        ElementView.__init__(self)
        
        self.model = model
        self._surface = self.model.surface
        
    def pre_render(self, surface):
        self._surface = self.model.surface