# mandel2a_cy.pyx
# cython: profile=True

def mandel(double real, double imag):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after 100 iterations, the absolute value of the resulting number is
       greater or equal to 2.'''
    z_r = z_i = 0
    for iter in range(0, 100):
        z_r, z_i = ( z_r*z_r - z_i*z_i + real,
                     2*z_r*z_i + imag )
        if (z_r**2 + z_i**2) >= 4:
            return False
    return (z_r**2 + z_i**2) < 4