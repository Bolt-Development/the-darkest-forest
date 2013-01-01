class ImageModel(object):
    def __init__(self, resource):
        self.resource = resource
        self.surface = resource.load()


class SpriteSheetModel(ImageModel):
    def __init__(self, resource):
        ImageModel.__init__(self, resource)

    def subsurface(self, rect):
        return self.surface.subsurface(rect)
