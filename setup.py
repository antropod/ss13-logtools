from setuptools import setup
from Cython.Build import cythonize

setup(
    name = "ss13-logtools",
    ext_modules=cythonize(["**/*.pyx"]),
)