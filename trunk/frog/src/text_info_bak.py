'''text_info.py

Textual information to be displayed
'''

from pyglet import font
from pyglet.font import Text

class Score(Text):
    def __init__(self, win, text, x, y):
        ft = font.load('Arial', 36)
        self.win = win
        Text.__init__(self, ft, text)
        self.score = 0
        self.x = x
        self.y = y

    def update(self):
        self.text = 'Score: %d'%self.score
        self.draw()

    def reached_pad(self):
        self.score += 10

time_string = 'Remaining time: %3.1f'
class Time(Text):
    def __init__(self, win,  x, y):
        ft = font.load('Arial', 36)
        self.win = win
        self.time_for_game = 10
        Text.__init__(self, ft, time_string%self.time_for_game)
        self.restart()
        self.x = x
        self.y = y

    def restart(self):
        self.time_left = self.time_for_game

    def update(self, dt):
        self.time_left -= dt
        if self.time_left >= 0:
            self.text = time_string%self.time_left
        else:
            self.text = time_string%0
        self.draw()