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
        self.fixed_width = self.show_border = self.show_background = True
        
        self._offset_x = self._offset_y = 15
        self._paragraph_offset_y = 0
        
        self.paragraph = ParagraphView(text_model, width - self._offset_x * 2)
        self.paragraph.show_background = True
        self.paragraph.x = self._offset_x
        self.paragraph.y = self._offset_y
        
        self.add_child(self.paragraph)
        
        self.choices = choices
        self.init_choices()
        
    def init_choices(self):
        model = self.paragraph._model
        
        x, y = self.width - self._offset_x, self.paragraph.y + self.paragraph.height + self._paragraph_offset_y
        for choice in self.choices:
            button = None
            found = False
            
            for child in self.children:
                try:
                    if child.text == choice:
                        button = child
                        found = True
                except:
                    pass
                    
            if not found:
                button = Button(TextModel(model.resource, choice, model.size))
            
            x -= button.width + self._offset_x
            if x < self._offset_x:
                x = self.width - self._offset_x
                y += button.height
            
            button.x = x
            button.y = y
            button.on('mouse_clicked', self.on_choice_made)
            
            self.add_child(button)
            
        self._height = y + button.height + self._offset_y
        self.emit('changed')
        
    def on_choice_made(self, event, **kwargs):
        button = kwargs['target']
        self.emit('choice_made', choice = button.text)
        self.emit(button.text)  # so you can listen for on('cancel') etc.
        
        self.visible = False
        
    def on_child_changed(self, event, **kwargs):
        ElementView.on_child_changed(self, event, **kwargs)
        self.init_choices()
        
    def _get_text(self):
        return self.paragraph.text
    def _set_text(self, value):
        self.paragraph.text = value
    text = property(_get_text, _set_text)
    
class ChooseDialog(ElementView):
    def __init__(self, text_model, *choices):
        ElementView.__init__(self)
        
        self.show_background = True
        self.show_border = True
        
        self.dialog = Dialog(text_model, 525, 'okay', 'cancel')
        self.dialog.show_border = False
        self.add_child(self.dialog)
        
        self._offset_x = self._offset_y = 15
        self.choices = choices
        self.init_choices()
        
    def init_choices(self):
        model = self.dialog.paragraph._model
        
        max_width = 0
        x, y = self._offset_x, self._offset_y
        for choice in self.choices:
            button = None
            found = False
            
            for child in self.children:
                try:
                    if child.text == choice:
                        button = child
                        found = True
                except:
                    pass
                    
            if not found:
                button = Button(TextModel(model.resource, choice, model.size))
            
            button.x = x
            button.y = y
            button.on('mouse_clicked', self.change_choice)
            
            y += button.height + self._offset_y
            
            max_width = max(max_width, button.x + button.width)
            
            self.add_child(button)
            
        self.dialog.x = max_width + self._offset_x
        
        self._width = self.dialog.x + self.dialog.width + self._offset_x
        self._height = y + button.height + self._offset_y
        self.emit('changed')
        
        
    def change_choice(self, event, **kwargs):
        print kwargs['target']
        
        
        
        
        
        
        
        
        