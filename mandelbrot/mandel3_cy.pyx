# mandel3_cy.pyx
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

colours = make_palette()
cdef int nb_colours = len(colours)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.profile(False)
cdef inline int mandel(double real, double imag, int max_iterations=20):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a maximum allowed number of iterations, the absolute value of
       the resulting number is greater or equal to 2.'''
    cdef double z_real = 0., z_imag = 0.
    cdef int i

    for i in range(0, max_iterations):
        z_real, z_imag = ( z_real*z_real - z_imag*z_imag + real,
                           2*z_real*z_imag + imag )
        if (z_real*z_real + z_imag*z_imag) >= 4:
            return i
    return -1

def create_fractal(int canvas_width, int canvas_height,
                       double min_x, double min_y, double pixel_size,
                       int nb_iterations, canvas):
    global colours, nb_colours
    cdef int x, y, start_y, end_y, current_colour, new_colour
    cdef double real, imag

    for x in range(0, canvas_width):
        real = min_x + x*pixel_size
        start_y = canvas_height
        current_colour = mandel(real, min_y, nb_iterations)
        for y in range(1, canvas_height):
            imag = min_y + y*pixel_size
            new_colour = mandel(real, imag, nb_iterations)

            if new_colour != current_colour:
                if current_colour == -1:
                    canvas.create_line(x, start_y, x, canvas_height-y,
                                        fill="black")
                else:
                    canvas.create_line(x, start_y, x, canvas_height-y,
                                        fill=colours[current_colour%nb_colours])
                current_colour = new_colour
                start_y = canvas_height - y

        if current_colour == -1:
            canvas.create_line(x, start_y, x, 0, fill="black")
        else:
            canvas.create_line(x, start_y, x, 0,
                                        fill=colours[current_colour%nb_colours])
