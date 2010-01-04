'''rectangles work

see http://bit-player.org/2009/the-17x17-challenge

'''

import random
import time

class BaseSolver(object):
    '''class definition containing basic methods to change the content
    of a grid - and change it back if needed - as well as the basic
    skeletton of solver'''
    def __init__(self, puzzle, max_iter, report=False):
        self.grid = puzzle.grid
        self.puzzle = puzzle
        self.max_iter = max_iter
        self.report = report
        #
        self.nb_steps = 0
        self.nb_colours = puzzle.nb_colours
        self.nb_rows = puzzle.nb_rows
        self.nb_columns = puzzle.nb_columns
        self.powers_of_two = puzzle.powers_of_two
        #
        self.init_solver()

    def solve(self, status_report=1000):
        '''Basic solver - greedy or hill climber, with regular status reports'''
        self.init_solver()
        while self.not_done():
            self.nb_steps += 1
            if self.report:
                if not self.nb_steps % status_report:
                    self.report_status()
            self.pick_new_configuration()
            self.compare_new_with_old()
        print("%s is done." % self.__class__.__name__)
        self.report_status()
        return self.puzzle.saved_info

    def init_solver(self):
        '''obtain starting values for the solver'''
        self.nb_rects, self.intersect_info = self.puzzle.identify_intersect_points(
            list(range(self.nb_colours))
        )
        self.nb_changes = 0
        self.previous_nb_changes = -1
        self.stuck = False

    def not_done(self):
        '''solver-dependent method to determine if a solver should end,
        either because a solution has been found or if it appears that
        it is stuck in a local minimum or equivalent.'''
        raise NotImplemented

    def pick_new_configuration(self):
        '''solver-dependent method to pick a new configuration'''
        raise NotImplemented

    def compare_new_with_old(self):
        '''solver-dependent method to compare a new configuration with
        an existing one and determine what to do afterwards.'''
        raise NotImplemented

    def report_status(self):
        '''solver-dependent method to report the progress'''''
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
        self.test_colours = [old_colour, new_colour]

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
        self.test_colours = [colour_1, colour_2]

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
        self.test_colours = [colour_1, colour_2]

    def revert_swap_row_colours(self):
        '''reverts the swapping of colour between two dots on a grid.
        inverse of swap_row_colours()'''
        self.row[self.colour_1], self.row[self.colour_2] =  (
                                    self.row[self.colour_1], self.row[self.colour_2])


class RandomDotGreedySolver(BaseSolver):
    '''Solves a given grid by picking a point at random and
        attempting to change its colour; if it reduces the number of problematic
        point, we keep the solution.'''


    def not_done(self):
        '''simple method to determine if the solver must terminate'''
        if (self.nb_rects == 0 or self.nb_steps >= self.max_iter or self.stuck):
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
        new_total, intersect_info = self.puzzle.identify_intersect_points(self.test_colours)
        if new_total < self.nb_rects:
            self.nb_rects = new_total
            self.intersect_info = intersect_info
            self.nb_changes += 1
        else:
            self.revert_change_dot_colour()

    def report_status(self):
        '''prints information about solver status'''
        if (self.nb_changes > self.nb_rects):
            print("nb_steps=", self.nb_steps, " nb_rects=", self.nb_rects,
              "nb_changes=", self.nb_changes)
        if self.nb_changes == self.previous_nb_changes:
            self.stuck = True
        self.previous_nb_changes = self.nb_changes
        return self.nb_rects, self.nb_changes

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
        new_total, intersect_info = self.puzzle.identify_intersect_points()
        if new_total < self.nb_rects:
            self.nb_rects = new_total
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
        RandomDotGreedySolver.init_solver()
        self.hill_climb = self.nb_rows

    def compare_new_with_old(self):
        '''compares the new configuration with the old - reverts back
        if it does not reduce the number of rectangles.'''
        # Note: we require to strictly reduce the number so that we don't
        # accidentally cycle back an forth between equivalent solutions.
        new_total, intersect_info = self.puzzle.identify_intersect_points()
        if new_total < self.nb_rects + self.hill_climb:
            self.nb_rects = new_total
            self.intersect_info = intersect_info
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

#def cycle(puzzle):
#    solver = SelectiveRandomDotGreedySolver(puzzle, 50000)
#    puzzle = solver.solve(status_report=100)
#    print("zooming")
#    solver = SelectiveRandomDotGreedySolver(puzzle, 2000)
#    puzzle = solver.solve(status_report=100)
#    for i in range(70):
#        print("hill climbing")
#        solver = RandomDotGreedySolverWithHillClimb(puzzle, 2000)
#        puzzle = solver.solve(status_report=2000)
#        print("random change")
#        solver = RandomDotGreedySolver(puzzle, 5000)
#        puzzle = solver.solve(status_report=200)
#        print("swapping")
#        solver = RandomGreedyDotSwapperSolver(puzzle, 5000)
#        puzzle = solver.solve(status_report=70)
#        print("zooming")
#        solver = SelectiveRandomDotGreedySolver(puzzle, 2000)
#        puzzle = solver.solve(status_report=70)
#        print("swapping")
#        solver = RandomGreedyDotSwapperSolver(puzzle, 5000)
#        puzzle = solver.solve(status_report=100)
#        print("zooming")
#        solver = SelectiveRandomDotGreedySolver(puzzle, 2000)
#        puzzle = solver.solve(status_report=70)
#
#puzzle = RandomGrid(3, 10, 10)
#puzzle.initialise()
#cycle(puzzle)
#
#puzzle.print_grid()
