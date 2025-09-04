# %%
# Alex Medina
# AST 5765
# Homework 3

# %%
# General libraries
import numpy as np
import matplotlib.pyplot as plt
import hw3_amedina_supportfunc as sup

# %%
print('Problem 2 \n')

# %%
print('2h)')

test_square_1 = np.arange(0, 10) #test array from 0 to 9
print("Test array:",test_square_1, '\n')

test1 = sup.square(test_square_1)
print("Square method result:",test1, '\n')

# %%
print('2i)')

test_square_2 = np.arange(0, 25, dtype=float).reshape(5, 5) #test array from 0 to 9
print("Test 5x5:",test_square_2, '\n')

test2 = sup.square(test_square_2)
print("Square method result:",test2, '\n')

# %%
print('Problem 3 \n')

# %%
# I need numbers 1, 2, 4, 5.5, 7

a = 1
b = 7
n = 5 # 5 evenly spaced numbers
name = "hw3_amedina_q3_plot"

sup.squareplot(a, b, n, name)


