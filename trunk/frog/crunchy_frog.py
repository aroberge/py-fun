''' froggie.py; a Frogger-like game.

By Andre Roberge

This module is meant to define only the basic windowing functions and
contain the main loop.  The idea is that the possible states of the game
could be quickly and easily grasped by looking at this module.
The actual game details are contained in other modules.
'''

from pyglet import window
from pyglet import clock
from pyglet import media
from pyglet.window import key
from pyglet.gl import *

from pyglet import options

from src.game import World, Game

SPEED_TEST = False
world = World()
if SPEED_TEST:
    options['gl_error_check'] = False
    win = window.Window(world.window_width, world.window_height, vsync=False)
    fps_display = clock.ClockDisplay()
else:
    win = window.Window(world.window_width, world.window_height)
    clock.set_fps_limit(60)

glEnable(GL_BLEND)  # required for transparency handling
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
win.clear() # start with a blank (black) window to display something quickly
win.flip()  # even if loading times are slow

# the game state (pause, restart, etc) can be assigned via the keyboard
@win.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        win.has_exit = True
    elif symbol == key.R:
        restart()
    elif symbol == key.P or symbol == key.SPACE:
        game.switch_pause_state()
    # the following are for diagnostic
    elif symbol == key.I and  modifiers == (key.MOD_SHIFT | key.MOD_CTRL):
        if game.frog.invincible:
            game.frog.invincible = False
        else:
            game.frog.invincible = True
    elif symbol == key.L and  modifiers == (key.MOD_SHIFT | key.MOD_CTRL):
        game.level += 1

def restart():
    global game
    game = Game(win)
    # Ensure that the playing character ("game.frog") receives event information
    win.push_handlers(game.frog)

restart()

# the simplest possible loop!
while not win.has_exit:
    win.dispatch_events()
    media.dispatch_events() # required for sound
    dt = clock.tick()
    win.clear()
    game.update(dt)  # all the complexity is hidden here!
    if SPEED_TEST:
        fps_display.draw()
    win.flip()