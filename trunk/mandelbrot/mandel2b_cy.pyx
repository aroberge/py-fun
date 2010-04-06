# mandel2b_cy.pyx
# cython: profile=True

cdef extern from "complexobject.h":

    struct Py_complex:
        double real
        double imag

    ctypedef class __builtin__.complex [object PyComplexObject]:
        cdef Py_complex cval


def mandel(complex c, int max_iterations=20):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a maximum allowed number of iterations, the absolute value of
       the resulting number is greater or equal to 2.'''
    cdef int i
    cdef complex z

    z = 0. + 0.j

    for i in range(0, max_iterations):
        z = z*z + c
        if abs(z) >= 2:
            return False
    return abs(z) < 2