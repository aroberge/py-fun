'''pad.py


'''
import os
from pyglet import image

DIR = os.path.dirname(__file__)

class LillyPad(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        img_filename = os.path.join(DIR, "images", 'pad.png')
        self.pad_image = self.pad_empty = image.load(img_filename)
        self.width = self.pad_image.width
        self.height = self.pad_image.height
        img_filename = os.path.join(DIR, "images", 'padfull.png')
        self.pad_full = image.load(img_filename)

    def update(self):
        self.pad_image.blit(self.x, self.y)

    def set_occupied(self):
        self.pad_image = self.pad_full
        self.occupied = True

    def set_empty(self):
        self.pad_image = self.pad_empty
        self.occupied = False