# viewing keyboard events

import pyglet
from pyglet.window import key
from pyglet.gl import *

from src.ball import Ball
from src.game_info import GameInfo

game_window = pyglet.window.Window(width=600, height=400, caption="Breakout")
game_info = GameInfo(game_window)
ball = Ball(game_window.width/2, game_window.height/2, 20, game=game_info)

class Paddle(object):
    def __init__(self, x, y, width, height, color=(1.0, 1.0, 1.0, 1.0),
                 move_increment=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.move_increment = move_increment

    def draw(self):
        glBegin(GL_QUADS)
        glColor4f(*self.color)
        glVertex2i(self.x, self.y)
        glVertex2i(self.x + self.width, self.y)
        glVertex2i(self.x + self.width, self.y + self.height)
        glVertex2i(self.x, self.y + self.height)
        glEnd()

    def move_by(self, dx):
        self.x += dx
        self.stay_within_bounds()

    def move_left(self):
        self.move_by(-self.move_increment)

    def move_right(self):
        self.move_by(self.move_increment)

    def move_to(self, x):
        self.x = x
        self.stay_within_bounds()

    def stay_within_bounds(self):
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > game_window.width:
            self.x = game_window.width - self.width


paddle = Paddle(100, 10, 100, 10)
game_info.paddle = paddle


@game_window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        paddle.move_left()
    elif symbol == key.RIGHT:
        paddle.move_right()
    elif symbol == key.F:
        # todo: need to reset screen size and scale everything
        if game_window.fullscreen:
            game_window.set_fullscreen(False)
        else:
            game_window.set_fullscreen(True)


# capturing auto-repeat
@game_window.event
def on_text_motion(symbol):
    if symbol == key.LEFT:
        paddle.move_left()
    elif symbol == key.RIGHT:
        paddle.move_right()

game_window.set_mouse_visible(False)
@game_window.event
def on_mouse_motion(x, y, dx, dy):
    if game_window.fullscreen:
        paddle.move_by(int(dx))
    else:
        paddle.move_to(x)

@game_window.event
def on_draw():
    game_window.clear()
    ball.draw()
    paddle.draw()
    game_info.draw()

def update(dt):
    ball.update(dt)
pyglet.clock.schedule_interval(update, 1/30.)

if __name__ == '__main__':
    pyglet.app.run()
