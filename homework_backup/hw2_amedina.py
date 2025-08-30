# %%
# Alex Medina
# AST 5765
# Homework 2

# %%
# General libraries
import numpy as np
import matplotlib.pyplot as plt

# %%
print('Problem 2: \n')

# %%
# a1

x = np.arange(0, 1001) # Array of x integers from 0 to 1000
print("Because 1 to 1000 is 1000 numbers, but we need the 0, we need 1001 elements")

# print(len(x)) # To check number of elements

# %%
# a2

print("Type:",type(x)) # Printing the datatype using the type
print("Max:",np.max(x)) # Max and min of array using np commands
print("Min:",np.min(x))

# %%
# b1

# Only intuitive way I think is by normalization

x = (x/1000) * (2 * np.pi) # x/1000 will normalize to 0 to 1

# print(len(x)) # Verifying still same elements

# %%
# b2

print("Max:",np.max(x))
print("Min:",np.min(x))

# %%
# c

y = np.sin(x) # Array with values of sin(x)

# print(type(y))
# print(len(y))

# %%
# d

print(y[234]) # Element 234 of y
print("""
      Element 234 in y is not the 234th element because with python
      the first element is 0, second element is element 1
      so the 234th element is element 233 and element 234 is
      the 235th element in the y array""")

# %%
print('Problem 3: \n')

# %%
# a

plt.figure()
plt.plot(x, y)
plt.title("Graph of y = sin(x)")
plt.xlabel("x")
plt.ylabel("y")

# b

# https://www.geeksforgeeks.org/data-visualization/exporting-plots-to-pdf-matplotlib/

plt.savefig('sine_graph.png', format="png") #Saves in directory with script
plt.show()


# %%
print('Problem 4: \n')

# %%
# a1

numb_r = round((1 * 2) / 0.02 + 1) # Denominator is step size
# print(numb_r)

# r_test = np.arange(-1, 1.02, 0.02)
# print(len(r_test))
# print(r_test)

# Alternative (my preference)

r = np.zeros(101) # Empty array of 101 elements
i = np.arange(numb_r) # Array with values from 0 to 100
r = -1 + i * 0.02 # Populating r with values from -1 to 1
# print(len(r))
# print(np.min(r))
# print(np.max(r))


# %%
# a2

# r_mid = np.where((r >= -0.5) & (r <= 0.5))
# r_beg = np.zeros(25)
# r_beg = r_beg + -0.5
# r_end = np.zeros(25)
# r_end = r_end + 0.5
# r_final = np.concatenate((r_beg, r[r_mid], r_end))

# https://numpy.org/doc/2.1/reference/generated/numpy.clip.html 

r_clip = np.clip(r, -0.5, 0.5) # Clipping values below -0.5

# print(r_clip)

# %%
# b1

r_x = np.arange(101) # For x axis

plt.figure()
plt.plot(r_x, r)
plt.plot(r_x, r_clip, color='orange')
plt.title("Clipped Ramp")
plt.xlabel("x")
plt.ylabel("y")

# b2
plt.savefig('clipped_ramp.pdf', format="pdf") #Saves in directory with script
plt.show()

# %%
print('Problem 5: \n')

# %%
print("""
      The first python package that I found is called Astronomica.
      The use is similar to astropy, where is analyzes and visualizes
      astronomical data. However, on reddit, I see that some find
      it easier for calculating simple things like planet mean
      anomaly, even something useful like converting between julia
      and gregorian dates. The first example in the intro is actually
      a calculation of coordinates, so it seems to be a very general
      purpose package for performing calculations of astro data.

      The second package that I found is more of a niche type of 
      package called Skyfield. It is used to calculate the positions
      of stars and planets, and even satellites. It can be used in
      conjuction with astropy to return in astropy units but default
      is that it agrees with units from US Naval Observatory.
""")


