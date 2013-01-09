try:
    from .common.PubSub import *
except:
    from common.PubSub import*
    
class TextModel(PubSub):
    def __init__(self, resource, text="", size=14):
        PubSub.__init__(self)
        
        self._color = (255, 255, 255)
        self.load_font(resource, size)
        self.set_text(text)
        
    def get_resource(self):
        return self._resource
    resource = property(get_resource)
    
    def load_font(self, resource, size):
        self._resource = resource
        self._font = resource.load(size=size)
        self._size = size
        try:
            self.set_text(self._text)
        except:
            self.set_text('')
        self.emit('change')
    def get_font(self):
        return self._font
    font = property(get_font)
            
    def get_size(self):
        return self._size
    def set_size(self, size):
        self._size = size
        self.set_text(self._text)
    size = property(get_size, set_size)
        
    def get_text(self):
        return self._text
    def set_text(self, text):
        self._text = text
        self._width, self._height = self._font.size(self._text)
        self.emit('change')
    text = property(get_text, set_text)
            
    def get_color(self):
        return self._color
    def set_color(self, color, emit=True):
        self._color = color
        self.emit('change')
    color = property(get_color, set_color)
    
    def get_width(self):
        return self._width
    def get_height(self):
        return self._height
    width = property(get_width)
    height = property(get_height)
