import pygame
from .common.PubSub import *

class Engine(PubSub):
    def __init__(self, width=854, height=480):
        PubSub.__init__(self)

        self.width = width
        self.height = height

    def init(self):
        if not hasattr(self, 'initialized'):
            self._init_pygame()
        
            self.init_font()
            self._init_clock()
            self.init_flow_controls()

            self.initialized = True
            self.emit('init', emitter = self)

    def init_flow_controls(self, value=False):
        self.active = value
        self.paused = value
        
        self.last_click_elapsed = [0 for x in xrange(12)]

    def _init_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode([self.width, self.height])

    def init_font(self, fontsize=35):
        if not hasattr(self, 'fontsize'):
            self.fontsize = 0
            
        if not self.fontsize == fontsize:
            self.fontsize = fontsize
            self.default_font = pygame.font.SysFont("None", self.fontsize)
            self.emit('font_changed', font=self.default_font)

    def _init_clock(self, fps=30):
        self.fps = fps
        self.frame_count = 0

        self.clock = pygame.time.Clock()
        
    def set_caption(self, string):
        self.init()
        pygame.display.set_caption(string)

    def toggle_pause(self):
        self.set_paused(not self.paused)

    def set_paused(self, boolean):
        self.init()
        if not self.paused == boolean:
            self.paused = boolean
            self.emit('pause', paused = self.paused)

    def stop(self):
        self.init()
        
        if self.active:
            self.active = False
            self.emit('stopped')

    def start(self, start_paused = False):
        self.init()
        
        if not self.active:
            self.active = True
            self.paused = start_paused
            
            self.emit('started')
            self._loop()
            self._handle_stop()

    def _loop(self):
        elapsed = 0
        while self.active:
            if not self.paused:
                self._tick(elapsed)
            self._render()
            self._handle_pygame_events()
            elapsed = self.clock.tick(self.fps)
            self.frame_count = self.frame_count + 1

    def _tick(self, elapsed):
        self.emit('tick', elapsed = elapsed)
        self.last_click_elapsed = [elapsed + x for x in self.last_click_elapsed]

    def _render(self):
        self.screen.fill((0, 0, 0), (0, 0, self.width, self.height))
        self.emit('render', surface = self.screen)
        pygame.display.update()

    def _handle_stop(self):
        pygame.quit()

    def _handle_pygame_events(self):
        any_input = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                any_input = True
                if event.key == pygame.K_ESCAPE:
                    self.stop()
                else:
                    name = pygame.key.name(event.key)
                    self.emit('key_down', name = name, key = event.key)

                    # or you can listen for specific keys
                    self.emit(''.join([name, '_down']))
            elif event.type == pygame.KEYUP:
                any_input = True
                name = pygame.key.name(event.key)
                self.emit('key_up', name = name, key = event.key)
                self.emit(''.join([name, '_up']))
            elif event.type == pygame.MOUSEMOTION:
                any_input = True
                self.emit('mouse_motion', position=event.pos, relative=event.rel, button_states=event.buttons)
            elif event.type == pygame.MOUSEBUTTONUP:
                any_input = True
                self.emit('mouse_up', position=event.pos, button=event.button)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                any_input = True
                
                old = self.last_click_elapsed[event.button]
                self.last_click_elapsed[event.button] = 0
                self.emit('mouse_down', position=event.pos, button=event.button, double= old < 200)
                

        if not any_input:
            self.emit('no_input')

if __name__ == '__main__':
    pass
