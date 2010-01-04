''' test solver for diagnostic


'''

import pstats, cProfile   # 1

#import pyximport  # 2
#pyximport.install() # 2

import time
from solver import RandomDotGreedySolver
from grid import RandomGrid

def main():
    puzzle = RandomGrid(3, 10, 10)
    test_solver = RandomDotGreedySolver(puzzle, 10000)
    #begin = time.time()    # 0
    test_solver.solve()
    #print "time elapsed=", time.time()-begin   # 0

if __name__ == "__main__":
    #main()     # 0
    cProfile.run("main()", "Profile.prof")  # 1
    s = pstats.Stats("Profile.prof")  # 1
    s.strip_dirs().sort_stats("time").print_stats()  # 1