from ..common.PubSub import *
class Grid(PubSub):
    def __init__(self, width, height, columns, rows):
        PubSub.__init__(self)

        self.width = width
        self.height = height

        self.columns = columns
        self.rows = rows

        self.space_width = self.width / float(self.columns)
        self.space_height = self.height / float(self.rows)

        self.elems = []
        self.tagged = []
        self.is_init = False

    def init(self, generator):
        for column in xrange(self.columns):
            for row in xrange(self.rows):
                self.elems.append(generator(self, column, row))
        self.is_init = True
        self.emit('init', emitter = self)
        
    def to_index(self, column, row):
        return column * self.rows + row
    
    def position_to_index(self, x, y):
        return x / self.space_width, y / self.space_height

    def tag(self, column, row):
        try:
            element = self.get(column, row)
            self.tagged.append(element)
            self.emit('tagged', target=element)
        except:
            pass
        
    def untag(self, column, row):
        try:
            element = self.get(column, row)
            self.tagged.remove(element)
            self.emit('untagged', target=element)
        except:
            pass
        
    def clear_tags(self):
        self.emit('cleared_taggs', tags=self.tagged)
        self.tagged = []

    def get(self, column, row):
        if not self.is_init:
            return None
        
        guarded_column = column % self.columns
        guarded_row = row % self.rows

        if guarded_column < 0:
            guarded_column += self.columns
        if guarded_row < 0:
            guarded_row += self.rows

        index = self.to_index(guarded_column, guarded_row);
        return self.elems[index];

    def map_over_elems(self, fun):
        return [fun(element) for element in self.elems]
    
if __name__ == '__main__':
    pass
