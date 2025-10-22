import numpy as np

def radprof(im, cy, cx, binsz=1.):
    '''
SYNTAX:
    radprof(im, cy, cx, binsz=1.)

PURPOSE:
    Compute the radial profile of a 2D image (im) around a point (cy, cx).

INPUTS:
    im:	2D array of image fluxes.
    cy:	Y coordinate of point.
    cx:	X coordinate of point.
    binsz: Bin size.  FINDME: it would be good to accept an array of bin sizes
    
OUTPUTS:
    This function returns:
    bins: (returned) a 1D array giving the central radius in each annulus
    prof: (returned) a 1D array giving the average value of an
          image in each of a series of concentric, annular bins centered on
          a given point.
    sr: (returned) 1D array of sorted pixel radii from (cy, cx)
    sim: (returned) 1D array of image values corresponding to sr


EXAMPLE/TEST:


MODIFICATION HISTORY:
2007-10-01 0.1	jh@physics.ucf.edu	Initial version, cribbed from
					Greenfield tutorial.
2007-10-04 0.2  jh@physics.ucf.edu	Exposed sr and sim
2008-10-09 0.3  jh@physics.ucf.edu	Reimplemented.  Now slow but right.
    '''

    y,x = np.indices(im.shape, dtype=float) # first determine radii of all pixels
    r = np.sqrt(  (x-cx)**2
              +   (y-cy)**2 )
  # FINDME: not sure the sort is needed anymore
    ind = np.argsort(r.flat)          # get sorted indices (could use sort
  # if we didn't need to arrange image values too)
    sr  =  r.flat[ind]                # sorted radii
    sim = im.flat[ind]                # image values sorted by radii
    bins =  np.arange(binsz / 2., sr[-1], binsz)
    ri = np.digitize(sr, bins)
    nb = ri.max()+1
    prof = np.zeros(nb)
    for i in np.unique(ri):
        prof[i] = np.mean(sim[ri == i])
    return bins - binsz / 2., prof, sr, sim

def oldfastwrong():
    y, x = np.indices(im.shape, dtype=float) # first determine radii of all pixels
    r = np.sqrt(  (x-cx)**2
              + (y-cy)**2 )
    ind = np.argsort(r.flat)           # get sorted indices (could use sort
  # if we didn't need to arrange image values too)
    sr  =  r.flat[ind]                # sorted radii
    sim = im.flat[ind]                # image values sorted by radii
    ri = (sr/binsz).astype(int)       # integer part of radii (bin size = 1)

    deltar = ri[1:] - ri[:-1] # assume all radii represented (more work if not)
    rind = np.where(deltar)[0]         # location of changed radius
    nr = rind[1:] - rind[:-1]         # number in radius bin
    csim = np.cumsum(sim, dtype=float) # cumulative sum to figure out
  # sums for each radii bin
    tbin = csim[rind[1:]] - csim[rind[:-1]] # sum for image values in radius bins

    return tbin / nr, sr, sim
