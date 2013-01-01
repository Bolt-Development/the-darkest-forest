class ImageModel(object):
    def __init__(self, resource):
        self.filepath = resource.filepath
        self.surface = pygame.image.load(filepath)


class SpriteSheet(ImageModel):
    def __init__(self, resource):
        ImageModel.__init__(self, resource)

    def subsurface(self, rect):
        return self.surface.subsurface(rect)
