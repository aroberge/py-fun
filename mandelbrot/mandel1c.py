# mandel1c.py

import sys
if sys.version_info < (3,):
    range = xrange

def mandel(c, max_iterations=20):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a maximum allowed number of iterations, the absolute value of
       the resulting number is greater or equal to 2.'''
    z = 0
    for iter in range(0, max_iterations):
        z = z**2 + c
        z_sq = z.real**2 + z.imag**2
        if z_sq >= 4:
            return False
    return z_sq < 2