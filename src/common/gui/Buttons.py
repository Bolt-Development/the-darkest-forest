try:
    from .common.ElementView import *
    from .views.TextViews import *
except:
    from views.TextViews import *
    from common.ElementView import *
        

class Button(ElementView):
    def __init__(self, text_model):
        ElementView.__init__(self)
        
        self._text_view = TextView(text_model)
        self.add_child(self._text_view)
        
        self.show_background = True
        self.show_border = True
        
    
    def set_text(self, txt):
        self._text_view.text = txt
    def get_text(self):
        return self._text_view.text
    text = property(get_text, set_text)