# %%
# Alex Medina
# AST5765
# HW 8
# 17 October 2025

##### IMPORTS

import os
import numpy as np
import astropy.io.fits as fits

##### FROM HW7/PRACTICUM

datadir = "hw7_data/"
fext    = ".fits"

objfile  = []
darkfile = []

for filename in os.listdir(datadir):
    if filename.startswith('stars_13s_'):
        file = filename.split(fext)[0]
        objfile.append(file)
    elif filename.startswith('dark_13s_'):
        file = filename.split(fext)[0]
        darkfile.append(file)

objfile, darkfile = sorted(objfile), sorted(darkfile)

# Choosing a random indice from the list
randf  = objfile[int(np.random.uniform(0, len(objfile)))]
file   = fits.getdata(datadir + randf + fext)
nx, ny = file.shape

nobj, ndark = len(objfile), len(darkfile)

objarr  = np.zeros( (nobj, ny, nx))
darkarr = np.zeros( (ndark, ny, nx))

for i in range(nobj):
    if i < nobj - 1:
        objarr[i, :, :] = fits.getdata(datadir + objfile[i] + fext)
    else:
        objarr[i, :, :], objhead = fits.getdata(datadir + objfile[i] + fext, header=True)

for i in range(ndark):
    if i < ndark - 1:
        darkarr[i, :, :] = fits.getdata(datadir + darkfile[i] + fext)
    else:
        darkarr[i, :, :], darkhead = fits.getdata(datadir + darkfile[i] + fext, header=True)

# Median combine
darkmed = np.median(darkarr, axis=0)

# darkhead.add_history('The image is a median combination dark frame.')
# fits.writeto('dark_13s_med.fits', darkmed, header=darkhead, overwrite=True)

# Subtract median combined image from each objarr frame
obj_sub_dark = objarr - darkmed

# fits.writeto('hw7_amedina_prob2_graph1.fits', obj_sub_dark[0], overwrite=True)

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
    else:
        for i in range(len(arr)):
            max = np.max(arr[i, :, :])
            normal[i, :, :] = arr[i, :, :] / max

    normmed = np.median(normal, axis=0)

    return normmed, normalfac

# Region of interest
prob4tuple = ( (255, 255), (-255, -255))

# Output
objnorm, objfacs = normmedcomb(obj_sub_dark, prob4tuple)

# Writing to a .FITS
fits.writeto('sky_13s_mednorm.fits', objnorm, overwrite=True)

print(f'Normalization Factors: {objfacs} \n')

print('Problem 1 \n')
print('Completed. \n')

print('Problem 2 \n')

# Sky subtraction

def skycormednorm(o_arr, s_arr, region=None):
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
    if region:
        ((y1, x1), (y2, x2)) = region
        norm_fac = np.median(o_arr[x1:x2, y1:y2])
    else:
        norm_fac = np.median(o_arr[:, :])
    
    # Denormalize
    denormsky = s_arr * norm_fac

    # Subtract denormalized sky from object
    return o_arr - denormsky

# Apply sky subtraction fo all object frames

obj_sub_sky = np.zeros(obj_sub_dark.shape)

for i in range(len(obj_sub_dark)):
    obj_sub_sky[i, :, :] = skycormednorm(obj_sub_dark[i, :, :], objnorm)

# Write the last resulting frame
fits.writeto('stars_13s_9_nosky.fits', obj_sub_sky[-1, :, :], overwrite=True)

# Print
print(f'Pixel Value of object array subtracted by sky: {obj_sub_sky[-1, 217, 184]}')
