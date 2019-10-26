# What’s Cython, why and how to use it?

* Basic tutorial [Optimizing with Cython Introduction - Cython Tutorial](https://pythonprogramming.net/introduction-and-basics-cython-tutorial/)
* More [tutorials](https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html)
* Cython [documentation](https://cython.org/)

## How to use it

1. Save your Python file `py_extension.py` with the file suffix `py_extension.pyx`.
1. Add (as much) static types to your variables and functions (as you want), e.g.:
    1. `cdef int x,y,z`
    1. `cdef char *s`
    1. `cdef unicode `
    1. `cdef float x = 5.2 (single precision)`
    1. `cdef double x = 40.5 (double precision)`
    1. `cdef (unicode, int) tuple`
    1. `cdef list languages`
    1. `cdef dict abc_dict`
    1. `cdef object thing`
    1. `cpdef function`
    1. For mor ein depth info see [Cython Language Basics](https://cython.readthedocs.io/en/latest/src/userguide/language_basics.html)
1. Add to `setup.py`.
1. Compile `python3 setup.py build_ext --inplace`. Cython generates:
    1. A `py_extension.so`-extension file (shared object).
    1. A `py_extension.c`-file.
    1. A folder containing some information about the build. 
1. Now you may import the `py_extension.so`-file into your normal Python-scripts, by `import py_extension`.

