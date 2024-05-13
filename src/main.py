import datasetGenerator
from distributions import *
from tests import *
from utils import *

# Within 1% of the actual value
delta_p = 0.01
# Certainty of 99.9%
epsilon = 0.001

# Looking at the produced values for the estimated mean at face value, this bound seems to be overly restrictive
num_samples = chernoff_hoeffding_bound(delta_p, epsilon)
print(num_samples)

prob_dist_pattern = [
    # (const_0, 5), 
    # (const_1, 5), 
    (uniform_dist, int(num_samples*1.1)),
    (const_0, int(num_samples*1.1)),
    (uniform_dist, int(num_samples))
    ]

dataset = datasetGenerator.generate_dataset(prob_dist_pattern);

# TODO
# Collect a list of est_mean values and post-process on that list, and can also plot it
# Test detection time
# Test proportion of key discarded upon detection

est_mean_vals = []

test_first_location = True

# Loops over the dataset to find the location where it first detects a SCA
# Check these stopping values against the predictions made for transition times between two different probability distributions
current_pos = 0
while(current_pos < len(dataset) - num_samples):

    if(current_pos % 1000 == 0):
        print(current_pos)

    est_mean = sample_mean(dataset, current_pos, num_samples)
    if(not test_first_location):
       est_mean_vals.append(est_mean)
    # If we deviate away from a mean of 0.5 +- 0.05 then error
    if(test_first_location and abs(est_mean-0.5) >= 0.05):
        print("Detected SCA!\nDetected at location: " + str(current_pos) + ", Relative Pos: " + str(current_pos/num_samples))
        break;

    current_pos += 1


# print(sample_mean(dataset, sample_start, num_samples))