import ast
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import linregress

from matplotlib.transforms import ScaledTranslation

def rmse(lin_reg_coeff, x, y):
    error = math.sqrt(sum([(y - (lin_reg_coeff[1] + (x * lin_reg_coeff[0])))**2 for x, y in zip(x, y)])/len(y))
    return error

lines = []

with open("results.txt") as file:
    lines = [line.rstrip() for line in file]

num_samples = [n for n in ast.literal_eval(lines[3])]
mean_det_pos = [n for n in ast.literal_eval(lines[4])]
std_devs = [n for n in ast.literal_eval(lines[5])]

std_devs_squared = [x*x for x in std_devs]

mean_det_pos_lin_reg = linregress(num_samples, mean_det_pos)
std_dev_sqr_lin_reg = linregress(num_samples, std_devs_squared)
print(std_dev_sqr_lin_reg)

mean_det_pos_reg = [(mean_det_pos_lin_reg[1] + (mean_det_pos_lin_reg[0] * x)) for x in num_samples]
mean_det_pos_reg_err = math.sqrt(sum([(x-y)**2 for x, y in zip(mean_det_pos_reg, mean_det_pos)])/len(mean_det_pos_reg))
print("MEAN_DET_POS RMSE: " + str(mean_det_pos_reg_err))


fig, axs = plt.subplot_mosaic([['a)'], ['b)']],
                              layout='constrained')

for label, ax in axs.items():
    ax.text(
        0.0, 1.0, label, transform=(
            ax.transAxes + ScaledTranslation(-20/72, +7/72, fig.dpi_scale_trans)),
        fontsize='medium', va='bottom', fontfamily='serif',
        bbox=dict(facecolor='0.8', edgecolor='none', pad=3.0))

plt.subplot(2, 1, 1)
plt.scatter(num_samples, mean_det_pos, marker='x', color='orange')
plt.plot(num_samples, mean_det_pos_reg, linestyle='dashed', color='blue')
plt.xlabel("sliding window size")
plt.ylabel("average attack detection position (bits)")
plt.grid()

std_dev_reg = [(std_dev_sqr_lin_reg[1] + (std_dev_sqr_lin_reg[0] * x)) for x in num_samples]
std_dev_reg = [-(math.sqrt(abs(x))) if x<0 else math.sqrt(x) for x in std_dev_reg]

std_dev_reg_err = math.sqrt(sum([(x-y)**2 for x, y in zip(std_dev_reg, std_devs)])/len(std_dev_reg))
print("STD_DEV RMSE: " + str(std_dev_reg_err))

plt.subplot(2, 1, 2)
plt.scatter(num_samples, std_devs, marker='x', color='orange')
plt.plot(num_samples, std_dev_reg, linestyle='dashed', color='blue')
plt.xlabel("sliding window size")
plt.ylabel("standard deviation (bits)")
plt.grid()

plt.show()