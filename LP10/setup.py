from setuptools import setup
from Cython.Build import cythonize

setup(
    name="cyintegrate",
    ext_modules=cythonize(
        "cyintegrate.pyx",
        annotate=True,               # gives HTML-annotation
        compiler_directives={"language_level": "3"},
    ),
)