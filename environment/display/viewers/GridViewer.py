import numpy as np
from environment.display.base.BaseViewer import BaseViewer
from environment.display.base.Geom import *

class GridViewer(BaseViewer):
    def __init__( self,X,Y,world):
        super(GridViewer,self).__init__()
        self.grid_size = 100
        self.width = self.grid_size * X
        self.height = self.grid_size * Y
        self.world = world
        self.window = pyglet.window.Window(width=self.width, height=self.height)

        self.initialized = False
        self.geom_templates = [
            Square(width=self.grid_size,color = (255,255,255,255)),
            Circle(radius= self.grid_size/3, color=(255, 0, 0, 255)),
            Label( 'Key', color=(100, 100, 0, 255)),
            Label( 'Door', color=(0, 100, 100, 255))
        ]
    def render(self):
        if self.initialized== False:
            self.initialized = True

        glClearColor( 255, 255, 255, 255 )
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()

        for raw_grids in self.world.grids:
            for grid in raw_grids:
                #grid
                self.draw( grid, grid.pos )
                #item
                for item in grid.contents:
                    self.draw( item, grid.pos )

        self.window.flip()

    def draw( self, item, pos ):
        pos = ( np.array( pos ) + 0.5 ) * self.grid_size
        geom = self.geom_templates[item.looks_like]
        geom.setPos(pos)
        geom.render()
