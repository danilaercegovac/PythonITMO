from setuptools import setup
from Cython.Build import cythonize

setup(
    name="cyintegrate_nogil",
    ext_modules=cythonize(
        "cyintegrate_nogil.pyx",
        annotate=True,
        compiler_directives={"language_level": "3"},
    ),
)