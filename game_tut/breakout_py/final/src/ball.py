from pyglet.gl import *

class Ball(object):
    ''' Ball object that knows how to draw itself '''
    def __init__(self, x, y, r, dx=120, dy=120, color=(1.0, 1.0, 1.0, 1.0),
                 game=None):
        '''circle of radius r centered at (x, y) and opaque white by default'''
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.color = color
        self.game = game

    def draw(self):
        '''draws a circle'''
        glPushMatrix()
        glColor4f(*self.color)
        glTranslatef(self.x, self.y, 0)
        q = gluNewQuadric()
        slices = min(360, 6*self.r)
        gluDisk(q, 0, self.r, slices, 1)
        glPopMatrix()
        return

    def update(self, dt):
        '''moves the ball by a "normal" increment, ensuring it stays within
           the window by reversing its velocity direction if needed'''
        if (self.y - self.r < 0):
            self.game.over = True
            return
        self.x += self.dx * dt
        self.y += self.dy * dt
        if (self.x - self.r < 0) or (self.x + self.r > self.game._window.width):
            self.dx = - self.dx
        if (self.y + self.r > self.game._window.height):
            self.dy = - self.dy