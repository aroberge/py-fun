# mandel2c_cy.pyx
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
