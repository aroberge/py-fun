# mandel2g_cy.pyx
# cython: profile=True

import cython

@cython.profile(False)
cdef inline bint mandel(double real, double imag, int max_iterations=20):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a maximum allowed number of iterations, the absolute value of
       the resulting number is greater or equal to 2.'''
    cdef double z_real = 0., z_imag = 0.
    cdef int i

    for i in range(0, max_iterations):
        z_real, z_imag = ( z_real*z_real - z_imag*z_imag + real,
                           2*z_real*z_imag + imag )
        if (z_real*z_real + z_imag*z_imag) >= 4:
            return False
    return (z_real*z_real + z_imag*z_imag) < 4

def create_fractal(int canvas_width, int canvas_height,
                       double min_x, double min_y, double pixel_size,
                       int nb_iterations, canvas):
    cdef int x, y, start_y, end_y
    cdef double real, imag
    cdef bint start_line

    for x in range(0, canvas_width):
        real = min_x + x*pixel_size
        start_line = False
        for y in range(0, canvas_height):
            imag = min_y + y*pixel_size
            if mandel(real, imag, nb_iterations):
                if not start_line:
                    start_line = True
                    start_y = canvas_height - y
            else:
                if start_line:
                    start_line = False
                    end_y = canvas_height - y
                    canvas.create_line(x, start_y, x, end_y, fill="black")
        if start_line:
            end_y = canvas_height - y
            canvas.create_line(x, start_y, x, end_y, fill="black")