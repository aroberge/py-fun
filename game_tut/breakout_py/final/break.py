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

    def move(self, direction):
        if direction == 'right':
            self.x += self.move_increment
        elif direction == 'left':
            self.x -= self.move_increment
        else:
            print("Unexpected direction in Paddle move().")
            raise NotImplementedError

paddle = Paddle(100, 10, 100, 10)

@game_window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        paddle.move('left')
    elif symbol == key.RIGHT:
        paddle.move('right')

# capturing auto-repeat
@game_window.event
def on_text_motion(symbol):
    if symbol == key.LEFT:
        paddle.move('left')
    elif symbol == key.RIGHT:
        paddle.move('right')

game_window.set_mouse_visible(False)
@game_window.event
def on_mouse_motion(x, y, dx, dy):
    paddle.x = x
    if (paddle.x + paddle.width) > game_window.width:
        paddle.x = game_window.width - paddle.width


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
