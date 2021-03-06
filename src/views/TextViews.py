try:
    from .common.ElementView import *
    from .models.TextModels import *
except:
    from common.ElementView import *
    from models.TextModels import *

import string
import pygame
import sys
import re

class BaseTextView(ElementView):
    def __init__(self, model):
        ElementView.__init__(self, model)
        self._model.on('changed', self.on_change)
        
        self.dirty = True
        
    def on_change(self, even, **kwargs):
        self.make_dirty()   # change emits in this method
        self.dirty = True
        
    def init_surface(self):
        self._calculate_size()
        
        font = self._model.font
        text = self._model.text
        color = self._model.color
        
        scalar = pygame.transform.scale
        rot = pygame.transform.rotate
        
        self._surface = font.render(text, False, color)
        self._surface = scalar(self._surface, [int(x) for x in (self.width, self.height)])
        self._surface = rot(self._surface, self._rotation)
        
        self.dirty = False
        
    def on_render(self, event, **kwargs):
        if self.dirty: 
            self.init_surface()
        
        ElementView.on_render(self, event, **kwargs)
            
    def _get_font_size(self):
        return self._model.size
    def _set_font_size(self, value):
        self._model.load_font(self._model.resource, value)
    fontsize = property(_get_font_size, _set_font_size)
        
    def _get_text(self):
        return self._model.text
    def _set_text(self, text):
        self._model.text = text
    text = property(_get_text, _set_text)
    
    def _get_color(self):
        return self._model.color
    def _set_color(self, value):
        self._model.set_color(value)
    color = property(_get_color, _set_color)
        
class TextView(BaseTextView):
    def __init__(self, model):
        BaseTextView.__init__(self, model)
        
    def render(self, surface):
        if self.text == '\n':
            return
        
        blitter = pygame.Surface.blit
        blitter(surface, self._surface, (self.x, self.y, self.width, self.height))
        
        
class ParagraphView(ElementView):
    def __init__(self, model, width=300):
        ElementView.__init__(self, model)
        
        self._model.on('changed', self.on_model_changed)
        
        self._offset_x = self._offset_y = 6
        
        self.last_text = None
        self.model_dirty = True
        
        self._width = width
        self.ignore_model_size = True
        
        self.ignore_in_phrases = []
    
    ignore = '~`!@#$%^&*()_+=-{[}]\|'";:/?.>,<"
    
    def init_words(self):
        if self._model.text == self.last_text:
            self.handle_resize()
            return
        
        self.clear_children()
        
        txt = re.sub('\n', ' \n ', self._model.text).split(' ')
        for word in txt:
            if word == '\n':
                view = TextView(TextModel(self._model.resource, '\n', self._model.size))
                self.add_child(view)
                continue
            elif len(word.strip()) == 0:
                continue
                
            clean_word = word.translate(string.maketrans('', ''), string.punctuation)
            if len(clean_word) == 0:
                continue
                
            # strip punctuation before the word
            for character in word:
                if character == clean_word[0]:
                    break
                elif character in ParagraphView.ignore:
                    view = TextView(TextModel(self._model.resource, character, self._model.size))
                    view.justify = 'left'
                    self.add_child(view)
                    
            view = TextView(TextModel(self._model.resource, clean_word, self._model.size))
            self.add_child(view)
                
            # strip punctuation after word
            for character in word[::-1]:
                if character == clean_word[-1]:
                    break
                elif character in ParagraphView.ignore:
                    view = TextView(TextModel(self._model.resource, character, self._model.size))
                    view.justify = 'right'
                    self.add_child(view)
        
        self.handle_resize()
        self.last_text = self._model.text
        
    def handle_resize(self):
        max_height = 0
        x, y = self._offset_x * 2, self._offset_y
        
        newline = False
        for child in self.children:
            newline = False
            max_height = max(max_height, child.height)
            
            if child.text == '\n' or x + child.width > self._width - (self._offset_x * 2):
                x = self._offset_x * 2
                y += max(max_height, child.height)
                newline = True
                
            try:
                justify = child.justify
                if justify == 'left':
                    child.x = x + self._offset_x
                    child.y = y
                elif justify == 'right':
                    child.x = x - self._offset_x
                    child.y = y
                    
                    if newline:
                        child.y -= max(max_height, child_height)
            except:
                child.x = x
                child.y = y
                
            if newline:
                max_height = 0
            
            if child.text != '\n':
                x += child.width + self._offset_x
            else:
                x + self._offset_x
                
        self._height = y + max_height + self._offset_y * 2
        self.emit('changed')
    
    def on_model_changed(self, event, **kwargs):
        self.model_dirty = True
        
    def _get_font_size(self):
        return self._model.size
    def _set_font_size(self, value):
        for child in self.children:
            child.fontsize = value
        self._model.load_font(self._model.resource, value)
    fontsize = property(_get_font_size, _set_font_size)
        
    def pre_render(self, surface):
        if self.model_dirty or self._size_dirty:
            self.init_words()
            self.model_dirty = False
        
    def views_for_word(self, word):
        return [child for child in self.children if child._model.text == word]
    
    def views_for_phrase(self, phrase):
        words = phrase.split()
        # TODO
        
        
    def _get_text(self):
        return self._model.text
    def _set_text(self, value):
        self._model.text = value
    text = property(_get_text, _set_text)
    