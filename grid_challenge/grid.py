

'''rectangles work

see http://bit-player.org/2009/the-17x17-challenge

'''

import copy
import random
import sys

python_version = sys.version_info[0] + sys.version_info[1]/10.0
if python_version < 2.6:
    print("Python version 2.6 or greater is required.")
    sys.exit()

def intersect_for_two_rows(row_1, row_2):
    '''returns 0 if two rows (given colour, encoded as a bit string)
        do not form a rectangle -
        otherwise returns the points in common encoded as a bit string'''
    intersect = row_1 & row_2
    if not intersect:   # no point in common
        return 0
    # perhaps there is only one point in common of the form 000001000000...
    if not(intersect & (intersect-1)):
        return 0
    else:
        return intersect

def count_bits(x):
    '''counts the number of bits
    see http://stackoverflow.com/questions/407587/python-set-bits-count-popcount
    for reference and other alternative'''
    return bin(x).count('1')

class AbstractGrid(object):
    '''An AbstractGrid is a basic empty grid which contains all the basic methods
    and attribute that are common to all possible grids.
    Derived classes will usually define some initialisation scheme. '''

    def __init__(self, nb_colours, nb_rows, nb_columns):
        self.nb_colours = nb_colours
        self.nb_rows = nb_rows
        self.nb_columns = nb_columns
        # The colour information is encoded, for each row, and each colour
        # within that row, using a binary sequence.  For example, suppose that
        # we have a row with two colours, Red (R) and Green (G) as follows:
        #                 RRGRG
        # The colour pattern could be represented as:
        # row[Red] = RR.R. and row[Green] = ..G.G
        # We can represent these patterns as binary numbers
        # row[Red] = 11010 and row[Green] = 00101
        # We use the integer equivalent of these instead:
        # row[Red] = 26 and row[Green] = 5
        # Finally, instead of using colour names, as we represent each colour by
        # a number so that we could have something like
        # row[0] = 26 and row[1] = 5
        self.colours = list(range(nb_colours))
        self.powers_of_two = [2**i for i in range(nb_columns)]
        #
        self.grid = {}
        self.initialize()
        self.saved_info = None
        self.rects_info = [0 for c in self.colours]

    def initialize(self):
        '''Initializes a grid given the intial parameters and a colouring
        scheme.'''
        for row in range(self.nb_rows):
            self.grid[row] = {}
            for colour in self.colours:
                self.grid[row][colour] = 0  # initially empty
            # Then fill it according to some colour choice
            for column in range(self.nb_columns):
                self.grid[row][self.colour_choice()] += self.powers_of_two[column]

    def colour_choice(self):
        '''A grid is initialised according to a colour scheme to be
        specified.  This method needs to be overriden.
        Here we simply use the same colour all the time.'''
        return 0

    def print_grid(self, grid=None):
        '''prints a representation of a grid.
        Used for diagnostic only - no need to optimize further.'''
        if grid is None:
            grid = self.grid
        for row in grid:
            row_rep = []
            for column in range(self.nb_columns-1, -1, -1):
                colour_missing = True
                for colour_ in self.colours:
                    if self.powers_of_two[column] & grid[row][colour_]:
                        row_rep.append(str(colour_))
                        colour_missing = False
                if colour_missing:
                    row_rep.append(".")
            print("".join(row_rep))

    def save_grid(self):
        '''saves a given grid as a tuple, with the following information:
        0: the number of rows
        1: the number of columns
        2: the number of colours
        3: the grid itself
        4: the total number of rectangles formed.
        '''
        self.saved_info = (self.nb_rows, self.nb_columns, self.nb_colours,
                          copy.deepcopy(self.grid), sum(self.rects_info))
        return

    def print_saved_grid(self):
        '''prints the information about a saved grid.'''
        s = self.saved_info
        print("="*60)
        print("%sx%s %s with %s colours and %s rectangles." % (s[0], s[1],
                                        self.__class__.__name__, s[2], s[4]))
        print("-"*60)
        self.print_grid(s[3])
        print("="*60)

    def identify_bad_rows(self):
        '''identify the rows that contributes to rectangles.
        Used for diagnostic only - no need to optimize further.'''
        bad_rows = []
        for colour in self.colours:
            for row in self.grid:
                is_bad_row = False
                current_bad_rows = []
                for other_row in range(row+1, self.nb_rows):
                    intersect = intersect_for_two_rows(
                                                self.grid[row][colour],
                                                self.grid[other_row][colour])
                    if intersect:
                        locate = bin(intersect)[2:]
                        locate = locate.replace('1', 'X').replace('0', '.')
                        locate = '.'*(self.nb_columns-len(locate)) + locate
                        current_bad_rows.append((other_row, locate))
                        is_bad_row = True
                if is_bad_row:
                    current_bad_rows.insert(0, row)
                    bad_rows.append(["colour=%s"%colour, current_bad_rows])
        return bad_rows

    def identify_intersect_points(self, colours):
        '''identifies the dots that contribute to forming rectangles
        returns the total number of rectangles formed as well as the information
        about which point contribute to forming rectangles.'''
        intersect_info = []
        for colour in colours:
            self.rects_info[colour] = 0
            for row in self.grid:
                for other_row in range(row+1, self.nb_rows):
                    intersect = intersect_for_two_rows(
                                            self.grid[row][colour],
                                            self.grid[other_row][colour])
                    if intersect != 0:
                        nb_pts = count_bits(intersect)
                        self.rects_info[colour] += nb_pts*(nb_pts-1)//2
                        intersect_info.append([colour, row, other_row, intersect])
        return sum(self.rects_info), intersect_info

    def add_row(self):
        '''adds a row to an existing grid, fills each column with a
           colour obtained from a known method.
           Used for creating grids only - no need to optimize further.'''
        self.grid[self.nb_rows] = {}
        for colour_ in self.colours:
            self.grid[self.nb_rows][colour_] = 0
        for column in range(self.nb_columns):
            self.grid[self.nb_rows][self.colour_choice()] += self.powers_of_two[column]
        self.nb_rows += 1

    def add_column(self):
        '''adds a column to an existing grid, to the right of previously
        defined column, with each colour added obtained from a known method.
        Used for creating grids only - no need to optimize further.'''
        for row in self.grid:
            self.grid[row][self.colour_choice()] += self.powers_of_two[self.nb_columns]
        self.nb_columns += 1

class EmptyGrid(AbstractGrid):
    '''Grid created with no colour present'''

    def initialize(self):
        '''Initializes a grid given the intial parameters and a colouring
        scheme.'''
        for row in range(self.nb_rows):
            self.grid[row] = {}
            for colour in self.colours:
                self.grid[row][colour] = 0

    def colour_choice(self):
        '''Not a valid method for EmptyGrid'''
        print("colour_choice is not a valid method for %s", self.__class__.__name__)
        raise

    def add_empty_row(self):
        '''adds a row to an existing grid.
           Used for creating grids only - no need to optimize further.'''
        self.grid[self.nb_rows] = {}
        for colour_ in self.colours:
            self.grid[self.nb_rows][colour_] = 0
        self.nb_rows += 1

class RandomGrid(AbstractGrid):
    '''Grid initialized with colours chosen at random'''

    def colour_choice(self):
        '''Colour scheme is defined to be totally random'''
        return random.randint(0, self.nb_colours-1)


class ColourBalancedGrid(AbstractGrid):
    '''Grid initialized with colours that cycle through all possible choices,
    so as to keep the number of points of each colour as equal as possible'''

    def __init__(self, nb_colours, nb_rows, nb_columns):
        self.colour_cycle = self.colour_generator(nb_colours)
        AbstractGrid.__init__(self, nb_colours, nb_rows, nb_columns)

    def colour_generator(self, nb_colours):
        '''Generator that cycles through each colour in turn'''
        colour = 0
        while True:
            yield colour % nb_colours
            colour += 1

    def colour_choice(self):
        '''Colour scheme is defined to be totally random'''
        return self.colour_cycle.next()

if __name__ == "__main__":
    grid = AbstractGrid(4, 5, 5)
    grid.identify_intersect_points((0, 1, 2, 3))
    grid.save_grid()
    grid.print_saved_grid()

    grid = RandomGrid(3, 4, 4)
    grid.identify_intersect_points((0, 1, 2))
    grid.save_grid()
    grid.print_saved_grid()

    grid = ColourBalancedGrid(3, 5, 5)
    grid.identify_intersect_points((0, 1, 2))
    grid.save_grid()
    grid.print_saved_grid()