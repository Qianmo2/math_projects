# setup.py
from setuptools import setup
from Cython.Build import cythonize

# 注意：你可能需要添加额外的库或路径，根据 gmpy2 在你系统中的安装
setup(
    ext_modules=cythonize("cython_fib.pyx", annotate=True),
    compiler_directives={'language_level': "3"}
)
