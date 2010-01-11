# mandel1b.py

import sys
if sys.version_info < (3,):
    range = xrange

def mandel(c):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after 100 iterations, the absolute value of the resulting number is
       greater or equal to 2.'''
    z = 0
    for iter in range(0, 100):
        z = z**2 + c
        if abs(z) >= 2:
            return False
    return abs(z) < 2