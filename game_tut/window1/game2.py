# blank window with a title only

import pyglet

game_window = pyglet.window.Window(width=800, height=600, caption="My game")

@game_window.event
def on_draw():
    game_window.clear()

pyglet.app.run()
