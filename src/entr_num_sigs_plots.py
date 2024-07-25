import numpy as np
import matplotlib.pyplot as plt

import math

from sim.utils import *

eps = np.linspace(0.01, 0.1, 4)
delta = np.linspace(0.01, 0.2, 20)

def del_func(n, eps):
    return math.log2(n)*math.sqrt((2*math.log10(2/eps))/n)

def delta_func_to_solve(n, eps, d):
    return del_func(n, eps) - d

def find_upper_val(eps, d):
    n_val = 2
    while delta_func_to_solve(n_val, eps, d) > 0:
        n_val *= 10
    return n_val

def find_lower_val(eps, d):
    n_val = 2
    while delta_func_to_solve(n_val, eps, d) > 0:
        n_val *= 10
    return n_val/10

def bin_search(upper, lower, eps, d):

    mid = math.ceil((upper+lower)/2)

    # found soln
    if (mid == upper):
        return mid
    # mid is too high. soln between mid and lower
    if delta_func_to_solve(mid, eps, d) < 0:
        return bin_search(mid, lower, eps, d)
    else:
        return bin_search(upper, mid, eps, d)

def find_n_val(eps, d):
    # Find start
    upper = find_upper_val(eps, d)
    # Find end
    lower = find_lower_val(eps, d)
    # Binary Search
    return bin_search(upper, lower, eps, d)

n_vals = [math.log10(find_n_val(eps[0], d)) for d in delta]
n_ch_bound = [math.log10(chernoff_hoeffding_bound(d, eps[0])) for d in delta]

plt.plot(delta, n_vals)
plt.plot(delta, n_ch_bound)
plt.grid()
plt.show()