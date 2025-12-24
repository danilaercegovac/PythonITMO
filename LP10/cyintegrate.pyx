# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, nonecheck=False
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

from libc.math cimport sin, cos
cimport cython

@cython.cfunc
@cython.inline
cdef double rect_integrate_c(double (*func)(double), double a, double b, long n_iter):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef long i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += func(x) * step
    return acc


def integrate_cy_sin(double a, double b, long n_iter=100000):
    """Fast C-level integration for sin(x)."""
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")
    return rect_integrate_c(sin, a, b, n_iter)


def integrate_cy_cos(double a, double b, long n_iter=100000):
    """Fast C-level integration for cos(x)."""
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")
    return rect_integrate_c(cos, a, b, n_iter)


def integrate_cy_generic(f, double a, double b, long n_iter=100000):
    """
    Generic Cython integration, still calls Python function f(x), so speedup is limited.
    """
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")

    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef long i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step
    return acc
