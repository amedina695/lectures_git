# %%
# Alex Medina
# AST 5765
# Homework 8
# 31 October 2025

# Imports

import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import gaussian as g
from hw8_amedina import *

print('Problem 2 \n')

# Dividing by flat

flatcalc = fits.getdata('flat.fits')

objarr /= flatcalc

# Getting the images
# Already cleaned

for i in range(3):
    qm = np.median(objarr[i])
    qs = np.std(objarr[i])
    plt.figure( figsize = (6, 6 ))
    im = plt.imshow(objarr[i], cmap='grey', vmin=qm-0.1*qs, vmax=qm+2.0*qs)
    plt.title(objfile[i])
    plt.colorbar(im, fraction=0.045, pad=0.01)

# STARTING by eyeballing the alues

# Stellar photometry: 
photometry = np.array( [ # yguess, xguess, width, cy, cx, star, sky 
# star 0 
[ [ 698, 512, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 0
[464, 517, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 1
[228, 521, np.nan, np.nan, np.nan, np.nan, np.nan] ], # frame 2
# star 1 
[ [ 668, 520, np.nan, np.nan, np.nan, np.nan, np.nan],     # frame 0 
[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], # frame 1 
[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan] ] , # frame 2 
# star 2 
[ [ 568, 283, np.nan, np.nan, np.nan, np.nan, np.nan],           
# frame 0 
[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 1 
[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]  # frame 2 
], dtype=float) 

# Calculating offset
# Columns are [yguess, xguess, width, cy, cx, star, sky]
offset10 = photometry[0, 1, 0:2] - photometry[0, 0, 0:2]
offset20 = photometry[0, 2, 0:2] - photometry[0, 0, 0:2]

print(f'Offset in y and x for frame 0 to 1: {offset10}')
print(f'Offset in y and x for frame 0 to 2: {offset20}')

# Applying offsets to stars 1 and 2 based on frame 0
nstars, nframes = photometry.shape[:2]
for i in range(1, nstars):      # stars 1 and 2
    photometry[i, 1, 0:2] = photometry[i, 0, 0:2] + offset10
    photometry[i, 2, 0:2] = photometry[i, 0, 0:2] + offset20

print(photometry)

print('Problem 3a \n')

# FIT

def fitstars(o_arr, table, subz=15):
    nstars, nframes = table.shape[:2]

    for i in range(nstars):
        for j in range(nframes):

            yguess, xguess = int(table[i, j, 0]), int(table[i, j, 1])

            # Creating subarr that's a copy
            ytop = yguess+subz+1
            ybot = yguess-subz
            xtop = xguess+subz+1
            xbot = xguess-subz

            sub = o_arr[j, ybot:ytop, xbot:xtop].copy()
            sub -= np.median(sub) # subtract median
            
            # Fitting relative to subarr (width tuple) (center tuple) (height)
            guess = ((2.0, 2.0), (yguess - ybot, xguess - xbot), np.max(sub))

            # Fit on the subimage - onlt width and center
            fw, fc, fh, fe = g.fitgaussian(sub, guess=guess)

            # Average of the two widths
            sigma_avg = float((fw[0] + fw[1]) / 2.0)

            # Fitting back to original coords
            cy, cx = float(fc[0] + ybot), float(fc[1] + xbot)

            # Write results into the table
            table[i, j, 2] = sigma_avg
            table[i, j, 3] = cy
            table[i, j, 4] = cx

    return table

# Fits 9 positions
photometry = fitstars(objarr, photometry)

# Table
print('star frame  yguess    xguess    width    cy      cx  ')
print('-----------------------------------------------------------------')
nstars, nframes = photometry.shape[:2]
for i in range(nstars):
    for j in range(nframes):
        yg, xg = photometry[i, j, 0], photometry[i, j, 1]
        width  = photometry[i, j, 2]
        cy     = photometry[i, j, 3]
        cx     = photometry[i, j, 4]
        print(f"{i}     {j}     {yg}     {xg}     {width:.3f}      {cy:.3f}      {cx:.3f}")


print('Problem 3a \n')

# Average the fitted widths from all widths
allsigma = np.mean(photometry[..., 2])

# Photometry
aperture_rad  = 3.0 * allsigma           # Since Gaussian, 3 std should get 99% of the data
annulus_in    = 5.0 * allsigma  # At least 1 std away from aperture
annulus_out   = 8.0 * allsigma  # A few std away from inside ring

subimage_size = (annulus_out + 1) * 2 + 1  # FIX
