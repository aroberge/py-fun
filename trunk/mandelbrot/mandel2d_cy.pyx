# mandel2d_cy.pyx
# cython: profile=True

def mandel(double real, double imag, int max_iterations=20):
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

def draw_pixel(x, y, canvas):
    '''Simulates drawing a given pixel in black by drawing a black line
       of length equal to one pixel.'''
    return
    #canvas.create_line(x, y, x+1, y, fill="black")

def create_fractal(canvas_width, canvas_height,
                       min_x, min_y, pixel_size,
                       nb_iterations, canvas):
    for x in range(0, canvas_width):
        real = min_x + x*pixel_size
        for y in range(0, canvas_height):
            imag = min_y + y*pixel_size
            if mandel(real, imag, nb_iterations):
                draw_pixel(x, canvas_height - y, canvas)