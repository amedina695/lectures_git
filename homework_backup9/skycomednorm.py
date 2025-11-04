import numpy as np

def skycormednorm(objdata, normskydata, region=((None, None), (None, None))):
  """
    Denormalize the sky frame and remove it from the input data.

    This is the second half of normalized median combination.
    The routine finds the normalization of the object frame by
    taking the median of objdata[y1:y2, x1:x2].  It multiplies this by
    normskydata.  It subtracts the result from objdata.

    Parameters
    ----------
    objdata : ndarray, 2D
        Object frame to correct
    normskydata : ndarray, 2D
        Normalized sky frame
    region: tuple of 2 tuples of 2 ints, ((y1, x1), (y2, x2))
	    y1: bottom     of normalization region (default bottom edge)
        x1: left edge  of normalization region (default left   edge)
        y2: top        of normalization region (default top    edge)
        x2: right edge of normalization region (default right  edge)

    Returns
    -------
    output: ndarray, 2D
        The corrected object frame.

    Examples
    --------
    None yet.

    Revisions
    ---------
    2003-02-26 0.1 jh@oobleck.astro.cornell.edu Initial version.
    2004-04-03 0.2 jh@oobleck.astro.cornell.edu Modified for 2004 assignment.
    2004-04-05 0.3 jh@oobleck.astro.cornell.edu Fixed to use x1, x2, y1,
                  y2, and to subtract dark before sky normalization
                  calc.
    2007-10-21 0.4 jh@physics.ucf.edu Converted from IDL to Python.
                  Remove header stuff.
    2008-10-27 0.5 kstevenson@physics.ucf.edu  Updated docstring
    2009-10-01 0.6 jh@physics.ucf.edu  Tweaked docstring.  Shortened program.
    2009-11-12 0.7 jh@physics.ucf.edu  Tweaked docstring.
    2016-11-12 0.8 jh@physics.ucf.edu  Tweaked docstring.
    2018-10-11 0.9 jh@physics.ucf.edu  Do final subtraction in place.
  """
  ((y1, x1), (y2, x2)) = region            # set corners
  retval = objdata.copy()                  # copy the data
  norm   = np.median(objdata[y1:y2,x1:x2]) # calculate the normalization
  retval -= norm * normskydata             # de-normalize sky and subtract
  
  return retval
