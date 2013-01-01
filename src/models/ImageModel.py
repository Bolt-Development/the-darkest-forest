class ImageModel(object):
    def __init__(self, resource):
        self.resource = resource
        self.surface = self.resource.load()
