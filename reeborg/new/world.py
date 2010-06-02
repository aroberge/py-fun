
class World(object):
    '''World in which robots can interact.  It is borded by walls on the
    left hand side and at the bottom and can have additional walls put in as
    well as contain a number of artifacts and robots.

    Positions are indicated by integers (x, y).'''

    def __init__(self, nb_cols=0, nb_rows=0):
        '''usual initialisation.  Note that values of zero for either nb_rows
        or nb_cols or both are taken to mean that the world is
        unbounded in that direction (either up, or right, or both) other than
        the left-hand side and bottom borders.'''
        assert nb_rows >= 0 and nb_cols >= 0
        self._nb_rows = nb_rows
        self._nb_cols = nb_cols
        self._east_walls = set([])
        self._north_walls = set([])
        if nb_rows > 0 and nb_cols > 0:
            self._initialize_walls()
        self._artifacts = {}
        self._robots = {}

    def initialize_walls(self):
        ''' initialize the outside walls when needed'''
        for i in range(nb_rows):
            self._east_walls.add((nb_cols, i+1))
        for i in range(nb_cols):
            self._north_walls.add((i+1, nb_rows))

    def is_clear(self, x, y, direction):
        '''indicates if no wall (or border) is found at that location in the
        given direction'''
        assert x > 0 and y > 0
        if self._nb_cols != 0:
            assert x <= self._nb_cols
        if self._nb_rows != 0:
            assert y <= self._nb_rows

        if direction == "East":
            return (x, y) not in self._east_walls
        elif direction == "West":
            if x == 1:
                return False
            return (x-1, y) not in self._east_walls
        elif direction == "North":
            return (x, y) not in self._north_walls
        elif direction == "South":
            if y == 1:
                return False
            return (x, y-1) not in self._north_walls
        else:
            raise ValueError

    def build_wall(self, x, y, direction):
        '''if no wall is present at the given location and direction, builds one
        and returns True; otherwise returns False'''
        if direction == "East":
            return self._build_east_wall(x, y)
        elif direction == "West":
            return self._build_east_wall(x-1, y)
        elif direction == "North":
            return self._build_north_wall(x, y)
        elif direction == "South":
            return self._build_north_wall(x, y-1)
        else:
            raise ValueError

    def _build_east_wall(self, x, y):
        '''if no east wall is present at the given location, builds one and
        returns True; otherwise returns False'''
        assert x > 0 and y > 0
        if (x, y) in self._east_walls:
            return False
        self._east_walls.add((x, y))
        return True

    def _build_north_wall(self, x, y):
        '''if no north wall is present at the given location, builds one and
        returns True; otherwise returns False'''
        assert x > 0 and y > 0
        if (x, y) in self._north_walls:
            return False
        self._north_walls.add((x, y))
        return True

    def add_robot(self, robot):
        '''adds a robot in the world.  The intent of this function is
        to have a means to keep track of robot so that they can be rendered
        when the world is rendered itself'''
        assert robot.name not in self._robots
        self._robots[robot.name] = robot

    def remove_robot(self, robot):
        '''removes a named robot in the world.'''
        del self._robots[robot.name]