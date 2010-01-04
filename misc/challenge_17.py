'''rectangles work

see http://bit-player.org/2009/the-17x17-challenge

'''

import copy
import math
import random
import time

#nb_colours = 4
#nb_rows = 1
#nb_columns = 1
#max_rows = 17
#max_columns = 17
#
#colours = list(range(nb_colours))
#powers_of_two = [2**i for i in range(max_columns)]

def rectangles_for_two_rows(row_1, row_2):
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
    def __init__(self, nb_colours, max_rows, max_columns):
        self.nb_colours = nb_colours
        self.colours = list(range(nb_colours))
        self.max_rows = max_rows
        self.max_columns = max_columns
        self.powers_of_two = [2**i for i in range(max_columns)]
        self.grid = {}

    def initialise(self):
        '''initialise a grid according to some strategy'''
        raise NotImplemented

    def print_grid(self):
        '''prints a representation of the grid.
        Used for diagnostic only - no need to optimize further.'''
        for row in self.grid:
            row_rep = []
            for column in range(self.nb_columns-1, -1, -1):
                for colour_ in self.colours:
                    if self.powers_of_two[column] & self.grid[row][colour_]:
                        row_rep.append(str(colour_))
            print("".join(row_rep))

    def identify_bad_rows(self):
        '''identify the rows that contributes to rectangles.
        Used for diagnostic only - no need to optimize further.'''
        bad_rows = []
        for colour in self.colours:
            for row in self.grid:
                is_bad_row = False
                current_bad_rows = []
                for other_row in range(row+1, self.nb_rows):
                    intersect = rectangles_for_two_rows(
                                                self.grid[row][colour],
                                                self.grid[other_row][colour])
                    if intersect:
                        locate = bin(intersect)[2:]
                        locate = locate.replace('1', 'X').replace('0', '.')
                        locate = '.'*(nb_columns-len(locate)) + locate  # padding
                        current_bad_rows.append((other_row, locate))
                        is_bad_row = True
                if is_bad_row:
                    current_bad_rows.insert(0, row)
                    bad_rows.append(["colour=%s"%colour, current_bad_rows])
        return bad_rows

    def identify_intersect_points(self):
        '''identifies the dots that contribute to forming rectangles'''
        # possibly could cut down the calculation time by only computing
        # for colours that have changed...
        nb_intersect = [0 for colour in self.colours]
        intersect_info = []
        for colour in self.colours:
            for row in self.grid:
                for other_row in range(row+1, self.nb_rows):
                    intersect = rectangles_for_two_rows(
                                            self.grid[row][colour],
                                            self.grid[other_row][colour])
                    if intersect != 0:
                        nb_intersect[colour] += count_bits(intersect)
                        intersect_info.append([colour, row, other_row, intersect])
        return nb_intersect, intersect_info

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

    def add_column(self, colours_):
        '''adds a column to an existing grid, to the right of previously
        defined column, with each colour added obtained from a known method.
        Used for creating grids only - no need to optimize further.'''
        for row in self.grid:
            self.grid[row][self.colour_choice()] += self.powers_of_two[self.nb_columns]
        self.nb_columns += 1

    def colour_choice(self):
        raise NotImplemented


class RandomGrid(AbstractGrid):
    def initialise(self):
        self.nb_columns = self.max_columns
        self.nb_rows = 0
        for row in range(self.max_rows):
            self.add_row()
    def colour_choice(self):
        return random.randint(0, self.nb_colours-1)

class BaseSolver(object):
    '''class definition containing basic methods to change the content
    of a grid - and change it back if needed - as well as the basic
    skeletton of solver'''
    def __init__(self, puzzle, max_iter):
        self.grid = puzzle.grid
        self.puzzle = puzzle
        self.max_iter = max_iter
        self.nb_colours = puzzle.nb_colours
        self.nb_rows = puzzle.nb_rows
        self.nb_columns = puzzle.nb_columns
        self.powers_of_two = puzzle.powers_of_two

    def solve(self, status_report=1000):
        '''Basic solver - greedy or hill climber, with regular status reports'''
        self.init_solver()
        nb_steps = 0
        while self.not_done(nb_steps):
            nb_steps += 1
            if not nb_steps%status_report:
                self.report_status(nb_steps)
            self.pick_new_configuration()
            self.compare_new_with_old()
        #print("-"*30)
        self.report_status(nb_steps)
        return self.puzzle

    def init_solver(self):
        raise NotImplemented

    def not_done(self, nb_steps):
        raise NotImplemented

    def pick_new_configuration(self):
        raise NotImplemented

    def compare_new_with_old(self):
        raise NotImplemented

    def report_status(self, nb_steps):
        raise NotImplemented

    def change_dot_colour(self, row, column, old_colour, new_colour):
        '''changes the colour of a dot on a grid'''
        self.grid[row][old_colour] -= 2**column
        self.grid[row][new_colour] += 2**column
        # save values for inversion if needed
        self.row = self.grid[row]
        self.column = column
        self.old_colour = old_colour
        self.new_colour = new_colour

    def revert_change_dot_colour(self):
        '''reverts a change of colour of a dot on a grid.
        inverse of change_dot_colour'''
        self.row[self.old_colour] += 2**self.column
        self.row[self.new_colour] -= 2**self.column

    def swap_dot_colours(self, row_1, column_1, colour_1, row_2,
                                      column_2, colour_2):
        '''swap the colours of two dots on a grid'''
        self.grid[row_1][colour_1] -= 2**column_1
        self.grid[row_1][colour_2] += 2**column_1
        self.grid[row_2][colour_2] -= 2**column_2
        self.grid[row_2][colour_1] += 2**column_2
        # save values for inversion if needed
        self.row_1 = self.grid[row_1]
        self.column_1 = column_1
        self.colour_1 = colour_1
        self.row_2 = self.grid[row_2]
        self.column_2 = column_2
        self.colour_2 = colour_2

    def revert_swap_dot_colours(self):
        '''reverts the swapping of colour between two dots on a grid.
        inverse of swap_dot_colours()'''
        self.row_1[self.colour_1] += 2**self.column_1
        self.row_1[self.colour_2] -= 2**self.column_1
        self.row_2[self.colour_2] += 2**self.column_2
        self.row_2[self.colour_1] -= 2**self.column_2

    def swap_row_colours(self, row, colour_1, colour_2):
        '''On a given row: swap all dots of given colour with those of
        another.  For example, suppose we have a row with
        ...RR...GGGG, after the swap it will become ...GG...RRRR'''
        self.grid[row][colour_1], self.grid[row][colour_2] =  (
                            self.grid[row][colour_1], self.grid[row][colour_2])
        self.row = self.grid[row]
        self.colour_1 = colour_1
        self.colour_2 = colour_2

    def revert_swap_row_colours(self):
        '''reverts the swapping of colour between two dots on a grid.
        inverse of swap_row_colours()'''
        self.row[self.colour_1], self.row[self.colour_2] =  (
                                    self.row[self.colour_1], self.row[colour_2])


class RandomDotGreedySolver(BaseSolver):
    '''Solves a given grid by picking a point at random and
        attempting to change its colour; if it reduces the number of problematic
        point, we keep the solution.'''

    def init_solver(self):
        '''obtain starting values for the solver'''
        nb_intersect, self.intersect_info = self.puzzle.identify_intersect_points()
        self.total_intersect = sum(nb_intersect)
        self.nb_changes = 0
        self.previous_nb_changes = -1
        self.stuck = False

    def not_done(self, nb_steps):
        if (self.total_intersect == 0
            or nb_steps >= self.max_iter
            or self.stuck):
            return False
        return True

    def pick_new_configuration(self):
        '''pick a point (row, column) at random and change its colour'''
        row = random.randint(0, self.nb_rows-1)
        column = random.randint(0, self.nb_columns-1)
        for colour in self.grid[row]:
            if self.grid[row][colour] & 2**column:
                current_colour = colour
                break
        new_colour = random.randint(0, self.nb_colours-1)
        if new_colour == current_colour:
            new_colour = (current_colour+1)%self.nb_colours
        self.change_dot_colour(row, column, current_colour, new_colour)

    def compare_new_with_old(self):
        '''compares the new configuration with the old - reverts back
        if it does not reduce the number of rectangles.'''
        # Note: we require to strictly reduce the number so that we don't
        # accidentally cycle back an forth between equivalent solutions.
        new_intersect, intersect_info = self.puzzle.identify_intersect_points()
        new_total = sum(new_intersect)
        if new_total < self.total_intersect:
            self.total_intersect = new_total
            self.intersect_info = intersect_info
            self.nb_changes += 1
        else:
            self.revert_change_dot_colour()

    def report_status(self, nb_steps, final=False):
        if (final or self.nb_changes > self.total_intersect):
            print("nb_steps=", nb_steps, " nb_intersect=", self.total_intersect,
              "nb_changes=", self.nb_changes)
        if self.nb_changes == self.previous_nb_changes:
            self.stuck = True
        self.previous_nb_changes = self.nb_changes
        return self.total_intersect, self.nb_changes

class RandomGreedyDotSwapperSolver(RandomDotGreedySolver):
    '''Solves a given grid by picking two points at random and
        attempting to interchange colour; if it reduces the number of problematic
        point, we keep the solution.'''

    def pick_new_configuration(self):
        '''pick two points (row, column) at random and interchange their colour'''

        row_1 = random.randint(0, self.nb_rows-1)
        column_1 = random.randint(0, self.nb_columns-1)
        for colour in self.grid[row_1]:
            if self.grid[row_1][colour] & 2**column_1:
                colour_1 = colour
                break

        row_2 = random.randint(0, self.nb_rows-1)
        column_2 = random.randint(0, self.nb_columns-1)
        for colour in self.grid[row_2]:
            if self.grid[row_2][colour] & 2**column_2:
                colour_2 = colour
                break
        # make sure we pick a different colour
        while colour_2 == colour_1:
            row_2 = random.randint(0, self.nb_rows-1)
            column_2 = random.randint(0, self.nb_columns-1)
            for colour in self.grid[row_2]:
                if self.grid[row_2][colour] & 2**column_2:
                    colour_2 = colour
                    break
        self.swap_dot_colours(row_1, column_1, colour_1, row_2, column_2,
                             colour_2)

    def compare_new_with_old(self):
        '''compares the new configuration with the old - reverts back
        if it does not reduce the number of rectangles.'''
        # Note: we require to strictly reduce the number so that we don't
        # accidentally cycle back an forth between equivalent solutions.
        new_intersect, intersect_info = self.puzzle.identify_intersect_points()
        new_total = sum(new_intersect)
        if new_total < self.total_intersect:
            self.total_intersect = new_total
            self.intersect_info = intersect_info
            self.nb_changes += 1
        else:
            self.revert_swap_dot_colours()

class RandomDotGreedySolverWithHillClimb(RandomDotGreedySolver):
    '''Solves a given grid by picking a point at random and
        attempting to change its colour; if it reduces the number of problematic
        point or raise it by a small amount above the best solution found so
        far, we keep the solution.'''

    def init_solver(self):
        '''obtain starting values for the solver'''
        nb_intersect, self.intersect_info = self.puzzle.identify_intersect_points()
        self.total_intersect = sum(nb_intersect)
        self.nb_changes = 0
        self.previous_nb_changes = -1
        self.stuck = False
        self.hill_climb = self.nb_rows

    def not_done(self, nb_steps):
        if (self.total_intersect == 0
            or nb_steps >= self.max_iter
            or self.stuck):
            return False
        return True

    def compare_new_with_old(self):
        '''compares the new configuration with the old - reverts back
        if it does not reduce the number of rectangles.'''
        # Note: we require to strictly reduce the number so that we don't
        # accidentally cycle back an forth between equivalent solutions.
        new_intersect, intersect_info = self.puzzle.identify_intersect_points()
        new_total = sum(new_intersect)
        if new_total < self.total_intersect + self.hill_climb:
            if new_total < self.total_intersect:
                self.intersect_info = intersect_info
                self.total_intersect = new_total
            self.nb_changes += 1
        else:
            self.revert_change_dot_colour()

class SelectiveRandomDotGreedySolver(RandomDotGreedySolver):
    '''Solves a given grid by picking a "bad" point at random and
        attempting to change its colour; if it reduces the number of problematic
        point, we keep the solution.'''

    def pick_new_configuration(self):
        '''pick a "bad" point (row, column) at random and change its colour'''
        random.shuffle(self.intersect_info)
        choice = self.intersect_info[0]

        current_colour = choice[0]
        row = choice[random.randint(1, 2)]
        intersect = choice[3]

        new_colour = random.randint(0, self.nb_colours-1)
        if new_colour == current_colour:
            new_colour = (current_colour+1)%self.nb_colours

        bad_points = []
        for index, power_ in enumerate(self.puzzle.powers_of_two):
            if power_ & intersect:
                bad_points.append(index)
        if not bad_points:
            raise
        random.shuffle(bad_points)
        column = bad_points[0]
        self.change_dot_colour(row, column, current_colour, new_colour)

def cycle(puzzle):
    solver = SelectiveRandomDotGreedySolver(puzzle, 50000)
    puzzle = solver.solve(status_report=100)
    print("zooming")
    solver = SelectiveRandomDotGreedySolver(puzzle, 2000)
    puzzle = solver.solve(status_report=100)
    for i in range(70):
        print("hill climbing")
        solver = RandomDotGreedySolverWithHillClimb(puzzle, 2000)
        puzzle = solver.solve(status_report=2000)
        print("random change")
        solver = RandomDotGreedySolver(puzzle, 5000)
        puzzle = solver.solve(status_report=200)
        print("swapping")
        solver = RandomGreedyDotSwapperSolver(puzzle, 5000)
        puzzle = solver.solve(status_report=70)
        print("zooming")
        solver = SelectiveRandomDotGreedySolver(puzzle, 2000)
        puzzle = solver.solve(status_report=70)
        print("swapping")
        solver = RandomGreedyDotSwapperSolver(puzzle, 5000)
        puzzle = solver.solve(status_report=100)
        print("zooming")
        solver = SelectiveRandomDotGreedySolver(puzzle, 2000)
        puzzle = solver.solve(status_report=70)

puzzle = RandomGrid(3, 10, 10)
puzzle.initialise()
cycle(puzzle)
#puzzle.print_grid()
#for i in range(3, 11):
#    puzzle.add_row()
#    print("-"*30, puzzle.nb_rows, "x", puzzle.nb_columns)
#    puzzle.print_grid()
#    print("-"*30)
#    cycle(puzzle)
#    print("="*30, puzzle.nb_rows, "x", puzzle.nb_columns)
#    puzzle.print_grid()
#    print("="*30, puzzle.nb_rows, "x", puzzle.nb_columns)


puzzle.print_grid()

import sys
sys.exit()


# Hypothesis: solutions are more likely when number of dots of each
# colour is approximately equal.  So, we add colours to a grid in a cycle

def colour_generator():
    '''cycles through each colour in turn'''
    global nb_colours
    colour_ = 0
    while True:
        yield colour_ % nb_colours
        colour_ += 1
colour_cycle = colour_generator()


#def rectangles_for_two_rows(row_1, row_2):
#    '''returns 0 if two rows (given colour, encoded as a bit string)
#        do not form a rectangle -
#        otherwise returns the points in common encoded as a bit string'''
#    try:
#        assert row_1 >= 0 and row_2 >= 0
#    except:
#        print("row_1=", row_1, "row_2=", row_2)
#        print("intersect=", row_1 & row_2)
#        raise
#    intersect = row_1 & row_2
#    assert intersect >= 0
#    if not intersect:   # no point in common
#        return 0
#    # perhaps there is only one point in common of the form 000001000000...
#    if not(intersect & (intersect-1)):
#        return 0
#    else:
#        return intersect
#
#def identify_bad_rows(grid):
#    '''identify the rows that contributes to rectangles'''
#    bad_rows = []
#    for colour in colours:
#        for row in grid:
#            is_bad_row = False
#            current_bad_rows = []
#            for other_row in range(row+1, nb_rows):
#                intersect = rectangles_for_two_rows(grid[row][colour], grid[other_row][colour])
#                if intersect:
#                    locate = bin(intersect)[2:]
#                    locate = locate.replace('1', 'X').replace('0', '.')
#                    locate = '.'*(nb_columns-len(locate)) + locate  # padding
#                    current_bad_rows.append((other_row, locate))
#                    is_bad_row = True
#            if is_bad_row:
#                current_bad_rows.insert(0, row)
#                bad_rows.append(["colour=%s"%colour, current_bad_rows])
#    return bad_rows
#
#def count_intersect_points(grid):
#    '''counts the number of points that contribute to forming rectangles'''
#    nb_intersect = 0
#    intersect_info = []
#    for colour in colours:
#        for row in grid:
#            for other_row in range(row+1, nb_rows):
#                intersect = rectangles_for_two_rows(grid[row][colour],
#                                                    grid[other_row][colour])
#                if intersect != 0:
#                    nb_intersect += count_bits(intersect)
#                    intersect_info.append([colour, row, other_row, intersect])
#    return nb_intersect, intersect_info
#
#def random_solve_greedy(grid):
#    '''solves a given grid by picking a problematic point at random and
#    attempting to change its colour; if it reduces the number of problematic
#    point or keep it constant, we keep the solution.  Every so often,
#    we keep a new solution to avoid getting stuck in a bad loop.'''
#    nb_intersect, intersect_info = count_intersect_points(grid)
#    best_intersect = nb_intersect
#    max_deviation = len(grid)//2
#    best_grid = copy.deepcopy(grid)
#    nb_steps = 1
#    restart_every = 8*len(grid)
#    status_report = restart_every**2
#    #restart = False
#    max_nb_steps = 4*len(grid)*1000
#    print("max_nb_steps=", max_nb_steps)
#    while nb_intersect:
#        random.shuffle(intersect_info)
#        nb_steps += 1
#        if not nb_steps%status_report:
#            print("nb_steps=", nb_steps, " nb_intersect=", nb_intersect)
#        #if not nb_steps%restart_every:
#        #    restart=True
#        if nb_steps >= max_nb_steps:
#            print("MAX nb_steps=", nb_steps, " nb_intersect=", nb_intersect)
#            return best_grid
#        for choices in intersect_info:  # attempt to cycle through all rows with bad points
#            old_colour, row1, row2, intersect = choices
#            rows = [row1, row2]
#            random.shuffle(rows)
#            row = rows[0]
#            new_colour = (old_colour+random.randint(1, nb_colours-1)) % nb_colours
#            bad_points = []
#            for index, power_ in enumerate(powers_of_two):
#                if power_ & intersect:
#                    bad_points.append(index)
#            if not bad_points:
#                print("error: bad_points =", bad_points, " choices=", choices)
#                continue
#            random.shuffle(bad_points)
#            column = bad_points[0]
#
#            grid[row][old_colour] -= 2**column
#            try:
#                assert grid[row][old_colour] >= 0
#            except:
#                print("*"*40)
#                print("column=", column)
#                print("bad_points=", bad_points)
#                print("intersect=", intersect, bin(intersect))
#                grid[row][old_colour] += 2**column
#                print("2**column=", 2**column, " grid[row][old_colour]=", grid[row][old_colour])
#                raise
#
#            grid[row][new_colour] += 2**column
#            new_intersect, new_info = count_intersect_points(grid)
#            if new_intersect <= nb_intersect or new_intersect <= best_intersect+max_deviation: # or restart:
#                if new_intersect < best_intersect:
#                    best_intersect = new_intersect
#                    best_grid = copy.deepcopy(grid)
#                if new_intersect == 0:
#                    return grid
#                nb_intersect = new_intersect
#                intersect_info = new_info
#                break
#            else:
#                grid[row][old_colour] += 2**column
#                grid[row][new_colour] -= 2**column
#        #restart=False
#    return grid
#
#for i in range(1, max_columns):
#    nb_columns = add_column(grid, nb_columns)

for i in range(1, max_rows):
    now = time.time()
    nb_rows = add_row(grid, nb_rows)
    # here would be solver
    print("="*30, "\ngrid: ", nb_rows, "x", nb_columns, "\n", "- "*15)
    print_grid(grid)
    print("bad_rows=", identify_bad_rows(grid))
    print("intersect points=", count_intersect_points(grid)[0])
    grid = random_solve_greedy(grid)
    print_grid(grid)
    print("bad_rows=", identify_bad_rows(grid))
    print("intersect points=", count_intersect_points(grid)[0])
    print("time=", time.time()-now)

    #now = time.time()
    #nb_columns = add_column(grid, nb_columns)
    ## here would be solver
    #print("="*30, "\ngrid: ", nb_rows, "x", nb_columns, "\n", "- "*15)
    #print_grid(grid)
    #print("bad_rows=", identify_bad_rows(grid))
    #print("intersect points=", count_intersect_points(grid)[0])
    #grid = random_solve_greedy(grid)
    #print_grid(grid)
    #print("bad_rows=", identify_bad_rows(grid))
    #print("intersect points=", count_intersect_points(grid)[0])
    #print("time=", time.time()-now)