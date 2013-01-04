try:
    from .common.PubSub import *
except:
    from common.PubSub import *

from ImageModels import *

class AnimationModel(PubSub):
    def __init__(self, spritesheet_resource, frame_position, frame_size, frame_count, interval=200):
        PubSub.__init__(self)
        
        self.spritesheet = SpriteSheetModel(spritesheet_resource)
        self.frame_size = frame_size
        self.current_frame = 0
        self.frame_count = frame_count
        self.interval = interval
        self.position = frame_position
        
    def next_frame(self):
        self.current_frame += 1
        
        if self.current_frame >= self.frame_count:
            self.emit('finished')
            self.current_frame = 0
        
        xy = [self.position[0] + (self.frame_size[0] * self.current_frame), self.position[1]]
        
        self.emit('frame_change', frame = self.current_frame, rect = xy + list(self.frame_size))
        
    def current(self):
        rect = [self.position[0] + (self.frame_size[0] * self.current_frame), self.position[1]]
        rect += list(self.frame_size)
        
        return self.spritesheet.subsurface(rect)
