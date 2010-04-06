# Simplified main file

import pyglet

from src.ball import Ball
from src.game_info import GameInfo

game_window = pyglet.window.Window(width=600, height=400, caption="Breakout")
game_info = GameInfo(game_window)
ball = Ball(game_window.width/2, game_window.height/2, 20, game=game_info)

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
