# cython: profile=False

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