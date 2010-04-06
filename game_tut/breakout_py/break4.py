# Adding a ball at the center of the screen

import pyglet

# For simple but nice looking games, we would normally use images to represent
# objects.  Here we will use some simple graphical shapes created by Pyglet
# itself.  However, Pyglet uses OpenGL for graphics, which is very low level
# and may look a bit daunting.
from pyglet.gl import *

game_window = pyglet.window.Window(width=600, height=400, caption="Breakout")

class Ball(object):
    ''' Ball object that knows how to draw itself '''
    def __init__(self, x, y, r, color=(1.0, 1.0, 1.0, 1.0)):
        '''circle of radius r centered at (x, y) and opaque white by default'''
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self):
        '''draws a circle'''
        # This is a very low level function which does not need to be
        # understood at this time
        glPushMatrix()
        glColor4f(*self.color)
        glTranslatef(self.x, self.y, 0)
        q = gluNewQuadric()
        # a circle is written as a number of triangular slices; we use
        # a maximum of 360 which looked smooth even for a circle as
        # large as 1500 px.
        # Smaller circles can be drawn with fewer slices - the rule we
        # use amount to approximately 1 slice per px on the circumference
        slices = min(360, 6*self.r)
        gluDisk(q, 0, self.r, slices, 1)
        glPopMatrix()
        return

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


if __name__ == '__main__':
    pyglet.app.run()
