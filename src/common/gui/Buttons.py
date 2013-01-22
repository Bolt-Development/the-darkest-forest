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
        
        self._text_view = None
        if text_model is not None:
            self._text_view = TextView(text_model)
            self._text_view.x = self._offset_x
            self._text_view.y = self._offset_y
        
            self.add_child(self._text_view)
        
        self.show_background = True
        self.show_border = True
        
    def on_mouse_clicked(self, event, **kwargs):
        print 'click', self.text
        
    def on_mouse_entered(self, event, **kwargs):
        print 'enter', self.text
    
    def on_mouse_exited(self, event, **kwargs):
        print 'exit', self.text
        
    def _get_color(self):
        return self.border_color
    def _set_color(self, value):
        self._text_view.color = value
        self.border_color = value
    color = property(_get_color, _set_color)
        
    def _get_inner_size(self):
        ElementView._get_inner_size(self)
        
        self._inner_width += self._offset_x
        self._inner_height += self._offset_y
    
    def set_text(self, txt):
        if self._text_view is None:
            print 'trying to change text on a button with no text model! [Buttons.py]'
            return
        self._text_view.text = txt
    def get_text(self):
        if self._text_view is None:
            return 'Button ' + str(self.id)
        return self._text_view.text
    text = property(get_text, set_text)
    
class Toggle(Button):
    def __init__(self, model, active=False):
        Button.__init__(self, model)
        
        self.default_text = ''
        if model is not None:
            self.default_text = model.text
        
        self.show_background = False
        self.show_border = False
        
        self.background_color = (0, 0, 255)
        
        self.inactive_color = self.background_color
        self.active_color = self.background_color
        
        self._active_image = None
        self._inactive_image = None
        
        self._active = not active
        self.on_mouse_clicked(None)
        
    def on_mouse_clicked(self, event, **kwargs):
        self.active = not self._active
        
        if self.active:
            self.background_color = self.active_color
            if self.active_image is not None:
                self._active_image.x = self._text_view.width + 10
                self.add_child(self.active_image)
            else:
                self.text = self.default_text + ' On'
                
            if self.inactive_image is not None:
                self.remove_child(self.inactive_image)
        else:
            self.background_color = self.inactive_color
            if self.active_image is not None:
                self.remove_child(self.active_image)
                
            if self.inactive_image is not None:
                self._inactive_image.x = self._text_view.width + 10
                self.add_child(self.inactive_image)
            else:
                self.text = self.default_text + ' Off'
                
        self.emit('toggled', state = self.active)
            
    def _get_active(self):
        return self._active
    def _set_active(self, value):
        if value != self._active:
            if value:
                self.emit('on')
            else:
                self.emit('off')
        self._active = value
    active = property(_get_active, _set_active)
    
    def _get_active_image(self):
        return self._active_image
    
    def _get_inactive_image(self):
        return self._inactive_image
    
    def _set_active_image(self, img):
        self._active_image = img
        
        if self.active:
            self.text = self.default_text
            self._active_image.x = self._text_view.width + 10
            self.add_child(self._active_image)
        
    def _set_inactive_image(self, img):
        self._inactive_image = img
        
        if not self.active:
            self.text = self.default_text
            self._inactive_image.x = self._text_view.width + 10
            self.add_child(self._inactive_image)
        
    active_image = property(_get_active_image, _set_active_image)
    inactive_image = property(_get_inactive_image, _set_inactive_image)