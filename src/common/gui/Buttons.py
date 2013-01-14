try:
    from .common.ElementView import *
    from .views.TextViews import *
except:
    from views.TextViews import *
    from common.ElementView import *
        

class Button(ElementView):
    def __init__(self, text_model):
        ElementView.__init__(self)
        
        self._offset_x = 10
        self._offset_y = 3
        
        self._text_view = TextView(text_model)
        self._text_view.x = self._offset_x
        self._text_view.y = self._offset_y * 2
        
        self.add_child(self._text_view)
        
        self.show_background = True
        self.show_border = True
    
    def _get_inner_size(self):
        ElementView._get_inner_size(self)
        
        self._inner_width += self._offset_x
        self._inner_height += self._offset_y
    
    def set_text(self, txt):
        self._text_view.text = txt
    def get_text(self):
        return self._text_view.text
    text = property(get_text, set_text)