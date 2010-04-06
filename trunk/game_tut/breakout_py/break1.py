# blank window with a title only

import pyglet

game_window = pyglet.window.Window(width=600, height=400, caption="Breakout")

@game_window.event
def on_draw():
    game_window.clear()

if __name__ == '__main__':
    pyglet.app.run()
