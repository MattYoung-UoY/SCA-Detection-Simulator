import math
from utils import *

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

delta_p_vals = np.linspace(0.01, 0.2, 20)
epsilon_vals = np.linspace(0.01, 0.5, 50)
X, Y = np.meshgrid(delta_p_vals, epsilon_vals)

log_10_sample_vals = [[math.log10(chernoff_hoeffding_bound(d, e)) for d in delta_p_vals] for e in epsilon_vals]

ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, np.array(log_10_sample_vals), cmap='viridis', edgecolor='none')
ax.set_xlabel("delta_p")
ax.set_ylabel("epsilon")
plt.show()