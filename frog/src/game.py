'''game.py

'''

import os
import random
from pyglet import image
from pyglet import font
from pyglet.font import Text

import util
from lane import Car, Log
from pad import LillyPad

DIR = os.path.dirname(__file__)
img_filename = os.path.join(DIR, "images", 'bg.png')

time_string = 'Remaining time: %3.1f'
score_string = 'Score: %d'

class World(object):
    width = 800
    height = 600
    x = 0
    y = 0
    nb_lanes = 10
    lane_width = height/10
    lane_with_cars = [1, 2, 3, 4]
    lane_with_logs = [6, 7, 8]
    pad_lane = 9
    background = image.load(img_filename)
    # position of each lane
    y_values = [lane_width*i for i in range(10)]
    # starting position; 0: from left; width: from right
    x_values = [0, 0, 0, width, width, 0, width, 0, width]
    vx_values = [0, 35, 60, 60, 35, 0, 40, 80, 60]

class Game(object):
    def __init__(self, window):
        self.world = World()
        self.score = Score(10, self.world.height+10)
        self.time_remaining = Time(200, self.world.height+10)
        self.message = Message(50, 5)
        self.max_nb_levels = 3
        self.level = 1
        self.over = False
        self.level_completed = False
        self.spawn_delay = {}
        self.approx_nb_object_per_lane = []
        for lane in range(self.world.nb_lanes):
            self.approx_nb_object_per_lane.append(4.0)
        self.pads = []
        for i in range(5):
            self.pads.append(LillyPad(45 + 160*i, 540))
        self.cars = []
        for lane in self.world.lane_with_cars:
            self.cars.append(Car(lane, self.world.x_values, self.world.y_values,
                                 self.world.vx_values))
            self.spawn_delay[lane] = self.calculate_delay(lane, self.cars[-1].width,
                                               self.world.vx_values[lane])
        self.logs = []
        for lane in self.world.lane_with_logs:
            self.logs.append(Log(lane, self.world.x_values, self.world.y_values,
                                 self.world.vx_values))
            self.spawn_delay[lane] = self.calculate_delay(lane, self.logs[-1].width,
                                               self.world.vx_values[lane])
        self.frog = None  # initialised in main module


    def calculate_delay(self, lane, width, vx):
        factor = random.gauss(self.approx_nb_object_per_lane[lane], 1.0)
        delay = 1.0 * width/vx + self.world.width/(factor*vx)
        return delay

    def set_level_completed(self, lives):
        self.score.score += lives*40*self.level
        self.score.score += 100*self.level
        self.score.score += self.time_remaining.time_left*self.level
        self.level += 1
        if self.level > self.max_nb_levels:
            self.game_won()
        self.message.text = "Level completed; press spacebar to start"
        self.paused = True
        self.level_completed = True
        self.update(0)

    def game_won(self):
        self.over = True
        self.message.text = "You won!  Your score is %d"%self.score.score
        self.paused = True
        self.update(0)

    def new_level(self):

        self.message.text = "Press spacebar to start"
        # less time
        self.time_remaining.time_for_game -= 2
        self.time_remaining.restart()
        # faster movement
        for i, v in enumerate(self.world.vx_values):
            if i in self.world.lane_with_cars:
                self.world.vx_values[i] = v*1.3
        for lane in self.world.lane_with_cars:
            self.approx_nb_object_per_lane[lane] += 0.5 # more cars
        for lane in self.world.lane_with_logs:
            self.approx_nb_object_per_lane[lane] /= 1.1 # fewer logs
        self.level_completed = False
        self.frog.start_new_level(lives=4)
        for pad in self.pads:
            pad.set_empty()
        self.update(0)

    def update(self, dt):
        self.world.background.blit(0, 0)
        for pad in self.pads:
            pad.update()

        if self.frog.dying: # we pause the animation
            saved_dt = dt
            dt = 0
        else:  # we see if we need to generate new moving objects
            for lane in self.spawn_delay:
                self.spawn_delay[lane] -= dt
                if self.spawn_delay[lane] < 0:
                    if lane in self.world.lane_with_cars:
                        self.cars.append(Car(lane, self.world.x_values, self.world.y_values,
                                             self.world.vx_values))
                        self.spawn_delay[lane] = self.calculate_delay(lane, self.cars[-1].width,
                                                   self.world.vx_values[lane])
                    elif lane in self.world.lane_with_logs:
                        self.logs.append(Log(lane, self.world.x_values, self.world.y_values,
                                             self.world.vx_values))
                        self.spawn_delay[lane] = self.calculate_delay(lane, self.logs[-1].width,
                                                   self.world.vx_values[lane])

        for car in self.cars:
            car.update(dt)
        for log in self.logs:
            log.update(dt)

        # Remove objects that have left the world
        self.cars = [car for car in self.cars if not util.outside_world(car, self.world)]
        self.logs = [log for log in self.logs if not util.outside_world(log, self.world)]

        self.time_remaining.update(dt)
        if self.frog.dying:
            dt = saved_dt
        self.frog.update(dt, self.pads, self.cars, self.logs)
        self.score.update()
        if self.paused:
            self.message.update()
        elif self.over:
            self.message.text = "Game over"
            self.message.update()

class Score(Text):
    def __init__(self, x, y):
        ft = font.load('Arial', 36)
        Text.__init__(self, ft, score_string%0)
        self.score = 0
        self.x = x
        self.y = y

    def update(self):
        self.text = score_string%self.score
        self.draw()

    def reached_pad(self):
        self.score += 10

class Time(Text):
    def __init__(self,  x, y):
        ft = font.load('Arial', 36)
        self.time_for_game = 30
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

class Message(Text):
    def __init__(self,  x, y):
        ft = font.load('Arial', 36)
        Text.__init__(self, ft, "Press space bar to start")
        self.x = x
        self.y = y

    def update(self):
        self.draw()