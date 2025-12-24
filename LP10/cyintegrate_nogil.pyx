# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, nonecheck=False

from libc.math cimport sin
cimport cython

@cython.cfunc
cdef double rect_integrate_sin_nogil(double a, double b, long n_iter) nogil:
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef long i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += sin(x) * step
    return acc


def integrate_sin_nogil(double a, double b, long n_iter=100000):
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")
    cdef double res
    with nogil:
        res = rect_integrate_sin_nogil(a, b, n_iter)
    return res
