'''lane.py

Objects, such as cars and logs, that move along a lane.

'''

import os
import random

from pyglet import image
from pyglet.gl import *

DIR = os.path.dirname(__file__)

car_images = []
for i in range(1, 5):
    img_filename = os.path.join(DIR, "images", 'car0%d.png'%i)
    car_images.append(image.load(img_filename))

img_filename = os.path.join(DIR, "images", 'car_limo01.png')
car_images.append(image.load(img_filename))
img_filename = os.path.join(DIR, "images", 'car_truck01.png')
car_images.append(image.load(img_filename))

img_filename = os.path.join(DIR, "images", 'log.png')
log_image = image.load(img_filename)

class LaneObject(object):
    def __init__(self, lane, y_values):
        self.y = y_values[lane]
        self.lane = lane

    def update(self, dt):
        self.x += self.vx*dt
        if self.vx < 0:
            # flip the image
            glLoadIdentity()
            # make the origin coincide with image, then rotate
            glTranslatef(self.x, self.y, 0)
            glRotatef(180, 0, 1, 0)
            # blit the image in the opposite quadrant
            self.image.blit(-self.image.width, 0)
            # restore previous coordinate system
            glRotatef(-180, 0, 1, 0)
            glTranslatef(-self.x, -self.y, 0)
        else:
            self.image.blit(self.x, self.y)

class Car(LaneObject):
    '''could be a car, a limo or a truck'''
    def __init__(self, lane, x_values, y_values, vx):
        super(Car, self).__init__(lane, y_values)
        self.image = car_images[random.randint(0, len(car_images)-1)]
        if x_values[lane] == 0:
            self.x = 0 - self.image.width
            self.vx = vx
        else:
            self.x = x_values[lane]
            self.vx = -vx

        self.width = self.image.width
        self.height = self.image.height

class Log(LaneObject):
    '''floating log'''
    def __init__(self, lane, x_values, y_values, vx):
        super(Log, self).__init__(lane, y_values)
        self.image = log_image
        if x_values[lane] == 0:
            self.x = 0 - self.image.width
            self.vx = vx
        else:
            self.x = x_values[lane]
            self.vx = -vx

        self.width = self.image.width
        self.height = self.image.height
