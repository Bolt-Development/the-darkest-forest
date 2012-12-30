from Tile import *
# TODO :: import PubSub


class TileContents(PubSub):
    def __init__(self, tile):
        PubSub.__init__(self)

        self.tile = tile
        self.contents = []

    def add_content(self, content):
        if content in self.contents:
            self.contents.append(content)
            self.emit('added', added = content)


    def remove_content(self, content):
        if content in self.contents:
            self.contents.remove(content)
            self.emit('removed', removed = content)


if __name__ == '__main__':
    pass
