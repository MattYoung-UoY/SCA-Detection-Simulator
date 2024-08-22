"""Licensed under the MIT License.
Full license can be found in the "LICENSE" file in the repository root directory.

Copyright (c) 2024 Matt Young

Used to generate Fig.4 from *insert paper DOI*

Simulates an attack where the attacker switches which state they are blocking with a certain frequency.
Two different attack frequencies are simulated here for the same sampling window width.
"""

from utils.datasetGenerator import *
from utils.distributions import *
from utils.bounds import *
from utils.convolutions import *

import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation

""" Creates a distribution pattern list based on the specified parameters

Args:
    switching_freq(float): The frequency at which the attacker switches the state that they are blocking
    window_width(int): The window_size
    total_bits(int): The total number of bits that the distribution pattern should cover
"""
def get_key_bit_dist_pattern(switching_freq, window_size, total_bits):
    # The size of each region where a state is blocked
    switching_size = int(window_size * (1/(2*switching_freq)))

    # How many times the blocked state should switch
    num_switches = total_bits/switching_size
    prob_dists = []

    # For each switch...
    for i in range(math.floor(num_switches)):
        # If an even numbered region...
        if i%2 == 0:
            # Block a state corresponding to a '1' key bit
            prob_dists.append((lower_third, switching_size))
        else:
            # Else block a state corresponding to a '0' key bit
            prob_dists.append((upper_third, switching_size))

    # A fraction of a state blocking region may be needed
    remainder = num_switches % 1
    # Creates the final required distribution and adds it to the list
    if remainder != 0:
        if num_switches % 2 == 0:
            prob_dists.append((upper_third, int(remainder * switching_size)))
        else:
            prob_dists.append((lower_third, int(remainder * switching_size)))
    
    return prob_dists


# Estimate should be within 5% of the actual value
delta_p = 0.05
# Certainty of 99.9%
epsilon = 0.001

# Calculate the size of the window
window_size = chernoff_hoeffding_bound(delta_p, epsilon)
print(window_size)

# We want to simulate for 3 window widths
num_bits = window_size * 3

# Calculations and plotting for the first frequency

switching_frequency_1 = 1
prob_dist_pattern_1 = get_key_bit_dist_pattern(switching_frequency_1, window_size, num_bits)
dataset_1 = generate_dataset(prob_dist_pattern_1);
est_mean_1 = ([None] * window_size) + est_mean(dataset_1[1], window_size)
total_samples_1 = sum([x[1] for x in prob_dist_pattern_1])

rel_x_vals_est_mean = [x/window_size for x in range(0, total_samples_1)]
rel_x_vals_samples = [x/window_size for x in range(0, total_samples_1)]

fig, axs = plt.subplot_mosaic([['a)', 'b)'], ['c)', 'd)']],
                              layout='constrained')

for label, ax in axs.items():
# Use ScaledTranslation to put the label
# - at the top left corner (axes fraction (0, 1)),
# - offset 20 pixels left and 7 pixels up (offset points (-20, +7)),
# i.e. just outside the axes.
    ax.text(
        0.0, 1.0, label, transform=(
            ax.transAxes + ScaledTranslation(-20/72, +7/72, fig.dpi_scale_trans)),
        fontsize='medium', va='bottom', fontfamily='serif',
        bbox=dict(facecolor='0.8', edgecolor='none', pad=3.0))

plt.subplot(2, 2, 1)
plt.xlabel("Key-bit Position (Relative to Window Size)")
plt.ylabel("Distribution Mean")
plt.plot(rel_x_vals_samples, dataset_1[0])
plt.grid()

plt.subplot(2, 2, 3)
plt.xlabel("Sliding Window End Position (Relative to Window Size)")
plt.ylabel("Sample Mean")
plt.plot(rel_x_vals_est_mean, est_mean_1)
plt.plot([0, (total_samples_1/window_size)], [0.5, 0.5], linestyle='dashed', color='blue')
plt.plot([0, (total_samples_1/window_size)], [0.5+delta_p, 0.5+delta_p], linestyle='dashed', color='red')
plt.plot([0, (total_samples_1/window_size)], [0.5-delta_p, 0.5-delta_p], linestyle='dashed', color='red')
plt.grid()

# Calculation and plotting for the second frequency

switching_frequency_2 = 1.5
prob_dist_pattern_2 = get_key_bit_dist_pattern(switching_frequency_2, window_size, num_bits)
dataset_2 = generate_dataset(prob_dist_pattern_2);
est_mean_2 = ([None] * window_size) + est_mean(dataset_2[1], window_size)
total_samples_2 = sum([x[1] for x in prob_dist_pattern_2])

rel_x_vals_est_mean = [x/window_size for x in range(0, total_samples_1)]
rel_x_vals_samples = [x/window_size for x in range(0, total_samples_1)]

plt.subplot(2, 2, 2)
plt.xlabel("Key-bit Position (Relative to Window Size)")
plt.ylabel("Distribution Mean")
plt.plot(rel_x_vals_samples, dataset_2[0])
plt.grid()

plt.subplot(2, 2, 4)
plt.xlabel("Sliding Window End Position (Relative to Window Size)")
plt.ylabel("Sample Mean")
plt.plot(rel_x_vals_est_mean, est_mean_2)
plt.plot([0, (total_samples_2/window_size)], [0.5, 0.5], linestyle='dashed', color='blue')
plt.plot([0, (total_samples_2/window_size)], [0.5+delta_p, 0.5+delta_p], linestyle='dashed', color='red')
plt.plot([0, (total_samples_2/window_size)], [0.5-delta_p, 0.5-delta_p], linestyle='dashed', color='red')
plt.grid()

plt.show()