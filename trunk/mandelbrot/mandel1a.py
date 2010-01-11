# mandel1a.py

def mandel(c):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after 20 iterations, the absolute value of the resulting number is
       greater or equal to 2.'''
    z = 0
    for iter in range(0, 20):
        z = z**2 + c
        if abs(z) >= 2:
            return False
    return abs(z) < 2