# cython: profile=True

def mandel(double real, double imag, int max_iter=20):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a specified number of iterations (or 20 by default),
       the absolute value of the resulting number is greater or equal to 2.'''
    cdef double z_r, old_z_r, z_i

    z_r = 0.
    z_i = 0.
    for i in xrange(0, max_iter):
        old_z_r = z_r
        z_r = z_r*z_r - z_i*z_i + real
        z_i = 2*old_z_r*z_i + imag
        if (z_r*z_r + z_i*z_i) >= 4:
            return False
    return (z_r*z_r + z_i*z_i) < 4

def create_fractal(int width, int height, int min_x, int min_y,
                   double delta_x, double delta_y):
    '''draw a fractal on a fake canvas'''
    cdef double imag, real
    x_values = []
    for x in xrange(0, width):
        x_values.append(x*delta_x + min_x)
    cols = []
    for y in xrange(height, 0, -1):
        imag = (height - y)*delta_y + min_y
        rows = ['#FFFFFF' for x in xrange(0, width)]
        for x in xrange(0, width):
            real = x_values[x]
            if mandel(real, imag):
                rows[x] = '#000000'
        cols.append(tuple(rows))
    return tuple(cols)