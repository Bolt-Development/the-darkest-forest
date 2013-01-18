class ImageModel(object):
    def __init__(self, resource):
        self.resource = resource
        self.surface = resource.load()
        
    def get_width(self):
        return self.surface.get_width()
    
    def get_height(self):
        return self.surface.get_height()
    
    width = property(get_width)
    height = property(get_height)
    
class SpriteSheetModel(ImageModel):
    def __init__(self, resource):
        ImageModel.__init__(self, resource)

    def subsurface(self, rect):
        return self.surface.subsurface(rect)
