try:
    from .common.ElementView import *
    from .views.TextViews import *
    from .models.TextModels import *
except:
    from views.TextViews import *
    from models.TextModels import *
    from common.ElementView import *
    
from Buttons import *
from Layouts import *
    
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
        
        self.choice_layout = HBox()
        self.choices = choices
        self.init_choices()
        
        self.add_child(self.choice_layout)
        
    def init_choices(self):
        model = self.paragraph._model
        
        for choice in self.choices:
            button = Button(TextModel(model.resource, choice, model.size))
            button.on('mouse_clicked', self.on_choice_made)
                
            self.choice_layout.add_child(button)
        
    def on_choice_made(self, event, **kwargs):
        button = kwargs['target']
        self.emit('choice_made', choice = button.text)
        self.emit(button.text)  # so you can listen for on('cancel') etc.
        
        self.visible = False
        
    def on_child_changed(self, event, **kwargs):
        self.choice_layout.x = max(self.choice_layout.x, self.width - self.choice_layout.width - self._offset_x)
        self.choice_layout.y = max(self.choice_layout.y, self.paragraph.y + self.paragraph.height)
        self._height = self.choice_layout.y + self.choice_layout.height + self._offset_y
        
        
    def _get_text(self):
        return self.paragraph.text
    def _set_text(self, value):
        self.paragraph.text = value
        self.emit('changed')
    text = property(_get_text, _set_text)
    
class Confirm(Dialog):
    def __init__(self, text_model, width=300):
        Dialog.__init__(self, text_model, width, 'okay')
    
class ChooseDialog(ElementView):
    def __init__(self, text_model, *choices):
        ElementView.__init__(self)
        
        self.show_background = True
        self.show_border = True
        
        self.dialog = Dialog(text_model, 525, 'okay', 'cancel')
        self.dialog.show_border = False
        self.add_child(self.dialog)
        
        self.dialog.on('choice_made', self.on_choice_made)
        
        self._offset_x = self._offset_y = 15
        
        self.choice_layout = VBox()
        self.choice_layout.x = self._offset_x
        
        self.choices = choices
        self.init_choices()
        self.add_child(self.choice_layout)
        
        self.choice = None
        
    def init_choices(self):
        model = self.dialog.paragraph._model
        
        max_width = 0
        x, y = self._offset_x, self._offset_y
        for choice in self.choices:
            button = Button(TextModel(model.resource, choice, model.size))
            button.on('mouse_clicked', self.change_choice)
            self.choice_layout.add_child(button)
            
        self.position_elements()
        
    def change_choice(self, event, **kwargs):
        button = kwargs['target']
        
        if self.choice is not None:
            self.choice.color = (255, 255, 255)
        
        if button != self.choice:
            button.color = (255, 255, 51)
            self.choice = button
        else:
            button.color = (255, 255, 255)
            self.choice = None
            
        if self.choice is not None:
            self.emit(self.choice.text + '_selected')
        else:
            self.emit('nothing_selected')
            
        
    def on_choice_made(self, event, **kwargs):
        choice = kwargs['choice']
        if self.choice is None or choice == 'cancel':
            self.emit('choice_made', choice = 'nothing')
            self.emit('nothing') 
            self.emit('cancel')
        else:
            self.emit('choice_made', choice = self.choice.text)
            self.emit(self.choice.text)
            
        self.visible = False
        
    def _get_text(self):
        return self.dialog.text
    def _set_text(self, value):
        self.dialog.text = value
    text = property(_get_text, _set_text)
        
    def on_child_changed(self, event, **kwargs):
        self.position_elements()
        
    def position_elements(self):
        self.dialog.x = self.choice_layout.x + self.choice_layout.width + self._offset_x
        self.width = self.dialog.x + self.dialog.width + self._offset_x
        
        under_layout = self.choice_layout.y + self.choice_layout.height
        under_paragraph = self.dialog.paragraph.y + self.dialog.paragraph.height
        
        self.dialog.choice_layout.y = max(under_layout, under_paragraph)
        self.emit('changed')
        
        