try:
    from .common.ElementView import *
except:
    from common.ElementView import *
    
import pygame

class TileView(ElementView):
    def __init__(self, tile):
        self._tile = tile
        self._tile_dirty = True
        
    def _get_tile(self):
        return self._tile
    def _set_tile(self, value):
        if value != self._tile:
            self._tile = value
        self.emit('tile_changed')
        
    
        
    def render(self, surface):
        blitter = pygame.Surface.blit
        blitter(surface, self._surface, (self.x, self.y, self.width, self.height))
    
    def pre_render(self, surface):
        if self._tile_dirty:
            self._clean_up()