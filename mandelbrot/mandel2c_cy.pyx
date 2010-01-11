# mandel2c_cy.pyx
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