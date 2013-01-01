from TestingUtils import *

class GridView(object):
    def __init__(self, grid, width, height):
        self.grid = grid
        
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        
        self.scale_x = width / float(self.grid.width)
        self.scale_y = height / float(self.grid.height)
        
    def on_render(self, event, **kwargs):
        surface = kwargs['surface']
        self.render_on_surface(surface)
        
    def on_mouse_moved(self, event, **kwargs):
        x, y  = kwargs['position']
        column, row = self.position_to_column_row(x, y)
        if column and row:
            self.grid.tag('mouse_over', column, row)
            
    def on_mouse_down(self, event, **kwargs):
        x, y  = kwargs['position']
        column, row = self.position_to_column_row(x, y)
        if column and row:
            self.grid.tag('mouse_down_' + str(kwargs['button']), column, row)
            
        
    def position_on_self(self, tile): 
        x = self.x + (self.scale_x * tile.column * tile.width) + 1
        y = self.y + (self.scale_y * tile.row * tile.height) + 1
        w = self.scale_x * tile.width - 1
        h = self.scale_y * tile.height - 1
        return [x, y, w, h]
        
    def position_to_column_row(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                dx = ((x - self.x) / float(self.width)) * self.grid.columns
                dy = ((y - self.y) / float(self.height)) * self.grid.rows
                return dx, dy
        return False, False
        
    def render_on_surface(self, surface):
        for column in xrange(self.grid.columns):
            x = self.x + (self.scale_x * column * self.grid.space_width)
            pygame.draw.line(surface, (255, 255, 255), (x, self.y), (x, self.grid.height * self.scale_y))
        pygame.draw.line(surface, (255, 255, 255), (self.x + self.width, self.y), (self.x + self.width, self.grid.height * self.scale_y))
            
        for row in xrange(self.grid.rows):
            y = self.y + (self.scale_y * row * self.grid.space_height)
            pygame.draw.line(surface, (255, 255, 255), (self.x, y), (self.x + self.grid.width * self.scale_x, y))
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y + self.height), (self.x + self.grid.width * self.scale_x, self.y + self.height))

        mouse_over = self.grid.get_tag('mouse_over')
        if mouse_over:
            pygame.draw.rect(surface, (0, 0, 255), self.position_on_self(mouse_over))
            
        mouse_down = self.grid.get_tag('mouse_down_1')
        if mouse_down:
            pygame.draw.rect(surface, (0, 255, 255), self.position_on_self(mouse_down))

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
        grid = Grid(engine.width, engine.height, 10, 6)
        grid.init(tile_generator)
        
        view = GridView(grid, engine.width - 200, engine.height - 1)
        
        # benefits of MVC
        mini_view = GridView(grid, 100, 100)
        mini_view.x = engine.width - mini_view.width - 1
        
        engine.on('render', view.on_render)
        engine.on('render', mini_view.on_render)
        
        engine.on('mouse_motion', view.on_mouse_moved)
        engine.on('mouse_motion', mini_view.on_mouse_moved)
        
        engine.on('mouse_down', view.on_mouse_down)
        engine.on('mouse_down', mini_view.on_mouse_down)

    
    engine = Engine()
    engine.set_caption('Grid Testing')
    engine.on('init', on_init, memory=True)
    engine.start()
