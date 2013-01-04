from ImageModels import *

class AnimationModel(object):
    def __init__(self, spritesheet_resource, frame_size):
        self.spritesheet = SpriteSheetModel(spritesheet_resource)
        self.frame_size = frame_size
        self.current_frame = 0

