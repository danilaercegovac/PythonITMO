from __future__ import annotations

import math
from typing import Callable


def integrate(
    f: Callable[[float], float],
    a: float,
    b: float,
    *,
    n_iter: int = 100_000
) -> float:
    """
    Compute a definite integral using the left Riemann sum (rectangle method).

    The function approximates the integral of `f(x)` over [a, b] by splitting
    the interval into `n_iter` subintervals of equal width and summing areas
    of rectangles with heights f(a + i*step).

    Parameters
    f:
        A single-variable callable representing the integrand f(x).
        Must accept a float and return a float.
    a:
        Left boundary of integration interval.
    b:
        Right boundary of integration interval.
    n_iter:
        Number of rectangles (iterations). Must be a positive integer.
        Larger values generally improve accuracy but increase runtime.

    Returns
    float
        Approximate value of the definite integral ∫[a,b] f(x) dx.

    Raises
    ValueError
        If `n_iter <= 0`.

    Examples
    --------
    Trigonometric example: ∫[0,π] sin(x) dx = 2

    >>> import math
    >>> round(integrate(math.sin, 0.0, math.pi, n_iter=200_000), 6)
    2.0

    Polynomial example: ∫[0,1] (x^2 + 2x + 1) dx = 7/3 ≈ 2.333333...

    >>> f = lambda x: x*x + 2*x + 1
    >>> abs(integrate(f, 0.0, 1.0, n_iter=200_000) - (7/3)) < 1e-4
    True
    """
    if n_iter <= 0:
        raise ValueError("n_iter must be a positive integer")

    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


if __name__ == "__main__":
    print(integrate(math.cos, 0, math.pi, n_iter=1000))
