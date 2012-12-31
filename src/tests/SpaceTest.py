from TestingUtils import *

class GridView(object):
    def __init__(self, grid):
        self.grid = grid
        
    def on_render(self, event, **kwargs):
        surface = kwargs['surface']
        self.render_on_surface(surface)
        
    def render_on_surface(self, surface):
        for column in xrange(self.grid.columns):
            for row in xrange(self.grid.rows):
                space = self.grid.get(column, row)
                self.render_space(space, surface)   # ideally handled by a tile view class
                
    def render_space(self, space, surface):
        x, y = space.column * space.width, space.row * space.height
        left = x + space.width
        bottom = y + space.height
        
        pygame.draw.line(surface, (255, 255, 255), (x, y), (left, y))
        pygame.draw.line(surface, (255, 255, 255), (left, y), (left, bottom))
        pygame.draw.line(surface, (255, 255, 255), (x, bottom), (left, bottom))
        pygame.draw.line(surface, (255, 255, 255), (x, y), (x, bottom))

if __name__ == '__main__':
    add_source_folder()
    
    from models.Engine import *
    from models.space.Grid import *
    from models.space.Tile import *

    grid = None

    def on_init(event, **kwargs):
        engine = kwargs['emitter']
        def tile_generator(grid, column, row):
            return Tile(column, row, grid.space_width, grid.space_height)
        grid = Grid(engine.width, engine.height, 100, 100)
        grid.init(tile_generator)
        
        view = GridView(grid)
        engine.on('render', view.on_render)

    
    engine = Engine()
    engine.set_caption('Grid Testing')
    engine.on('init', on_init, memory=True)
    engine.start()
