"""Licensed under the MIT License.
Full license can be found in the "LICENSE" file in the repository root directory.

Copyright (c) 2024 Matt Young

Used to generate Fig.1 from *insert paper DOI*

Plots various graphs to illustrate the Chernoff-Hoeffding bound.
"""

import math
from utils.bounds import *

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# 3D Plot

# delta_p and epsilon values to use
delta_p_vals = np.linspace(0.01, 0.2, 20)
epsilon_vals = np.linspace(0.01, 0.5, 50)
X, Y = np.meshgrid(delta_p_vals, epsilon_vals)

# caluclates the Chernoff-Horffding bound and applies a logarithmic scale
log_10_ch_bound_vals = [[math.log10(chernoff_hoeffding_bound(d, e)) for d in delta_p_vals] for e in epsilon_vals]

ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, np.array(log_10_ch_bound_vals), cmap='viridis', edgecolor='none')
ax.set_xlabel("delta_p")
ax.set_ylabel("epsilon")
plt.show()

#Contour Plot

# delta_p and epsilon values to use
# each epsilon value will be a different curve on the plot
delta_p_vals = np.linspace(0.01, 0.2, 20)
epsilon_vals_contour = [0.001, 0.01, 0.1, 1]
# Gets the Chernoff-Hoeffding bound and applies a logarithmic scaling
num_samples_contour = [[math.log10(chernoff_hoeffding_bound(delta, eps)) for delta in delta_p_vals] for eps in epsilon_vals_contour]
# Specifies different markers for each of the curves
markers = [".", "D", "x", "s"]

# Plots each curve with it's corresponding marker
for i in range(len(epsilon_vals_contour)):
    plt.plot(delta_p_vals, num_samples_contour[i], label=str(epsilon_vals_contour[i]), marker=markers[i])

plt.legend(loc="upper right")
plt.xlabel("delta_mu")
plt.ylabel("log(n) (log(bits))")
plt.grid()
plt.show()