import pyglet

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
        self._window = game_window

    def draw(self):
        '''draws "Game over!" on screen if game is finished'''
        if self.over:
            self.game_over_label.draw()