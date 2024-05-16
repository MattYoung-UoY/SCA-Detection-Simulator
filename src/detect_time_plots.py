# How long to detect a problem?
# Based on equation:
    # | p_N - p^hat | < t
    # 1/n sum(p_i n_i) = p^hat
    # 
    # For p_N = 0.5 and going from p_U to p_0
    # n_U/n = 0.9
# Plot the est_mean arrays for 4 different (distributions? fixed tolerances?)
# Issue is not knowing what probability distribution Eve is using.
    # If Eve doesn't block enough in one go, not enough low entropy to gain information
    # How much information gained by Eve can be removed by PA, Key-Distillation, etc.

from sim.datasetGenerator import *
from sim.distributions import *
from sim.tests import *
from sim.utils import *
from sim.convolutions import *

import matplotlib.pyplot as plt

def first_error_loc(est_vals, x_vals, nominal, tol):
    for i in range(0, len(est_vals)):
        if(est_vals[i] <= nominal-tol):
            # print("Detected intolerable deviation @ " + str(rel_x_vals_est_mean[i]))
            # break
            return x_vals[i]

# Within 5% of the actual value
delta_p = 0.05
# Certainty of 99.9%
epsilon = 0.001

nominal = 0.5
tolerance = 0.45

# Looking at the produced values for the estimated mean at face value, this bound seems to be overly restrictive
num_samples = chernoff_hoeffding_bound(delta_p, epsilon)
print(num_samples)

prob_dist_pattern_quarter_skew = [
    # (const_0, 5), 
    # (const_1, 5), 
    (uniform_dist, int(num_samples*1)),
    (quarter_mean, int(num_samples*0.5))
    # (const_0, int(num_samples*0.25))
    ]

prob_dist_pattern_simple = [
    # (const_0, 5), 
    # (const_1, 5), 
    (uniform_dist, int(num_samples*1)),
    # (quarter_mean, int(num_samples*0.5))
    (const_0, int(num_samples*0.25))
    ]

working_distribution = prob_dist_pattern_quarter_skew
total_samples = sum([x[1] for x in working_distribution])

def first_error_locs_sample():
    est_mean_vals = est_mean(generate_dataset(working_distribution), num_samples)
    rel_x_vals_est_mean = [x/num_samples for x in range(0, total_samples-num_samples)]
    return first_error_loc(est_mean_vals, rel_x_vals_est_mean, tolerance)

first_error_locs = []
for i in range(0, 2500):
    if(i % 100 == 0):
        print(i)
    first_error_locs.append(first_error_locs_sample())

average_first_error_loc = sum(first_error_locs)/len(first_error_locs)

print("Average first error location: " + str(average_first_error_loc))