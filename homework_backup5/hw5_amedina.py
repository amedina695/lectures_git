# %%
# Alex Medina
# AST 5765
# Homework 5
# 20 September 2025

# %%
# General libraries
import numpy as np
import matplotlib.pyplot as plt

# %%
print('Problem 1 \n')

print('Completed. \n')

# %%
print('Problem 2 \n')

# %%
# For reproducibility
rng = np.random.default_rng(1)

# From practicum 3
data_ccd       = np.zeros(400) # Empty array with 400 elements
n_p            = 10000
# np.random.poisson but with rng for reproducibility
data_ccd[:396] = rng.poisson(n_p, 396) # First 396 elements from Poisson dist

low            = 0
high           = 1e6
data_ccd[396:] = rng.uniform(low, high, 4) # Last 4 elements from uniform dist
#print(data_ccd)

# Sigma clipping
mean0       = np.mean(data_ccd)
median0     = np.median(data_ccd)
std0        = np.std(data_ccd, ddof=0) # std of current data as limit
# ddof 0 for poisson distribution
max_std0    = 5 * std0 # Want a range of 5 sigma

# Limits
low_limit0  = median0 - max_std0
high_limit0 = median0 + max_std0

# Clipped array
clip1       = data_ccd[(low_limit0 < data_ccd) & (data_ccd < high_limit0)]

#print(len(clip1))
#print(clip1)

mean1       = np.mean(clip1)
median1     = np.median(clip1)
std1        = np.std(clip1, ddof=0)

print('Practicum 3 work copied, creating sub subsample. \n')

# %%
# Creating a sub subsample

max_std1    = 5 * std1
low_limit1  = median1 - max_std1
high_limit1 = median1 + max_std1

# Clipped array 2
clip2       = clip1[(low_limit1 < clip1) & (clip1 < high_limit1)]

# Stats for sub sample
mean2       = np.mean(clip2)
median2     = np.median(clip2)
std2        = np.std(clip2, ddof=0)

# Expected std from possion is sqrt of mean
expected_std = np.sqrt(mean2)

print("Sub-subsample mean:", mean2)
print("Sub-subsample median:", median2)
print("Sub-subsample standard deviation:", std2)
print("Sub-subsample expected std (Poisson):", expected_std,"\n")

# %%
print("""
The final mean and median are very similar, within a few
digits of each other.

The expected standard deviation of a Poisson distribution is 
the square root of its mean, so the expected value we get is 
about 100 while the final standard deviation is also within
a few digits. 

This method won't ALWAYS get remove every bad pixel because
there could be outliers that are onlt slightly off from but still
are outliers. Also, this method assumes that the data is somewhat
normally distributed because we are using the standard deviation
to remove the oultiers. \n
""")

# %%
print('Problem 3 \n')

# %%
def sigrej(x, limits, mask=None):
    """
    Sigma clipping algorithm to remove bad pixels.

    Parameters
    ----------
    x : array_like
        Data.
    limits : float
        Threshold to reject pixels.
    mask : array_like of bool but optional
        Initial good pixel mask.
    
    Returns
    -------
    good_mask : ndarray of bool
        Modified boolean mask

    """
    x = np.asarray(x) # Converts input to array

    # Boolean mask
    if mask is None:
        # No mask means all good pixels
        good_mask = np.ones_like(x, dtype=bool)
    else:
        # Mask has same shape as data
        if mask.shape != x.shape:
            raise ValueError("Mask must have same shape as data.")
        good_mask = np.asarray(mask, dtype=bool)
    
    # Return modified boolean mask
    for N in limits:
        # Same as above
        xg = x[good_mask]
        mean = np.mean(xg)
        median = np.median(xg)
        std = np.std(xg)

        low_limit, high_limit = median - N * std, median + N * std

        #Update mask
        good_mask &= (x >= low_limit) & (x <= high_limit)

    return good_mask

print("Function created. \n")

# %%
# Running test on data_ccd

test_mask = sigrej(data_ccd, (5.0, 5.0))
cleaned_data = data_ccd[test_mask]
#print(len(cleaned_data))

mean3 = np.mean(cleaned_data)
median3 = np.median(cleaned_data)
std3 = np.std(cleaned_data, ddof=0)

print("Clean data mean:", mean3)
print("Clean data median:", median3)
print("Clean data standard deviation:", std3)
print("Hard code from problem 2 and function produce same results. \n")


