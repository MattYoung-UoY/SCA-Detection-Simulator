"""Licensed under the MIT License.
Full license can be found in the "LICENSE" file in the repository root directory.

Copyright (c) 2024 Matt Young

Used to generate Fig.3 from arxiv.2305.18006

Processes the results that are saved to file by detection_time_sims.py
"""

import ast
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import linregress

from matplotlib.transforms import ScaledTranslation

""" Calculates the root mean squared error of the datapoints against a given linear function
"""
def rmse(lin_reg_coeff, x, y):
    error = math.sqrt(sum([(y - (lin_reg_coeff[1] + (x * lin_reg_coeff[0])))**2 for x, y in zip(x, y)])/len(y))
    return error

# Reads the lines from file and stores them in a list
lines = []

with open("results.txt") as file:
    lines = [line.rstrip() for line in file]

# Reads the corresponding lists from file
# literal_eval takes the string representation of the list, and converts that to the corresponding list
num_samples = [n for n in ast.literal_eval(lines[3])]
mean_det_pos = [n for n in ast.literal_eval(lines[4])]
std_devs = [n for n in ast.literal_eval(lines[5])]

# Here we calculate a regression model for the std_dev
# As the relationship for the std_dev is a sqrt relationship, we square the std_dev values, and then perform a linear regression
# To obtain the square root relationship, we apply a square root to the entire linear function produced by the linear regression
std_devs_squared = [x*x for x in std_devs]
std_dev_sqr_lin_reg = linregress(num_samples, std_devs_squared)
print(std_dev_sqr_lin_reg)
std_dev_reg = [(std_dev_sqr_lin_reg[1] + (std_dev_sqr_lin_reg[0] * x)) for x in num_samples]
std_dev_reg = [-(math.sqrt(abs(x))) if x<0 else math.sqrt(x) for x in std_dev_reg]
# Calculating the RMSE for the std_dev regression model
std_dev_reg_err = math.sqrt(sum([(x-y)**2 for x, y in zip(std_dev_reg, std_devs)])/len(std_dev_reg))
print("STD_DEV RMSE: " + str(std_dev_reg_err))

# Calculating a linear regression model for the mean
mean_det_pos_lin_reg = linregress(num_samples, mean_det_pos)
# Using the linear regression model to caluclate the points to plot for the linear function
mean_det_pos_reg = [(mean_det_pos_lin_reg[1] + (mean_det_pos_lin_reg[0] * x)) for x in num_samples]
# Calculating the RMSE of the linear regression model
mean_det_pos_reg_err = math.sqrt(sum([(x-y)**2 for x, y in zip(mean_det_pos_reg, mean_det_pos)])/len(mean_det_pos_reg))
print("MEAN_DET_POS RMSE: " + str(mean_det_pos_reg_err))

# Specifies the subplot layout
fig, axs = plt.subplot_mosaic([['a)'], ['b)']],
                              layout='constrained')

# Creates the subplot labels
for label, ax in axs.items():
    ax.text(
        0.0, 1.0, label, transform=(
            ax.transAxes + ScaledTranslation(-20/72, +7/72, fig.dpi_scale_trans)),
        fontsize='medium', va='bottom', fontfamily='serif',
        bbox=dict(facecolor='0.8', edgecolor='none', pad=3.0))

# Plots the mean and the linear regression model
plt.subplot(2, 1, 1)
plt.scatter(num_samples, mean_det_pos, marker='x', color='orange')
plt.plot(num_samples, mean_det_pos_reg, linestyle='dashed', color='blue')
plt.xlabel("sliding window size")
plt.xticks([10, 10000, 20000, 30000, 40000, 50000])
plt.ylabel("mean fault detection position (bits)")
plt.grid()

# Plots the standard deviation and the regression model
plt.subplot(2, 1, 2)
plt.scatter(num_samples, std_devs, marker='x', color='orange')
plt.plot(num_samples, std_dev_reg, linestyle='dashed', color='blue')
plt.xlabel("sliding window size")
plt.xticks([10, 10000, 20000, 30000, 40000, 50000])
plt.ylabel("standard deviation (bits)")
plt.grid()

plt.show()