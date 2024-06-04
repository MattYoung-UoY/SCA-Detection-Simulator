from sim.datasetGenerator import *
from sim.distributions import *
from sim.tests import *
from sim.utils import *
from sim.convolutions import *

import matplotlib.pyplot as plt

def expected_bit_losses(eps, p0, p1, pN, d_p):
    return expected_relative_losses(p0, p1, pN, d_p) * chernoff_hoeffding_bound(d_p, eps)

def expected_relative_losses(p0, p1, pN, d_p):
    return (pN-d_p-p0)/(p1-p0)

# Need to incorporate this
def expected_key_rate_abs(eps, p0, p1, pN, d_p, total_num_bits):
    return total_num_bits - expected_bit_losses(eps, p0, p1, pN, d_p)

# TODO
# Define expected_key_rate_rel function and incorporate that into plots

# Within 5% of the actual value
# delta_p = 0.025
# Certainty of 99.9%
epsilon = 0.001

# Looking at the produced values for the estimated mean at face value, this bound seems to be overly restrictive
# num_samples = chernoff_hoeffding_bound(delta_p, epsilon)
# print(num_samples)

# prob_dist_pattern = [
#     # (const_0, 5), 
#     # (const_1, 5), 
#     (uniform_dist, int(num_samples*1.05)),
#     (quarter_mean, int(num_samples*1.05)),
#     (uniform_dist, int(num_samples*1.05))
#     ]

# total_samples = sum([x[1] for x in prob_dist_pattern])
# rel_x_vals_est_mean = [x/num_samples for x in range(0, total_samples-num_samples)]

# rel_x_vals_samples = [x/num_samples for x in range(0, total_samples)]

# END OF CONSTANT DEFINITIONS
# START OF DATASET GENERATION AND TESTING

# TODO
# Collect a list of est_mean values and post-process on that list, and can also plot it
#
# Test detection time
# Test proportion of key discarded upon detection
    # These two are the same thing 

num_thresholds = 21
num_samples_per_threshold = 100
first_threshold_loc = 0.02
last_threshold_loc = 0.25
threshold_jump = (last_threshold_loc-first_threshold_loc)/(num_thresholds-1) if num_thresholds > 1 else 0
threshold_crossings = []
exp_rel_losses = []
absolute_threshold_crossings = []
exp_absolute_losses = []
delta_p_vals = []

attack_start_loc = 1.05

for i in range(num_thresholds):

    delta_p = first_threshold_loc + (i * threshold_jump)
    print(delta_p)
    delta_p_vals.append(delta_p)
    num_samples = chernoff_hoeffding_bound(delta_p, epsilon)
    print(num_samples)

    prob_dist_pattern = [
    # (const_0, 5), 
    # (const_1, 5), 
    (uniform_dist, int(num_samples*attack_start_loc)),
    (quarter_mean, int(num_samples*1.05))
    ]

    threshold_cross_loc = 0

    for j in range(num_samples_per_threshold):

        dataset = generate_dataset(prob_dist_pattern)
        threshold_cross_loc += (est_mean_threshold(dataset[1], num_samples, 0.5, delta_p) / num_samples) - attack_start_loc + 1

    threshold_cross_loc /= (num_samples_per_threshold)

    threshold_crossings.append(threshold_cross_loc)
    exp_rel_losses.append(expected_relative_losses(0.5, 0.25, 0.5, delta_p))

    absolute_threshold_crossings.append(threshold_cross_loc*num_samples)
    exp_absolute_losses.append(expected_bit_losses(epsilon, 0.5, 0.25, 0.5, delta_p))

    # total_samples = sum([x[1] for x in prob_dist_pattern])
    # rel_x_vals_est_mean = [x/num_samples for x in range(0, total_samples-num_samples)]

    # rel_x_vals_samples = [x/num_samples for x in range(0, total_samples)]


# END OF DATASET GENERATION AND TESTING
# START OF PLOTS

rmse_rel = math.sqrt(sum([(actual-est)**2 for actual, est in zip(exp_rel_losses, threshold_crossings)])/num_thresholds)
# Could also plot the expected value using the equation
plt.subplot(1, 2, 1)
plt.xlabel("delta_p/threshold value")
plt.ylabel("Proportion of discarded key (relative to window size)")
plt.plot(delta_p_vals, threshold_crossings, marker='x')
plt.plot(delta_p_vals, exp_rel_losses, marker='x')
plt.grid()
plt.title("RMSE: " + str(rmse_rel))

rmse_abs = math.sqrt(sum([(actual-est)**2 for actual, est in zip(exp_absolute_losses, absolute_threshold_crossings)])/num_thresholds)
plt.subplot(1, 2, 2)
plt.xlabel("delta_p/threshold value")
plt.ylabel("Number of discarded key bits")
plt.plot(delta_p_vals, absolute_threshold_crossings, marker='x')
plt.plot(delta_p_vals, exp_absolute_losses, marker='x')
plt.grid()
plt.title("RMSE: " + str(rmse_abs))
plt.show()