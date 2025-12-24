import math
import timeit

from integrate_py import integrate
import cyintegrate


def bench()-> None:
    """
    Run performance comparisons between:
    - pure Python integration
    - Cython generic integration (calls Python function inside loop)
    - Cython sin integration (pure C loop + libc math)
    """
    n_iter = 5_000_000
    print(f"Benchmark Cython, n_iter={n_iter}\n")

    t_py = timeit.timeit(
        stmt="integrate(math.sin, 0.0, math.pi, n_iter=n_iter)",
        number=3,
        globals={"integrate": integrate, "math": math, "n_iter": n_iter},
    )
    print(f"Python integrate: {t_py:.6f} sec (avg={t_py/3:.6f})")

    t_cy_generic = timeit.timeit(
        stmt="cyintegrate.integrate_cy_generic(math.sin, 0.0, math.pi, n_iter=n_iter)",
        number=3,
        globals={"cyintegrate": cyintegrate, "math": math, "n_iter": n_iter},
    )
    print(f"Cython generic (calls Python f): {t_cy_generic:.6f} sec (avg={t_cy_generic/3:.6f})")

    t_cy_sin = timeit.timeit(
        stmt="cyintegrate.integrate_cy_sin(0.0, math.pi, n_iter=n_iter)",
        number=3,
        globals={"cyintegrate": cyintegrate, "math": math, "n_iter": n_iter},
    )
    print(f"Cython sin (pure C math): {t_cy_sin:.6f} sec (avg={t_cy_sin/3:.6f})")


if __name__ == "__main__":
    bench()