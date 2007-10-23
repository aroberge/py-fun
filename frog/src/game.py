'''game.py

'''

import os
import random
from pyglet import image
from pyglet import font
from pyglet.font import Text

from pyglet.gl import *


import util
from lane import Car, Log
from pad import LillyPad
from frog import Frog

DIR = os.path.dirname(__file__)
img_filename = os.path.join(DIR, "images", 'bg.png')

time_string = 'Time: %3.1f'
score_string = 'Score: %d'

class World(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        # physical dimensions of the frog world are determined from an
        # existing image
        self.background = image.load(img_filename)
        self.width = self.background.width
        self.height = self.background.height
        # window dimension is adapted to leave room for information at the top
        # this is used to initialised the actual window in the main module
        self.window_width = self.width
        self.window_height = self.height + 60
        # The background image is composed of horizontal lanes in which
        # non-playing characters (NPC) can move; these are relevant details
        self.nb_lanes = 10
        self.lane_width = self.height/self.nb_lanes
        self.lane_with_cars = [1, 2, 3, 4]
        self.lane_with_logs = [6, 7, 8]
        self.pad_lane = 9
        # position of each lane
        self.y_values = [self.lane_width*i for i in range(10)]
        # starting position of moving NPC:
        # 0: from left; self.width: from the right; -1: either side
        self.x_values = [0, 0, 0, self.width, self.width, -1, self.width, 0, self.width]
        # initial velocities of moving NPC
        self.vx_values = [0, 35, 60, 60, 35, 0, 50, 80, 60]

class Game(object):
    def __init__(self, window):
        self.world = World()
        self.score = Score(10, self.world.height+10)
        self.time_for_game = 60
        self.time_remaining = Time(250, self.world.height+10,
                                    self.time_for_game)
        self.message = Message(50, self.world.height/2)
        self.max_nb_levels = 10
        self.level = 1
        self.over = False
        self.begin = True
        self.paused = True
        self.level_completed = False
        self.out_of_time = False
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
                                 self.world.vx_values[lane]))
            self.spawn_delay[lane] = self.calculate_delay(lane, self.cars[-1].width,
                                               self.world.vx_values[lane])
        self.logs = []
        for lane in self.world.lane_with_logs:
            self.logs.append(Log(lane, self.world.x_values, self.world.y_values,
                                 self.world.vx_values[lane]))
            self.spawn_delay[lane] = self.calculate_delay(lane, self.logs[-1].width,
                                               self.world.vx_values[lane])
        self.frog = Frog(self, self.world)


    def calculate_delay(self, lane, width, vx):
        factor = random.gauss(self.approx_nb_object_per_lane[lane], 1.0)
        delay = 1.0 * width/vx + self.world.width/(factor*vx)
        return delay

    def set_level_completed(self, lives):
        self.score.score += lives*40*self.level
        self.score.score += 100*self.level
        self.score.score += self.time_remaining.time_left*self.level
        self.message.text = "Level %d completed; \npress spacebar to continue"%self.level
        self.level += 1
        if self.level > self.max_nb_levels:
            self.game_won()
        self.paused = True
        self.level_completed = True
        self.update(0)

    def game_won(self):
        self.over = True
        self.message.text = "You won!  Your score is %d"%self.score.score
        self.paused = True
        self.update(0)

    def new_level(self):
        # less time
        self.time_remaining.time_for_game -= 2
        self.time_remaining.restart()
        # more cars
        for lane in self.world.lane_with_cars:
            self.approx_nb_object_per_lane[lane] += 0.5
        self.level_completed = False
        self.frog.start_new_level(lives=4)
        for pad in self.pads:
            pad.set_empty()
        self.update(0)

    def update(self, dt):
        if self.over or self.level_completed or self.paused:
            dt = 0
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
                    # continuously faster moving objects
                    more = 20
                    vx = self.world.vx_values[lane] + more*(self.level-1) + more*(
                        self.time_remaining.time_for_game
                        - self.time_remaining.time_left)/self.time_remaining.time_for_game
                    if lane in self.world.lane_with_cars:
                        self.cars.append(Car(lane, self.world.x_values, self.world.y_values,
                                             vx))
                        self.spawn_delay[lane] = self.calculate_delay(lane, self.cars[-1].width,
                                                   vx)
                    elif lane in self.world.lane_with_logs:
                        self.logs.append(Log(lane, self.world.x_values, self.world.y_values,
                                             vx))
                        self.spawn_delay[lane] = self.calculate_delay(lane, self.logs[-1].width,
                                                   vx)

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
        if self.begin:
            self.message.text = "Press spacebar to begin"
            self.message.update(paused=True)
        elif self.out_of_time:
            self.message.text = "Out of time; press spacebar to continue"
            self.message.update(paused=True)
        elif self.level_completed:
            #self.message.text = "Level %d completed; press spacebar to continue"%(self.level-1)
            self.message.update(paused=True)
        elif self.paused:
            self.message.text = "Press spacebar to resume"
            self.message.update(paused=True)
        elif self.over:
            self.message.text = "Game over"
            self.message.update(paused=True)
        else:
            self.message.text = ""
            self.message.update(paused=False)

    def switch_pause_state(self):
        self.begin = False
        if self.paused:
            self.paused = False
            if self.level_completed:
                self.new_level()
                self.level_completed = False
            elif self.out_of_time:
                self.time_remaining.restart()
                self.out_of_time = False
        else:
            self.paused = True


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
    def __init__(self,  x, y, time_for_game):
        ft = font.load('Arial', 36)
        self.time_for_game = time_for_game
        Text.__init__(self, ft, time_string%self.time_for_game)
        self.restart()
        self.x = x
        self.y = y

    def restart(self):
        self.time_left = self.time_for_game
        self.color = (1, 1, 1, 1) # white

    def update(self, dt):
        self.time_left -= dt
        if self.time_left >= 0:
            if self.time_left < 5:
                self.color = (1.0, 0.5, 0, 1) # orange
            elif self.time_left < 15:
                self.color = (1.0, 1.0, 0, 1) # yellow
            self.text = time_string%self.time_left
        else:   # ensure time displayed is never negative
            self.color = (1.0, 0, 0, 1) # red
            self.text = time_string%0
        self.draw()

class Message(Text):
    def __init__(self,  x, y):
        ft = font.load('Arial', 36)
        Text.__init__(self, ft, "Press space bar to start")
        self.x = x
        self.y = y

    def update(self, paused=False):
        if paused: # darken screen
            color = (0, 0.5, 0, 0.8)
            glColor4f(*color)
            self.draw()
        else:
            color = (1.0, 1.0, 1.0, 1.0)
            glColor4f(*color)
