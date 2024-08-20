from utils.datasetGenerator import *
from utils.distributions import *
from utils.bounds import *
from utils.convolutions import *

import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation

def get_prob_dist_pattern(switching_freq, window_width, num_bit):
    switching_size = int(window_width * (1/(2*switching_freq)))

    num_switches = num_bit/switching_size
    prob_dists = []

    for i in range(math.floor(num_switches)):
        if i%2 == 0:
            prob_dists.append((lower_third, switching_size))
        else:
            prob_dists.append((upper_third, switching_size))

    remainder = num_switches % 1
    if remainder != 0:
        if num_switches % 2 == 0:
            prob_dists.append((upper_third, int(remainder * switching_size)))
        else:
            prob_dists.append((lower_third, int(remainder * switching_size)))
    
    return prob_dists


# Within 5% of the actual value
delta_p = 0.05
# Certainty of 99.9%
epsilon = 0.001

# Looking at the produced values for the estimated mean at face value, this bound seems to be overly restrictive
num_samples = chernoff_hoeffding_bound(delta_p, epsilon)
print(num_samples)

num_bits = num_samples * 3

# Calculations and plotting for the first frequency

switching_frequency_1 = 1
prob_dist_pattern_1 = get_prob_dist_pattern(switching_frequency_1, num_samples, num_bits)
dataset_1 = generate_dataset(prob_dist_pattern_1);
est_mean_1 = ([None] * num_samples) + est_mean(dataset_1[1], num_samples)
total_samples_1 = sum([x[1] for x in prob_dist_pattern_1])

rel_x_vals_est_mean = [x/num_samples for x in range(0, total_samples_1)]
rel_x_vals_samples = [x/num_samples for x in range(0, total_samples_1)]

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
plt.plot([0, (total_samples_1/num_samples)], [0.5, 0.5], linestyle='dashed', color='blue')
plt.plot([0, (total_samples_1/num_samples)], [0.5+delta_p, 0.5+delta_p], linestyle='dashed', color='red')
plt.plot([0, (total_samples_1/num_samples)], [0.5-delta_p, 0.5-delta_p], linestyle='dashed', color='red')
plt.grid()

# Calculation and plotting for the second frequency

switching_frequency_2 = 1.5
prob_dist_pattern_2 = get_prob_dist_pattern(switching_frequency_2, num_samples, num_bits)
dataset_2 = generate_dataset(prob_dist_pattern_2);
est_mean_2 = ([None] * num_samples) + est_mean(dataset_2[1], num_samples)
total_samples_2 = sum([x[1] for x in prob_dist_pattern_2])

rel_x_vals_est_mean = [x/num_samples for x in range(0, total_samples_1)]
rel_x_vals_samples = [x/num_samples for x in range(0, total_samples_1)]

plt.subplot(2, 2, 2)
plt.xlabel("Key-bit Position (Relative to Window Size)")
plt.ylabel("Distribution Mean")
plt.plot(rel_x_vals_samples, dataset_2[0])
plt.grid()

plt.subplot(2, 2, 4)
plt.xlabel("Sliding Window End Position (Relative to Window Size)")
plt.ylabel("Sample Mean")
plt.plot(rel_x_vals_est_mean, est_mean_2)
plt.plot([0, (total_samples_2/num_samples)], [0.5, 0.5], linestyle='dashed', color='blue')
plt.plot([0, (total_samples_2/num_samples)], [0.5+delta_p, 0.5+delta_p], linestyle='dashed', color='red')
plt.plot([0, (total_samples_2/num_samples)], [0.5-delta_p, 0.5-delta_p], linestyle='dashed', color='red')
plt.grid()

plt.show()