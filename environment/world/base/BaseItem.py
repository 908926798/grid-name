# from environment.display.base.Geom import *

class Grid():
    def __init__(self,pos,world):
        self.pos = pos
        self.world = world
        self.looks_like = 0
        self.contents = []

    def addContent( self,item ):
        self.contents.append(item)
        item.grid = self
        item.world = self.world


class Item():
    def __init__( self):
        self.world = None
        self.grid = None
        self.geom = None
        self.looks_like = None

    def touched( self ):
        raise NotImplementedError