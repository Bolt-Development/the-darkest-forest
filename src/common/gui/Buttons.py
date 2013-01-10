try:
    from .common.ElementView import *
    from .views.TextViews import *
except:
    from views.TextViews import *
    from common.ElementView import *
        

class Button(ElementView):
    def __init__(self, text_model):
        ElementView.__init__(self)
        
        text_view = TextView(text_model)
        self.add_child(text_view)
        
        self.show_background = True
        self.show_border = True
        