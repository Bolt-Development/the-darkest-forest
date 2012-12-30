# TODO :: import pubsub
from TileContents import *


class Tile(PubSub):
    def __init__(self, column, row, width, height):
        PubSub.__init__(self)
        
        self.column = column
        self.row = row
        self.width = width
        self.height = height

        # TODO :: add global position variable
        self.contents = TileContents()


if __name__ == '__main__':
    pass
