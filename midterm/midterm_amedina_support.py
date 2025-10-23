##### MEDINA Support

# General libraries
import numpy as np
import matplotlib.pyplot as plt

def gaussian(N, mean, std, binwidth):

    bc_index = []
    g_values = []
    # Evaluating Gaussian at bin center
    for i in range(0, 101):

        bin_center = (1/2) * (i + (i+1))
        g = ( 1.0 / (std * np.sqrt( 2 * np.pi )) ) * np.exp( - (bin_center - mean)**2  / ( 2 * std**2 ) )
        expected_draws = N * g * binwidth

        bc_index.append(bin_center)
        g_values.append(expected_draws)

    return g_values, bc_index