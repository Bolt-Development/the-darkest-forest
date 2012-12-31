from ..common.PubSub import *


class Tile(PubSub):
    def __init__(self, column, row, width, height):
        PubSub.__init__(self)
        
        self.column = column
        self.row = row
        self.width = width
        self.height = height

        self.contents = []


    def add_contents(self, conts, unique = True):
        if unique:
            if conts not in self.contents:
                self.contents.append(conts)
        else:
            self.contents.append(conts)

    def remove_contents(self, conts):
        try:
            self.remove(conts)
        except:
            pass

    


if __name__ == '__main__':
    pass
