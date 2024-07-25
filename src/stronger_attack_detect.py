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

switching_freq = 3
switching_size = 1/(switching_freq*2)
num_of_bits = 3 * num_samples

prob_dist_pattern = []

current_bits_generated = 0
switches = 0

while current_bits_generated < num_of_bits:

    if switches % 2 == 0:
        prob_dist_pattern.append((upper_third, int(num_samples*switching_size)))
    else:
        prob_dist_pattern.append((lower_third, int(num_samples*switching_size)))

    current_bits_generated += switching_size * num_samples
    switches += 1

dataset = generate_dataset(prob_dist_pattern);

est_mean = est_mean(dataset[1], num_samples)
print(len(est_mean)/num_samples)

total_samples = sum([x[1] for x in prob_dist_pattern])
rel_x_vals_est_mean = [x/num_samples for x in range(0, total_samples)]

rel_x_vals_samples = [x/num_samples for x in range(0, total_samples)]

plt.subplot(3, 1, 1)
plt.xlabel("Key-bit Position (Relative to Window Size)")
plt.ylabel("Actual Mean")
plt.plot(rel_x_vals_samples, dataset[0])
plt.grid()

plt.subplot(3, 1, 2)
plt.xlabel("Sliding Window End Position (Relative to Window Size)")
plt.ylabel("Estimated Mean")
plt.plot(rel_x_vals_est_mean, ([None]*num_samples) + est_mean)
plt.plot([0, (total_samples/num_samples)], [0.5, 0.5], linestyle='dashed', color='blue')
plt.plot([0, (total_samples/num_samples)], [0.5+delta_p, 0.5+delta_p], linestyle='dashed', color='red')
plt.plot([0, (total_samples/num_samples)], [0.5-delta_p, 0.5-delta_p], linestyle='dashed', color='red')
plt.grid()

plt.show()