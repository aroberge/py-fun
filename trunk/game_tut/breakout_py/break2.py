# Add a Game over screen; adapted from the "Hello world" example

import pyglet

game_window = pyglet.window.Window(width=600, height=400, caption="Breakout")

game_over = pyglet.text.Label('Game over!',
                          font_name='Times New Roman',
                          font_size=72,
                          x=game_window.width//2, y=game_window.height//2,
                          anchor_x='center', anchor_y='center',
                          color=(255, 0, 0, 255))

@game_window.event
def on_draw():
    game_window.clear()
    game_over.draw()

if __name__ == '__main__':
    pyglet.app.run()
