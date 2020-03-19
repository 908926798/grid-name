import pyglet
import math
from pyglet.gl import *

class Geom(object):
    def __init__(self):
        self.pos = None
        self.color = (0,0,0,255)

    def render(self):
        raise NotImplementedError

    def setPos( self ,pos ):
        self.pos = pos

class Polygon(Geom):
    def __init__(self, filled = True,color = (0,0,0,255)):
        super(Polygon,self).__init__()
        self.filled = filled
        self.color = color
        self.v = None

    def render(self):
        if self.filled:
            if   len(self.v) == 4 : glBegin(GL_QUADS)
            elif len(self.v)  > 4 : glBegin(GL_POLYGON)
            else: glBegin(GL_TRIANGLES)

            glColor4f( *self.color )
            for p in self.v:
                glVertex2f(p[0], p[1])  # draw each vertex
            glEnd()

        glColor4f(*(0,0,0,255))
        glBegin(GL_LINE_LOOP)
        for p in self.v:
            glVertex2f(p[0], p[1])  # draw each vertex
        glEnd()

class Square(Polygon):
    def __init__(self,filled=True,width = None,color=((255,255,255,255))):
        super(Square,self).__init__(filled,color )
        self.width = width

    def setPos( self ,pos ):
        self.pos = pos
        x,y = pos
        hw = self.width/2
        self.v=(
            (x-hw,y-hw),
            (x+hw,y-hw),
            (x+hw,y+hw),
            (x-hw,y+hw)
        )

class Circle(Polygon):
    def __init__(self,filled=True,radius=None,color=((255,255,255,255))):
        super(Circle,self).__init__(filled,color )
        self.res = 30
        self.radius = radius

    def setPos( self , pos ):
        self.pos=pos
        self.v = []
        for i in range(self.res):
            ang = 2*math.pi*i / self.res
            self.v.append((math.cos(ang)*self.radius + pos[0], math.sin(ang)*self.radius + pos[1]))


class Label(Geom):
    def __init__(self,text,color=(255,245,225)):
        Geom.__init__(self)
        self.label = pyglet.text.Label(text,
                              font_size=32,
                              color=color,
                              anchor_x='center', anchor_y='center')

    def render(self):
        self.label.draw()

    def setPos(self,pos):
        self.label.x = pos[0]
        self.label.y = pos[1]



class Point(Geom):
    def __init__(self):
        Geom.__init__(self)
    def render1(self):
        glBegin(GL_POINTS) # draw point
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()

class Compound(Geom):
    def __init__(self, gs):
        Geom.__init__(self)
        self.gs = gs
        for g in self.gs:
            g.attrs = [a for a in g.attrs if not isinstance(a, Color)]
    def render1(self):
        for g in self.gs:
            g.render()

class PolyLine(Geom):
    def __init__(self, v, close):
        Geom.__init__(self)
        self.v = v
        self.close = close
        self.linewidth = LineWidth(1)
        self.add_attr(self.linewidth)
    def render1(self):
        glBegin(GL_LINE_LOOP if self.close else GL_LINE_STRIP)
        for p in self.v:
            glVertex3f(p[0], p[1],0)  # draw each vertex
        glEnd()
    def set_linewidth(self, x):
        self.linewidth.stroke = x

class Line(Geom):
    def __init__(self, start=(0.0, 0.0), end=(0.0, 0.0)):
        Geom.__init__(self)
        self.start = start
        self.end = end
        self.linewidth = LineWidth(1)
        self.add_attr(self.linewidth)

    def render1(self):
        glBegin(GL_LINES)
        glVertex2f(*self.start)
        glVertex2f(*self.end)
        glEnd()

class Image(Geom):
    def __init__(self, fname, width, height):
        Geom.__init__(self)
        self.width = width
        self.height = height
        img = pyglet.image.load(fname)
        self.img = img
        self.set_color(1,1,1,1)
        self.flip = False
    def render1(self):
        self.img.blit(-self.width/2, -self.height/2, width=self.width, height=self.height)
