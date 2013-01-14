try:
    from .common.ElementView import *
    from .views.TextViews import *
    from .models.TextModels import *
except:
    from views.TextViews import *
    from models.TextModels import *
    from common.ElementView import *
    
from Buttons import *
    
class Dialog(ElementView):
    def __init__(self, text_model, width=300, *choices):
        ElementView.__init__(self)
        
        self._width = width
        self.fixed_width = True
        
        self._offset_x = self._offset_y = 15
        self.paragraph = ParagraphView(text_model, width - self._offset_x * 2)
        self.paragraph.x = self._offset_x
        self.paragraph.y = self._offset_y
        
        self.add_child(self.paragraph)
        
        self.choices = choices
        #self.init_choices()
        
    def init_choices(self):
        model = self.paragraph._model
        
        x, y = self.width - self._offset_x, self.paragraph.y + self.paragraph.height
        for choice in self.choices:
            button = Button(TextModel(model.resource, choice, model.size))
            
            x -= button.width + self._offset_x
            if x < self._offset_x:
                x = self.width - self._offset_x
                y += button.height
            
            button.x = x
            button.y = y
            button.on('mouse_clicked', self.on_choice_made)
            
            self.add_child(button)
            
        self._height = y
        
    def on_choice_made(self, event, **kwargs):
        button = kwargs['target']
        self.emit('choice_made', choice = button.text)
        self.emit(button.text)  # so you can listen for on('cancel') etc.
        
        self.visible = False
        
    def on_child_changed(self, event, **kwargs):
        print 'changed'
        self.make_dirty()
        