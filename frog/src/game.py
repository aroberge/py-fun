'''game.py

'''

import os
import random
from pyglet import image
from pyglet import font
from pyglet.font import Text

from pyglet.gl import *

import util
from lane import Car, Log, LillyPad, Turtle, Snake
from frog import Frog

DIR = os.path.dirname(__file__)
img_filename = os.path.join(DIR, "images", 'bg.png')

time_string = 'Time: %3.1f'
score_string = 'Score: %d'

class World(object):
    '''World contains dimensions and other information about the area
    in which the game is played.'''
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
        self.lane_with_snakes = 5
        self.pad_lane = 9
        # position of each lane
        self.y_values = [self.lane_width*i for i in range(10)]
        # starting position of moving NPC:
        # 0: from left; self.width: from the right; -1: either side
        self.x_values = [0, 0, 0, self.width, self.width, -1, self.width, 0, self.width]
        # initial velocities of moving NPC
        self.vx_values = [0, 45, 70, 70, 45, 20, 50, 90, 60]
        #
        self.level_with_snakes = 4
        self.level_with_turtles = 2

class Game(object):
    '''Game is the main class.

    It controls the various aspect of the games, so as to simplify the
    main loop contained in the main script.
    '''
    def __init__(self, window):
        self.world = World()
        self.score = Score(10, self.world.height+10)
        self.time_for_game = 60
        self.time_remaining = Time(350, self.world.height+10,
                                    self.time_for_game)

        self.message = Message(50, self.world.height/2)
        # game specifics
        self.max_nb_levels = 10
        self.level = 1
        self.display_level = Level(self, 200, self.world.height+10)
        self.speed_increment = 15  # speed increment from level to level
        # flags controlling the flow
        self.over = False
        self.won = False
        self.begin = True
        self.paused = True
        self.level_completed = False
        self.out_of_time = False

        # Main character
        self.frog = Frog(self, self.world)
        self.nb_extra_lives = 4 # total # lives is one more.
        # the following may seem redundant; we use this so that we have a
        # hard value (4) specified only once (just above) to prevent inconsistencies
        self.frog.spare_lives = self.nb_extra_lives
        # Other non-playing characters
        self.spawn_delay = {}
        self.approx_nb_object_per_lane = []
        for lane in range(self.world.nb_lanes):
            self.approx_nb_object_per_lane.append(4.0)
        # initially, start with no snake
        self.approx_nb_object_per_lane[self.world.lane_with_snakes] = 0
        self.pads = []
        for i in range(5):
            self.pads.append(LillyPad(45 + 160*i, 540))
        self.cars = []
        for lane in self.world.lane_with_cars:
            self.append_cars(lane, self.world.vx_values)
        self.logs = []
        for lane in self.world.lane_with_logs:
            self.append_logs(lane, self.world.vx_values)
        self.snakes = []
        #self.append_snake(self.world.lane_with_snakes, self.world.vx_values)


    def append_cars(self, lane, vx_value):
        self.cars.append(Car(lane, self.world.x_values, self.world.y_values,
                             vx_value[lane]))
        self.spawn_delay[lane] = self.calculate_delay(lane, self.cars[-1].width,
                            vx_value[lane])

    def append_snake(self, lane, vx_value):
        self.snakes.append(Snake(lane, self.world.x_values, self.world.y_values,
                             vx_value[lane]))
        self.spawn_delay[lane] = self.calculate_delay(lane, self.snakes[-1].width,
                            vx_value[lane])

    def append_logs(self, lane, vx_value):
        r = random.randint(0, 2)
        if r == 2:
            Floating = Turtle
        else:
            Floating = Log
        self.logs.append(Floating(lane, self.world.x_values, self.world.y_values,
                             vx_value[lane]))
        self.spawn_delay[lane] = self.calculate_delay(lane, self.logs[-1].width,
                                    vx_value[lane])

    def new_level(self):
        '''create a new level, more difficult to complete'''
        # less time
        self.time_remaining.time_for_game -= 2
        self.time_remaining.restart()
        # more cars
        for lane in self.world.lane_with_cars:
            self.approx_nb_object_per_lane[lane] += 0.2
        # a tiny increase in the number of logs
        for lane in self.world.lane_with_logs:
            self.approx_nb_object_per_lane[lane] += 0.1

        # restart
        self.level_completed = False
        self.frog.spare_lives = self.nb_extra_lives
        for pad in self.pads:
            pad.set_empty()
        self.update(0)

    def calculate_delay(self, lane, width, vx):
        '''calculate time delay before creation of a new object'''
        # New objects (cars, logs, etc) are created randomly after a
        # certain time has elapsed.  The time delay has two components:
        # * a time delay ensuring that objects are not created too
        #   close to each other; in its simplest form (self.level==1)
        #   it is equal to the time taken to move one object length; at
        #   higher levels, except for logs, objects will be created closer
        #   together
        # * a time delay based on a gaussian distribution ensuring that
        #   not too many objects are present at once;
        factor = random.gauss(self.approx_nb_object_per_lane[lane], 1.0)
        if lane in self.world.lane_with_logs:
            delay = 1.0 * width/vx + self.world.width/(factor*vx)
        else:
            delay = 1.0 * width/(vx*self.level) + self.world.width/(factor*vx)
        # Prevent extreme situation:
        # an object can not move more than 2/3 of a screen before a new
        # one appear
        delay = min(delay, 2.0*self.world.width/(3*vx))
        return delay

    def set_level_completed(self, lives):
        self.score.score += lives*40*self.level
        self.score.score += 100*self.level
        self.score.score += self.time_remaining.time_left*self.level
        if self.level == self.max_nb_levels:
            self.game_won()
        else:
            self.level += 1
            if self.level == self.world.level_with_snakes:
                self.append_snake(self.world.lane_with_snakes, self.world.vx_values)
            elif self.level > self.world.level_with_snakes:
                self.approx_nb_object_per_lane[self.world.lane_with_snakes] += 0.3
            self.paused = True
            self.level_completed = True
            self.update(0)

    def game_won(self):
        self.over = True
        self.won = True
        self.paused = True
        self.update(0)

    def update(self, dt):
        if self.over or self.level_completed or self.paused:
            dt = 0
        if self.frog.dying:
            saved_dt = dt # we have a special "dying frog" animation
            dt = 0    # and will pause the overall animation

        # recreating the background
        self.world.background.blit(0, 0)
        for pad in self.pads:
            pad.update()
        #
        self.time_remaining.update(dt)

        if dt != 0: # animation continues
            # determine the new speed of the moving objects
            vx = []
            more = self.speed_increment
            for lane, vx_value in enumerate(self.world.vx_values):
                # keep snakes moving slowly
                if lane == self.world.lane_with_snakes:
                    vx.append(vx_value)
                else:
                    vx.append(vx_value + more*(self.level-1) + more*(
                    self.time_remaining.time_for_game - self.time_remaining.time_left
                          )/self.time_remaining.time_for_game)

            # determine if we need to generate new moving objects
            for lane in self.spawn_delay:
                self.spawn_delay[lane] -= dt
                if self.spawn_delay[lane] < 0:
                    if lane in self.world.lane_with_cars:
                        self.append_cars(lane, vx)
                    elif lane in self.world.lane_with_logs:
                        self.append_logs(lane, vx)
                    elif lane == self.world.lane_with_snakes:
                        self.append_snake(lane, vx)
            # adjust the speed of all moving objects
            for car in self.cars:
                if car.vx < 0:
                    car.vx = - vx[car.lane]
                else:
                    car.vx = vx[car.lane]
            for log in self.logs:
                if log.vx < 0:
                    log.vx = - vx[log.lane]
                else:
                    log.vx = vx[log.lane]

        # Remove objects that have left the world
        self.cars = [car for car in self.cars if not util.outside_world(car, self.world)]
        self.logs = [log for log in self.logs if not util.outside_world(log, self.world)]
        self.snakes = [snake for snake in self.snakes if not util.outside_world(snake, self.world)]
        for car in self.cars:
            car.update(dt)
        for log in self.logs:
            log.update(dt)
        for snake in self.snakes:
            snake.update(dt)

        if self.frog.dying:
            dt = saved_dt
        self.frog.update(dt, self.pads, self.cars, self.logs, self.snakes)
        self.score.update()
        self.display_level.update()
        if self.begin:
            self.message.text = "Press spacebar to begin"
            self.message.update(paused=True)
        elif self.out_of_time:
            self.message.text = "Out of time; press spacebar to continue"
            self.message.update(paused=True)
        elif self.level_completed:
            self.message.text = "Level %d completed;\n"\
                            "Press spacebar to continue"%(self.level-1)
            self.message.update(paused=True)
        elif self.paused:
            self.message.text = "Press spacebar to resume"
            self.message.update(paused=True)
        elif self.over:
            if self.won:
                self.message.text = "You won!  Your score is %d"%self.score.score
                self.message.text += "\nPress 'r' to restart"
            else:
                self.message.text = "Game over; press 'r' to restart"
            self.message.update(paused=True)
        elif self.frog.invincible:
            self.message.text = "Invincible"
            self.message.update(paused=False)
        else:
            self.message.text = ""
            self.message.update(paused=False)


    def switch_pause_state(self):
        self.begin = False
        if self.paused:
            if self.level_completed:
                self.new_level()
                self.level_completed = False
                self.paused = False
            elif self.out_of_time:
                self.time_remaining.restart()
                self.out_of_time = False
                self.paused = False
            else:
                self.paused = False
        else:
            if self.frog.dying or self.frog.sinking:
                self.paused = False # let the animation finish
            else:
                self.paused = True


class Score(Text):
    def __init__(self, x, y):
        ft = font.load('Arial', 30)
        Text.__init__(self, ft, score_string%0)
        self.score = 0
        self.x = x
        self.y = y

    def update(self):
        self.text = score_string%self.score
        self.draw()

    def reached_pad(self):
        self.score += 10

class Level(Text):
    def __init__(self, game, x, y):
        ft = font.load('Arial', 30)
        Text.__init__(self, ft, 'Level %s'%game.level)
        self.game = game
        self.x = x
        self.y = y

    def update(self):
        self.text = 'Level %s'%self.game.level
        self.draw()


class Time(Text):
    def __init__(self,  x, y, time_for_game):
        ft = font.load('Arial', 30)
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
        ft = font.load('Arial', 30)
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
            self.draw()
