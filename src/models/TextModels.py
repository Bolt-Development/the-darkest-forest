class TextModel(object):
    def __init__(self, resource, text, size):
        self.text = text
        self.resource = resource
        self.font = resource.load()
        self.size = size

        self.width, self.height = self.font.size()
