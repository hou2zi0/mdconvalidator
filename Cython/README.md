# What’s Cython, why and how to use it?

* Basic tutorial [Optimizing with Cython Introduction - Cython Tutorial](https://pythonprogramming.net/introduction-and-basics-cython-tutorial/)
* More [tutorials](https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html)
* Cython [documentation](https://cython.org/)

## How to use it

1. Save your Python file `py_extension.py` with the file suffix `py_extension.pyx`.
1. Add (as much) static types to your variables and functions (as you want), e.g.:
    1. `cdef int`
    1. `cdef float`
    1. `cdef double`
    1. `cdef char`
    1. `cdef unicode`
    1. `cdef (unicode, int)`
    1. `cdef list `
    1. `cdef dict`
    1. `cdef object`
    1. `cpdef function`, e.g. `cpdef int addition(int x, int y)`:
        1. `cpdef` introduces a new function that’s usable in Python as well as in C.
        1. The first `int` declares the type of the function’s return value.
        1. `addition()` specifies the function name.
        1. The `int`s inside the parentheses declare the types of the parameters.
    1. For more in depth info see [Cython Language Basics](https://cython.readthedocs.io/en/latest/src/userguide/language_basics.html)
1. Add to `setup.py`.
1. Compile `python3 setup.py build_ext --inplace`. Cython generates:
    1. A `py_extension.so`-extension file (shared object).
    1. A `py_extension.c`-file.
    1. A folder containing some information about the build. 
1. Now you may import the `py_extension.so`-file into your normal Python-scripts, by `import py_extension`.

