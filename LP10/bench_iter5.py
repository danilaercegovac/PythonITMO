import math
import timeit

from integrate_processes import integrate_processed
from integrate_threads import integrate_threaded
from integrate_threads_nogil import integrate_sin_threaded_nogil

import cyintegrate_nogil


def bench() -> None:
    """
    The benchmark integrates sin(x) over [0, pi] using a fixed total number
    of rectangles (`n_iter`) and compares three strategies:
    - pure Python threading (GIL-limited)
    - multiprocessing (true parallelism but higher overhead)
    - threading with Cython noGIL kernel (true parallelism with low overhead)
    """
    n_iter = 20_000_000
    print(f"Iteration 5 benchmark (sin, [0, pi]), n_iter={n_iter}\n")

    # baseline Cython noGIL single
    t_single = timeit.timeit(
        stmt="cyintegrate_nogil.integrate_sin_nogil(0.0, math.pi, n_iter=n_iter)",
        number=3,
        globals={"cyintegrate_nogil": cyintegrate_nogil, "math": math, "n_iter": n_iter},
    )
    print(f"Cython noGIL single: {t_single:.6f} (avg={t_single/3:.6f})\n")

    for n_jobs in [2, 4, 6, 8]:
        # обычные python threads (GIL) — почти нет ускорения
        t_thr = timeit.timeit(
            stmt="integrate_threaded(math.sin, 0.0, math.pi, n_jobs=n_jobs, n_iter=n_iter)",
            number=3,
            globals={"integrate_threaded": integrate_threaded, "math": math, "n_jobs": n_jobs, "n_iter": n_iter},
        )

        # процессы (параллельно)
        t_proc = timeit.timeit(
            stmt="integrate_processed(math.sin, 0.0, math.pi, n_jobs=n_jobs, n_iter=n_iter)",
            number=3,
            globals={"integrate_processed": integrate_processed, "math": math, "n_jobs": n_jobs, "n_iter": n_iter},
        )

        # threads + nogil (должно ускоряться)
        t_nogil_thr = timeit.timeit(
            stmt="integrate_sin_threaded_nogil(0.0, math.pi, n_jobs=n_jobs, n_iter=n_iter)",
            number=3,
            globals={"integrate_sin_threaded_nogil": integrate_sin_threaded_nogil, "math": math, "n_jobs": n_jobs, "n_iter": n_iter},
        )

        print(
            f"n_jobs={n_jobs}: "
            f"threads(GIL)={t_thr/3:.6f}, "
            f"processes={t_proc/3:.6f}, "
            f"threads(noGIL)={t_nogil_thr/3:.6f}"
        )


if __name__ == "__main__":
    bench()