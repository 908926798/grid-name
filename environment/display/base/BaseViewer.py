import pyglet
from pyglet.gl import *

class BaseViewer(object):
    def __init__(self):
        self.geoms = {}

        glEnable(GL_BLEND)
        # glEnable(GL_MULTISAMPLE)
        glEnable(GL_LINE_SMOOTH)
        # glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glLineWidth(2.0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def render(self, return_rgb_array=False):
        glClearColor(255,255,255,255)
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        # self.transform.enable()
        self.window.flip()