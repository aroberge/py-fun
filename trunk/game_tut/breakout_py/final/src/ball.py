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
        if self.collide_with_rectangle(self.game.paddle):
            self.dy = - self.dy


    def collide_with_rectangle(self, rect):
        '''determines if a collision (overlap) occurs with a rectangular
        object.'''

        # Cases where the ball is clearly outside the rectangle
        if (self.x + self.r) < rect.x:
            return False
        elif (self.x - self.r) > rect.x + rect.width:
            return False
        elif (self.y + self.r) < rect.y:
            return False
        elif (self.y - self.r) > self.y + rect.height:
            return False

        # Cases where the ball is clearly inside the rectangle
        if (rect.x < self.x < (rect.x + rect.width)  and
            rect.y < self.y < (rect.y + rect.height)):
            return True

        ## Cases where one of the edges of the ball is clearly inside the rect.
        #if rect.x < self.x < (rect.x + rect.width):
        #    if ((self.y + self.r > rect.y)
        #        (self.y - self.r < rect.y + rect.height)):
        #        return True
        #elif rect.y < self.y < (rect.y + rect.height):
        #    if ((self.x + self.r > rect.x) or
        #        (self.x - self.r < rect.x + rect.width)):
        #        return True

        # we are left with edge cases
        r2 = self.r**2

        if self.x < rect.x:
            x2 = (rect.x - self.x)**2
            if self.y < rect.y:
                if x2 + (rect.y - self.y)**2 < r2:
                    return True
                else:
                    return False
            elif self.y > rect.y + rect.height:
                if x2 + (rect.y + rect.height - self.y)**2 < r2:
                    return True
                else:
                    return False
        else:   # self.x >= rect.x + rect.width
            x2 = (self.x - rect.x - rect.width)**2
            if self.y < rect.y:
                if x2 + (rect.y - self.y)**2 < r2:
                    return True
                else:
                    return False
            elif self.y > rect.y + rect.height:
                if x2 + (rect.y + rect.height - self.y)**2 < r2:
                    return True
                else:
                    return False
