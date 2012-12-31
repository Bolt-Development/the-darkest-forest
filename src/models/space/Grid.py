from ..common.PubSub import *

class Grid(PubSub):
    def __init__(self, width, height, columns, rows):
        PubSub.__init__(self)

        self.width = width
        self.height = height

        self.columns = columns
        self.rows = rows


if __name__ == '__main__':
    pass
