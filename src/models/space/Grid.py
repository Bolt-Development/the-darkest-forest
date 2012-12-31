from ..common.PubSub import *

class Grid(PubSub):
    def __init__(self, width, height, columns, rows):
        PubSub.__init__(self)

        self.width = width
        self.height = height

        self.columns = columns
        self.rows = rows

        self.space_width = self.width / self.columns
        self.space_height = self.height / self.rows

        self.elems = []
        self.init = False

    def init(self, generator):
        for column in xrange(self.columns):
            for row in xrange(self.rows):
                self.elems.append(generator(self, column, row))
        self.emit('init', emitter = self)


    def get(self, column, row):
        if not self.init:
            return None
        
        guarded_column = column % self.columns
        guarded_row = row % self.rows

        if guarded_column < 0:
            guarded_column += self.columns
        if guarded_row < 0:
            guarded_row += self.rows

        index = self.to_index(guarded_column, guarded_row);
        return self.elems[index];

if __name__ == '__main__':
    pass
