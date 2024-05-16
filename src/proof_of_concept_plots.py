from sim.datasetGenerator import *
from sim.distributions import *
from sim.tests import *
from sim.utils import *
from sim.convolutions import *

import matplotlib.pyplot as plt

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
    (const_0, int(num_samples*2)),
    (uniform_dist, int(num_samples*2))
    ]

dataset = generate_dataset(prob_dist_pattern);

# TODO
# Collect a list of est_mean values and post-process on that list, and can also plot it
# Test detection time
# Test proportion of key discarded upon detection

est_mean = est_mean(dataset, num_samples)

total_samples = sum([x[1] for x in prob_dist_pattern])
rel_x_vals_est_mean = [x/num_samples for x in range(0, total_samples-num_samples)]

rel_x_vals_samples = [x/num_samples for x in range(0, total_samples)]

plt.subplot(1, 2, 1)
plt.xlabel("Key-bit Position (Relative to Window Size)")
plt.ylabel("Key-Bit Value")
plt.plot(rel_x_vals_samples, dataset)
plt.grid()

plt.subplot(1, 2, 2)
plt.xlabel("Sliding Window Start Position (Relative to Window Size)")
plt.ylabel("Estimated Sample Mean")
plt.plot(rel_x_vals_est_mean, est_mean)
plt.grid()

plt.show()