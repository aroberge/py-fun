# Making the ball bounce within the window - except at the bottom

import pyglet
from pyglet.gl import *

game_window = pyglet.window.Window(width=600, height=400, caption="Breakout")

class Ball(object):
    ''' Ball object that knows how to draw itself '''
    def __init__(self, x, y, r, dx=120, dy=120, color=(1.0, 1.0, 1.0, 1.0)):
        '''circle of radius r centered at (x, y) and opaque white by default'''
        self.x = x
        self.y = y
        self.r = r
        # note that we chose to give these some default values
        self.dx = dx
        self.dy = dy
        self.color = color

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
            game_info.over = True
            return
        self.x += self.dx * dt
        self.y += self.dy * dt
        if (self.x - self.r < 0) or (self.x + self.r > game_window.width):
            self.dx = - self.dx
        if (self.y + self.r > game_window.height):
            self.dy = - self.dy

class GameInfo(object):
    '''A simple class to keep track of game information '''
    def __init__(self, game_window):
        self.over = False
        self.game_over_label = pyglet.text.Label('Game over!',
                          font_name='Times New Roman',
                          font_size=72,
                          x=game_window.width//2, y=game_window.height//2,
                          anchor_x='center', anchor_y='center',
                          color=(255, 0, 0, 255))
        self.game_window = game_window

    def draw(self):
        '''draws "Game over!" on screen if game is finished'''
        if self.over:
            self.game_over_label.draw()

game_info = GameInfo(game_window)
ball = Ball(game_window.width/2, game_window.height/2, 20)

@game_window.event
def on_draw():
    game_window.clear()
    ball.draw()
    game_info.draw()

def update(dt):
    ball.update(dt)
pyglet.clock.schedule_interval(update, 1/30.)

if __name__ == '__main__':
    pyglet.app.run()
