# mandel3a_cy.pyx
# cython: profile=True

import cython

@cython.profile(False)
def mandel(double real, double imag):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after 1000 iterations, the absolute value of the resulting number is
       greater or equal to 2.'''

    cdef double z_r = 0, z_i = 0
    cdef int iter

    z_r = z_i = 0
    for iter in range(0, 1000):
        z_r, z_i = ( z_r*z_r - z_i*z_i + real,
                     2*z_r*z_i + imag )
        if (z_r*z_r + z_i*z_i) >= 4:
            return False
    return (z_r*z_r + z_i*z_i) < 4

def create_fractal(int canvas_width, int canvas_height,
                   double min_x, double min_y,
                   double max_x, double max_y,
                   double delta_x, double delta_y, canvas):
    cdef int x, y
    for x in range(0, canvas_width):
        real = min_x + x*delta_x
        for y in range(0, canvas_height):
            imag = min_y + y*delta_y
            if mandel(real, imag):
                y = canvas_height - y
                canvas.create_line(x, y, x+1, y, fill="black")
