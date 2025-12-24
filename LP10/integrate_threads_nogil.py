import concurrent.futures as futures

import cyintegrate_nogil


def integrate_sin_threaded_nogil(
    a: float,
    b: float,
    *,
    n_jobs: int = 2,
    n_iter: int = 1_000_000
) -> float:
    """
    Compute the integral of sin(x) on [a, b] in parallel using threads and a noGIL Cython kernel.

    Demonstrates true multithreaded speed-up for a CPU-bound task in CPython.
    The key idea is that each thread calls a Cython function (`integrate_sin_nogil`) which
    releases the Global Interpreter Lock (GIL) and performs the heavy computation entirely
    in C while running under `nogil`.

    Parameters
    ----------
    a : float
        Left boundary of integration interval.
    b : float
        Right boundary of integration interval.
    n_jobs : int, optional
        Number of worker threads to use. Must be a positive integer.
        Typical values are 2, 4, 6, 8 depending on CPU core count.
    n_iter : int, optional
        Total number of rectangles for the whole interval.
        This value will be divided between threads (`n_iter // n_jobs` per thread).
        Must be a positive integer.

    Returns
    -------
    float
        Approximate value of the definite integral of sin(x) over [a, b].

    Raises
    ------
    ValueError
        If `n_jobs <= 0` or `n_iter <= 0`.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs must be positive")
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")

    step_job = (b - a) / n_jobs
    iters_per_job = n_iter // n_jobs

    with futures.ThreadPoolExecutor(max_workers=n_jobs) as ex:
        fs = [
            ex.submit(
                cyintegrate_nogil.integrate_sin_nogil,
                a + i * step_job,
                a + (i + 1) * step_job,
                iters_per_job,
            )
            for i in range(n_jobs)
        ]
        return sum(f.result() for f in futures.as_completed(fs))