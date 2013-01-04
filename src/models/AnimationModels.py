from TextModels import *

class AnimationModel(object):
    def __init__(self, spritesheet_resource, frame_size):
        self.spritesheet = SpritesheetModel(spritesheet_resource.load())
        self.frame_size = frame_size
        self.current_frame

