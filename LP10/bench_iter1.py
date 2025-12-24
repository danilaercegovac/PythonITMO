import math
import timeit

from integrate_py import integrate

def bench() -> None:
    """
    Run a baseline performance benchmark for the pure Python `integrate()`.
    The function measures runtime for different iteration counts (`n_iter`)
    and prints total and average execution time.
    """
    print("Benchmark: integrate(math.sin, 0, pi)")
    for n_iter in [10_000, 50_000, 100_000, 300_000, 1_000_000]:
        t = timeit.timeit(
            stmt="integrate(math.sin, 0.0, math.pi, n_iter=n_iter)",
            number=5,
            globals={"integrate": integrate, "math": math, "n_iter": n_iter},
        )
        print(f"n_iter={n_iter:>9}: {t:.6f} sec (5 runs) -> avg {t/5:.6f} sec")

if __name__ == "__main__":
    bench()
