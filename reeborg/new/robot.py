""" Robot is adapted from/inspired by rur-ple's robot_factory."""

import random

class Robot(object):

    deltas = [ (0, 1), (-1, 0), (0, -1), (1, 0) ]
    directions = ['North', 'West', 'South', 'East']
    ids = 0

    def __init__(self, world=None, x=1, y=1, facing='East', bag=None):
        # East; value by default - tied to lessons
        self.world = world
        self.x = x
        self.y = y
        if bag is None:
            self.bag = {}
        else:
            self.bag = bag
        self.direction_index = self.directions.index(facing)
        self.raised = None

## ====== Tests =================

    def front_is_clear(self):
        ''' True if no wall or border in front of robot'''
        return self._is_clear(0)

    def left_is_clear(self):
        '''True if no walls or borders are to the immediate left
           of the robot.'''
        return self._is_clear(1)

    def right_is_clear(self):
        '''Returns True if no walls or borders are to the immediate
           right of the robot.'''
        return self._is_clear(3)

    def _is_clear(self, direction):
        '''Return True if there are no wall or borders directly next to
        the robot in the direction indicated'''
        facing = self.direction_index + direction
        facing %= 4
        return self.world.is_clear(self.x, self.y, self.directions[facing])

    def facing_north(self):
        ''' True if Robot facing North'''
        return self.direction_index == 0

    def facing_east(self):
        ''' True if Robot facing East'''
        return self.direction_index == 3

    def facing_south(self):
        ''' True if Robot facing north'''
        return self.direction_index == 2

    def facing_west(self):
        ''' True if Robot facing West'''
        return self.direction_index == 1

    def have_in_bag(self, obj=None):
        '''True if some object of the specified type are Robot's bag'''
        return obj in self.bag

    def is_here(self, obj=None):
        '''True if at least one of the specified object is present
           at current robot position.'''
        return self.world.is_here(self.x, self.y, obj)

## ====== Actions =================

    def move(self):
        '''Robot moves one street/avenue in direction where it is facing'''
        if self.front_is_clear():
            xx, yy = self.deltas[self.direction_index]
            self.x += xx
            self.y += yy
        else:
            self._say_and_raise("Wall in front.")

    def turn_left(self):
        '''Robot turns left by 90 degrees.'''
        self.direction_index += 1
        self.direction_index %= 4

    def turn_right(self):
        '''Robot turns right by 90 degrees.'''
        self.direction_index += 3
        self.direction_index %= 4

    def turn_around(self):
        '''Robot turns by 180 degrees.'''
        self.direction_index += 2
        self.direction_index %= 4

    def put(self, obj):
        '''Robot put one specified object down at current location.'''
        if self.have_in_bag(obj):
            self.bag[obj] -= 1
            self.world.add_artifact(self.x, self.y, obj)
            if self.bag[obj] == 0:
                del self.bag[obj]
        else:
            self._say_and_raise("Carrying no such object.", obj)

    def pick(self, obj):
        '''Robot picks up one specified objectat current location.'''
        if self.is_here(obj):
            self.world.remove_artifact(self.x, self.y, obj)
            if obj in self.bag:
                self.bag[obj] += 1
            else:
                self.bag[obj] = 1
        else:
            self._say_and_raise("No such object here.", obj)

    def build_wall(self):
        '''Robot builds a wall in front of itself'''
        facing = self.directions[self.direction_index]
        self.world.build_wall(self.x, self.y, facing)

    def roll_dice(self, n=6):
        '''handy dice used by robot to perform experiments'''
        return random.randint(1, n)

    def say(self, msg):
        '''Message output by robot'''
        print(msg)

    def _say_and_raise(self, msg, obj=None):
        '''robots says message and records the fact that an "exception" has
           been raised.'''
        self.say(msg)
        self.raised = msg, obj



