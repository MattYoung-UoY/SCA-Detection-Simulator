"""Licensed under the MIT License.
Full license can be found in the "LICENSE" file in the repository root directory.

Copyright (c) 2024 Matt Young

Used to generate Fig.2 from *insert paper DOI*

A simple proof of concept simulation of one instance of a state-blocking side-channel attack against a QKD system.
"""

from utils.datasetGenerator import *
from utils.distributions import *
from utils.bounds import *
from utils.convolutions import *

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.transforms import ScaledTranslation

# Estimate to be within 5% of the actual value
delta_p = 0.05
# Certainty of 99.9%
epsilon = 0.001

window_size = chernoff_hoeffding_bound(delta_p, epsilon)
print(window_size)

# Using the probability distributions from utils.distributions, specifies the pattern of probability distributions to draw key bits from, and how many bits to draw from each distribution
# Uses a uniform distribution for 2 window widths which represents nominal behaviour
# Followed by a probability distribution of mean=1/3 for 2 window widths which represents an ongoing attack
key_bit_dist_pattern = [
    (uniform_dist, int(window_size*2)),
    (lower_third, int(window_size*2))
    ]

# Generates random key bits using the specified distribution pattern
dataset = generate_dataset(key_bit_dist_pattern)

mean_est = est_mean(dataset[1], window_size)

# Finds the location of the first detection
first_detection = 0
for i in range(len(mean_est)):
    # If difference between estimate of mean and nominal value (0.5) is greater than delta_p then detected an attack
    if abs(mean_est[i] - 0.5) >= delta_p:
        first_detection = i
        break
# Converting detection location to be in terms of window widths
first_detection /= window_size
# Corrects for the fact that the mean_est vals start 1 window width late due to having to wait for window_size number of bits to be sent first
first_detection += 1
print(first_detection)

# Pads the mean_est values ready for plotting
mean_est = ([None]*window_size) + mean_est

# Gets the bit locations in terms of window widths to use for x-axis values
total_samples = len(mean_est)
x_vals = [(x/window_size) for x in range(0, total_samples)]

# Specifies the subplot layout
fig, axs = plt.subplot_mosaic([['a)'], 
                               ['b)']],
                              layout='constrained')

# Creates the subplot labels
for label, ax in axs.items():
    ax.text(
        0.0, 1.0, label, transform=(
            ax.transAxes + ScaledTranslation(-20/72, +7/72, fig.dpi_scale_trans)),
        fontsize='medium', va='bottom', fontfamily='serif',
        bbox=dict(facecolor='0.8', edgecolor='none', pad=3.0))

# Creates subplot a.)
plt.subplot(2, 1, 1)
plt.xlabel("Key-bit Position (Relative to Window Size)")
plt.ylabel("Distribution Mean")
plt.plot(x_vals, dataset[0])
x_ticks = plt.xticks()[0]
plt.grid()

# Creates subplot b.)
plt.subplot(2, 1, 2)
plt.xlabel("Sliding Window End Position (Relative to Window Size)")
plt.ylabel("Sample Mean")
plt.plot(x_vals, mean_est)
# The nominal mean dashed blue line
plt.plot([1, (total_samples/window_size)], [0.5, 0.5], linestyle='dashed', color='blue')
# The detection threshold dashed red lines
plt.plot([1, (total_samples/window_size)], [0.5+delta_p, 0.5+delta_p], linestyle='dashed', color='red')
plt.plot([1, (total_samples/window_size)], [0.5-delta_p, 0.5-delta_p], linestyle='dashed', color='red')
# The start of attack and first detection orange dashed lines respectively
plt.plot([2, 2], [0.5-delta_p, min(mean_est[window_size:])-0.025], linestyle='dashed', color='orange')
plt.plot([first_detection, first_detection], [0.5-delta_p, min(mean_est[window_size:])-0.025], linestyle='dashed', color='orange')
# Plots a point far over on the left to force matplotlib to show the empty region on the left of the plot
plt.plot([0.01], [0.49])
plt.grid()

plt.show()