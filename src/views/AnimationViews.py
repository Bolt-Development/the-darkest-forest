import pygame

class AnimationView(object):
    def __init__(self, model):
        self.model = model
        self.model.on('frame_change', self.on_change)
        self.current = None
        
        self.x = self.y = 0
        self.scale_x = self.scale_y = 1.0
        
    def on_render(self, event, **kwargs):
        if self.current is None:
            self.current = self.model.current()
            
        surface = kwargs['surface']

        width = self.current.get_width() * self.scale_x
        height = self.current.get_height() * self.scale_y

        modified = self.current.copy()
        modified = pygame.transform.scale(modified, [int(x) for x in (width, height)])

        pygame.Surface.blit(surface,
                            modified,
                            [self.x, self.y, width, height])
        
    def on_change(self, event, **kwargs):
        self.current = self.model.current()