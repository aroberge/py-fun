'''Explicitly constructing solutions for
http://bit-player.org/2009/the-17x17-challenge
'''

import copy
import random
import sys
import time
import grid


def choose_problem(n):
    global grid_size, nb_colours, base_colour_pattern
    if n == 3:
        grid_size = 10
        nb_colours = 3
        base_colour_pattern = [4, 3, 3]
    else:
        grid_size = 17
        nb_colours = 4
        base_colour_pattern = [5, 4, 4, 4]

choose_problem(4)
enough_rows = grid_size + 5

bit_patterns = {}
for i in range(grid_size+1):
    bit_patterns[i] = []
for x in range(2**grid_size):
    bit_patterns[bin(x).count('1')].append(x)

colour_patterns = {}
for colour in range(nb_colours):
    colour_patterns[colour] = []
    for row in range(enough_rows):   # more rows than we possibly need...
        colour_patterns[colour].append(
            base_colour_pattern[(row+colour)%nb_colours])

allowed_patterns = {}
for i in [0, 1]:
    j = base_colour_pattern[i]
    allowed_patterns[j] = copy.deepcopy(bit_patterns[j])

#The idea is as follows:
#    1) Create an empty grid.
#    2) Add rows with a single colour following a pre-assigned
#       pattern, so that no rectangles are created.  Make sure that
#       the number of rows is equal or greater than the number of columns.
#    3) Add a second colour...
#    4) Continue adding colours until only two are left
#    5) Add last two colours together

def add_row(patterns, new_grid):
    '''adds a row to a grid without creating conflicts with rows already
       present'''
    remaining_patterns = []
    row_added = False
    new_pattern = None
    random.shuffle(patterns)
    for i, pattern in enumerate(patterns):
        if row_added:
            break
        if not new_grid.grid:
            new_grid.add_empty_row()
            new_grid.grid[new_grid.nb_rows-1][0] = pattern
            remaining_patterns = patterns[1:]
            new_pattern = pattern
            row_added = True
        else:
            for row in new_grid.grid:
                old_pattern = new_grid.grid[row][0]
                if not grid.intersect_for_two_rows(pattern, old_pattern):
                    new_grid.add_empty_row()
                    new_grid.grid[new_grid.nb_rows-1][0] = pattern
                    new_pattern = pattern
                    remaining_patterns = patterns[i+1:]
                    row_added = True
                    break
    return new_pattern, remaining_patterns

def reduce_patterns(new_pattern, patterns):
    '''from existing list of patterns, remove those that conflict with an
    individual one'''
    remaining = []
    for pattern in patterns:
        if not grid.intersect_for_two_rows(pattern, new_pattern):
            remaining.append(pattern)
    return remaining

grid_created = {}
for i in range(enough_rows):
    grid_created[i] = 0

def create_grid(new_grid):
    for row in range(enough_rows):
        nb_pts = colour_patterns[0][row]
        patterns = bit_patterns[nb_pts]
        if not patterns:
            break
        used_pattern, remaining_patterns = add_row(patterns, new_grid)
        bit_patterns[nb_pts] = remaining_patterns
        if used_pattern is None:
            break
        for i in (0, 1):
            nb_pts = colour_patterns[0][i]
            bit_patterns[nb_pts] = reduce_patterns(used_pattern, bit_patterns[nb_pts])
    grid_created[new_grid.nb_rows] += 1
    if new_grid.nb_rows >= grid_size:
        print '-'*10, "nb_rows = ", new_grid.nb_rows
        new_grid.print_grid()


if __name__ == "__main__":
    begin = time.time()
    for i in range(10000):
        bit_patterns_copy = copy.deepcopy(bit_patterns)
        new_grid = grid.EmptyGrid(nb_colours, 0, grid_size)
        create_grid(new_grid)
        bit_patterns = copy.deepcopy(bit_patterns_copy)
        if not i%100:
            print "iteration:", i, "   time elapsed:", time.time() - begin
            for i in range(enough_rows):
                print i, grid_created[i]

