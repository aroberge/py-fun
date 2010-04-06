# mandel2a_cy.pyx
# cython: profile=True

def mandel(c, int max_iterations=20):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a maximum allowed number of iterations, the absolute value of
       the resulting number is greater or equal to 2.'''
    cdef int i

    for i in range(0, max_iterations):
        z = z**2 + c
        if abs(z) >= 2:
            return False
    return abs(z) < 2