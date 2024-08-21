"""Licensed under the MIT License.
Full license can be found in the "LICENSE" file in the repository root directory.

Copyright (c) 2024 Matt Young

Runs many simulations for a variety of window sizes and finds the first instance of a detection of an attack.
Each simulation is refered to as a trial in the code.
"""

from utils.datasetGenerator import *
from utils.distributions import *
from utils.convolutions import *
from utils.bounds import *

import matplotlib.pyplot as plt

import numpy as np

# To calculate the execution time
import time

""" Calculates the first detection locations for a set of trials with a given window size

Args:
    params: params[0] - window size, params[1] - number of trials

Returns:
    A tuple of the window size used, and a list of the results from the trials

"""
def calculate_trials_results(params):
    print(params[0])
    key_bit_dist_pattern = [
    (uniform_dist, int(params[0])),
    (lower_third, int(params[0]))
    ]
    trials_results_list = []
    # For each trial
    for t in range(params[1]):
        # Generates the random key bits, and calculates the estimates of the mean
        dataset = generate_dataset(key_bit_dist_pattern)
        mean_est = est_mean(dataset[1], int(params[0]))

        # For each estimate of the mean...
        for i in range(len(mean_est)):
            # If the difference between the nominal mean and the estimated mean is beyond the detection threshold...
            if abs(0.5-mean_est[i])>=0.05:
                # Record the position the detection happened
                trials_results_list.append(i)
                break
    # Return a tuple with the window size used, and the results obtained
    return (params[0], trials_results_list)

if __name__ == '__main__':

    start_time = time.time()

    """ Calculates the standard deviation of a list of values
    """
    def std_dev(values):
        n = len(values)
        mu = sum(values)/n
        s = math.sqrt(sum([((x-mu)**2) for x in values])/n)
        return s

    """ Performs a linear regression

    More information on how this is done can be found here:
    https://mattyoung-uoy.github.io/ml/linreg.html

    Args:
        x_inp: A list of x coordinates for datapoints
        y_inp: A list of corresponding y coordinates for each x coordinate

    Returns:
        A list of two values, the first being the y-intersect, and the second being the gradient
    """
    def lin_reg(x_inp, y_inp):
        x = np.array([[1, a] for a in x_inp])
        y = np.array(y_inp)
        beta = np.matmul(np.transpose(x), x)
        beta = np.linalg.inv(beta)
        beta = np.matmul(beta, np.transpose(x))
        beta = np.matmul(beta, y)
        return beta

    """ Calculates the root mean squared error of the datapoints against a given linear function
    """
    def rmse(lin_reg_coeff, x, y):
        error = math.sqrt(sum([(y - (lin_reg_coeff[0] + (x * lin_reg_coeff[1])))**2 for x, y in zip(x, y)])/len(y))
        return error

    # If set to False, the results will be saved to file
    # Recommended when execution takes a long time
    plot_results = True

    # # Datapoints from Fig.### of the paper
    # num_samples = np.linspace(100, 50000, 16)
    # num_samples = [int(x) for x in num_samples]
    # n_trials = 1000

    # Smaller example
    num_samples = np.linspace(10, 1000, 4)
    num_samples = [int(x) for x in num_samples]
    n_trials = 100
    
    # How many trials should be in each block
    block_size = 10
    # and how many blocks do we need per set or trials for each window size
    num_blocks = int(n_trials/block_size)

    # Creates a list that contains the window sizes needed for each block
    block_num_samples = []
    for n in num_samples:
        block_num_samples = block_num_samples + ([int(n)] * num_blocks)

    # Creates a list that contains the number of trials per block
    block_sizes = [block_size] * len(block_num_samples)


    # Multi-threading code
    import multiprocessing

    # Tries to get the number of cores in the cpu
    # If it fails, defaults to 2
    try:
        cpus = multiprocessing.cpu_count()
    except NotImplementedError:
        cpus = 2

    pool = multiprocessing.Pool(processes=cpus)
    # Executes the calculate_trials_results function with the zipped lists as input and stores the results
    results_list = pool.map(calculate_trials_results, zip(block_num_samples, block_sizes))

    # End of multi-threading code

    # Adds each set of results to a dictionary based on which window size they are the results for
    res_dict = {}

    for res in results_list:
        if res[0] not in res_dict:
            res_dict.update({res[0] : res[1]})
        else:
            res_dict.update({res[0] : res_dict.get(res[0]) + res[1]})

    # Converts the dictionary into a list (this will automatically be in order of window size)
    res_list = []
    for x in res_dict:
        res_list.append(res_dict.get(x))

    # Calculates the mean and std_dev for each set of results for each window size
    trial_means = [sum(trial)/len(trial) for trial in res_list]
    std_devs = [std_dev(trial) for trial in res_list]

    # Performs a linear regression on the mean and calculates the error
    coefficients = lin_reg(num_samples, trial_means)
    print(coefficients)
    error = rmse(coefficients, num_samples, trial_means)

    # Plots the results if needed
    if plot_results:
        plt.subplot(2, 1, 1)
        plt.grid()
        plt.scatter(num_samples, trial_means, marker='x', color='red')
        plt.plot([num_samples[0], num_samples[len(num_samples)-1]], 
                [coefficients[0] + (coefficients[1] * num_samples[0]), coefficients[0] + (coefficients[1] * (num_samples[len(num_samples)-1]))],
                linestyle='dashed')

        plt.subplot(2, 1, 2)
        plt.grid()
        plt.plot(num_samples, std_devs, marker='x')

        plt.show()
    # Otherwise saves the results to file
    else:

        f = open("foo.txt", "w")
        f.write(str(coefficients) + "\n")
        f.write("RMSE: " + str(error) + "\n")
        f.write("--- %s seconds ---\n" % (time.time() - start_time))
        f.write(str(num_samples) + "\n") 
        f.write(str(trial_means) + "\n")
        f.write(str(std_devs))
        f.close()

