# Every game needs a game over screen !

import pyglet

game_window = pyglet.window.Window(width=600, height=400, caption="Breakout")

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

@game_window.event
def on_draw():
    game_window.clear()
    game_info.draw()

if __name__ == '__main__':
    game_info.over = True  # test it!
    pyglet.app.run()
