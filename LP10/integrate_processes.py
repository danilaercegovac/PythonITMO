from __future__ import annotations

import concurrent.futures as futures
from functools import partial
from typing import Callable

from integrate_py import integrate


def integrate_processed(
    f: Callable[[float], float],
    a: float,
    b: float,
    *,
    n_jobs: int = 2,
    n_iter: int = 100_000,
) -> float:
    """
    Parallel integration using processes (ProcessPoolExecutor).
    This typically speeds up CPU-bound Python code, because each process has its
    own Python interpreter and its own GIL.

    Parameters
    ----------
    f : Callable[[float], float]
        Integrand (MUST be pickleable).
    a, b : float
        Integration interval boundaries.
    n_jobs : int
        Number of worker processes.
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

    step_job = (b - a) / n_jobs
    iters_per_job = n_iter // n_jobs

    with futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        spawn = partial(executor.submit, integrate, f, n_iter=iters_per_job)
        fs = [
            spawn(a + i * step_job, a + (i + 1) * step_job)
            for i in range(n_jobs)
        ]
        return sum(fut.result() for fut in futures.as_completed(fs))
