from ..common.PubSub import *

class TileContents(PubSub):
    def __init__(self, tile, contents):
        PubSub.__init__(self)

        self.tile = tile
        self.contents = contents


if __name__ == '__main__':
    pass
