try:
    from .common.ElementView import *
    from .models.TextModels import *
except:
    from common.ElementView import *
    from models.TextModels import *

import string
import pygame
import sys

class BaseTextView(ElementView):
    def __init__(self, model):
        ElementView.__init__(self, model)
        self._model.on('change', self.on_change)
        
        self.dirty = True
        
    def on_change(self, even, **kwargs):
        self.dirty = True
        
    def init_surface(self):
        self._calculate_size()
        
        font = self._model.font
        text = self._model.text
        color = self._model.color
        
        scalar = pygame.transform.scale
        rot = pygame.transform.rotate
        
        self._surface = font.render(text, True, color)
        self._surface = scalar(self._surface, [int(x) for x in (self._width, self._height)])
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
        
        self._model.on('change', self.on_model_changed)
        
        self._offset_x = self._offset_y = 6
        
        self.last_text = None
        self.model_dirty = True
        
        self._surface = None
        self._width = width
        
        self.ignore_in_phrases = []
    
    ignore = '~`!@#$%^&*()_+=-{[}]\|'";:/?.>,<\n"
    
    def init_words(self):
        if self._model.text == self.last_text:
            self.handle_resize()
            return
        
        self.clear_children()
        
        max_height = 0
        
        x, y = self._offset_x * 2, self._offset_y
        for line in self._model.text.split('\n'):
            for word in line.split(' '):
                if len(word.strip()) == 0:
                    continue
                
                clean_word =  word.translate(string.maketrans('', ''), string.punctuation)
                
                # strip punctuation before the word
                for character in word:
                    if character == clean_word[0]:
                        break
                    elif character in ParagraphView.ignore:
                        view = TextView(TextModel(self._model.resource, character, self._model.size))
                        self.add_child(view)
                        
                        view.x = x
                        view.y = y
                        
                        x = x + view.width
                    
                view = TextView(TextModel(self._model.resource, clean_word, self._model.size))
                self.add_child(view)
                
                max_height = max(max_height, view.height)
                
                if x + view.width > self._width - (self._offset_x * 2):
                    x = self._offset_x * 2
                    y += max(max_height, view.height)
                
                view.x = x
                view.y = y
                
                x += view.width + self._offset_x
                
                # strip punctuation after word
                for character in word[::-1]:
                    if character == clean_word[-1]:
                        break
                    elif character in ParagraphView.ignore:
                        view = TextView(TextModel(self._model.resource, character, self._model.size))
                        self.add_child(view)
                        
                        view.x = x - self._offset_x
                        view.y = y
                        
                        x = x + view.width + self._offset_x
                
            y += max_height
            x = self._offset_x * 2
        
        self._height = y
        self.last_text = self._model.text
        
    def handle_resize(self):
        max_height = 0
        x, y = self._offset_x, self._offset_y
        for child in self.children:
            max_height = max(max_height, child.height)
                
            if x + child.width > self._width - (self._offset_x * 2):
                x = self._offset_x
                y += max(max_height, child.height)
                
            child.x = x
            child.y = y
                
            x += child.width + self._offset_x
        y += max_height
        x = self._offset_x
    
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
            self._surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.model_dirty = False
            
            self._surface.fill((0, 0, 255, 45), (0, 0, self.width, self.height))
        
    def render(self, surface):
        blitter = pygame.Surface.blit
        blitter(surface, self._surface, (self.x, self.y, self.width, self.height))
        
    def views_for_word(self, word):
        return [child for child in self.children if child._model.text == word]
    
    def views_for_phrase(self, phrase):
        words = phrase.split()
        # TODO