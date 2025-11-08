# %%
# Alex Medina
# AST5765
# Homework 7
# 9 October 2025

##### IMPORTS

import os
import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits

##### FROM PRACTICUM

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

objarr  = np.zeros( (nobj,  ny, nx) )
darkarr = np.zeros( (ndark, ny, nx) )

##### Populating data cubes

for i in range(nobj):

    star_file = datadir + objfile[i] + fext

    if i < nobj - 1:
        objarr[i, :, :] = fits.getdata(star_file)
    else:
        objarr[i, :, :], objhead = fits.getdata( star_file, header= True )

for i in range(ndark):

    dark_file = datadir + darkfile[i] + fext

    if i < ndark - 1:
        darkarr[i, :, :] = fits.getdata(dark_file)
    else:
        darkarr[i, :, :], darkhead = fits.getdata( dark_file, header= True )


# print('Problem 2a and 2b \n')

# Median combine the image using np.median(arr, axis=axis)
darkmed = np.median(darkarr, axis=0)

# Calling to print pixel index [217, 184] of your darkmed
# print(f"Pixel index [217, 184] of dark image is {darkmed[217, 187]}. \n")

# print('Problem 2c \n')

# Writing the median to header histort
darkhead.add_history('The image is a median combination dark frame.')
# print('History added. \n')

# print('Problem 2d \n')

# Saving as a fits with the new header using writeto

outname = darkfile[ 0 ][:-1]                                # FIXED
fits.writeto(outname+'med'+fext,
             np.float32(darkmed), darkhead, overwrite=True) # FIXED 

# print('New .fits created and added with header. \n')

print('Problem 2e \n')

# Subtract median combined image from each objarr frame
objarr -= darkmed

print(f"Pixel index [217, 184] of first obj frame: {objarr[0, 217, 184]}.")

# Write first frame to save
fits.writeto('hw7_myname_prob2_graph1'+fext,
             np.float32(objarr[0]), objhead, overwrite=True )

# Pixel values before and after subtraction
print(f"Pixel index [217, 184] of first obj frame after: {objarr[0, 217, 184]}. \n")

##### RUBRIC

print(
"""
RUBRIC

QUESTION 1:
5pts: Correct naming structure
0pts: Incorrect naming structure

QUESTION 2:
a)
4pts: Calling single line with function
2pts: Just a function but multiple lines; single line but no function
0pts: Neither a single line and no function
b)
5pts: Call function with dark data and print out pixel values.
2.5pts: Only calling function.
0pts: Neither calling function to dark data nor printing out pixel values.
c)
4pts: Adding to the header history correctly, and adding relevant information.
2pts: Calling header but no information added.
0pts: Neither calling header nor adding information.
d)
5pts: Writing median dark to a correctly named file AND adding header to it.
2.5pts: Only writing median dark, or done correctly but wrong name.
0pts: Neither writing median dark nor adding header to it.
e)
12pts: Subtracting median combined image, writing correct file name, and printing pixel values.
8pts: Only doing 2 out of 3 parts of the problem and/or wrong steps.
4pts: Only doing 1 out of 3 parts of the problem and/or wrong steps.
0pts: Not completing problem or completely wrong.

QUESTION 3:
10pts: Writing a detailed rubric that covers points for all questions and parts.
5pts: Writing a rubric but not assigning points or lacking detail.
0pts: Not completing a rubric.

QUESTION 4:
5pts: Explain in log that code works on Stokes.
0pts: No indication of working on Stokes.
"""
)
