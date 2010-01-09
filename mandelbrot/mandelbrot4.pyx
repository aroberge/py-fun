# cython: profile=True
import cython

def make_palette():
    '''sample coloring scheme for the fractal - feel free to experiment'''
    colours = []

    for i in range(0, 25):
        colours.append('#%02x%02x%02x' % (i*10, i*8, 50 + i*8))
    for i in range(25, 5, -1):
        colours.append('#%02x%02x%02x' % (50 + i*8, 150+i*2,  i*10))
    for i in range(10, 2, -1):
        colours.append('#00%02x30' % (i*15))
    return colours

cdef colours = make_palette()
cdef int nb_colours = len(colours)

@cython.profile(False)
cdef inline int mandel(double real, double imag, int max_iter=1000):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a specified number of iterations (or 1000 by default),
       the absolute value of the resulting number is greater or equal to 2.'''
    cdef double z_r, z_i
    cdef int i

    z_r = 0.
    z_i = 0.
    for i in range(0, max_iter):
        z_r, z_i = z_r*z_r - z_i*z_i + real, 2*z_r*z_i + imag
        if (z_r*z_r + z_i*z_i) >= 4.:
            return i
    return -1

def create_fractal(int width, int height, double min_x, double min_y,
                   double delta_x, double delta_y):
    '''draws a fractal on a fake canvas'''
    global colours, nb_colours
    cdef double imag, real
    cdef int x, y, nb_iter

    x_values = []
    for x in range(0, width):
        x_values.append(x*delta_x + min_x)
    cols = []
    for y in range(height-1, -1, -1):
        imag = y*delta_y + min_y
        rows = ['#000000' for x in range(0, width)]
        for x in range(0, width):
            real = x_values[x]
            nb_iter = mandel(real, imag)
            if nb_iter != -1:
                rows[x] = colours[nb_iter%nb_colours]
        cols.append(tuple(rows))
    return tuple(cols)