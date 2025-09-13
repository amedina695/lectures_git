# %%
# Alex Medina
# AST 5765
# Homework 4
# September 11, 2025

# %%
# General libraries
import numpy as np
import matplotlib.pyplot as plt

# %%
print('Problem 2a \n')

# %%
N      = 10000 # Number of samples
sigma  = 13    # Standard deviation
mean   = 55    # Mean

# Creating a sample that is normally distributed
sample = np.random.normal(mean, sigma, N)

print('Created a sample that is normally distributed \n')


# %%
print('Problem 2b \n')

# %%
# According to the numpy method page
# Standard format for histrogram plot

# Plot
plt.figure()

# Bins from 0 to 1
# And each bin is width of 1
n_bins = range(0, 101)
count, bins, width = plt.hist(sample, bins=n_bins, rwidth=1)

plt.title("Histogram")
plt.xlabel("Amount")
plt.ylabel("Counts")

plt.savefig('hw4_amedina_histograph.png', format="png") #Saves in directory
plt.show()
print("Histogram created and saved as .png. \n")


# %%
print('Problem 2c \n')

# %%
# Gaussian for overplot

def gaussian(mean, std, bins):

    bc_index = []
    g_values = []
    # Evaluating Gaussian at bin center
    for i in range(0, 101):

        bin_center = (1/2) * (i + (i+1))
        g = ( 1.0 / (std * np.sqrt( 2 * np.pi )) ) * np.exp( - (bin_center - mean)**2  / ( 2 * std**2 ) )
        expected_draws = N * g

        bc_index.append(bin_center)
        g_values.append(expected_draws)

    return g_values, bc_index

print('Created Gaussian method to overplot. \n')

# %%
# Overplotting

gplot_values, bc_values = gaussian(mean, sigma, n_bins)

plt.figure()

count, bins, width = plt.hist(sample, bins=n_bins, rwidth=1)
plt.plot(bc_values, gplot_values, lw=2)

plt.title("Histogram with Overplot")
plt.xlabel("Amount")
plt.ylabel("Counts")
plt.savefig('hw4_amedina_histograph_o.png', format="png") #Saves in directory
plt.show()
print("Histogram with overplot created and saved as .png. \n")

# %%
print('Problem 3 (AST5765) submitted as a .pdf. \n')


