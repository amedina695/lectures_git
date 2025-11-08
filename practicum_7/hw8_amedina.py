# %%
# Alex Medina
# AST5765
# HW 8
# 17 October 2025

##### IMPORTS

import os
import numpy as np
import astropy.io.fits as fits

from hw7_amedina import *


##### FROM PRACTICUM 5

def normmedcomb(arr, region=None):
    """
    Sky subtraction using normalized sky frame.

    Parameters
    ----------
    arr : 2D array
        Dark subtracted object frame
    region : optional tuple
        Region of array from which to normalize
        Of the form (( (y1, x1), (y2, x2) ))
    
    Returns
    -------
    Normalized sky frame and normalization factos
    """

    normal    = np.zeros(arr.shape)
    normalfac = np.zeros(len(arr))

    if region:
        ((y1, x1), (y2, x2)) = region
        for i in range(len(arr)):
            normalfac[i]    = np.median(arr[i, x1:x2, y1:y2])
            normal[i, :, :] = arr[i, :, :] / normalfac[i]
            if len(arr) == 0:
                normalfac    = np.median(arr[x1:x2, y1:y2])
                normal[:, :] = arr[:, :] / normalfac

    else:
        for i in range(len(arr)):
            max = np.max(arr[i, :, :])
            normal[i, :, :] = arr[i, :, :] / max

    normmed = np.median(normal, axis=0)

    return normmed, normalfac

# Region of interest
norm_region = ( (255, 255), (-255, -255))

# Output
objnorm, objfacs = normmedcomb(objarr, norm_region)

# Writing to a .FITS
fits.writeto('sky_13s_mednorm.fits', objnorm, overwrite=True)

# print(f'Normalization Factors: {objfacs} \n')

# print('Problem 1 \n')
# print('Completed. \n')

# print('Problem 2 \n')

# Sky subtraction # FIXED

def skycormednorm(objdata, normskydata, region=((None, None), (None, None))):
    """
    Sky subtraction using normalized sky frame.

    Parameters
    ----------
    o_arr : 2D array
        Dark subtracted object frame
    s_arr : 2D array
        Normalized sky frame
    region : optional tuple
        Region of array from which to normalize
        Of the form (( (y1, x1), (y2, x2) ))
    
    Returns
    -------
    Sky subtracted object frame
    """
    # Calculate normalization factors
    ((y1, x1), (y2, x2)) = region            # set corners
    retval = objdata.copy()                  # copy the data
    norm   = np.median(objdata[y1:y2,x1:x2]) # calculate the normalization
    retval -= norm * normskydata             # de-normalize sky and subtract
  
    return retval

# Apply sky subtraction fo all object frames

for i in np.arange(nobj):
    objarr[i] = skycormednorm(objarr[i], objnorm, norm_region) # FIXED

# Write the last resulting frame
savedata = np.float32(objarr[-1])  # will use twice, so compute only once
fits.writeto(objfile[-1]+'_nosky'+fext, savedata, objhead, overwrite=True, output_verify='silentfix')

print(f"{savedata[217, 184]}")