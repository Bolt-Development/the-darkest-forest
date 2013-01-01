class ImageModel(object):
    def __init__(self, resource):
        self.filepath = resource.filepath
        self.surface = pygame.image.load(filepath)