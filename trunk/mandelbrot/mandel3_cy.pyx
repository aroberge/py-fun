# mandel3_cy.pyx
# cython: profile=True

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


def draw_pixel(x, y, canvas):
    '''Simulates drawing a given pixel in black by drawing a black line
       of length equal to one pixel.'''
    canvas.create_line(x, y, x+1, y, fill="black")

def create_fractal(canvas_width, canvas_height, min_x, min_y, max_x, max_y,
                       delta_x, delta_y, canvas):
    for x in range(0, canvas_width):
        real = min_x + x*delta_x
        for y in range(0, canvas_height):
            imag = min_y + y*delta_y
            if mandel(real, imag):
                draw_pixel(x, canvas_height - y, canvas)
