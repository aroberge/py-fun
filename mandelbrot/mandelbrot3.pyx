# cython: profile=True

import cython

cdef inline int mandel(double real, double imag, int max_iter=1000):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a specified number of iterations (or 20 by default),
       the absolute value of the resulting number is greater or equal to 2.'''
    cdef double z_r, old_z_r, z_i
    cdef int i

    z_r = 0.
    z_i = 0.
    for i in xrange(0, max_iter):
        old_z_r = z_r
        z_r = z_r*z_r - z_i*z_i + real
        z_i = 2*old_z_r*z_i + imag
        if (z_r*z_r + z_i*z_i) >= 4.:
            return i
    return -1

def create_fractal(int width, int height, double min_x, double min_y,
                   double delta_x, double delta_y):
    '''draw a fractal on a fake canvas'''
    cdef double imag, real
    cdef int x, y, nb_iter
    cdef red, green, blue

    x_values = []
    for x in xrange(0, width):
        x_values.append(x*delta_x + min_x)
    cols = []
    for y in xrange(height-1, -1, -1):
        imag = (height - y)*delta_y + min_y
        rows = ['#000000' for x in xrange(0, width)]
        for x in xrange(0, width):
            real = x_values[x]
            nb_iter = mandel(real, imag)
            if nb_iter != -1:
                if nb_iter < 10:
                    red = 25*nb_iter
                    green = 0
                    blue = 0
                elif nb_iter < 100:
                    red = 255
                    green = 25*nb_iter/10
                    blue = 0
                else:
                    red = 255
                    green = 255
                    blue = 25*nb_iter/100
                rows[x] = '#%02x%02x%02x' % (red, green, blue)
        cols.append(tuple(rows))
    return tuple(cols)