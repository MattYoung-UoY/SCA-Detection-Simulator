from sim.datasetGenerator import *
from sim.distributions import *
from sim.tests import *
from sim.utils import *
from sim.convolutions import *

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.transforms import ScaledTranslation

# Within 5% of the actual value
delta_p = 0.05
# Certainty of 99.9%
epsilon = 0.001

# Looking at the produced values for the estimated mean at face value, this bound seems to be overly restrictive
num_samples = chernoff_hoeffding_bound(delta_p, epsilon)
print(num_samples)

prob_dist_pattern = [
    # (const_0, 5), 
    # (const_1, 5), 
    (uniform_dist, int(num_samples*2)),
    (lower_third, int(num_samples*2))
    ]

dataset = generate_dataset(prob_dist_pattern);

# TODO
# Collect a list of est_mean values and post-process on that list, and can also plot it
# Test detection time
# Test proportion of key discarded upon detection

est_mean = est_mean(dataset[1], num_samples)

first_detection = 0
for i in range(len(est_mean)):
    if abs(est_mean[i] - 0.5) >= delta_p:
        first_detection = i
        break
first_detection /= num_samples
first_detection += 1

est_mean = ([None]*num_samples) + est_mean
total_samples = len(est_mean)
rel_x_vals_est_mean = [(x/num_samples) for x in range(0, total_samples)]

rel_x_vals_samples = [x/num_samples for x in range(0, total_samples)]

fig, axs = plt.subplot_mosaic([['a)'], ['b)']],
                              layout='constrained')
    
for label, ax in axs.items():
    ax.text(
        0.0, 1.0, label, transform=(
            ax.transAxes + ScaledTranslation(-20/72, +7/72, fig.dpi_scale_trans)),
        fontsize='medium', va='bottom', fontfamily='serif',
        bbox=dict(facecolor='0.8', edgecolor='none', pad=3.0))

plt.subplot(2, 1, 1)
plt.xlabel("Key-bit Position (Relative to Window Size)")
plt.ylabel("Distribution Mean")
plt.plot(rel_x_vals_samples, dataset[0])
x_ticks = plt.xticks()[0]
print()
plt.grid()

plt.subplot(2, 1, 2)
plt.xlabel("Sliding Window End Position (Relative to Window Size)")
plt.ylabel("Sample Mean")
plt.plot(rel_x_vals_est_mean, est_mean)
plt.plot([1, (total_samples/num_samples)], [0.5, 0.5], linestyle='dashed', color='blue')
plt.plot([1, (total_samples/num_samples)], [0.5+delta_p, 0.5+delta_p], linestyle='dashed', color='red')
plt.plot([1, (total_samples/num_samples)], [0.5-delta_p, 0.5-delta_p], linestyle='dashed', color='red')
plt.plot([first_detection, first_detection], [0.5-delta_p, min(est_mean[num_samples:])-0.025], linestyle='dashed', color='orange')
plt.plot([2, 2], [0.5-delta_p, min(est_mean[num_samples:])-0.025], linestyle='dashed', color='orange')
plt.plot([0.01], [0.49])
print(first_detection)
plt.grid()

plt.show()