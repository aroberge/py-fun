''' froggie.py

Frogger-like game with graphics adapted from Lee Harr's (creator of pygsear).

'''
import os

from pyglet import window
from pyglet import clock
from pyglet import media
from pyglet.window import key
from pyglet.gl import *

from src.frog import Frog
from src.game import World, Game

clock.set_fps_limit(60)

world = World()
win = window.Window(World.width, World.height+60)
glEnable(GL_BLEND)  # required for transparency handling
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
win.clear()
win.flip()

@win.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        win.has_exit = True
    elif symbol == key.R:
        restart()
    elif symbol == key.P or symbol == key.SPACE:
        if game.paused:
            game.paused = False
            if game.level_completed:
                game.new_level()
        else:
            game.paused = True


def restart():
    global game, frog
    game = Game(win)
    game.over = False
    game.paused = True
    frog = Frog(game, world)
    win.push_handlers(frog)
    game.frog = frog

restart()

while not win.has_exit:
    win.dispatch_events()
    media.dispatch_events()
    dt = clock.tick()
    win.clear()

    if game.over or game.level_completed:
        dt = 0
    if game.paused:
        dt = 0
    game.update(dt)

    win.flip()