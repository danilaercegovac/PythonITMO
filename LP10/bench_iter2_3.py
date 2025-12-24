import math
import timeit

from integrate_py import integrate
from integrate_threads import integrate_threaded
from integrate_processes import integrate_processed


def bench()-> None:
    """
    Run benchmark comparisons for:
    - single-thread baseline
    - threads (ThreadPoolExecutor)
    - processes (ProcessPoolExecutor)

    Prints total and average runtime for each strategy and each value of n_jobs.
    """
    n_iter = 2_000_000
    print(f"Benchmark n_iter={n_iter} for sin on [0, pi]\n")

    # baseline
    t_base = timeit.timeit(
        stmt="integrate(math.sin, 0.0, math.pi, n_iter=n_iter)",
        number=3,
        globals={"integrate": integrate, "math": math, "n_iter": n_iter},
    )
    print(f"BASE (single): {t_base:.6f} sec (3 runs) avg={t_base/3:.6f}\n")

    for n_jobs in [2, 4, 6, 8]:
        t_thr = timeit.timeit(
            stmt="integrate_threaded(math.sin, 0.0, math.pi, n_jobs=n_jobs, n_iter=n_iter)",
            number=3,
            globals={
                "integrate_threaded": integrate_threaded,
                "math": math,
                "n_jobs": n_jobs,
                "n_iter": n_iter,
            },
        )

        t_proc = timeit.timeit(
            stmt="integrate_processed(math.sin, 0.0, math.pi, n_jobs=n_jobs, n_iter=n_iter)",
            number=3,
            globals={
                "integrate_processed": integrate_processed,
                "math": math,
                "n_jobs": n_jobs,
                "n_iter": n_iter,
            },
        )

        print(f"n_jobs={n_jobs}: threads={t_thr:.6f} (avg={t_thr/3:.6f}), "
              f"processes={t_proc:.6f} (avg={t_proc/3:.6f})")


if __name__ == "__main__":
    bench()
