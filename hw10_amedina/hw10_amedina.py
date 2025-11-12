# %%
# Alex Medina
# AST 5765
# Homework 8
# 8 November 2025

###### IMPORTS

import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import gaussian as g
import disk as d
from hw9_amedina import *


##### PRACTICUM ( Karalidi work)

def apphot( image, mask, photrad, skyin, skyout, center ):
    """Function that does aperture photometry on an image provided.
    In: 
    - 2D image that we want to do the photometry on
    - mask for bad pixels
    - radius for aperture photometry
    - inner radius of sky annulus
    - outer radius of sky annulus
    - tuple with center coordinates of star
    
    Out:
     tuple with stellar flux and average sky (per pixel) values
    """
    # a) cut out image around star, center at star
    nx = int( 2*skyout +1 )
    ny = nx 
    
    #get the coordinates in the original image:
    y1 = int( np.max( [0, np.floor( center[ 0 ] - ny /2 )] ))
    x1 = int( np.max( [0, np.floor( center[ 1 ] - nx /2 )] ))
    y2 = int( np.max( [image.shape[0], np.floor( center[ 0 ] + ny /2 )] ))
    x2 = int( np.max( [image.shape[1], np.floor( center[ 1 ] + nx /2 )] ))
    
    subimage   = image[ y1: y2, x1:x2 ].copy()
    maskcut    = mask[ y1: y2, x1:x2 ].copy()
    
    # Udate my central coordinates
    cutcenter = ( center[0] - y1, center[1] -x1 )
    shape = subimage.shape
    
    # b) mask of the sky annulus
    skymask = d.disk( skyout, cutcenter, shape)^d.disk( skyin, cutcenter, shape ) #*maskcut 
    
    # c) average of sky
    skyavg = np.sum( skymask * subimage ) / np.sum( skymask )
    
    # d) subtract average sky from subimage, e) mask for the aperture
    # f) total flux
    apmask = d.disk( photrad, cutcenter, shape )
    flux = np.sum( apmask * subimage ) - skyavg * np.sum( apmask )
    
    return (flux, skyavg)

print('Problem 2 \n')

def dophot(table, objframes, mask, photrad, skyin, skyout):
    """
    Parameters
    ----------
    table : array
        Photometery table with [yguess, xguess, width, cy, cx, star, sky]
    objframes : array
        Star frames
    mask : array
        Good/bad pixel mask
    photrad : 
        Aperture radius
    skyin : 
        Inner annulus radius
    skyout : 
        Outer sky annulus radius
    Returns
    -------
    array
        Updated table that adds flux and skyavg values
    """
    nstars, nframes = table.shape[:2]

    for i in range(nstars):
        for j in range(nframes):
            cy = table[i, j, 3]
            cx = table[i, j, 4]

            flux, skyavg = apphot(objframes[j], mask, photrad, skyin, skyout, (cy, cx))
            # STAR and SKY are the last two columns in phot array
            table[i, j, 5] = flux
            table[i, j, 6] = skyavg
    
    return table

# Write flattened ASCII table

# Running
mask_shape = objarr[0].shape
im_mask    = np.ones(mask_shape, dtype=bool )

photometry = dophot(photometry, objarr, im_mask, aperture_rad, annulus_in, annulus_out)

# Printing and saving to ASCII text file
nstars, nframes = photometry.shape[:2]
with open('hw10_amedina_result.txt', 'w') as f:
    f.write('star frame  yguess    xguess    width    cy      cx   star    sky\n')
    f.write('-----------------------------------------------------------------\n')
    for i in range(nstars):
        for j in range(nframes):
            yguess, xguess, width, cy, cx, star, sky = photometry[i, j, :7]
            f.write(f'{i} {j} {yguess} {xguess} {width:.3f}'
                    f'{cy:.3f} {cx:.3f} {star:12.5e}  {sky:10.5e} \n')
