from __future__ import annotations

import concurrent.futures as futures
from functools import partial
from typing import Callable

from integrate_py import integrate


def integrate_threaded(
    f: Callable[[float], float],
    a: float,
    b: float,
    *,
    n_jobs: int = 2,
    n_iter: int = 100_000,
) -> float:
    """
    Parallel integration using threads (ThreadPoolExecutor).

    Note: In CPython, CPU-bound code is limited by GIL, so this usually does NOT
    speed up pure-Python computations. It is implemented for comparison with
    ProcessPoolExecutor and with Cython noGIL version (iteration 5).

    Parameters
    ----------
    f : Callable[[float], float]
        Integrand.
    a, b : float
        Integration interval boundaries.
    n_jobs : int
        Number of worker threads.
    n_iter : int
        Total number of rectangles.

    Returns
    -------
    float
        Approximate integral value.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs must be positive")
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")

    # dividing work
    step_job = (b - a) / n_jobs
    iters_per_job = n_iter // n_jobs

    with futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        spawn = partial(executor.submit, integrate, f, n_iter=iters_per_job)
        fs = [
            spawn(a + i * step_job, a + (i + 1) * step_job)
            for i in range(n_jobs)
        ]
        return sum(fut.result() for fut in futures.as_completed(fs))
