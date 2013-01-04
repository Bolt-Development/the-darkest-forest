try:
    from .Common.PubSub import *
except:
    from Common.PubSub import *

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
        
        if self.current_frame > self.frame_count:
            self.emit('finished')
            self.current_frame = 0
        
        xy = [self.position[i] + (self.frame_size[i] * self.current_frame) for i in xrange(2)]
        
        self.emit('frame_change', frame = self.current_frame, rect = xy + self.frame_size)
