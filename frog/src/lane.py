'''lane.py

Objects, such as cars and logs, that move or reside along a lane.

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
log_images = [image.load(img_filename)]
img_filename = os.path.join(DIR, "images", 'log_medium.png')
log_images.append(image.load(img_filename))
img_filename = os.path.join(DIR, "images", 'log_small.png')
log_images.append(image.load(img_filename))

img_filename = os.path.join(DIR, "images", 'snake.png')
snake_image = image.load(img_filename)

turtle_images = []
for i in range(5):
    img_filename = os.path.join(DIR, "images", 'turtle%d.png'%i)
    turtle_images.append(image.load(img_filename))

class LaneObject(object):
    def __init__(self, lane, y_values):
        self.y = y_values[lane]
        self.lane = lane

    def update(self, dt):
        self.x += self.vx*dt
        if self.vx < 0:
            # flip the image about the y axis...
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

class Snake(LaneObject):
    def __init__(self, lane, x_values, y_values, vx):
        super(Snake, self).__init__(lane, y_values)
        self.image = snake_image
        if random.randint(0, 1) == 0:
            self.x = 0 - self.image.width
            self.vx = vx
        else:
            self.x = max(x_values)
            self.vx = -vx

        self.width = self.image.width
        self.height = self.image.height

class Log(LaneObject):
    '''floating log'''
    def __init__(self, lane, x_values, y_values, vx):
        super(Log, self).__init__(lane, y_values)
        self.image = log_images[random.randint(0, len(log_images)-1)]
        self.sunk = False  # a log always floats
        if x_values[lane] == 0:
            self.x = 0 - self.image.width
            self.vx = vx
        else:
            self.x = x_values[lane]
            self.vx = -vx

        self.width = self.image.width
        self.height = self.image.height

class Turtle(LaneObject):
    '''swimming_turtle'''
    def __init__(self, lane, x_values, y_values, vx):
        super(Turtle, self).__init__(lane, y_values)
        # the following is a series of floating/diving turtle images
        self.images = turtle_images
        self.sunk = False
        # fully at the surface:
        self.image = self.images[0]  #
        if x_values[lane] == 0:
            self.x = 0 - self.image.width
            self.vx = vx
        else:
            self.x = x_values[lane]
            self.vx = -vx

        self.width = self.image.width
        self.height = self.image.height

        self.swimming_cycle = [1.5, 0.4, 0.4, 0.4, 0.4]
        self.half_cycle_length = len(self.swimming_cycle)
        r = self.swimming_cycle[:]
        r.reverse()

        self.half_total_cycle_time = 0
        s = []
        for t in self.swimming_cycle:
            self.half_total_cycle_time += t
            s.append(self.half_total_cycle_time)
        self.swimming_cycle = s[:]
        total = 0
        for t in r:
            total += t
            self.swimming_cycle.append(self.half_total_cycle_time+total)
        # start at arbitrary time in the cycle
        self.cycle_time = random.random()*self.half_total_cycle_time*2


    def update(self, dt):
        self.cycle_time += dt
        if self.cycle_time > 2*self.half_total_cycle_time:
            self.cycle_time = 0
        self.image = self.images[0]
        if self.cycle_time < self.half_total_cycle_time:
            # cycle forward
            for i in range(self.half_cycle_length-1):
                if self.cycle_time > self.swimming_cycle[i]:
                    self.image = self.images[i+1]
        else:
            # cycle backward
            self.image = self.images[-1]
            for i in range(self.half_cycle_length, 2*self.half_cycle_length):
                if self.cycle_time > self.swimming_cycle[i]:
                    self.image = self.images[2*self.half_cycle_length-i-2]
        if self.image == self.images[-1]:
            self.sunk = True
        else:
            self.sunk = False
        super(Turtle, self).update(dt)

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