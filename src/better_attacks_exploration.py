from sim.datasetGenerator import *
from sim.distributions import *
from sim.tests import *
from sim.utils import *
from sim.convolutions import *

import numpy as np

import matplotlib.pyplot as plt

# Within 5% of the actual value
delta_p = 0.05
# Certainty of 99.9%
epsilon = 0.001

# Looking at the produced values for the estimated mean at face value, this bound seems to be overly restrictive
num_samples = chernoff_hoeffding_bound(delta_p, epsilon)
print(num_samples)

switching_size = 0.5

prob_dist_pattern = [
    # (const_0, 5), 
    # (const_1, 5), 
    (lower_third, int(num_samples*switching_size)),
    (upper_third, int(num_samples*switching_size)),
    (lower_third, int(num_samples*switching_size)),
    (upper_third, int(num_samples*switching_size)),
    (lower_third, int(num_samples*switching_size)),
    (upper_third, int(num_samples*switching_size)),
    (lower_third, int(num_samples*switching_size)),
    (upper_third, int(num_samples*switching_size)),
    (lower_third, int(num_samples*switching_size)),
    (upper_third, int(num_samples*switching_size))
    ]

dataset = generate_dataset(prob_dist_pattern)

# TODO
# Collect a list of est_mean values and post-process on that list, and can also plot it
# Test detection time
# Test proportion of key discarded upon detection

est_mean = est_mean(dataset[1], num_samples)

# fft_est_mean = np.fft.fft(est_mean, axis=0)

total_samples = sum([x[1] for x in prob_dist_pattern])
rel_x_vals_est_mean = [x/num_samples for x in range(0, total_samples-num_samples)]

rel_x_vals_samples = [x/num_samples for x in range(0, total_samples)]

plt.subplot(3, 1, 1)
plt.xlabel("Key-bit Position (Relative to Window Size)")
plt.ylabel("Actual Mean")
plt.plot(rel_x_vals_samples, dataset[0])
plt.grid()

plt.subplot(3, 1, 2)
plt.xlabel("Sliding Window Start Position (Relative to Window Size)")
plt.ylabel("Estimated Sample Mean")
plt.plot(rel_x_vals_est_mean, est_mean)
plt.plot([0, (total_samples/num_samples)-1], [0.5, 0.5], linestyle='dotted', color='green')
plt.plot([0, (total_samples/num_samples)-1], [0.5+delta_p, 0.5+delta_p], linestyle='dashed', color='red')
plt.plot([0, (total_samples/num_samples)-1], [0.5-delta_p, 0.5-delta_p], linestyle='dashed', color='red')
plt.grid()

# plt.subplot(3, 1, 3)
# plt.plot(fft_est_mean)
# plt.grid()

plt.show()