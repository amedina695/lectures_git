"""This file is titled support.py, with class naming convention, 
with the purpose of being used to add support functions for homework
assignments.

"""

# Imports

import os # standard library imports first
import numpy as np
# import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
# import astropy.io.fits as fits

# My functions
# Creating a square function

def square(x):
    """A function that takes an input of a scalar
    or an array if any dimension or type and returns
    the square.

    Parameters
    -----------
    x: int or array_like

    Returns
    -------
    squared result: int or array

    References
    ----------
    https://numpy.org/doc/2.2/reference/generated/numpy.asarray.html

    Examples
    --------

    For an integer

    >>> x = 9
    >>> print(square(x))
    81

    For an array

    >>> a=[1,2,3]
    >>> print(square(a))
    [1, 4, 9]

    """

    x = np.asarray(x) # Converts input to array
    return x**2

    pass
